/* Gmail MIME + reconciliation for OWN generated two-part messages only.
 * No generic MIME reinterpretation: unexpected normalization/edits fail closed.
 * Official contracts: Gmail raw is base64url RFC2822; drafts.get?format=raw;
 * messages.list q=rfc822msgid + labelIds=SENT then messages.get?format=raw.
 * Calls never retry create/send automatically. No external actions on import.
 */
const encoder=new TextEncoder();
const decoder=new TextDecoder('utf-8',{fatal:true});
const SUBJECT='Seu kit Praia Digital Academy';
function email(value){if(typeof value!=='string'||value.length>254||! /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}$/.test(value))throw Error('INVALID_EMAIL');return value;}
function b64(bytes){let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(s);}
function fromB64(text){const s=text.replace(/[\r\n\t ]/g,'');if(!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(s))throw Error('INVALID_BASE64');const str=atob(s);return Uint8Array.from(str,c=>c.charCodeAt(0));}
export function encodeRaw(text){return b64(encoder.encode(text)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
export function decodeRaw(raw){if(typeof raw!=='string'||raw.length>36*1024*1024||!/^[-_A-Za-z0-9]*={0,2}$/.test(raw))throw Error('INVALID_RAW');let s=raw.replace(/-/g,'+').replace(/_/g,'/').replace(/=+$/,'');s+='='.repeat((4-s.length%4)%4);return decoder.decode(fromB64(s));}
async function digest(bytes){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');}
function orderFrom(row){const original=typeof row.payload==='string'?JSON.parse(row.payload):row.payload;const o=original&&{...original,package_sha256:original.package_sha256??original.sha256,package_bytes:original.package_bytes??original.bytes};if(original?.package_sha256&&original.sha256&&original.package_sha256!==original.sha256)throw Error('CONFLICTING_PACKAGE_HASH');if(original?.package_bytes!==undefined&&original.bytes!==undefined&&original.package_bytes!==original.bytes)throw Error('CONFLICTING_PACKAGE_SIZE');if(!o||typeof o.id!=='string'||o.id.length>250||!o.id||! /^[a-z0-9][a-z0-9-]{0,119}$/.test(o.sku||'')||typeof o.edition!=='string'||/[\r\n\x00-\x1f]/.test(o.edition)||o.edition.length>100||typeof o.title!=='string'||!o.title||o.title.length>240||/[\r\n\x00-\x1f]/.test(o.title)||!/^[a-f0-9]{64}$/.test(o.package_sha256||'')||!Number.isInteger(o.package_bytes)||o.package_bytes<1||o.package_bytes>18*1024*1024)throw Error('INVALID_MAIL_ORDER');email(o.email);return o;}
async function intent(order,senderEmail,messageDomain){
 const sender=email(senderEmail);if(!/^[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$/.test(messageDomain))throw Error('INVALID_MESSAGE_DOMAIN');
 const marker=await digest(encoder.encode(JSON.stringify([order.id,order.sku,order.edition,order.package_sha256])));
 const messageId='<academy.'+marker+'@'+messageDomain+'>';
 const text=['Olá!','',`Seu conteúdo comprado está no arquivo ZIP anexo: ${order.title}.`,`Edição: ${order.edition}.`,'','Abra o ZIP para acessar os materiais digitais.','Em caso de dificuldade com o arquivo, responda a este e-mail.','','Praia Digital Academy'].join('\r\n');
 return {sender,recipient:order.email,messageId,marker,text,filename:order.sku+'.zip',boundary:'praia_'+marker};
}
const lines=s=>s.match(/.{1,76}/g)?.join('\r\n')||'';
export async function buildMessage(row,zipBytes,{senderEmail,messageDomain='praia.digital',now=Date.now()}={}){
 const o=orderFrom(row);if(!(zipBytes instanceof Uint8Array)||zipBytes.length!==o.package_bytes||await digest(zipBytes)!==o.package_sha256)throw Error('ATTACHMENT_HASH_MISMATCH');
 const i=await intent(o,senderEmail,messageDomain);const date=new Date(now);if(!Number.isFinite(date.getTime()))throw Error('INVALID_DATE');
 const mime=[`From: ${i.sender}`,`To: ${i.recipient}`,`Date: ${date.toUTCString()}`,`Subject: ${SUBJECT}`,`Message-ID: ${i.messageId}`,`X-Praia-Order: ${i.marker}`,'MIME-Version: 1.0',`Content-Type: multipart/mixed; boundary="${i.boundary}"`,'',`--${i.boundary}`,'Content-Type: text/plain; charset=UTF-8','Content-Transfer-Encoding: base64','',lines(b64(encoder.encode(i.text))),`--${i.boundary}`,'Content-Type: application/zip',`Content-Disposition: attachment; filename="${i.filename}"`,'Content-Transfer-Encoding: base64','',lines(b64(zipBytes)),`--${i.boundary}--`,''].join('\r\n');
 return {raw:encodeRaw(mime),messageId:i.messageId};
}
function entity(text){const split=text.indexOf('\r\n\r\n');if(split<0)throw Error('BAD_MIME');const head=text.slice(0,split);if(head.length>65536)throw Error('HEADER_LIMIT');const headers=new Map();for(const line of head.replace(/\r\n[ \t]+/g,' ').split('\r\n')){const m=/^([A-Za-z0-9-]+):[ \t]*(.*)$/.exec(line);if(!m||/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(m[2]))throw Error('BAD_HEADER');const k=m[1].toLowerCase();headers.set(k,[...(headers.get(k)||[]),m[2].trim()]);}return{headers,body:text.slice(split+4)};}
function single(headers,name){const found=headers.get(name);if(!found||found.length!==1)throw Error('MISSING_OR_DUPLICATE_HEADER');return found[0];}
export async function verifyRaw(row,raw,options){
 const o=orderFrom(row);const i=await intent(o,options.senderEmail,options.messageDomain||'praia.digital');const main=entity(decodeRaw(raw).replace(/\r?\n/g,'\r\n'));
 for(const name of ['cc','bcc','reply-to','resent-to','resent-cc','resent-bcc','resent-from','resent-sender','sender'])if(main.headers.has(name))throw Error('EXTRA_RECIPIENT_OR_SENDER');
 if(single(main.headers,'from')!==i.sender||single(main.headers,'to')!==i.recipient||single(main.headers,'subject')!==SUBJECT||single(main.headers,'message-id')!==i.messageId||single(main.headers,'x-praia-order')!==i.marker||single(main.headers,'mime-version')!=='1.0')throw Error('MAIL_INTENT_MISMATCH');
 if(main.headers.has('content-transfer-encoding')&&single(main.headers,'content-transfer-encoding').toLowerCase()!=='7bit')throw Error('UNEXPECTED_TOP_ENCODING');
 if(single(main.headers,'content-type')!==`multipart/mixed; boundary="${i.boundary}"`)throw Error('MIME_TYPE_MISMATCH');
 const chunks=main.body.split('--'+i.boundary);
 if(chunks.length!==4||chunks[0].trim()!==''||chunks[3].trim()!=='--')throw Error('MIME_PART_COUNT');
 const parts=chunks.slice(1,3).map(s=>entity(s.replace(/^\r\n/,'').replace(/\r\n$/,'')));
 if(single(parts[0].headers,'content-type').toLowerCase()!=='text/plain; charset=utf-8'||single(parts[0].headers,'content-transfer-encoding').toLowerCase()!=='base64'||decoder.decode(fromB64(parts[0].body))!==i.text)throw Error('MAIL_BODY_MISMATCH');
 if(single(parts[1].headers,'content-type').toLowerCase()!=='application/zip'||single(parts[1].headers,'content-disposition')!==`attachment; filename="${i.filename}"`||single(parts[1].headers,'content-transfer-encoding').toLowerCase()!=='base64')throw Error('ATTACHMENT_TYPE_MISMATCH');
 const attachment=fromB64(parts[1].body);if(attachment.length!==o.package_bytes||await digest(attachment)!==o.package_sha256)throw Error('ATTACHMENT_HASH_MISMATCH');
 return true;
}
export class GmailDelivery {
 constructor(composio,options){this.api=composio;this.options={senderEmail:email(options.senderEmail),messageDomain:options.messageDomain||'praia.digital'};}
 async createExactDraft(row,checked){const built=await buildMessage(row,checked.zipBytes,this.options);const result=await this.api.draft(built.raw);if(!/^[A-Za-z0-9_-]+$/.test(result?.id||''))throw Error('INVALID_DRAFT_RESPONSE');return{id:result.id};}
 async verifyExactDraft(row){if(!/^[A-Za-z0-9_-]+$/.test(row.draft_id||''))throw Error('INVALID_DRAFT_ID');const d=(await this.api.call('gmail','GET','/gmail/v1/users/me/drafts/'+row.draft_id+'?format=raw')).data;if(d?.id!==row.draft_id||typeof d?.message?.raw!=='string')throw Error('DRAFT_RESPONSE_MISMATCH');return verifyRaw(row,d.message.raw,this.options);}
 async findVerifiedSent(row){
  const o=orderFrom(row);const i=await intent(o,this.options.senderEmail,this.options.messageDomain);const query=new URLSearchParams({q:'rfc822msgid:'+i.messageId,labelIds:'SENT',maxResults:'2',includeSpamTrash:'true'});
  const page=(await this.api.call('gmail','GET','/gmail/v1/users/me/messages?'+query)).data;
  // More than100 matches is anomalous. Do not treat a truncated page as zero.
  if(!page||page.nextPageToken||(page.messages?.length>2)|| (page.messages!==undefined&&!Array.isArray(page.messages)))throw Error('INCOMPLETE_SENT_SEARCH');
  const results=[];const seen=new Set();
  for(const found of page.messages||[]){if(!/^[A-Za-z0-9_-]+$/.test(found?.id||'')||seen.has(found.id))throw Error('INVALID_SENT_SEARCH');seen.add(found.id);const message=(await this.api.call('gmail','GET','/gmail/v1/users/me/messages/'+found.id+'?format=raw')).data;if(message?.id!==found.id||!message?.labelIds?.includes('SENT'))throw Error('SENT_MESSAGE_MISMATCH');await verifyRaw(row,message.raw,this.options);results.push({id:message.id});}
  return results;
 }
 async sendExistingDraft(id){return this.api.sendDraft(id);}
}
