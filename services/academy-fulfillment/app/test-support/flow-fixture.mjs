/** Node-only synthetic provider/storage fixture. Never a deployable adapter. */
import {DatabaseSync} from 'node:sqlite';
import {createHash,createHmac} from 'node:crypto';
import {registerHooks} from 'node:module';
import {Coordinator} from '../coordinator.mjs';
// Load the real entrypoint under a minimal Node class shim. This is NOT workerd
// or a Cloudflare input/output-gate validation.
registerHooks({resolve(specifier,context,next){return specifier==='cloudflare:workers'?{url:specifier,shortCircuit:true}:next(specifier,context);},load(url,context,next){return url==='cloudflare:workers'?{format:'module',source:'export class DurableObject {constructor(ctx,env){this.ctx=ctx;this.env=env;}}',shortCircuit:true}:next(url,context);}});
const {default:worker,AcademyLedger}=await import('../worker.mjs');
export const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export const SID='cs_test_FIXTURE1';
export async function fixture(){
 const db=new DatabaseSync(':memory:'),kv=new Map(),drafts=new Map(),sent=new Map(),calls=[];
 let alarm=null;
 const storage={sql:{exec(query,...args){const p=db.prepare(query);return p.columns().length?p.all(...args):(p.run(...args),[]);}},transactionSync(fn){db.exec('BEGIN IMMEDIATE');try{const value=fn();db.exec('COMMIT');return value;}catch(error){db.exec('ROLLBACK');throw error;}},get:async k=>kv.get(k),put:async(k,v)=>kv.set(k,v),getAlarm:async()=>alarm,setAlarm:async t=>{alarm=t;},deleteAlarm:async()=>{alarm=null;}};
 const zip=new TextEncoder().encode('PUBLIC FIXTURE ONLY. NOT REAL COURSE MATERIAL.');
 const offer={automatic_enabled:true,sku:'fixture-kit',title:'Kit fictício',edition:'2026-private-kit-v2',currency:'brl',unit_amount:2900,price_id:'price_FIXTURE1',product_id:'prod_FIXTURE1',file_id:'asset_FIXTURE1',sha256:hash(zip),bytes:zip.length};
 const catalog={offers_by_payment_link:{plink_FIXTURE1:offer}};
 const catalogBytes=new TextEncoder().encode(JSON.stringify(catalog));
 const data={private:true,zip,session:{id:SID,object:'checkout.session',livemode:false,mode:'payment',status:'complete',payment_status:'paid',payment_link:'plink_FIXTURE1',currency:'brl',amount_total:2900,amount_subtotal:2900,total_details:{amount_discount:0,amount_shipping:0,amount_tax:0},payment_intent:'pi_FIXTURE1',customer_details:{email:'buyer@example.invalid'}},
  charge:{id:'ch_FIXTURE1',payment_intent:'pi_FIXTURE1',livemode:false,paid:true,captured:true,refunded:false,amount_refunded:0,disputed:false,status:'succeeded',currency:'brl',amount:2900,amount_captured:2900}};
 const env={WEBHOOK_INTAKE_ENABLED:'true',AUTOMATIC_DELIVERY_ENABLED:'true',WATCHDOG_ENABLED:'false',STRIPE_MODE:'test',STRIPE_ACCOUNT_ID:'acct_FIXTURE1',STRIPE_WEBHOOK_SECRET:'whsec_PUBLIC_LOCAL_FIXTURE_NOT_SECRET',SENDER_EMAIL:'owner@example.invalid',TEST_BUYER_EMAIL:'buyer@example.invalid',CATALOG_FILE_ID:'catalog_FIXTURE1',CATALOG_SHA256:hash(catalogBytes),CATALOG_BYTES:String(catalogBytes.length),EXPECTED_OFFER_COUNT:'1'};
 const durable=new AcademyLedger({storage},env),ledger=durable.ledger;
 env.LEDGER={idFromName:name=>name,get:()=>durable};
 const client={identity:async()=>{calls.push('identity');return true;},session:async()=>structuredClone(data.session),lineItems:async()=>({has_more:false,data:[{quantity:1,currency:'brl',amount_total:2900,amount_subtotal:2900,price:{id:'price_FIXTURE1',product:'prod_FIXTURE1',livemode:false,type:'one_time',currency:'brl',unit_amount:2900}}]}),
  downloadVerifiedZip:async selected=>{calls.push('fixture-download');const bytes=selected.file_id===env.CATALOG_FILE_ID?catalogBytes:data.zip;if(!data.private||bytes.length!==selected.bytes||hash(bytes)!==selected.sha256)throw Error('FIXTURE_ASSET_CHANGED');return bytes;},
  draft:async(raw,guard)=>{if(guard&&guard()!==true)throw Error('FIXTURE_WRITE_DENIED');calls.push('draft');const id='draft_FIXTURE'+(drafts.size+1);drafts.set(id,raw);return{id};},
  sendDraft:async(id,guard)=>{if(guard&&guard()!==true)throw Error('FIXTURE_WRITE_DENIED');calls.push('send');const mid='message_FIXTURE'+(sent.size+1);sent.set(mid,drafts.get(id));return{id:mid};},
  call:async(kind,method,path)=>{
   if(kind==='stripe'){
    if(path==='/v1/account')return{data:{id:env.STRIPE_ACCOUNT_ID}};
    if(path==='/v1/payment_intents/pi_FIXTURE1')return{data:{id:'pi_FIXTURE1',livemode:false,status:'succeeded',currency:'brl',amount:2900,amount_received:2900,latest_charge:'ch_FIXTURE1'}};
    if(path==='/v1/charges/ch_FIXTURE1')return{data:structuredClone(data.charge)};
   }
   if(kind==='gmail'){
    const u=new URL(path,'https://fixture.invalid'),id=u.pathname.split('/').at(-1);
    if(u.pathname.endsWith('/messages'))return{data:{messages:[...sent.keys()].map(id=>({id}))}};
    if(u.pathname.includes('/drafts/'))return{data:{id,message:{raw:drafts.get(id)}}};
    if(u.pathname.includes('/messages/'))return{data:{id,raw:sent.get(id),labelIds:['SENT']}};
   }
   throw Error('UNEXPECTED_FIXTURE_ROUTE');
  }};
 const coordinator=new Coordinator(ledger,storage,env,client);
 const event=()=>({id:'evt_FIXTURE1',object:'event',type:'checkout.session.completed',livemode:false,created:Math.floor(Date.now()/1000),data:{object:{id:SID}}});
 const request=(e=event(),options={})=>{const body=options.body??JSON.stringify(e),timestamp=options.timestamp??Math.floor(Date.now()/1000);const sig=options.signature??createHmac('sha256',env.STRIPE_WEBHOOK_SECRET).update(timestamp+'.'+body).digest('hex');return new Request('https://worker.fixture.invalid/stripe-webhook',{method:'POST',headers:{'stripe-signature':`t=${timestamp},v1=${sig}`},body});};
 return{worker,durable,ledger,coordinator,storage,db,env,client,data,catalog,offer,calls,kv,drafts,sent,event,request,
  intake:(e,options)=>worker.fetch(request(e,options),env),run:()=>coordinator.run(Date.now()),close:()=>db.close(),get alarm(){return alarm;}};
}
