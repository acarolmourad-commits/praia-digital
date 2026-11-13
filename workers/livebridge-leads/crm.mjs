import {HTML,CSS,JS} from './crm-ui.mjs';
const ADMIN='comercial@praia.digital';
const HOSTS=new Set(['crm.praia.digital','praia-livebridge-leads.kleber-f63.workers.dev','worker.test']);
const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY','X-Robots-Tag':'noindex, nofollow','Content-Security-Policy':"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"};
const reply=(data,status=200,extra={})=>new Response(JSON.stringify(data),{status,headers:{...headers,'Content-Type':'application/json; charset=utf-8',...extra}});
const random=()=>Array.from(crypto.getRandomValues(new Uint8Array(32)),b=>b.toString(16).padStart(2,'0')).join('');
export const digest=async s=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s))),b=>b.toString(16).padStart(2,'0')).join('');
const fail=(message,status=422)=>{throw Object.assign(new Error(message),{status});};
const str=(v,n,required=false)=>{if(typeof v!=='string'||v.trim().length>n||(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/).test(v)||(required&&!v.trim()))fail('Confira os campos informados.');return v.trim();};
const date=v=>{v=str(v,10);if(v&&(!/^\d{4}-\d{2}-\d{2}$/.test(v)||!Number.isFinite(Date.parse(v))||new Date(v).toISOString().slice(0,10)!==v))fail('Data inválida.');return v;};
const money=v=>{if(!Number.isSafeInteger(v)||v<0||v>100000000000)fail('Valor inválido.');return v;};
async function body(req){if(!req.headers.get('Content-Type')?.startsWith('application/json'))fail('Formato inválido.',415);let size=0;const parts=[];const reader=req.body?.getReader();if(!reader)fail('Dados ausentes.');while(true){const r=await reader.read();if(r.done)break;size+=r.value.length;if(size>16000){await reader.cancel();fail('Texto muito longo.',413);}parts.push(r.value);}const bytes=new Uint8Array(size);let at=0;for(const p of parts){bytes.set(p,at);at+=p.length;}try{return JSON.parse(new TextDecoder().decode(bytes));}catch{fail('Dados inválidos.',400);}}
const query=(env,sql,...args)=>env.LEADS_DB.prepare(sql).bind(...args);
export async function crm(request,env){
 const url=new URL(request.url),p=url.pathname,method=request.method;
 if(!HOSTS.has(url.hostname))return reply({error:'Endereço inválido.'},403);
 try{
 if(method==='GET'&&['/crm','/crm/','/crm/app.css','/crm/app.js'].includes(p)){
 const asset=p.endsWith('.css')?[CSS,'text/css']:p.endsWith('.js')?[JS,'text/javascript']:[HTML,'text/html'];
 return new Response(asset[0],{headers:{...headers,'Content-Type':asset[1]+'; charset=utf-8'}});
 }
 if(!p.startsWith('/crm/api/'))return reply({error:'Não encontrado.'},404);
 if(method!=='GET'&&(request.headers.get('Origin')!==url.origin||!request.headers.get('Content-Type')?.startsWith('application/json')))return reply({error:'Origem ou formato inválido.'},403);
 const now=Date.now();
 if(p==='/crm/api/login'&&method==='POST'){
 const ip=request.headers.get('CF-Connecting-IP')||'unknown';
 if(!(await env.LEAD_LIMITER.limit({key:'crm-login:'+ip})).success)return reply({error:'Aguarde um minuto.'},429);
 const token=random(),hash=await digest(token);
 const claim=await query(env,`INSERT INTO crm_auth(id,token_hash,expires_at,next_send) VALUES('admin',?,?,?) ON CONFLICT(id) DO UPDATE SET token_hash=excluded.token_hash,expires_at=excluded.expires_at,next_send=excluded.next_send WHERE crm_auth.next_send<=? AND (crm_auth.token_hash IS NULL OR crm_auth.expires_at<=?)`,hash,now+900000,now+90000,now,now).run();
 if(!claim.meta?.changes)return reply({error:'Um código já foi solicitado. Use o código recebido; se expirou, tente novamente após 15 minutos.'},429);
 try{await env.EMAIL.send({from:'solicitacoes@avisos.praia.digital',to:ADMIN,subject:'Seu acesso ao CRM Praia Digital',text:`Código de acesso ao CRM Praia Digital (válido por 15 minutos):\n\n${token}\n\nAbra https://crm.praia.digital/crm/ e cole o código. Não compartilhe este código. Se não solicitou acesso, ignore esta mensagem.`});}
 catch{await query(env,"UPDATE crm_auth SET token_hash=NULL WHERE token_hash=?",hash).run();return reply({error:'Não foi possível enviar o código. Tente novamente em 90 segundos.'},503);}
 return reply({ok:true});
 }
 if(p==='/crm/api/verify'&&method==='POST'){
 if(!(await env.LEAD_LIMITER.limit({key:'crm-verify:'+(request.headers.get('CF-Connecting-IP')||'unknown')})).success)return reply({error:'Aguarde um minuto.'},429);
 const b=await body(request);const token=str(b.code,64,true);if(!/^[a-f0-9]{64}$/.test(token))fail('Código inválido ou expirado.',401);
 const used=await query(env,"UPDATE crm_auth SET token_hash=NULL WHERE id='admin' AND token_hash=? AND expires_at>? RETURNING id",await digest(token),now).first();
 if(!used)fail('Código inválido ou expirado.',401);
 const session=random();await query(env,'INSERT INTO crm_sessions(token_hash,expires_at) VALUES(?,?)',await digest(session),now+28800000).run();
 await query(env,'DELETE FROM crm_sessions WHERE expires_at<=?',now).run();
 return reply({ok:true},200,{'Set-Cookie':`__Host-crm=${session}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=28800`});
 }
 const cookie=request.headers.get('Cookie')?.match(/(?:^|;\s*)__Host-crm=([a-f0-9]{64})(?:;|$)/)?.[1];
 if(!cookie)return reply({error:'Entre para acessar o CRM.'},401);
 const sessionHash=await digest(cookie);
 if(!await query(env,'SELECT expires_at FROM crm_sessions WHERE token_hash=? AND expires_at>?',sessionHash,now).first())return reply({error:'Sessão encerrada. Entre novamente.'},401);
 if(p==='/crm/api/logout'&&method==='POST'){await query(env,'DELETE FROM crm_sessions WHERE token_hash=?',sessionHash).run();return reply({ok:true},200,{'Set-Cookie':'__Host-crm=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0'});}
 if(p==='/crm/api/data'&&method==='GET'){
 const customers=await query(env,'SELECT * FROM crm_customers ORDER BY name').all();
 const deals=await query(env,`SELECT d.*,o.status AS email_status FROM crm_deals d LEFT JOIN notification_outbox o ON o.lead_id=d.lead_id AND o.kind='team' ORDER BY d.updated_at DESC`).all();
 return reply({customers:customers.results,deals:deals.results,admin:ADMIN});
 }
 if(p==='/crm/api/deals'&&method==='POST'){
 const b=await body(request),id=str(b.id,36,true);if(!/^[a-f0-9-]{36}$/.test(id))fail('Identificador inválido.');
 const email=str(b.email,254,true).toLowerCase();if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))fail('E-mail inválido.');
 const name=str(b.name,100,true),business=str(b.business,100),phone=str(b.phone,30),service=str(b.service,120,true),description=str(b.description,3000),source=str(b.source,50,true),time=new Date().toISOString();
 await env.LEADS_DB.batch([
 query(env,'INSERT INTO crm_customers(id,email,name,business,phone,created_at,updated_at) VALUES(?,?,?,?,?,?,?) ON CONFLICT(email) DO NOTHING',crypto.randomUUID(),email,name,business,phone,time,time),
 query(env,`INSERT INTO crm_deals(id,customer_id,service,description,source,created_at,updated_at) SELECT ?,id,?,?,?,?,? FROM crm_customers WHERE email=? ON CONFLICT(id) DO NOTHING`,id,service,description,source,time,time,email)
 ]);return reply({ok:true,id},201);
 }
 const dm=p.match(/^\/crm\/api\/deals\/([a-zA-Z0-9-]+)$/);
 if(dm&&method==='PATCH'){
 const b=await body(request);if(!Number.isSafeInteger(b.version))fail('Versão inválida.');
 if(!['novo','contato','proposta','negociacao','ganho','perdido'].includes(b.stage)||!['planejado','andamento','entregue'].includes(b.delivery)||![0,1].includes(b.archived))fail('Etapa inválida.');
 if(b.delivery!=='planejado'&&b.stage!=='ganho')fail('A execução e a entrega exigem um negócio fechado.');
 const amount=money(b.amount_cents),received=money(b.received_cents);if(received>amount||(received>0&&b.stage!=='ganho'))fail('Recebimentos exigem negócio fechado e não podem superar o valor contratado.');
 const time=new Date().toISOString();
 const r=await query(env,`UPDATE crm_deals SET service=?,stage=?,amount_cents=?,received_cents=?,delivery=?,due_date=?,next_contact=?,next_action=?,owner=?,archived=?,updated_at=?,version=version+1,closed_at=CASE WHEN ?='ganho' THEN COALESCE(closed_at,?) ELSE NULL END WHERE id=? AND version=?`,str(b.service,120,true),b.stage,amount,received,b.delivery,date(b.due_date),date(b.next_contact),str(b.next_action,500),str(b.owner,100,true),b.archived,time,b.stage,time,dm[1],b.version).run();
 if(!r.meta?.changes)return reply({error:'Este registro mudou. Atualize a tela antes de salvar.'},409);return reply({ok:true});
 }
 const cm=p.match(/^\/crm\/api\/customers\/([a-zA-Z0-9-]+)$/);
 if(cm&&method==='PATCH'){
 const b=await body(request),email=str(b.email,254,true).toLowerCase();if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||!Number.isSafeInteger(b.version))fail('Dados inválidos.');
 if(await query(env,'SELECT id FROM crm_customers WHERE email=? AND id!=?',email,cm[1]).first())fail('Este e-mail já pertence a outro cadastro.');
 const r=await query(env,'UPDATE crm_customers SET name=?,email=?,phone=?,business=?,updated_at=?,version=version+1 WHERE id=? AND version=?',str(b.name,100,true),email,str(b.phone,30),str(b.business,100),new Date().toISOString(),cm[1],b.version).run();
 if(!r.meta?.changes)return reply({error:'Cadastro alterado. Atualize a tela.'},409);return reply({ok:true});
 }
 const am=p.match(/^\/crm\/api\/deals\/([a-zA-Z0-9-]+)\/activity$/);
 if(am){
 if(!await query(env,'SELECT id FROM crm_deals WHERE id=?',am[1]).first())return reply({error:'Registro não encontrado.'},404);
 if(method==='GET'){const r=await query(env,'SELECT * FROM crm_activity WHERE deal_id=? ORDER BY id DESC LIMIT 200',am[1]).all();return reply({activity:r.results});}
 if(method==='POST'){const b=await body(request);await query(env,"INSERT INTO crm_activity(deal_id,created_at,kind,body) VALUES(?,?,'nota',?)",am[1],new Date().toISOString(),str(b.body,4000,true)).run();return reply({ok:true},201);}
 }
 return reply({error:'Não encontrado.'},404);
 }catch(e){if(e.status)return reply({error:e.message},e.status);console.error(JSON.stringify({event:'crm_operation_failed'}));return reply({error:'Não foi possível concluir. Seus dados não foram confirmados. Tente novamente.'},503);}
}
