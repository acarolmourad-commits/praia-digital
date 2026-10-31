import {ConsumerComposio} from './consumer-composio.mjs';
import {validateSession} from './payment.mjs';
import {GmailDelivery} from './gmail.mjs';
import {processOne} from '../durable/process.mjs';
export class Coordinator {
 constructor(ledger,storage,env,client=new ConsumerComposio(env)){this.ledger=ledger;this.storage=storage;this.env=env;this.client=client;this.ledger.sql.exec('CREATE TABLE IF NOT EXISTS pending_sessions(id TEXT PRIMARY KEY,due INTEGER NOT NULL)');}
 async catalog(){
  const sha=this.env.CATALOG_SHA256;
  if(!/^[a-f0-9]{64}$/.test(sha||''))throw Error('CATALOG_NOT_CONFIGURED');
  const cached=await this.storage.get('approved-catalog');
  if(cached?.sha===sha)return cached.data;
  const data=await this.client.downloadVerifiedZip({file_id:this.env.CATALOG_FILE_ID,sha256:sha,bytes:Number(this.env.CATALOG_BYTES)});
  const parsed=JSON.parse(new TextDecoder().decode(data));
  const offers=parsed.offers_by_payment_link;
  if(!offers||Object.keys(offers).length!==Number(this.env.EXPECTED_OFFER_COUNT))throw Error('CATALOG_SCOPE_MISMATCH');
  await this.storage.put('approved-catalog',{sha,data:parsed});return parsed;
 }
 nextDue(){return this.ledger.rows("SELECT MIN(due) AS due FROM (SELECT due FROM events WHERE state='PENDING' UNION ALL SELECT MAX(due,lease_until) FROM orders WHERE state NOT IN ('SENT','HELD','REVOKED') UNION ALL SELECT due FROM pending_sessions)")[0]?.due??null;}
 async schedule(now=Date.now()){const due=this.nextDue();if(due===null)await this.storage.deleteAlarm();else await this.storage.setAlarm(Math.max(now+1000,due));return due;}
 async run(now=Date.now()){
  if(this.env.AUTOMATIC_DELIVERY_ENABLED!=='true')return;
  const due=await this.schedule(now);
  if(due===null||due>now)return;
  // Re-arm BEFORE external calls so provider failure does not exhaust six alarms.
  await this.storage.setAlarm(now+300000);
  await this.client.identity();
  const catalog=await this.catalog();
  const gmail=new GmailDelivery(this.client,{senderEmail:this.env.SENDER_EMAIL,messageDomain:'praia.digital'});
  const provider={
   findVerifiedSent:row=>gmail.findVerifiedSent(row),
   createExactDraft:(row,checked)=>gmail.createExactDraft(row,checked),
   verifyExactDraft:(row,checked)=>gmail.verifyExactDraft(row,checked),
   sendExistingDraft:id=>gmail.sendExistingDraft(id),
   validateCurrentPaymentAndPackage:async order=>{
    const result=await validateSession(this.client,order.session_id,catalog,this.env);
    if(!result.ok)return result;
    // Current order must still match the immutable order accepted earlier.
    const row=this.ledger.get(order.id);
    if(!row||row.fingerprint!==result.fingerprint)return{ok:false};
    const zipBytes=await this.client.downloadVerifiedZip(result.order);
    return{ok:true,zipBytes,offer:result.order};
   }
  };
  for(const event of this.ledger.pendingEvents(2,now)){
   try{
   if(event.type.startsWith('checkout.session.')){
    const result=await validateSession(this.client,event.object_id,catalog,this.env);
    if(result.ok){this.ledger.acceptVerifiedOrder(result.order,result.fingerprint,now);this.ledger.sql.exec('DELETE FROM pending_sessions WHERE id=?',event.object_id);}
    else if(result.pending&&event.type!=='checkout.session.async_payment_failed')this.ledger.sql.exec('INSERT INTO pending_sessions(id,due) VALUES(?,?) ON CONFLICT(id) DO UPDATE SET due=excluded.due',event.object_id,now+300000);
    else {await this.storage.put('held-event:'+event.id,{reason:event.type==='checkout.session.async_payment_failed'?'ASYNC_PAYMENT_FAILED':result.reason||'POLICY_REJECTED',at:now});this.ledger.sql.exec('DELETE FROM pending_sessions WHERE id=?',event.object_id);}
   }else{
    let chargeId=event.object_id;
    if(event.type==='charge.dispute.created'){const d=(await this.client.call('stripe','GET','/v1/disputes/'+event.object_id)).data;chargeId=typeof d.charge==='string'?d.charge:d.charge?.id;}
    if(!/^ch_[A-Za-z0-9]+$/.test(chargeId||''))throw Error('INVALID_RISK_EVENT');
    const c=(await this.client.call('stripe','GET','/v1/charges/'+chargeId)).data;
    if(c.livemode!==(this.env.STRIPE_MODE==='live'))throw Error('WRONG_RISK_ENVIRONMENT');
    if(c.refunded||c.amount_refunded>0||c.disputed){for(const row of this.ledger.rows('SELECT id FROM orders WHERE json_extract(payload,\'$.payment_intent\')=?',c.payment_intent))this.ledger.revoke(row.id);}
   }
   this.ledger.markEventDone(event.id);
   }catch(error){this.ledger.retryEvent(event.id,now,error.message==='ORDER_CONFLICT'||error.message==='INVALID_RISK_EVENT');}
  }
  const pending=this.ledger.rows('SELECT id,due FROM pending_sessions WHERE due<=? ORDER BY due,id LIMIT 2',now);
  for(const item of pending){try{const result=await validateSession(this.client,item.id,catalog,this.env);if(result.ok){this.ledger.acceptVerifiedOrder(result.order,result.fingerprint,now);this.ledger.sql.exec('DELETE FROM pending_sessions WHERE id=?',item.id);}else if(!result.pending){await this.storage.put('held-session:'+item.id,{reason:result.reason,at:now});this.ledger.sql.exec('DELETE FROM pending_sessions WHERE id=?',item.id);}else this.ledger.sql.exec('UPDATE pending_sessions SET due=? WHERE id=?',now+300000,item.id);}catch(error){this.ledger.sql.exec('UPDATE pending_sessions SET due=? WHERE id=?',now+300000,item.id);await this.storage.put('retry-session:'+item.id,{reason:'PROVIDER_RETRY',at:now});}}
  for(const row of this.ledger.due(now,1)){try{await processOne(this.ledger,provider,row.id,crypto.randomUUID(),Date.now());}catch(error){this.ledger.sql.exec("UPDATE orders SET due=?,error=? WHERE id=? AND state NOT IN ('SENT','HELD','REVOKED')",now+60000,'PROCESS_RETRY',row.id);}}

  await this.schedule(Date.now());
 }
}
