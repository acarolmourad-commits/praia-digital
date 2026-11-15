/** Consolidation contract tests. Actual PR modules, Node storage/provider fixtures. */
import assert from 'node:assert/strict';
import {test,after} from 'node:test';
import {DatabaseSync} from 'node:sqlite';
import {fixture,SID,hash} from './test-support/flow-fixture.mjs';
import {validateSession} from './payment.mjs';
import {Ledger} from '../durable/store.mjs';
import {verifiedEvent,verifiedPayloadDigest} from './signature.mjs';
let clock=1800000000000,networkCalls=0;const realNow=Date.now;
Date.now=()=>clock;globalThis.fetch=()=>{networkCalls++;throw Error('NETWORK_DISABLED');};
after(()=>{Date.now=realNow;});
async function use(fn){const f=await fixture();try{await fn(f);}finally{f.close();}}
const sends=f=>f.calls.filter(c=>c==='send').length;
const drafts=f=>f.calls.filter(c=>c==='draft').length;
async function paidDraft(f){assert.equal((await f.intake()).status,200);await f.run();assert.equal(f.ledger.get(SID).state,'DRAFT_READY');}
async function finish(f){clock+=2000;await f.run();}
function conflictOrder(f){const row=f.ledger.get(SID);assert.throws(()=>f.ledger.acceptVerifiedOrder(JSON.parse(row.payload),'conflicting-fingerprint',Date.now()),/ORDER_CONFLICT/);}
async function conflictEvent(f){const e=f.event();e.data.object.extra='signed conflicting bytes';assert.equal((await f.intake(e)).status,503);}

test('real Worker entrypoint, signed receipt, coordinator, validator and MIME complete a synthetic flow once',async()=>use(async f=>{
 await paidDraft(f);await finish(f);assert.equal(f.ledger.get(SID).state,'SENT');assert.equal(drafts(f),1);assert.equal(sends(f),1);
 const row=f.ledger.rows('SELECT * FROM events')[0];assert.match(row.payload_sha256,/^[a-f0-9]{64}$/);
 assert.equal(f.sent.size,1);
}));
test('unsigned, stale, tampered and LIVE events do not persist or simulate delivery',async()=>{
 for(const kind of ['unsigned','stale','tampered','live'])await use(async f=>{
  const e=f.event();let req;
  if(kind==='unsigned')req=f.request(e,{signature:'0'.repeat(64)});
  if(kind==='stale')req=f.request(e,{timestamp:Math.floor(clock/1000)-301});
  if(kind==='live'){e.livemode=true;req=f.request(e);}
  if(kind==='tampered'){const signed=f.request(e);req=new Request(signed.url,{method:'POST',headers:signed.headers,body:JSON.stringify(e)+' '});}
  assert.notEqual((await f.worker.fetch(req,f.env)).status,200);assert.equal(f.ledger.rows('SELECT * FROM events').length,0);
  await f.run();assert.equal(drafts(f),0);assert.equal(sends(f),0);
 });
});
test('verified digest derives from exact signed bytes, not JSON claimed proof',async()=>use(async f=>{
 const e=f.event();e.payload_sha256='f'.repeat(64);const body=JSON.stringify(e);
 const parsed=await verifiedEvent(f.request(e),f.env.STRIPE_WEBHOOK_SECRET);
 assert.equal(verifiedPayloadDigest(parsed),hash(body));assert.equal(verifiedPayloadDigest({...parsed}),undefined);
}));
test('missing signed-byte proof is rejected by the ledger',async()=>use(async f=>{
 assert.throws(()=>f.ledger.recordEvent({id:'evt_FIXTURE1',type:'checkout.session.completed',object_id:SID,created:1}),/INVALID_RECEIPT_PROOF/);
 assert.equal(f.ledger.rows('SELECT * FROM events').length,0);
}));
test('eight concurrent duplicate intakes create one receipt and one simulated send',async()=>use(async f=>{
 const e=f.event();const replies=await Promise.all(Array.from({length:8},()=>f.intake(e)));
 assert(replies.every(r=>r.status===200));assert.equal(f.ledger.rows('SELECT * FROM events').length,1);
 await Promise.all([f.run(),f.run()]);await finish(f);assert.equal(drafts(f),1);assert.equal(sends(f),1);
}));
test('different success events for the same session preserve one order',async()=>use(async f=>{
 await paidDraft(f);await finish(f);const e=f.event();e.id='evt_FIXTURE2';e.type='checkout.session.async_payment_succeeded';
 assert.equal((await f.intake(e)).status,200);await f.run();assert.equal(sends(f),1);
}));
test('new signature delivery timestamp with identical event bytes remains a safe duplicate',async()=>use(async f=>{
 const e=f.event();assert.equal((await f.intake(e)).status,200);clock+=2000;
 assert.equal((await f.intake(e)).status,200);assert.equal(f.ledger.intakeHeld(),false);assert.equal(f.ledger.rows('SELECT * FROM events').length,1);
}));
for(const field of ['created','payload_sha256','object_id'])test('durable receipt conflict in '+field+' blocks new effects',async()=>use(async f=>{
 await paidDraft(f);const prior=f.ledger.rows('SELECT * FROM events')[0];
 const bad={id:prior.id,type:prior.type,object_id:prior.object_id,created:prior.created,payload_sha256:prior.payload_sha256};
 bad[field]=field==='created'?prior.created+1:field==='object_id'?'cs_test_FIXTURE2':'a'.repeat(64);
 assert.throws(()=>f.ledger.recordEvent(bad),/EVENT_CONFLICT/);assert.equal(f.ledger.intakeHeld(),true);
 assert.equal(f.ledger.rows('SELECT * FROM events')[0].state,'HELD');assert.equal(f.ledger.get(SID).state,'HELD');
 const before=f.calls.length;await finish(f);assert.equal(f.calls.length,before);assert.equal(sends(f),0);assert.equal(f.alarm,null);
 assert.throws(()=>f.ledger.recordEvent({...bad,...prior}),/EVENT_INTAKE_QUARANTINED/);
}));
test('changed signed payload is durably quarantined before Worker error reply',async()=>use(async f=>{
 await paidDraft(f);await conflictEvent(f);assert.equal(f.ledger.intakeHeld(),true);await finish(f);assert.equal(sends(f),0);
}));
test('receipt conflict during validation invalidates stale draft transition',async()=>use(async f=>{
 assert.equal((await f.intake()).status,200);const original=f.client.downloadVerifiedZip;
 f.client.downloadVerifiedZip=async offer=>{const bytes=await original(offer);if(offer.file_id==='asset_FIXTURE1')await conflictEvent(f);return bytes;};
 await f.run();assert.equal(f.ledger.intakeHeld(),true);assert.equal(drafts(f),0);assert.equal(sends(f),0);
}));
test('receipt conflict during raw draft verification prevents send CAS',async()=>use(async f=>{
 await paidDraft(f);const original=f.client.call;
 f.client.call=async(kind,method,path)=>{const r=await original(kind,method,path);if(path.includes('/drafts/'))await conflictEvent(f);return r;};
 await finish(f);assert.equal(f.ledger.intakeHeld(),true);assert.equal(sends(f),0);
}));
test('order fingerprint conflict persists a terminal hold and preserves original snapshot',async()=>use(async f=>{
 await paidDraft(f);const prior=f.ledger.get(SID);conflictOrder(f);const held=f.ledger.get(SID);
 assert.equal(held.state,'HELD');assert.equal(held.error,'ORDER_CONFLICT');assert.equal(held.payload,prior.payload);assert.equal(held.fingerprint,prior.fingerprint);assert(held.version>prior.version);
 assert.equal(f.ledger.acceptVerifiedOrder(JSON.parse(prior.payload),prior.fingerprint,clock).state,'HELD');await finish(f);assert.equal(sends(f),0);
}));
test('order conflict during draft verification invalidates stale send transition',async()=>use(async f=>{
 await paidDraft(f);const original=f.client.call;
 f.client.call=async(kind,method,path)=>{const r=await original(kind,method,path);if(path.includes('/drafts/'))conflictOrder(f);return r;};
 await finish(f);assert.equal(f.ledger.get(SID).state,'HELD');assert.equal(sends(f),0);
}));
test('pending-session order conflict is terminal rather than a provider retry',async()=>use(async f=>{
 await paidDraft(f);const cached=await f.storage.get('approved-catalog');cached.data.offers_by_payment_link.plink_FIXTURE1.title='Changed fixture title';
 f.ledger.sql.exec('INSERT INTO pending_sessions VALUES(?,?)',SID,clock);await f.run();
 assert.equal(f.ledger.get(SID).state,'HELD');assert.equal(f.ledger.rows('SELECT * FROM pending_sessions').length,0);
 assert.equal(f.kv.get('held-session:'+SID).reason,'ORDER_CONFLICT');assert.equal(sends(f),0);
}));
test('known accepted message survives order conflict during actual simulated send',async()=>use(async f=>{
 await paidDraft(f);const original=f.client.sendDraft;
 f.client.sendDraft=async(id,guard)=>{const response=await original(id,guard);conflictOrder(f);return response;};
 await finish(f);assert.equal(f.ledger.get(SID).state,'SENT');assert.equal(f.ledger.get(SID).revoked,1);assert.equal(sends(f),1);
 await finish(f);assert.equal(sends(f),1);
}));
for(const conflict of ['order','receipt'])for(const lost of [false,true])test(conflict+' conflict during draft creation preserves uncertainty when response is '+(lost?'lost':'received'),async()=>use(async f=>{
 assert.equal((await f.intake()).status,200);const original=f.client.draft;
 f.client.draft=async(raw,guard)=>{const response=await original(raw,guard);if(conflict==='order')conflictOrder(f);else await conflictEvent(f);
  if(lost)throw Error('FIXTURE_DRAFT_RESPONSE_LOST');return response;};
 await f.run();assert.equal(f.drafts.size,1);assert.equal(f.ledger.get(SID).state,'UNCERTAIN');
 assert.equal(f.ledger.get(SID).hold_reason,conflict==='order'?'ORDER_CONFLICT':'EVENT_CONFLICT');
 clock+=130000;await f.run();assert.equal(drafts(f),1);assert.equal(sends(f),0);
 assert.equal(f.ledger.get(SID).state,conflict==='order'?'HELD':'UNCERTAIN');
 assert.equal(f.ledger.get(SID).hold_reason,conflict==='order'?'ORDER_CONFLICT':'EVENT_CONFLICT');
}));
for(const conflict of ['order','receipt'])test(conflict+' conflict plus lost send response preserves hold reason and never resends',async()=>use(async f=>{
 await paidDraft(f);const original=f.client.sendDraft;
 f.client.sendDraft=async(id,guard)=>{await original(id,guard);if(conflict==='order')conflictOrder(f);else await conflictEvent(f);throw Error('FIXTURE_SEND_RESPONSE_LOST');};
 await finish(f);assert.equal(f.ledger.get(SID).state,'SENDING');assert.equal(sends(f),1);
 assert.equal(f.ledger.get(SID).hold_reason,conflict==='order'?'ORDER_CONFLICT':'EVENT_CONFLICT');
 clock+=130000;await f.run();assert.equal(sends(f),1);
 assert.equal(f.ledger.get(SID).state,conflict==='order'?'SENT':'SENDING');
 assert.equal(f.ledger.get(SID).hold_reason,conflict==='order'?'ORDER_CONFLICT':'EVENT_CONFLICT');
}));
test('unknown simulated send is held without automatic resend',async()=>use(async f=>{
 await paidDraft(f);f.client.sendDraft=async()=>{f.calls.push('send');throw Error('FIXTURE_RESPONSE_UNKNOWN');};
 await finish(f);assert.equal(f.ledger.get(SID).state,'UNCERTAIN');await finish(f);assert.equal(f.ledger.get(SID).state,'HELD');assert.equal(sends(f),1);
}));
test('lost send response is reconciled from exact Sent MIME without resend',async()=>use(async f=>{
 await paidDraft(f);const original=f.client.sendDraft;f.client.sendDraft=async(id,guard)=>{await original(id,guard);throw Error('FIXTURE_RESPONSE_LOST');};
 await finish(f);assert.equal(f.ledger.get(SID).state,'UNCERTAIN');await finish(f);assert.equal(f.ledger.get(SID).state,'SENT');assert.equal(sends(f),1);
}));
for(const [name,mutate] of [
 ['failed status',c=>c.status='failed'],['pending status',c=>c.status='pending'],['missing status',c=>delete c.status],
 ['wrong currency',c=>c.currency='usd'],['missing currency',c=>delete c.currency],['wrong amount',c=>c.amount=1],
 ['missing amount',c=>delete c.amount],['partial capture',c=>c.amount_captured=1],['zero capture',c=>c.amount_captured=0],['missing capture',c=>delete c.amount_captured],
])test('contradictory Charge '+name+' cannot authorize a plan or draft',async()=>use(async f=>{
 mutate(f.data.charge);const checked=await validateSession(f.client,SID,f.catalog,f.env);assert.equal(checked.ok,false);
 assert.equal((await f.intake()).status,200);await f.run();assert.equal(f.ledger.get(SID),null);assert.equal(drafts(f),0);
}));
for(const [name,mutate] of [
 ['unpaid',f=>f.data.session.payment_status='unpaid'],['refund',f=>f.data.charge.amount_refunded=1],
 ['dispute',f=>f.data.charge.disputed=true],['private file changed',f=>f.data.zip=new TextEncoder().encode('changed')],
 ['file made public',f=>f.data.private=false],
])test(name+' after draft prevents simulated send',async()=>use(async f=>{
 await paidDraft(f);mutate(f);await finish(f);assert.equal(sends(f),0);
}));
test('legacy schema without payload proof is refused without silent migration',()=>{
 const db=new DatabaseSync(':memory:');db.exec('CREATE TABLE events(id TEXT PRIMARY KEY,type TEXT,object_id TEXT,created INTEGER)');
 const storage={sql:{exec(q,...a){const p=db.prepare(q);return p.columns().length?p.all(...a):(p.run(...a),[]);}},transactionSync(fn){db.exec('BEGIN');try{const r=fn();db.exec('COMMIT');return r;}catch(e){db.exec('ROLLBACK');throw e;}}};
 try{assert.throws(()=>new Ledger(storage),/LEDGER_SCHEMA_REVIEW_REQUIRED/);assert.equal(db.prepare("SELECT count(*) AS n FROM sqlite_master WHERE name='intake_holds'").get().n,0);}finally{db.close();}
});
test('runtime flags remain independent and default OFF blocks processing',async()=>use(async f=>{
 f.env.WEBHOOK_INTAKE_ENABLED='false';assert.equal((await f.intake()).status,503);assert.equal(f.ledger.rows('SELECT * FROM events').length,0);
 f.env.WEBHOOK_INTAKE_ENABLED='true';assert.equal((await f.intake()).status,200);f.env.AUTOMATIC_DELIVERY_ENABLED='false';await f.run();assert.equal(f.calls.length,0);
}));
test('test suite attempted no network access',()=>assert.equal(networkCalls,0));
