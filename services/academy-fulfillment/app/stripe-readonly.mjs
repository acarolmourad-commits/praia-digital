import {providerRoute} from './composio.mjs';
export class StripeReadonly {
 constructor(env,fetcher=fetch){this.env=env;this.fetcher=fetcher;
  if(!['test','live'].includes(env.STRIPE_MODE)||!env.STRIPE_READONLY_API_KEY?.startsWith('rk_'+env.STRIPE_MODE+'_'))throw Error('STRIPE_RESTRICTED_KEY_REQUIRED');
 }
 async call(method,path){
  const {url}=providerRoute('stripe',method,path);
  if(method!=='GET')throw Error('STRIPE_WRITE_NOT_ALLOWED');
  const response=await this.fetcher('https://api.stripe.com'+url.pathname+url.search,{method:'GET',headers:{Authorization:'Bearer '+this.env.STRIPE_READONLY_API_KEY,'Stripe-Version':'2026-10-28.endive'},redirect:'error',signal:AbortSignal.timeout(25000)});
  if(!response.ok)throw Error('STRIPE_READ_HTTP_'+response.status);
  return{status:response.status,data:await response.json()};
 }
}
