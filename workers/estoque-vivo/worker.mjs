import {InventoryRoom} from './room.mjs';
import {AppError,text} from './domain.mjs';
import {assets} from './assets.mjs';
export {InventoryRoom};
const COOKIE='__Host-ev_session';
const PAIR=/^([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})\.([A-Za-z0-9_-]{43})$/;
const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY','X-Robots-Tag':'noindex, nofollow','Content-Security-Policy':"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; worker-src 'self'; manifest-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'self'",'Permissions-Policy':'camera=(), microphone=(), geolocation=()'};
const token=()=>btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(32)))).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');
export const digest=async s=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s)))].map(b=>b.toString(16).padStart(2,'0')).join('');
function json(body,status=200,cookie){return new Response(JSON.stringify(body),{status,headers:{...headers,'Content-Type':'application/json; charset=utf-8',...(cookie?{'Set-Cookie':cookie}:{})}});}
function cookie(value,age=43200){return `${COOKIE}=${value}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${age}`;}
async function body(req){if(req.headers.get('Content-Type')?.split(';')[0]!=='application/json')throw new AppError('Formato inválido.',415);if(!req.body)throw new AppError('Dados ausentes.',400);const reader=req.body.getReader();let chunks=[],n=0;while(true){const {done,value}=await reader.read();if(done)break;n+=value.byteLength;if(n>12000){await reader.cancel();throw new AppError('Dados muito longos.',413);}chunks.push(value);}const a=new Uint8Array(n);let offset=0;for(const c of chunks){a.set(c,offset);offset+=c.length;}try{const parsed=JSON.parse(new TextDecoder().decode(a));if(!parsed||typeof parsed!=='object'||Array.isArray(parsed))throw new Error();return parsed;}catch{throw new AppError('Dados inválidos.',400);}}
export default {async fetch(req,env){const url=new URL(req.url),path=url.pathname;
 try{
  if(path==='/api/push-config'&&req.method==='GET'){let k;try{k=JSON.parse(env.VAPID_KEYS||'null');}catch{}return json({enabled:!!k,publicKey:k?.publicKey||null});}
  if(path==='/health')return json({ok:true,service:'estoque-vivo',version:'1.2.0'});
  if(!path.startsWith('/api/')){if(req.method!=='GET')return json({error:'Método inválido.'},405);const asset=assets[path];if(!asset)return json({error:'Página não encontrada.'},404);return new Response(asset.encoding==='base64'?Uint8Array.from(atob(asset.body),c=>c.charCodeAt(0)):asset.body,{headers:{...headers,'Content-Security-Policy':headers['Content-Security-Policy'].replace("connect-src 'self';",`connect-src 'self' ${url.origin.replace(/^http/,'ws')};`),'Content-Type':asset.type}});}
  if(path==='/api/integration/order'){
   if(req.method!=='POST')return json({error:'Método inválido.'},405);
   if(req.headers.has('Origin'))return json({error:'Use esta API somente em um servidor autorizado.'},403);
   const ip=req.headers.get('CF-Connecting-IP')||'unknown';
   if(env.API_LIMITER&&!(await env.API_LIMITER.limit({key:'integration:'+ip})).success)return json({error:'Muitas tentativas. Aguarde um minuto.'},429);
   const key=req.headers.get('Authorization')?.match(/^Bearer EI1-([0-9a-f-]{36})\.([0-9a-f-]{36})\.([A-Za-z0-9_-]{43})$/);
   if(!key||!PAIR.test(key[1]+'.'+key[3])||!PAIR.test(key[2]+'.'+key[3]))return json({error:'Chave de integração inválida.'},401);
   const b=await body(req),payloadHash=await digest(JSON.stringify(b));
   const content={reference:b.reference,status:b.status,items:Array.isArray(b.items)?b.items.map(i=>({sku:String(i?.sku||'').trim().toUpperCase(),quantity:i?.quantity})).sort((a,b)=>a.sku.localeCompare(b.sku)):null};
   const r=await env.ROOMS.getByName(key[1]).integrationWrite(key[2],await digest(key[3]),b,payloadHash,await digest(JSON.stringify(content)));
   const {status,...payload}=r;return json(payload,status);
  }
  if(req.method!=='GET'&&req.method!=='POST')return json({error:'Método inválido.'},405);
  if((req.method==='POST'||path==='/api/events')&&req.headers.get('Origin')!==url.origin)return json({error:'Origem não autorizada.'},403);
  const ip=req.headers.get('CF-Connecting-IP')||'unknown';
  const authPath=path==='/api/create'||path==='/api/login';
  const limiter=authPath?env.AUTH_LIMITER:env.API_LIMITER;
  if(limiter&&!(await limiter.limit({key:ip})).success)return json({error:'Muitas tentativas. Aguarde um minuto.'},429);
  if(authPath){if(req.method!=='POST')return json({error:'Método inválido.'},405);const b=await body(req),actor=text(b.actor,60);const session=token();let id,r,key;
   if(path==='/api/create'){id=crypto.randomUUID();key=token();r=await env.ROOMS.getByName(id).initialize(id,text(b.name,100),await digest(key),await digest(session),actor);}
   else {const match=PAIR.exec(String(b.key||'').replace(/^EV1-/,'').trim());if(!match)throw new AppError('Chave inválida.',401);[,id,key]=match;r=await env.ROOMS.getByName(id).login(await digest(key),await digest(session),actor);}
   if(!r.ok)return json({error:r.error},r.status);return json({ok:true,...(path==='/api/create'?{key:`EV1-${id}.${key}`}:{})},200,cookie(`${id}.${session}`));
  }
  const raw=req.headers.get('Cookie')?.split(';').map(s=>s.trim()).find(s=>s.startsWith(COOKIE+'='))?.slice(COOKIE.length+1);const match=PAIR.exec(raw||'');if(!match)return json({error:'Entre no espaço da sua marca.'},401);const [,id,secret]=match,hash=await digest(secret),room=env.ROOMS.getByName(id);
  if(path==='/api/events'){if(req.method!=='GET')return json({error:'Método inválido.'},405);const h=new Headers(req.headers);h.set('X-Session-Hash',hash);return room.fetch(new Request(req.url,{method:'GET',headers:h}));}
  let r,extraCookie;
  if(path==='/api/state'&&req.method==='GET')r=await room.snapshot(hash);
  else if(path==='/api/export'&&req.method==='GET')r=await room.historyPage(hash,Number(url.searchParams.get('before')||1000000000));
  else if(path==='/api/orders'&&req.method==='GET')r=await room.ordersPage(hash,{before:Number(url.searchParams.get('before')||1000000000),status:url.searchParams.get('status')||'',q:url.searchParams.get('q')||''});
  else if(path==='/api/connections'&&req.method==='GET')r=await room.connectionsList(hash);
  else if(req.method==='POST'){
   const b=await body(req);
   if(path==='/api/logout'){r=await room.logout(hash);extraCookie=cookie('',0);}
   else if(path==='/api/rotate'){if(b.confirm!=='ALTERAR CHAVE'||!/^[A-Za-z0-9_-]{43}$/.test(b.new_key||''))throw new AppError('Confirme a alteração da chave.');const s=token();r=await room.rotate(hash,await digest(b.new_key),await digest(s));if(r.ok){extraCookie=cookie(`${id}.${s}`);}}
   else if(['/api/push-subscribe','/api/push-unsubscribe','/api/push-test'].includes(path)){const action=path.slice('/api/push-'.length),endpoint=b.subscription?.endpoint||b.endpoint||'';r=await room.configurePush(hash,action,b,await digest(endpoint));}
   else if(path==='/api/order')r=await room.orderWrite(hash,b,await digest(JSON.stringify({path,body:b})));
   else if(path==='/api/connection'){
    if(!b.revoke&&!/^[A-Za-z0-9_-]{43}$/.test(b.connection_key||''))throw new AppError('Chave de integração inválida.');
    const {connection_key,...clean}=b;r=await room.connectionWrite(hash,{...clean,key_hash:connection_key?await digest(connection_key):''},await digest(JSON.stringify({path,body:b})));
   }
   else if(path==='/api/member'){if(!b.revoke&&!/^[A-Za-z0-9_-]{43}$/.test(b.member_key||''))throw new AppError('Chave de acesso inválida.');const {member_key,...clean}=b;r=await room.mutate(hash,'member',{...clean,member_hash:member_key?await digest(member_key):''},await digest(JSON.stringify(b)));}
   else if(['/api/product','/api/movement','/api/archive'].includes(path))r=await room.mutate(hash,path.slice(5),b,await digest(JSON.stringify({path,body:b})));
   else throw new AppError('Ação não encontrada.',404);
  }else throw new AppError('Ação não encontrada.',404);
  const {status,...payload}=r;return json(payload,status,extraCookie);
 }catch(e){if(e instanceof AppError)return json({error:e.message},e.status);console.error(JSON.stringify({event:'inventory_request_failed'}));return json({error:'Serviço indisponível. Nenhuma operação foi confirmada nesta resposta. Tente novamente com os mesmos dados.'},503);}
}};
