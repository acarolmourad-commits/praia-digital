/* Offline integration: real coordinator, SQLite ledger, validator and Gmail MIME.
 * All provider calls are fixtures; no credentials/network/email operations. */
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {Ledger} from '../durable/store.mjs';
import {Coordinator} from './coordinator.mjs';
import {ConsumerComposio} from './consumer-composio.mjs';
const realNow=Date.now;let clock=1800000000000;Date.now=()=>clock;
async function fixture(useConsumer=false){
 const db=new DatabaseSync(':memory:'),kv=new Map(),drafts=new Map(),sent=new Map(),calls=[];let alarm=null;
 const storage={sql:{exec(q,...a){const p=db.prepare(q);return p.columns().length?p.all(...a):(p.run(...a),[]);}},transactionSync(fn){db.exec('BEGIN IMMEDIATE');try{const r=fn();db.exec('COMMIT');return r;}catch(e){db.exec('ROLLBACK');throw e;}},get:async k=>kv.get(k),put:async(k,v)=>kv.set(k,v),deleteAlarm:async()=>{alarm=null;},setAlarm:async n=>{alarm=n;}};
 const ledger=new Ledger(storage),zip=new TextEncoder().encode('PK fixture private file bytes');
 const sha=[...new Uint8Array(await crypto.subtle.digest('SHA-256',zip))].map(x=>x.toString(16).padStart(2,'0')).join('');
 const offer={automatic_enabled:true,sku:'example-kit',title:'Kit de exemplo',edition:'2026-private-kit-v2',currency:'brl',unit_amount:2900,price_id:'price_test',product_id:'prod_test',file_id:'fakefile',sha256:sha,bytes:zip.length};
 const catalog={offers_by_payment_link:{plink_test:offer}};
 const env={AUTOMATIC_DELIVERY_ENABLED:'true',STRIPE_MODE:'test',STRIPE_ACCOUNT_ID:'acct_test',TEST_BUYER_EMAIL:'owner@example.invalid',SENDER_EMAIL:'owner@example.invalid',CATALOG_SHA256:'b'.repeat(64),EXPECTED_OFFER_COUNT:'1'};
 kv.set('approved-catalog',{sha:env.CATALOG_SHA256,data:catalog});
 const sessions=new Map();const session=id=>({id,object:'checkout.session',livemode:false,mode:'payment',status:'complete',payment_status:'paid',payment_link:'plink_test',currency:'brl',amount_total:2900,amount_subtotal:2900,total_details:{amount_discount:0,amount_shipping:0,amount_tax:0},payment_intent:'pi_test',customer_details:{email:env.TEST_BUYER_EMAIL}});
 const charge={id:'ch_test',payment_intent:'pi_test',livemode:false,paid:true,captured:true,refunded:false,amount_refunded:0,disputed:false};
 const client={identity:async()=>true,session:async id=>{if(id==='cs_poison')throw Error('fixture API unavailable');return sessions.get(id)||session(id);},lineItems:async()=>({has_more:false,data:[{quantity:1,currency:'brl',amount_total:2900,amount_subtotal:2900,price:{id:'price_test',product:'prod_test',livemode:false,type:'one_time',currency:'brl',unit_amount:2900}}]}),downloadVerifiedZip:async()=>zip,
 draft:async raw=>{const id='draft_'+(drafts.size+1);drafts.set(id,raw);calls.push('draft');return{id};},sendDraft:async id=>{calls.push('send');const mid='message_'+(sent.size+1);sent.set(mid,drafts.get(id));return{id:mid};},
 call:async(kind,method,path)=>{
  if(kind==='stripe'){
   if(path==='/v1/account')return{data:{id:'acct_test'}};
   if(path==='/v1/payment_intents/pi_test')return{data:{id:'pi_test',livemode:false,status:'succeeded',currency:'brl',amount:2900,amount_received:2900,latest_charge:'ch_test'}};
   if(path==='/v1/charges/ch_test')return{data:charge};
  }
  if(kind==='gmail'){
   const u=new URL(path,'https://fixture.invalid'),parts=u.pathname.split('/'),id=parts.at(-1);
   if(u.pathname.endsWith('/messages'))return{data:{messages:[...sent.keys()].map(id=>({id}))}};
   if(u.pathname.includes('/drafts/'))return{data:{id,message:{raw:drafts.get(id)}}};
   if(u.pathname.includes('/messages/'))return{data:{id,raw:sent.get(id),labelIds:['SENT']}};
  }
  throw Error('UNEXPECTED_FIXTURE_ROUTE '+path);
 }};
 let runtimeClient=client;
 if(useConsumer){
  const accounts={stripe:'coup_stripe_fixture',gmail:'coup_gmail_fixture',googledrive:'coup_drive_fixture'};
  const consumerEnv={...env,COMPOSIO_ORG_ID:'org_fixture',COMPOSIO_CONSUMER_PROJECT_ID:'proj_fixture',COMPOSIO_USER_API_KEY:'fixture-user-key',COMPOSIO_USER_ID:'fixture-owner',COMPOSIO_CONSUMER_SESSION_ID:'trs_fixture',COMPOSIO_CONSUMER_ACCOUNTS_JSON:JSON.stringify(accounts)};
  runtimeClient=new ConsumerComposio(consumerEnv,async(url,options)=>{
   if(options.method==='GET'){const b=runtimeClient.sessionClient.creationBody();return Response.json({session_id:'trs_fixture',config:{...b,toolkits:{enabled:b.toolkits.enable},tools:Object.fromEntries(Object.keys(accounts).map(k=>[k,{enabled:[]}])),manage_connections:{enabled:false}}});}
   const b=JSON.parse(options.body),u=new URL(b.endpoint);for(const p of b.parameters||[])if(p.in==='query')u.searchParams.append(p.name,p.value);
   const path=u.pathname+u.search;let data;
   if(u.pathname==='/gmail/v1/users/me/profile')data={emailAddress:env.SENDER_EMAIL};
   else if(b.toolkit_slug==='stripe'&&u.pathname.includes('/checkout/sessions/'))data=u.pathname.endsWith('/line_items')?await client.lineItems():await client.session(u.pathname.split('/').at(-1));
   else if(u.pathname==='/gmail/v1/users/me/drafts'&&b.method==='POST')data=await client.draft(b.body.message.raw);
   else if(u.pathname==='/gmail/v1/users/me/drafts/send')data=await client.sendDraft(b.body.id);
   else data=(await client.call(b.toolkit_slug,b.method,path)).data;
   return Response.json({result_type:'completed',status:200,data});
  });
  // Binary metadata/hash adapter has separate tests; this fixture focuses on
  // authoritative payment and exact Gmail MIME through actual session proxy.
  runtimeClient.downloadVerifiedZip=client.downloadVerifiedZip;
 }
 const c=new Coordinator(ledger,storage,env,runtimeClient);
 const event=(id,type='checkout.session.completed',object='cs_valid',created=1)=>ledger.recordEvent({id,type,object_id:object,created});
 return{db,kv,ledger,client,c,calls,charge,sessions,session,event,drafts,sent,get alarm(){return alarm;},run:()=>c.run(clock)};
}
let count=0;async function test(name,fn,useConsumer=false){const f=await fixture(useConsumer);try{await fn(f);console.log('PASS',name);count++;}finally{f.db.close();}}
try{
 await test('consumer session proxy completes exact payment-to-draft-to-send once',async f=>{f.event('evt_consumer');await f.run();assert.equal(f.ledger.get('cs_valid').state,'DRAFT_READY');clock+=2000;await f.run();assert.equal(f.ledger.get('cs_valid').state,'SENT');assert.deepEqual(f.calls,['draft','send']);},true);
 await test('idle queue clears alarm without any provider calls',async f=>{f.client.identity=async()=>{throw Error('unexpected identity');};await f.run();assert.equal(f.alarm,null);});
 await test('future work schedules exactly due without provider calls',async f=>{f.client.identity=async()=>{throw Error('unexpected identity');};f.ledger.sql.exec('INSERT INTO pending_sessions VALUES(?,?)','cs_valid',clock+900000);await f.run();assert.equal(f.alarm,clock+900000);});
 await test('real validator and MIME draft then send once across duplicate events',async f=>{f.event('evt_one');await f.run();assert.equal(f.ledger.get('cs_valid').state,'DRAFT_READY');clock+=2000;await f.run();assert.equal(f.ledger.get('cs_valid').state,'SENT');f.event('evt_two');await f.run();assert.deepEqual(f.calls,['draft','send']);});
 await test('poison earliest event gets deferred while later valid order progresses',async f=>{f.event('evt_poison','checkout.session.completed','cs_poison',0);f.event('evt_valid');await f.run();assert.equal(f.ledger.get('cs_valid').state,'DRAFT_READY');const e=f.ledger.rows('SELECT * FROM events WHERE id=?','evt_poison')[0];assert.equal(e.state,'PENDING');assert.ok(e.due>clock);assert.equal(e.attempts,1);});
 await test('async failed unpaid is held and pending tracking removed',async f=>{f.sessions.set('cs_valid',{...f.session('cs_valid'),payment_status:'unpaid'});f.ledger.sql.exec('INSERT INTO pending_sessions VALUES(?,?)','cs_valid',clock);f.event('evt_failed','checkout.session.async_payment_failed');await f.run();assert.equal(f.ledger.rows('SELECT * FROM pending_sessions').length,0);assert.equal(f.kv.get('held-event:evt_failed').reason,'ASYNC_PAYMENT_FAILED');assert.equal(f.ledger.get('cs_valid'),null);assert.deepEqual(f.calls,[]);});
 await test('pending-session API poison does not starve later pending session',async f=>{f.ledger.sql.exec('INSERT INTO pending_sessions VALUES(?,?)','cs_poison',clock);f.ledger.sql.exec('INSERT INTO pending_sessions VALUES(?,?)','cs_valid',clock);await f.run();assert.equal(f.ledger.get('cs_valid').state,'DRAFT_READY');assert.ok(f.ledger.rows('SELECT due FROM pending_sessions WHERE id=?','cs_poison')[0].due>clock);});
 await test('late paid event after unpaid yields one deliverable order',async f=>{f.sessions.set('cs_valid',{...f.session('cs_valid'),payment_status:'unpaid'});f.event('evt_pending');await f.run();assert.equal(f.ledger.get('cs_valid'),null);assert.equal(f.ledger.rows('SELECT * FROM pending_sessions').length,1);f.sessions.delete('cs_valid');f.event('evt_paid','checkout.session.async_payment_succeeded');await f.run();assert.equal(f.ledger.get('cs_valid').state,'DRAFT_READY');assert.equal(f.ledger.rows('SELECT * FROM pending_sessions').length,0);});
 await test('refund after draft prevents actual send',async f=>{f.event('evt_paid');await f.run();f.charge.amount_refunded=2900;f.charge.refunded=true;clock+=2000;f.event('evt_refund','charge.refunded','ch_test');await f.run();assert.equal(f.ledger.get('cs_valid').state,'REVOKED');assert.deepEqual(f.calls,['draft']);});
 await test('disabled automatic mode has no provider side effects',async f=>{f.c.env.AUTOMATIC_DELIVERY_ENABLED='false';f.event('evt_paid');await f.run();assert.equal(f.ledger.get('cs_valid'),null);assert.deepEqual(f.calls,[]);assert.equal(f.alarm,null);});
 await test('ambiguous send held rather than retried',async f=>{f.event('evt_paid');await f.run();f.client.sendDraft=async()=>{f.calls.push('send');throw Error('ambiguous timeout');};clock+=2000;await f.run();assert.equal(f.ledger.get('cs_valid').state,'UNCERTAIN');clock+=2000;await f.run();assert.equal(f.ledger.get('cs_valid').state,'HELD');assert.deepEqual(f.calls,['draft','send']);});
}finally{Date.now=realNow;}
console.log(count+' coordinator integration tests passed');
