import {DurableObject} from 'cloudflare:workers';
import {Ledger} from '../durable/store.mjs';
import {verifiedEvent} from './signature.mjs';
import {Coordinator} from './coordinator.mjs';
const TYPES=new Set(['checkout.session.completed','checkout.session.async_payment_succeeded','checkout.session.async_payment_failed','charge.refunded','charge.dispute.created']);
export class AcademyLedger extends DurableObject {
 constructor(ctx,env){super(ctx,env);this.ctx=ctx;this.env=env;this.ledger=new Ledger(ctx.storage);}
 async intake(event){
  // Storage input/output gates protect this storage-only sequence.
   const record=this.ledger.recordEvent(event);
   const due=Date.now()+1000, existing=await this.ctx.storage.getAlarm();
   if(existing===null||existing>due)await this.ctx.storage.setAlarm(due);
   return {persisted:true,event_id:record.id};
 }
 async wake(){
  if(this.env.AUTOMATIC_DELIVERY_ENABLED!=='true')return;
  await new Coordinator(this.ledger,this.ctx.storage,this.env).schedule();
 }
 async alarm(){
  if(this.env.AUTOMATIC_DELIVERY_ENABLED!=='true')return;
  await new Coordinator(this.ledger,this.ctx.storage,this.env).run();
 }
}
export default {async scheduled(event,env,ctx){
 if(env.WATCHDOG_ENABLED!=='true'||env.AUTOMATIC_DELIVERY_ENABLED!=='true')return;
 const id=env.LEDGER.idFromName(env.STRIPE_ACCOUNT_ID+':'+env.STRIPE_MODE);
 ctx.waitUntil(env.LEDGER.get(id).wake());
},async fetch(request,env){
 const path=new URL(request.url).pathname;
 if(request.method==='GET'&&path==='/health')return Response.json({service:'academy-fulfillment',automatic_delivery:env.AUTOMATIC_DELIVERY_ENABLED==='true'});
 if(request.method!=='POST'||path!=='/stripe-webhook')return new Response('Not found',{status:404});
 if(env.WEBHOOK_INTAKE_ENABLED!=='true')return new Response('Not enabled',{status:503});
 try{
  const e=await verifiedEvent(request,env.STRIPE_WEBHOOK_SECRET);
  if(!['test','live'].includes(env.STRIPE_MODE)||e.livemode!==(env.STRIPE_MODE==='live')||(e.account&&e.account!==env.STRIPE_ACCOUNT_ID)||!/^evt_[A-Za-z0-9]+$/.test(e.id||''))return new Response('Invalid event',{status:400});
  if(!TYPES.has(e.type))return new Response('Ignored',{status:200});
  const objectId=e.data?.object?.id;if(typeof objectId!=='string'||!Number.isInteger(e.created))return new Response('Invalid object',{status:400});
  const id=env.LEDGER.idFromName(env.STRIPE_ACCOUNT_ID+':'+env.STRIPE_MODE);
  const ack=await env.LEDGER.get(id).intake({id:e.id,type:e.type,object_id:objectId,created:e.created});
  return ack.persisted===true&&ack.event_id===e.id?new Response('Recorded',{status:200}):new Response('Not persisted',{status:503});
 }catch(_){return new Response('Webhook not accepted',{status:503});}
}};
