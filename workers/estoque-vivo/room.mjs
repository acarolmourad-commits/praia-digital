import {migrateProduction,productionWrite,productionPage} from './production.mjs';
import {alertLevel,validSubscription,sendPush} from './push.mjs';
import {migrateOrders,connectionWrite,orderWrite,integrationWrite,ordersPage,connectionsList} from './orders.mjs';
import {DurableObject} from 'cloudflare:workers';
import {AppError,text,integer,uuid,productInput,movementInput,nextStock} from './domain.mjs';
export class InventoryRoom extends DurableObject {
 constructor(ctx,env){super(ctx,env);this.sql=ctx.storage.sql;ctx.blockConcurrencyWhile(async()=>{this.sql.exec(`
CREATE TABLE IF NOT EXISTS workspace(id TEXT PRIMARY KEY,name TEXT NOT NULL,key_hash TEXT NOT NULL,created_at TEXT NOT NULL,revision INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY,actor TEXT NOT NULL,expires INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY,sku TEXT NOT NULL UNIQUE COLLATE NOCASE,name TEXT NOT NULL,variant TEXT NOT NULL,category TEXT NOT NULL,minimum INTEGER NOT NULL,physical INTEGER NOT NULL CHECK(physical>=0),reserved INTEGER NOT NULL DEFAULT 0 CHECK(reserved>=0 AND reserved<=physical),version INTEGER NOT NULL DEFAULT 1,archived INTEGER NOT NULL DEFAULT 0,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS movements(id TEXT PRIMARY KEY,product_id TEXT NOT NULL,type TEXT NOT NULL,quantity INTEGER NOT NULL,delta_physical INTEGER NOT NULL,delta_reserved INTEGER NOT NULL,after_physical INTEGER NOT NULL,after_reserved INTEGER NOT NULL,channel TEXT NOT NULL,reference TEXT NOT NULL,note TEXT NOT NULL,actor TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS movement_time ON movements(created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS movement_reference ON movements(product_id,type,channel,reference) WHERE reference<>'';
CREATE TABLE IF NOT EXISTS operations(id TEXT PRIMARY KEY,payload_hash TEXT NOT NULL,response TEXT NOT NULL);
`);this.migrate();});}
 migrate(){
  const add=(table,name,sql)=>{if(!this.sql.exec(`PRAGMA table_info(${table})`).toArray().some(c=>c.name===name))this.sql.exec(`ALTER TABLE ${table} ADD COLUMN ${sql}`);};
  this.ctx.storage.transactionSync(()=>{
   migrateOrders(this);
   migrateProduction(this);
   add('sessions','member_id',"member_id TEXT NOT NULL DEFAULT 'owner'");
   add('operations','member_id',"member_id TEXT NOT NULL DEFAULT 'owner'");
   add('movements','member_id',"member_id TEXT NOT NULL DEFAULT 'owner'");
   add('movements','seller_id',"seller_id TEXT NOT NULL DEFAULT 'owner'");
   add('products','alert_at','alert_at INTEGER NOT NULL DEFAULT 150');
   add('products','alert_level','alert_level INTEGER NOT NULL DEFAULT 0');
   this.sql.exec(`CREATE TABLE IF NOT EXISTS members(id TEXT PRIMARY KEY,name TEXT NOT NULL,key_hash TEXT NOT NULL UNIQUE,active INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS allocations(product_id TEXT NOT NULL,member_id TEXT NOT NULL,reserved INTEGER NOT NULL CHECK(reserved>=0),PRIMARY KEY(product_id,member_id));
CREATE TABLE IF NOT EXISTS alerts(id TEXT PRIMARY KEY,product_id TEXT NOT NULL,available INTEGER NOT NULL,threshold INTEGER NOT NULL,level INTEGER NOT NULL,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS subscriptions(endpoint_hash TEXT PRIMARY KEY,member_id TEXT NOT NULL,session_hash TEXT NOT NULL,subscription TEXT NOT NULL,created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS push_jobs(id TEXT PRIMARY KEY,endpoint_hash TEXT NOT NULL,alert_id TEXT,payload TEXT NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,next_at INTEGER NOT NULL,created_at INTEGER NOT NULL,status TEXT NOT NULL DEFAULT 'pending');
CREATE INDEX IF NOT EXISTS push_due ON push_jobs(status,next_at);
CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY);`);
   if(!this.row('SELECT version FROM schema_version WHERE version=2')){
    this.sql.exec("INSERT OR IGNORE INTO allocations SELECT id,'owner',reserved FROM products WHERE reserved>0");
    this.sql.exec('INSERT INTO schema_version VALUES(2)');
    for(const p of this.sql.exec('SELECT id FROM products WHERE archived=0').toArray())this.evaluateAlert(p.id,new Date().toISOString());
   }
  });
 }
 row(q,...args){return this.sql.exec(q,...args).toArray()[0];}
 allocate(session,id,m,requested){
  if(!['reserve','fulfill','release'].includes(m.type))return;
  const member=session.role==='admin'?(requested||'owner'):session.member_id;
  if(session.role!=='admin'&&requested&&requested!==member)throw new AppError('Você só pode movimentar suas próprias reservas.',403);
  if(member!=='owner'){uuid(member);const profile=this.row('SELECT active FROM members WHERE id=?',member);if(!profile||(m.type==='reserve'&&!profile.active))throw new AppError('Influenciador não disponível para reserva.',409);}
  const current=this.row('SELECT reserved FROM allocations WHERE product_id=? AND member_id=?',id,member)?.reserved||0;
  const next=current+(m.type==='reserve'?m.quantity:-m.quantity);
  if(next<0)throw new AppError('Esta quantidade excede a reserva deste responsável.',409);
  this.sql.exec('INSERT INTO allocations VALUES(?,?,?) ON CONFLICT(product_id,member_id) DO UPDATE SET reserved=excluded.reserved',id,member,next);return member;
 }
 evaluateAlert(id,now){
  const p=this.row('SELECT * FROM products WHERE id=?',id);if(!p||p.archived)return;
  const available=p.physical-p.reserved,level=alertLevel(available,p.alert_at);
  if(level===p.alert_level)return;
  this.sql.exec('UPDATE products SET alert_level=? WHERE id=?',level,id);
  if(!level)return;
  const alertId=crypto.randomUUID();this.sql.exec('INSERT INTO alerts VALUES(?,?,?,?,?,?)',alertId,id,available,p.alert_at,level,now);
  const payload=JSON.stringify({title:level===2?'Produto sem estoque disponível':'Alerta de estoque: últimas unidades',body:`${p.name} (${p.sku}): ${available} disponíveis. Limite: ${p.alert_at}. Confira o painel antes de vender.`,tag:'stock-'+id,url:'/',at:now});
  for(const s of this.sql.exec('SELECT endpoint_hash FROM subscriptions').toArray())this.queuePush(s.endpoint_hash,payload,alertId);
 }
 queuePush(endpoint,payload,alertId=null){const now=Date.now();this.sql.exec('INSERT INTO push_jobs(id,endpoint_hash,alert_id,payload,next_at,created_at) VALUES(?,?,?,?,?,?)',crypto.randomUUID(),endpoint,alertId,payload,now,now);}
 removeSubscriptions(column,value){if(!['session_hash','member_id','endpoint_hash'].includes(column))throw new Error('Invalid subscription selector');this.sql.exec(`DELETE FROM push_jobs WHERE endpoint_hash IN (SELECT endpoint_hash FROM subscriptions WHERE ${column}=?)`,value);this.sql.exec(`DELETE FROM subscriptions WHERE ${column}=?`,value);}
 configurePush(hash,action,b,endpointHash){return this.safe(()=>{
  const session=this.session(hash);
  if(action==='unsubscribe'){this.sql.exec('DELETE FROM push_jobs WHERE endpoint_hash IN (SELECT endpoint_hash FROM subscriptions WHERE endpoint_hash=? AND member_id=?)',endpointHash,session.member_id);this.sql.exec('DELETE FROM subscriptions WHERE endpoint_hash=? AND member_id=?',endpointHash,session.member_id);return {ok:true};}
  if(!this.env.VAPID_KEYS)throw new AppError('Notificações ainda não configuradas no servidor.',503);
  if(action==='subscribe'){
   const sub=validSubscription(b.subscription);
   if(!this.row('SELECT endpoint_hash FROM subscriptions WHERE endpoint_hash=?',endpointHash)&&this.row('SELECT COUNT(*) AS n FROM subscriptions').n>=30)throw new AppError('Limite de 30 dispositivos com alertas por marca.',409);
   this.sql.exec('INSERT INTO subscriptions VALUES(?,?,?,?,?) ON CONFLICT(endpoint_hash) DO UPDATE SET member_id=excluded.member_id,session_hash=excluded.session_hash,subscription=excluded.subscription,created_at=excluded.created_at',endpointHash,session.member_id,hash,JSON.stringify(sub),Date.now());
   return {ok:true};
  }
  if(action==='test'){
   const sub=this.row('SELECT endpoint_hash FROM subscriptions WHERE session_hash=?',hash);if(!sub)throw new AppError('Ative as notificações neste dispositivo primeiro.');
   if(this.row('SELECT id FROM push_jobs WHERE endpoint_hash=? AND created_at>?',sub.endpoint_hash,Date.now()-60000))throw new AppError('Aguarde um minuto antes de testar novamente.',429);
   this.queuePush(sub.endpoint_hash,JSON.stringify({title:'Estoque Vivo: notificações ativas',body:'Este é um teste. Os próximos avisos serão gerados quando um produto entrar na faixa de alerta.',tag:'stock-test',url:'/'}));this.ctx.waitUntil(this.schedule());return {ok:true};
  }
  throw new AppError('Ação de notificação inválida.');
 });}
 async schedule(){const job=this.row("SELECT MIN(next_at) AS due FROM push_jobs WHERE status='pending'");if(job?.due)await this.ctx.storage.setAlarm(Math.max(Date.now()+100,job.due));}
 async alarm(){
  const jobs=this.sql.exec("SELECT j.*,s.subscription FROM push_jobs j JOIN subscriptions s ON s.endpoint_hash=j.endpoint_hash WHERE j.status='pending' AND j.next_at<=? ORDER BY j.next_at LIMIT 10",Date.now()).toArray();
  let keys;try{keys=JSON.parse(this.env.VAPID_KEYS||'null');}catch{}
  for(const job of jobs){
   if(!keys||Date.now()-job.created_at>900000){this.sql.exec("UPDATE push_jobs SET status='expired' WHERE id=?",job.id);continue;}
   if(job.alert_id){const a=this.row('SELECT a.level,p.alert_level,p.archived,(SELECT id FROM alerts WHERE product_id=a.product_id ORDER BY rowid DESC LIMIT 1) AS latest FROM alerts a JOIN products p ON p.id=a.product_id WHERE a.id=?',job.alert_id);if(!a||a.archived||a.level!==a.alert_level||a.latest!==job.alert_id){this.sql.exec("UPDATE push_jobs SET status='superseded' WHERE id=?",job.id);continue;}}
   this.sql.exec('UPDATE push_jobs SET next_at=?,attempts=attempts+1 WHERE id=?',Date.now()+60000,job.id);
   let status=0;try{status=await sendPush(JSON.parse(job.subscription),JSON.parse(job.payload),keys);}catch{console.warn(JSON.stringify({event:'push_send_failed'}));}
   if(status===404||status===410){this.removeSubscriptions('endpoint_hash',job.endpoint_hash);continue;}
   if(status>=200&&status<300)this.sql.exec("UPDATE push_jobs SET status='accepted' WHERE id=?",job.id);
   else if(job.attempts>=2||(status>=400&&status<500&&status!==429))this.sql.exec("UPDATE push_jobs SET status='failed' WHERE id=?",job.id);
   else this.sql.exec('UPDATE push_jobs SET next_at=? WHERE id=?',Date.now()+60000*(job.attempts+1),job.id);
  }
  this.sql.exec("DELETE FROM push_jobs WHERE status<>'pending' AND created_at<?",Date.now()-604800000);
  await this.schedule();
 }
 session(hash){const s=this.row('SELECT actor,expires,member_id FROM sessions WHERE hash=?',hash);if(!s||s.expires<=Date.now())throw new AppError('Entre novamente com a chave do espaço.',401);if(s.member_id!=='owner'){const m=this.row('SELECT name FROM members WHERE id=? AND active=1',s.member_id);if(!m)throw new AppError('Acesso encerrado pela marca.',401);s.actor=m.name;}return {...s,role:s.member_id==='owner'?'admin':'influencer'};}
 admin(s){if(s.role!=='admin')throw new AppError('Esta ação é exclusiva da gestão da marca.',403);}
 safe(fn){try{return {status:200,...fn()};}catch(e){if(e instanceof AppError)return {status:e.status,error:e.message};console.error(JSON.stringify({event:'inventory_operation_failed'}));return {status:503,error:'Não foi possível confirmar a operação. Tente novamente com os mesmos dados.'};}}
 initialize(id,name,keyHash,sessionHash,actor){return this.safe(()=>{if(this.row('SELECT id FROM workspace LIMIT 1'))throw new AppError('Espaço já existe.',409);this.ctx.storage.transactionSync(()=>{this.sql.exec('INSERT INTO workspace(id,name,key_hash,created_at) VALUES(?,?,?,?)',uuid(id),text(name,100),keyHash,new Date().toISOString());this.sql.exec('INSERT INTO sessions(hash,actor,expires,member_id) VALUES(?,?,?,?)',sessionHash,text(actor,60),Date.now()+43200000,'owner');});return {ok:true};});}
 login(keyHash,sessionHash,actor){return this.safe(()=>{const owner=this.row('SELECT id FROM workspace WHERE key_hash=?',keyHash),m=owner?null:this.row('SELECT id,name FROM members WHERE key_hash=? AND active=1',keyHash);if(!owner&&!m)throw new AppError('Chave inválida. Confira e tente novamente.',401);this.sql.exec('DELETE FROM sessions WHERE expires<=?',Date.now());if(this.row('SELECT COUNT(*) AS n FROM sessions').n>=50)throw new AppError('Limite de sessões. Encerre uma sessão ou aguarde sua expiração.',429);this.sql.exec('INSERT INTO sessions(hash,actor,expires,member_id) VALUES(?,?,?,?)',sessionHash,m?m.name:text(actor,60),Date.now()+43200000,m?.id||'owner');return {ok:true};});}
 snapshot(hash){return this.safe(()=>{
  const s=this.session(hash),w=this.row('SELECT id,name,revision FROM workspace');
  const filter=s.role==='admin'?'':' WHERE (m.member_id=? OR m.seller_id=?)',args=s.role==='admin'?[]:[s.member_id,s.member_id];
  return {ok:true,workspace:w,actor:s.actor,role:s.role,member_id:s.member_id,expires:s.expires,
   products:this.sql.exec("SELECT p.*,(SELECT COALESCE(SUM(l.quantity),0) FROM order_lines l JOIN orders o ON o.id=l.order_id WHERE l.product_id=p.id AND o.status='reserved') AS order_reserved FROM products p ORDER BY archived,name COLLATE NOCASE,sku").toArray(),
   movements:this.sql.exec("SELECT m.*,p.sku,p.name,p.variant,COALESCE(v.name,'Gestão da marca') AS seller_name FROM movements m JOIN products p ON p.id=m.product_id LEFT JOIN members v ON v.id=m.seller_id"+filter+' ORDER BY m.rowid DESC LIMIT 100',...args).toArray(),
   members:s.role==='admin'?this.sql.exec('SELECT id,name,active FROM members ORDER BY name').toArray():[],
   allocations:this.sql.exec("SELECT a.*,COALESCE(m.name,'Gestão da marca') AS name FROM allocations a LEFT JOIN members m ON m.id=a.member_id"+(s.role==='admin'?'':' WHERE a.member_id=?'),...(s.role==='admin'?[]:[s.member_id])).toArray(),
   alerts:this.sql.exec('SELECT a.*,p.name,p.sku FROM alerts a JOIN products p ON p.id=a.product_id ORDER BY a.rowid DESC LIMIT 50').toArray(),
   push:{enabled:!!this.env.VAPID_KEYS,subscribed:!!this.row('SELECT endpoint_hash FROM subscriptions WHERE session_hash=?',hash)},server_time:new Date().toISOString()};
 });}
 historyPage(hash,before){return this.safe(()=>{const s=this.session(hash),filter=s.role==='admin'?'':' AND (m.member_id=? OR m.seller_id=?)',args=s.role==='admin'?[]:[s.member_id,s.member_id];const rows=this.sql.exec("SELECT m.rowid AS cursor,m.*,p.sku,p.name,p.variant,COALESCE(v.name,'Gestão da marca') AS seller_name FROM movements m JOIN products p ON p.id=m.product_id LEFT JOIN members v ON v.id=m.seller_id WHERE m.rowid<?"+filter+' ORDER BY m.rowid DESC LIMIT 500',integer(before,1,1000000000),...args).toArray();return {ok:true,movements:rows,next_cursor:rows.length===500?rows.at(-1).cursor:null};});}
 productionWrite(hash,b,payloadHash){return productionWrite(this,hash,b,payloadHash);}
 productionPage(hash,query){return productionPage(this,hash,query);}
 orderWrite(hash,b,payloadHash){return orderWrite(this,hash,b,payloadHash);}
 integrationWrite(id,tokenHash,b,payloadHash,contentHash){return integrationWrite(this,id,tokenHash,b,payloadHash,contentHash);}
 connectionWrite(hash,b,payloadHash){return connectionWrite(this,hash,b,payloadHash);}
 ordersPage(hash,query){return ordersPage(this,hash,query);}
 connectionsList(hash){return connectionsList(this,hash);}
 logout(hash){return this.safe(()=>{this.removeSubscriptions('session_hash',hash);this.sql.exec('DELETE FROM sessions WHERE hash=?',hash);for(const ws of this.ctx.getWebSockets()){if(ws.deserializeAttachment()?.hash===hash)ws.close(1008,'Sessão encerrada');}return {ok:true};});}
 mutate(hash,action,b,payloadHash){const result=this.safe(()=>{const session=this.session(hash);uuid(b.operation_id);const old=this.row('SELECT * FROM operations WHERE id=?',b.operation_id);if(old){if(old.member_id!==session.member_id)throw new AppError('Tentativa pertencente a outro acesso.',403);if(old.payload_hash!==payloadHash)throw new AppError('Essa tentativa mudou. Reabra o formulário e confira os dados.',409);return {...JSON.parse(old.response),replayed:true};}
  const result=this.ctx.storage.transactionSync(()=>{
   if(this.row('SELECT COUNT(*) AS n FROM operations').n>=100000)throw new AppError('Limite do piloto atingido. Exporte o histórico e contate a Praia Digital.',409);
   const now=new Date().toISOString();let id;
   if(action==='product'){
    this.admin(session);
    const p=productInput(b);id=uuid(b.id||b.operation_id);const existing=this.row('SELECT * FROM products WHERE id=?',id);
    if(existing&&existing.sku!==p.sku&&this.row('SELECT id FROM production WHERE product_id=? LIMIT 1',id))throw new AppError('SKU vinculado à produção. Preserve o código.',409);
    if(existing){if(existing.sku!==p.sku&&this.row('SELECT order_id FROM order_lines WHERE product_id=? LIMIT 1',id))throw new AppError('Este SKU está vinculado a pedidos. Mantenha o código e edite os demais dados.',409);if(existing.archived)throw new AppError('Produto arquivado.',409);if(existing.version!==integer(b.expected_version,1,1000000000))throw new AppError('O produto mudou em outra tela. Reabra a edição.',409);}
    else if(this.row('SELECT COUNT(*) AS n FROM products').n>=2000)throw new AppError('O piloto aceita até 2.000 SKUs por espaço.',409);
    if(this.row('SELECT id FROM products WHERE sku=? AND id<>?',p.sku,id))throw new AppError('Esse SKU já está cadastrado, inclusive entre arquivados.',409);
    if(existing)this.sql.exec('UPDATE products SET sku=?,name=?,variant=?,category=?,minimum=?,alert_at=?,version=version+1,updated_at=? WHERE id=?',p.sku,p.name,p.variant,p.category,p.minimum,p.alert_at,now,id);
    else {this.sql.exec('INSERT INTO products(id,sku,name,variant,category,minimum,alert_at,physical,reserved,updated_at) VALUES(?,?,?,?,?,?,?,?,0,?)',id,p.sku,p.name,p.variant,p.category,p.minimum,p.alert_at,p.quantity,now);this.sql.exec('INSERT INTO movements(id,product_id,type,quantity,delta_physical,delta_reserved,after_physical,after_reserved,channel,reference,note,actor,created_at,member_id,seller_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',crypto.randomUUID(),id,'initial',p.quantity,p.quantity,0,p.quantity,0,'Manual','','Saldo inicial',session.actor,now,session.member_id,session.member_id);}
   }else if(action==='movement'){
    const m=movementInput(b);if(session.role!=='admin'&&!['sale','reserve','fulfill','release'].includes(m.type))throw new AppError('Influenciadores podem vender, reservar e concluir ou liberar suas reservas.',403);id=m.product_id;const p=this.row('SELECT * FROM products WHERE id=? AND archived=0',id);if(!p)throw new AppError('Produto não encontrado.',404);
    if(m.reference&&this.row('SELECT id FROM movements WHERE product_id=? AND type=? AND channel=? AND reference=?',id,m.type,m.channel,m.reference))throw new AppError('Já existe essa referência para o produto, tipo e canal. Confira o histórico antes de repetir.',409);
    const n=nextStock(p,m);const seller=this.allocate(session,id,m,b.reservation_owner)||session.member_id;
    this.sql.exec('UPDATE products SET physical=?,reserved=?,version=version+1,updated_at=? WHERE id=?',n.physical,n.reserved,now,id);
    this.sql.exec('INSERT INTO movements(id,product_id,type,quantity,delta_physical,delta_reserved,after_physical,after_reserved,channel,reference,note,actor,created_at,member_id,seller_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',b.operation_id,id,m.type,m.quantity,n.physical-p.physical,n.reserved-p.reserved,n.physical,n.reserved,m.channel,m.reference,m.note,session.actor,now,session.member_id,seller);
   }else if(action==='member'){
    this.admin(session);id=uuid(b.member_id);if(b.revoke){this.sql.exec('UPDATE members SET active=0 WHERE id=?',id);this.sql.exec('UPDATE connections SET active=0 WHERE seller_id=?',id);this.sql.exec('DELETE FROM sessions WHERE member_id=?',id);this.removeSubscriptions('member_id',id);}else{if(this.row('SELECT COUNT(*) AS n FROM members WHERE active=1').n>=100)throw new AppError('Limite de 100 influenciadores por marca.');if(this.row('SELECT id FROM members WHERE id=?',id))throw new AppError('Este acesso já existe.',409);this.sql.exec('INSERT INTO members(id,name,key_hash,active) VALUES(?,?,?,1)',id,text(b.member_name,60),b.member_hash);}
   }else if(action==='archive'){
    this.admin(session);
    id=uuid(b.id);const p=this.row('SELECT * FROM products WHERE id=?',id);if(!p)throw new AppError('Produto não encontrado.',404);if(this.row("SELECT id FROM production WHERE product_id=? AND status IN ('awaiting_payment','in_production') LIMIT 1",id))throw new AppError('Há encomendas pendentes para este produto.',409);if(p.physical||p.reserved)throw new AppError('Zere o saldo por uma movimentação justificada antes de arquivar.',409);this.sql.exec('UPDATE products SET archived=1,version=version+1,updated_at=? WHERE id=?',now,id);
   }else throw new AppError('Ação inválida.',404);
   this.sql.exec('UPDATE workspace SET revision=revision+1');if(action==='product'||action==='movement')this.evaluateAlert(id,now);const r={ok:true,id,revision:this.row('SELECT revision FROM workspace').revision};this.sql.exec('INSERT INTO operations(id,payload_hash,response,member_id) VALUES(?,?,?,?)',b.operation_id,payloadHash,JSON.stringify(r),session.member_id);return r;
  });return result;
 });if(result.ok){if(!result.replayed)this.broadcast(result.revision);this.ctx.waitUntil(this.schedule());}return result;}
 rotate(hash,newHash,newSessionHash){const r=this.safe(()=>{const s=this.session(hash);this.admin(s);this.ctx.storage.transactionSync(()=>{this.sql.exec('UPDATE workspace SET key_hash=?',newHash);this.sql.exec('UPDATE connections SET active=0');this.sql.exec('DELETE FROM sessions');this.sql.exec('DELETE FROM subscriptions');this.sql.exec('DELETE FROM push_jobs');this.sql.exec('INSERT INTO sessions(hash,actor,expires,member_id) VALUES(?,?,?,?)',newSessionHash,s.actor,Date.now()+43200000,'owner');});return {ok:true};});if(r.ok)for(const ws of this.ctx.getWebSockets())ws.close(1008,'Chave alterada');return r;}
 broadcast(revision){for(const ws of this.ctx.getWebSockets()){try{this.session(ws.deserializeAttachment()?.hash);ws.send(JSON.stringify({type:'changed',revision}));}catch{ws.close(1008,'Sessão encerrada');}}}
 async fetch(request){const hash=request.headers.get('X-Session-Hash');try{this.session(hash);}catch{return new Response('Entre novamente.',{status:401});}if(request.headers.get('Upgrade')?.toLowerCase()!=='websocket')return new Response('WebSocket esperado.',{status:426});if(this.ctx.getWebSockets().length>=30)return new Response('Limite de telas conectadas.',{status:429});const pair=new WebSocketPair();this.ctx.acceptWebSocket(pair[1]);pair[1].serializeAttachment({hash,lastMessage:0});pair[1].send(JSON.stringify({type:'ready',revision:this.row('SELECT revision FROM workspace').revision}));return new Response(null,{status:101,webSocket:pair[0]});}
 webSocketMessage(ws,message){try{const a=ws.deserializeAttachment();this.session(a?.hash);if(message!=='ping'||Date.now()-a.lastMessage<15000){ws.close(1008,'Mensagem não permitida');return;}a.lastMessage=Date.now();ws.serializeAttachment(a);ws.send('pong');}catch{ws.close(1008,'Sessão encerrada');}}
 webSocketClose(ws,code,reason){ws.close(code,reason);}
 webSocketError(ws){ws.close(1011,'Conexão interrompida');}
}
