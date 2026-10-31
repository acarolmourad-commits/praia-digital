/* Consumer-session proxy implementation, explicitly selected only after actual
 * consumer connection pins/configuration and real provider TEST validation. */
import {Composio,providerRoute} from './composio.mjs';
import {ConsumerSession} from './consumer-session.mjs';
export class ConsumerComposio extends Composio {
 constructor(env,fetcher=fetch){
  super(env,fetcher);
  let accounts;try{accounts=JSON.parse(env.COMPOSIO_CONSUMER_ACCOUNTS_JSON);}catch(_){throw Error('CONSUMER_ACCOUNTS_REQUIRED');}
  const policy=Object.fromEntries(Object.entries(accounts||{}).map(([kind,account])=>[kind,{account,tools:[]} ]));
  this.sessionClient=new ConsumerSession(env,policy,fetcher,true);
 }
 async call(kind,method,path,body){
  const {url}=providerRoute(kind,method,path); // SAME fixed internal allowlist.
  if(!this.sessionClient.checked||method!=='GET')await this.sessionClient.verifySession();
  const parameters=[...url.searchParams].map(([name,value])=>({in:'query',name,value}));
  if(kind==='stripe')parameters.push({in:'header',name:'Stripe-Version',value:'2026-10-28.endive'});
  const host={stripe:'https://api.stripe.com',drive:'https://www.googleapis.com',gmail:'https://gmail.googleapis.com'}[kind];
  const result=await this.sessionClient.request('/'+this.env.COMPOSIO_CONSUMER_SESSION_ID+'/proxy_execute','POST',{toolkit_slug:kind==='drive'?'googledrive':kind,endpoint:host+url.pathname,method,parameters,...(body?{body}:{})});
  // A blocked/failed response might follow an upstream side effect. Never retry.
  if(result.result_type!=='completed'||result.instant_charge||!Number.isInteger(result.status)||result.status<200||result.status>=300)throw Error('CONSUMER_PROXY_UNCONFIRMED');
  return result;
 }
}
