import {ConsumerComposio} from './consumer-composio.mjs';
import {StripeReadonly} from './stripe-readonly.mjs';
export class AcademyProviders extends ConsumerComposio {
 constructor(env,fetcher=fetch){
  // Consumer session is Google-only: the unrelated Stripe OAuth connection is
  // neither selected nor modified. Correct merchant uses approved restricted key.
  super(env,fetcher,['gmail','googledrive']);
  this.stripeReadonly=new StripeReadonly(env,fetcher);
 }
 call(kind,method,path,body){
  if(kind==='stripe'){if(body!==undefined)throw Error('STRIPE_BODY_NOT_ALLOWED');return this.stripeReadonly.call(method,path);}
  return super.call(kind,method,path,body);
 }
}
