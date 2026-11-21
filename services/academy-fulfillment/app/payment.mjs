/* Authoritative Stripe reads via pinned Composio connection. This module does
 * not accept webhook payload payment assertions; signature verification is an
 * independent prerequisite for intake. No provider writes or logs.
 * Docs: docs.stripe.com/api/checkout/sessions/object;
 * docs.stripe.com/payments/currencies/localize-prices/adaptive-pricing
 */
class PolicyError extends Error {constructor(reason,extras={}){super(reason);this.reason=reason;this.extras=extras;}}
const fail=(reason,extras)=>{throw new PolicyError(reason,extras);};
const idOf=value=>typeof value==='string'?value:value?.id;
const safeId=(value,prefix)=>typeof value==='string'&&new RegExp('^'+prefix+'_[A-Za-z0-9_]+$').test(value);
const positive=value=>Number.isSafeInteger(value)&&value>0;
export function safeBuyerEmail(email){return typeof email==='string'&&email.length<=254&&/^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}$/.test(email)&&!email.includes('..');}
async function fingerprintOrder(order){
 const bytes=new TextEncoder().encode(JSON.stringify(order));
 return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
}
export async function validateSession(client,sessionId,catalog,env){
 try {
  if(!safeId(sessionId,'cs'))fail('INVALID_SESSION_ID');
  if(!['test','live'].includes(env.STRIPE_MODE)||!safeId(env.STRIPE_ACCOUNT_ID,'acct'))fail('INVALID_ENVIRONMENT');
  const live=env.STRIPE_MODE==='live';
  const account=(await client.call('stripe','GET','/v1/account')).data;
  if(account?.id!==env.STRIPE_ACCOUNT_ID)fail('ACCOUNT_MISMATCH');
  const s=await client.session(sessionId);
  if(s?.id!==sessionId||s.object!=='checkout.session'||s.livemode!==live||s.mode!=='payment')fail('SESSION_ENVIRONMENT_MISMATCH');
  const link=idOf(s.payment_link);const offers=catalog?.offers_by_payment_link||catalog;
  if(!safeId(link,'plink')||!offers||!Object.hasOwn(offers,link))fail('UNKNOWN_PAYMENT_LINK');
  const offer=offers[link];
  if(offer.automatic_enabled!==true)fail('OFFER_NOT_ENABLED');
  if(offer.edition!=='2026-private-kit-v2'||typeof offer.sku!=='string'||!/^[a-z0-9][a-z0-9-]{0,119}$/.test(offer.sku))fail('INVALID_CATALOG_EDITION');
  if(typeof offer.title!=='string'||offer.title.length<1||offer.title.length>240||/[\x00-\x1f\x7f]/.test(offer.title))fail('INVALID_CATALOG_TITLE');
  if(!positive(offer.unit_amount)||offer.currency!=='brl'||!safeId(offer.price_id,'price')||!safeId(offer.product_id,'prod'))fail('INVALID_CATALOG_PRICE');
  if(typeof offer.file_id!=='string'||!/^[A-Za-z0-9_-]+$/.test(offer.file_id)||!/^[a-f0-9]{64}$/.test(offer.sha256||'')||!positive(offer.bytes)||offer.bytes>18*1024*1024)fail('INVALID_PACKAGE_MANIFEST');
  if(s.payment_status==='unpaid'&&['open','complete'].includes(s.status))fail('PAYMENT_PENDING',{pending:true});
  if(s.status==='expired')fail('SESSION_EXPIRED');
  if(s.status!=='complete'||s.payment_status!=='paid')fail('PAYMENT_NOT_CONFIRMED');
  const amount=offer.unit_amount;
  // Adaptive Pricing keeps base integration currency on Session and PI. Foreign
  // presentment_details is informational and cannot override any price checks.
  if(s.currency!=='brl'||s.amount_total!==amount||s.amount_subtotal!==amount)fail('SESSION_PRICE_MISMATCH');
  if(!s.total_details||['amount_discount','amount_shipping','amount_tax'].some(k=>s.total_details[k]!==0))fail('UNAPPROVED_PRICE_ADJUSTMENT');
  const lines=await client.lineItems(sessionId);
  if(lines?.has_more!==false||!Array.isArray(lines.data)||lines.data.length!==1)fail('UNEXPECTED_LINE_ITEMS');
  const item=lines.data[0],price=item.price;
  if(item.quantity!==1||price?.id!==offer.price_id||idOf(price.product)!==offer.product_id||price.livemode!==live||price.type!=='one_time'||price.currency!=='brl'||price.unit_amount!==amount||item.currency!=='brl'||item.amount_total!==amount||item.amount_subtotal!==amount)fail('LINE_ITEM_MISMATCH');
  const piId=idOf(s.payment_intent);if(!safeId(piId,'pi'))fail('INVALID_PAYMENT_INTENT');
  const pi=(await client.call('stripe','GET','/v1/payment_intents/'+piId)).data;
  if(pi?.id!==piId||pi.livemode!==live||pi.status!=='succeeded'||pi.currency!=='brl'||pi.amount!==amount||pi.amount_received!==amount)fail('PAYMENT_INTENT_MISMATCH');
  const chargeId=idOf(pi.latest_charge);if(!safeId(chargeId,'ch'))fail('INVALID_LATEST_CHARGE');
  const charge=(await client.call('stripe','GET','/v1/charges/'+chargeId)).data;
  if(charge?.id!==chargeId||idOf(charge.payment_intent)!==piId||charge.livemode!==live||charge.paid!==true||charge.captured!==true)fail('CHARGE_NOT_CONFIRMED');
  if(charge.refunded===true||(Number.isSafeInteger(charge.amount_refunded)&&charge.amount_refunded>0)||charge.disputed===true)fail('REFUNDED_OR_DISPUTED',{revoked:true});
  if(charge.refunded!==false||charge.amount_refunded!==0||charge.disputed!==false)fail('CHARGE_RISK_STATE_UNKNOWN');
  const email=s.customer_details?.email;if(!safeBuyerEmail(email))fail('INVALID_BUYER_EMAIL');
  if(!live&&(!safeBuyerEmail(env.TEST_BUYER_EMAIL)||email.toLowerCase()!==env.TEST_BUYER_EMAIL.toLowerCase()))fail('TEST_RECIPIENT_NOT_ALLOWED');
  // Fixed field order yields a reproducible immutable order fingerprint.
  const order={id:sessionId,session_id:sessionId,account_id:env.STRIPE_ACCOUNT_ID,livemode:live,payment_intent:piId,payment_link:link,price_id:offer.price_id,product_id:offer.product_id,sku:offer.sku,title:offer.title,edition:offer.edition,email,amount,currency:'brl',file_id:offer.file_id,sha256:offer.sha256,bytes:offer.bytes};
  return {ok:true,order,fingerprint:await fingerprintOrder(order)};
 } catch(error){
  if(error instanceof PolicyError)return {ok:false,pending:false,reason:error.reason,...error.extras};
  throw error; // Provider auth/quota/network failure is NOT a failed payment.
 }
}
