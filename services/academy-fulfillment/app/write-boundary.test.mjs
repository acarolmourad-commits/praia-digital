/** The last write boundary, including real asynchronous consumer preflight. */
import assert from 'node:assert/strict';
import {test,after} from 'node:test';
import {fixture,SID} from './test-support/flow-fixture.mjs';
import {ConsumerComposio} from './consumer-composio.mjs';
import {AcademyProviders} from './providers.mjs';
import {Composio} from './composio.mjs';
let clock=1800000000000,networkCalls=0;const realNow=Date.now;
Date.now=()=>clock;globalThis.fetch=()=>{networkCalls++;throw Error('NETWORK_DISABLED');};
after(()=>{Date.now=realNow;});
async function use(fn){const f=await fixture();try{await fn(f);}finally{f.close();}}
const envFor=f=>({...f.env,STRIPE_READONLY_API_KEY:'rk_test_PUBLIC_FIXTURE',COMPOSIO_ORG_ID:'org_fixture',COMPOSIO_CONSUMER_PROJECT_ID:'proj_fixture',COMPOSIO_USER_API_KEY:'PUBLIC_FIXTURE',COMPOSIO_USER_ID:'fixture-owner',COMPOSIO_CONSUMER_SESSION_ID:'trs_fixture',COMPOSIO_CONSUMER_ACCOUNTS_JSON:JSON.stringify({gmail:'coup_gmail_fixture',googledrive:'coup_drive_fixture'})});
function config(c){const b=c.sessionClient.creationBody();return{session_id:'trs_fixture',config:{...b,toolkits:{enabled:b.toolkits.enable},tools:Object.fromEntries(c.sessionClient.kinds.map(k=>[k,{enabled:[]}])),manage_connections:{enabled:false}}};}
async function receiptConflict(f){const e=f.event();e.data.object.extra='signed conflict during asynchronous preparation';assert.equal((await f.intake(e)).status,503);assert.equal(f.ledger.intakeHeld(),true);}
function orderConflict(f){const r=f.ledger.get(SID);assert.throws(()=>f.ledger.acceptVerifiedOrder(JSON.parse(r.payload),'conflicting-fingerprint',clock),/ORDER_CONFLICT/);}
async function beforePhase(f,phase){assert.equal((await f.intake()).status,200);if(phase==='send'){await f.run();assert.equal(f.ledger.get(SID).state,'DRAFT_READY');clock+=2000;}}
function installConsumer(f,hook=async()=>{},Adapter=ConsumerComposio){
 const real={draft:f.client.draft,send:f.client.sendDraft};const tally={preflights:0,writes:0};let c;
 const fetcher=async(url,options)=>{
  if(options.method==='GET'){tally.preflights++;await hook();return Response.json(config(c));}
  tally.writes++;const b=JSON.parse(options.body),sending=b.endpoint.endsWith('/drafts/send');
  // This is the remote fixture effect after the real adapter has consumed its
  // one-use guard. Do not invoke that guard a second time inside the fake server.
  return Response.json({result_type:'completed',status:200,data:sending?await real.send(b.body.id):await real.draft(b.body.message.raw)});
 };
 c=Adapter===AcademyProviders?new AcademyProviders(envFor(f),fetcher):new ConsumerComposio(envFor(f),fetcher,['gmail','googledrive']);
 f.client.draft=(raw,guard)=>c.draft(raw,guard);f.client.sendDraft=(id,guard)=>c.sendDraft(id,guard);
 return{c,tally};
}
for(const Adapter of [ConsumerComposio,AcademyProviders])for(const phase of ['draft','send'])test(Adapter.name+' blocks '+phase+' when a signed conflict arrives during session preflight',async()=>use(async f=>{
 await beforePhase(f,phase);const {tally}=installConsumer(f,()=>receiptConflict(f),Adapter);
 await f.run();assert.equal(tally.preflights,1);assert.equal(tally.writes,0);assert.equal(f.sent.size,0);
 assert.equal(f.drafts.size,phase==='draft'?0:1);assert.equal(f.ledger.get(SID).hold_reason,'EVENT_CONFLICT');
 clock+=130000;await f.run();assert.equal(tally.writes,0);
}));
for(const phase of ['draft','send'])for(const change of ['order-conflict','revoked','expired','version-changed','clock-backwards'])test(phase+' guard rejects '+change+' after asynchronous preflight',async()=>use(async f=>{
 await beforePhase(f,phase);const {tally}=installConsumer(f,async()=>{
  if(change==='order-conflict')orderConflict(f);
  if(change==='revoked')f.ledger.revoke(SID);
  if(change==='expired')clock+=120001;
  if(change==='version-changed')f.ledger.sql.exec('UPDATE orders SET version=version+1 WHERE id=?',SID);
  if(change==='clock-backwards')clock--;
 });
 await f.run();assert.equal(tally.preflights,1);assert.equal(tally.writes,0);assert.equal(f.sent.size,0);
}));
test('conflict during async MIME hashing is caught at the legacy transport boundary',async()=>use(async f=>{
 await beforePhase(f,'draft');const originalDigest=crypto.subtle.digest;
 let conflict=false,writes=0;
 const legacy=new Composio({...envFor(f),COMPOSIO_API_KEY:'PUBLIC_FIXTURE',GMAIL_CONNECTION_ID:'ca_fixture'},async()=>{writes++;return Response.json({status:200,data:{id:'draft_fixture'}});});
 f.client.draft=(raw,guard)=>legacy.draft(raw,guard);
 crypto.subtle.digest=async function(...args){const r=await originalDigest.apply(this,args);
  if(!conflict&&f.ledger.get(SID)?.state==='DRAFT_CREATING'){conflict=true;await receiptConflict(f);}return r;};
 try{await f.run();assert.equal(conflict,true);assert.equal(writes,0);assert.equal(f.drafts.size,0);assert.equal(f.ledger.get(SID).state,'UNCERTAIN');}
 finally{crypto.subtle.digest=originalDigest;}
}));
for(const method of ['draft','sendDraft'])for(const kind of ['missing','async','promise','false','undefined','throw'])test(method+' refuses '+kind+' guard without provider write',async()=>use(async f=>{
 const {c,tally}=installConsumer(f);
 const guard={missing:undefined,async:async()=>true,promise:()=>Promise.resolve(true),false:()=>false,undefined:()=>undefined,throw:()=>{throw Error('FIXTURE_DENIED');}}[kind];
 await assert.rejects(()=>c[method](method==='draft'?'Zml4dHVyZQ':'draft_fixture',guard));
 assert.equal(tally.writes,0);if(['missing','async'].includes(kind))assert.equal(tally.preflights,0);
}));
for(const method of ['draft','sendDraft'])test('legacy '+method+' also requires a synchronous explicit guard',async()=>{
 let writes=0;const c=new Composio({COMPOSIO_API_KEY:'PUBLIC_FIXTURE',COMPOSIO_USER_ID:'fixture',GMAIL_CONNECTION_ID:'ca_fixture'},async()=>{writes++;return Response.json({status:200,data:{id:'fixture'}});});
 const arg=method==='draft'?'Zml4dHVyZQ':'draft_fixture';
 await assert.rejects(()=>c[method](arg));await assert.rejects(()=>c[method](arg,async()=>true));
 await assert.rejects(()=>c[method](arg,()=>Promise.resolve(true)));assert.equal(writes,0);
});
test('one-use ledger guard cannot issue a second provider send',async()=>use(async f=>{
 await beforePhase(f,'send');const {c,tally}=installConsumer(f);
 f.client.sendDraft=async(id,guard)=>{const first=await c.sendDraft(id,guard);await assert.rejects(()=>c.sendDraft(id,guard),/USED/);return first;};
 await f.run();assert.equal(tally.writes,1);assert.equal(f.sent.size,1);assert.equal(f.ledger.get(SID).state,'SENT');
}));
test('no real network access was attempted',()=>assert.equal(networkCalls,0));
