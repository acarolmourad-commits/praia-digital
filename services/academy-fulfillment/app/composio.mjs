/* Fixed internal provider routes. Never expose this class as a public proxy. */
export class Composio {
 constructor(env,fetcher=fetch){this.env=env;this.fetcher=fetcher;}
 async call(kind,method,path,body){
  const allowed={stripe:[/^GET \/v1\/account$/, /^GET \/v1\/checkout\/sessions\/cs_[A-Za-z0-9_]+(?:\/line_items)?$/, /^GET \/v1\/payment_intents\/pi_[A-Za-z0-9]+$/, /^GET \/v1\/charges\/ch_[A-Za-z0-9]+$/, /^GET \/v1\/disputes\/dp_[A-Za-z0-9]+$/],drive:[/^GET \/drive\/v3\/files\/[A-Za-z0-9_-]+$/],gmail:[/^GET \/gmail\/v1\/users\/me\/profile$/, /^POST \/gmail\/v1\/users\/me\/drafts$/, /^POST \/gmail\/v1\/users\/me\/drafts\/send$/, /^GET \/gmail\/v1\/users\/me\/(drafts|messages)(?:\/[A-Za-z0-9_-]+)?$/]};
  const url=new URL(path,'https://placeholder.invalid');
  if(!allowed[kind]?.some(r=>r.test(method+' '+url.pathname))||url.origin!=='https://placeholder.invalid')throw Error('DISALLOWED_PROVIDER_ROUTE');
  const id=this.env[kind.toUpperCase()+'_CONNECTION_ID'];
  if(!/^ca_[A-Za-z0-9_-]+$/.test(id||'')||!this.env.COMPOSIO_API_KEY||!this.env.COMPOSIO_USER_ID)throw Error('PROVIDER_NOT_CONFIGURED');
  const host={stripe:'https://api.stripe.com',drive:'https://www.googleapis.com',gmail:'https://gmail.googleapis.com'}[kind];
  const parameters=[...url.searchParams].map(([name,value])=>({in:'query',name,value}));
  if(kind==='stripe')parameters.push({in:'header',name:'Stripe-Version',value:'2026-10-28.endive'});
  const response=await this.fetcher('https://backend.composio.dev/api/v3.1/tools/execute/proxy',{method:'POST',headers:{'content-type':'application/json','x-api-key':this.env.COMPOSIO_API_KEY},body:JSON.stringify({connected_account_id:id,user_id:this.env.COMPOSIO_USER_ID,endpoint:host+url.pathname,method,parameters,...(body?{body}:{} )}),redirect:'error',signal:AbortSignal.timeout(25000)});
  if(!response.ok)throw Error('COMPOSIO_HTTP_'+response.status);
  const result=await response.json();
  if(!Number.isInteger(result.status)||result.status<200||result.status>=300)throw Error('PROVIDER_HTTP_FAILURE');
  return result;
 }
 async identity(){const a=(await this.call('stripe','GET','/v1/account')).data;const g=(await this.call('gmail','GET','/gmail/v1/users/me/profile')).data;if(a?.id!==this.env.STRIPE_ACCOUNT_ID||g?.emailAddress!==this.env.SENDER_EMAIL)throw Error('PROVIDER_IDENTITY_MISMATCH');return true;}
 async session(id){if(!/^cs_[A-Za-z0-9_]+$/.test(id))throw Error('BAD_SESSION_ID');return(await this.call('stripe','GET','/v1/checkout/sessions/'+id)).data;}
 async lineItems(id){if(!/^cs_[A-Za-z0-9_]+$/.test(id))throw Error('BAD_SESSION_ID');return(await this.call('stripe','GET','/v1/checkout/sessions/'+id+'/line_items?limit=100')).data;}
 async privateMetadata(id){if(!/^[A-Za-z0-9_-]+$/.test(id))throw Error('BAD_FILE_ID');const fields='id,name,size,mimeType,trashed,driveId,owners(emailAddress),permissions(type,role,emailAddress)';const m=(await this.call('drive','GET','/drive/v3/files/'+id+'?fields='+encodeURIComponent(fields))).data;if(m?.trashed||m?.driveId||m?.owners?.length!==1||m.owners[0].emailAddress!==this.env.SENDER_EMAIL||m?.permissions?.length!==1||m.permissions[0].type!=='user'||m.permissions[0].role!=='owner'||m.permissions[0].emailAddress!==this.env.SENDER_EMAIL)throw Error('FILE_NOT_OWNER_ONLY');return m;}
 async draft(raw){if(typeof raw!=='string'||!/^[-_A-Za-z0-9]+$/.test(raw))throw Error('INVALID_MIME');return(await this.call('gmail','POST','/gmail/v1/users/me/drafts',{message:{raw}})).data;}
 async sendDraft(id){if(!/^[A-Za-z0-9_-]+$/.test(id))throw Error('INVALID_DRAFT_ID');return(await this.call('gmail','POST','/gmail/v1/users/me/drafts/send',{id})).data;}
 async downloadVerifiedZip(offer){
  if(!offer||!Number.isInteger(offer.bytes)||offer.bytes<1||offer.bytes>18*1024*1024||!/^[a-f0-9]{64}$/.test(offer.sha256||''))throw Error('INVALID_PACKAGE_MANIFEST');
  const meta=await this.privateMetadata(offer.file_id);
  if(Number(meta.size)!==offer.bytes)throw Error('PACKAGE_SIZE_CHANGED');
  const result=await this.call('drive','GET','/drive/v3/files/'+offer.file_id+'?alt=media');
  const binary=result.binary_data;
  const hosts=JSON.parse(this.env.COMPOSIO_DOWNLOAD_HOSTS_JSON||'[]');
  if(!binary?.url||Number(binary.size)!==offer.bytes)throw Error('INVALID_BINARY_RESPONSE');
  const url=new URL(binary.url);
  if(url.protocol!=='https:'||url.username||url.password||!hosts.includes(url.hostname))throw Error('UNAPPROVED_DOWNLOAD_ORIGIN');
  const response=await this.fetcher(url.toString(),{redirect:'error',signal:AbortSignal.timeout(25000)});
  if(!response.ok||!response.body)throw Error('DOWNLOAD_FAILED');
  const reader=response.body.getReader();let length=0;const chunks=[];
  while(true){const r=await reader.read();if(r.done)break;length+=r.value.length;if(length>offer.bytes){await reader.cancel();throw Error('DOWNLOAD_TOO_LARGE');}chunks.push(r.value);}
  if(length!==offer.bytes)throw Error('DOWNLOAD_TRUNCATED');
  const bytes=new Uint8Array(length);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.length;}
  const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
  if(hash!==offer.sha256)throw Error('PACKAGE_HASH_CHANGED');
  await this.privateMetadata(offer.file_id); // Permission drift during fetch fails closed.
  return bytes;
 }

}
