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
`);});}
 row(q,...args){return this.sql.exec(q,...args).toArray()[0];}
 session(hash){const s=this.row('SELECT actor,expires FROM sessions WHERE hash=?',hash);if(!s||s.expires<=Date.now())throw new AppError('Entre novamente com a chave do espaço.',401);return s;}
 safe(fn){try{return {status:200,...fn()};}catch(e){if(e instanceof AppError)return {status:e.status,error:e.message};console.error(JSON.stringify({event:'inventory_operation_failed'}));return {status:503,error:'Não foi possível confirmar a operação. Tente novamente com os mesmos dados.'};}}
 initialize(id,name,keyHash,sessionHash,actor){return this.safe(()=>{if(this.row('SELECT id FROM workspace LIMIT 1'))throw new AppError('Espaço já existe.',409);this.ctx.storage.transactionSync(()=>{this.sql.exec('INSERT INTO workspace(id,name,key_hash,created_at) VALUES(?,?,?,?)',uuid(id),text(name,100),keyHash,new Date().toISOString());this.sql.exec('INSERT INTO sessions VALUES(?,?,?)',sessionHash,text(actor,60),Date.now()+43200000);});return {ok:true};});}
 login(keyHash,sessionHash,actor){return this.safe(()=>{if(!this.row('SELECT id FROM workspace WHERE key_hash=?',keyHash))throw new AppError('Chave inválida. Confira e tente novamente.',401);this.sql.exec('DELETE FROM sessions WHERE expires<=?',Date.now());if(this.row('SELECT COUNT(*) AS n FROM sessions').n>=50)throw new AppError('Limite de sessões. Encerre uma sessão ou aguarde sua expiração.',429);this.sql.exec('INSERT INTO sessions VALUES(?,?,?)',sessionHash,text(actor,60),Date.now()+43200000);return {ok:true};});}
 snapshot(hash){return this.safe(()=>{const s=this.session(hash),w=this.row('SELECT id,name,revision FROM workspace');return {ok:true,workspace:w,actor:s.actor,expires:s.expires,products:this.sql.exec('SELECT * FROM products ORDER BY archived,name COLLATE NOCASE,sku').toArray(),movements:this.sql.exec('SELECT m.*,p.sku,p.name,p.variant FROM movements m JOIN products p ON p.id=m.product_id ORDER BY m.rowid DESC LIMIT 100').toArray(),server_time:new Date().toISOString()};});}
 historyPage(hash,before){return this.safe(()=>{this.session(hash);const rows=this.sql.exec('SELECT m.rowid AS cursor,m.*,p.sku,p.name,p.variant FROM movements m JOIN products p ON p.id=m.product_id WHERE m.rowid<? ORDER BY m.rowid DESC LIMIT 500',integer(before,1,1000000000)).toArray();return {ok:true,movements:rows,next_cursor:rows.length===500?rows.at(-1).cursor:null};});}
 logout(hash){return this.safe(()=>{this.sql.exec('DELETE FROM sessions WHERE hash=?',hash);for(const ws of this.ctx.getWebSockets()){if(ws.deserializeAttachment()?.hash===hash)ws.close(1008,'Sessão encerrada');}return {ok:true};});}
 mutate(hash,action,b,payloadHash){const result=this.safe(()=>{const session=this.session(hash);uuid(b.operation_id);const old=this.row('SELECT * FROM operations WHERE id=?',b.operation_id);if(old){if(old.payload_hash!==payloadHash)throw new AppError('Essa tentativa mudou. Reabra o formulário e confira os dados.',409);return {...JSON.parse(old.response),replayed:true};}
  const result=this.ctx.storage.transactionSync(()=>{
   if(this.row('SELECT COUNT(*) AS n FROM operations').n>=100000)throw new AppError('Limite do piloto atingido. Exporte o histórico e contate a Praia Digital.',409);
   const now=new Date().toISOString();let id;
   if(action==='product'){
    const p=productInput(b);id=uuid(b.id||b.operation_id);const existing=this.row('SELECT * FROM products WHERE id=?',id);
    if(existing){if(existing.archived)throw new AppError('Produto arquivado.',409);if(existing.version!==integer(b.expected_version,1,1000000000))throw new AppError('O produto mudou em outra tela. Reabra a edição.',409);}
    else if(this.row('SELECT COUNT(*) AS n FROM products').n>=2000)throw new AppError('O piloto aceita até 2.000 SKUs por espaço.',409);
    if(this.row('SELECT id FROM products WHERE sku=? AND id<>?',p.sku,id))throw new AppError('Esse SKU já está cadastrado, inclusive entre arquivados.',409);
    if(existing)this.sql.exec('UPDATE products SET sku=?,name=?,variant=?,category=?,minimum=?,version=version+1,updated_at=? WHERE id=?',p.sku,p.name,p.variant,p.category,p.minimum,now,id);
    else {this.sql.exec('INSERT INTO products(id,sku,name,variant,category,minimum,physical,reserved,updated_at) VALUES(?,?,?,?,?,?,?,0,?)',id,p.sku,p.name,p.variant,p.category,p.minimum,p.quantity,now);this.sql.exec('INSERT INTO movements VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',crypto.randomUUID(),id,'initial',p.quantity,p.quantity,0,p.quantity,0,'Manual','','Saldo inicial',session.actor,now);}
   }else if(action==='movement'){
    const m=movementInput(b);id=m.product_id;const p=this.row('SELECT * FROM products WHERE id=? AND archived=0',id);if(!p)throw new AppError('Produto não encontrado.',404);
    if(m.reference&&this.row('SELECT id FROM movements WHERE product_id=? AND type=? AND channel=? AND reference=?',id,m.type,m.channel,m.reference))throw new AppError('Já existe essa referência para o produto, tipo e canal. Confira o histórico antes de repetir.',409);
    const n=nextStock(p,m);
    this.sql.exec('UPDATE products SET physical=?,reserved=?,version=version+1,updated_at=? WHERE id=?',n.physical,n.reserved,now,id);
    this.sql.exec('INSERT INTO movements VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',b.operation_id,id,m.type,m.quantity,n.physical-p.physical,n.reserved-p.reserved,n.physical,n.reserved,m.channel,m.reference,m.note,session.actor,now);
   }else if(action==='archive'){
    id=uuid(b.id);const p=this.row('SELECT * FROM products WHERE id=?',id);if(!p)throw new AppError('Produto não encontrado.',404);if(p.physical||p.reserved)throw new AppError('Zere o saldo por uma movimentação justificada antes de arquivar.',409);this.sql.exec('UPDATE products SET archived=1,version=version+1,updated_at=? WHERE id=?',now,id);
   }else throw new AppError('Ação inválida.',404);
   this.sql.exec('UPDATE workspace SET revision=revision+1');const r={ok:true,id,revision:this.row('SELECT revision FROM workspace').revision};this.sql.exec('INSERT INTO operations VALUES(?,?,?)',b.operation_id,payloadHash,JSON.stringify(r));return r;
  });return result;
 });if(result.ok&&!result.replayed)this.broadcast(result.revision);return result;}
 rotate(hash,newHash,newSessionHash){const r=this.safe(()=>{const s=this.session(hash);this.ctx.storage.transactionSync(()=>{this.sql.exec('UPDATE workspace SET key_hash=?',newHash);this.sql.exec('DELETE FROM sessions');this.sql.exec('INSERT INTO sessions VALUES(?,?,?)',newSessionHash,s.actor,Date.now()+43200000);});return {ok:true};});if(r.ok)for(const ws of this.ctx.getWebSockets())ws.close(1008,'Chave alterada');return r;}
 broadcast(revision){for(const ws of this.ctx.getWebSockets()){try{this.session(ws.deserializeAttachment()?.hash);ws.send(JSON.stringify({type:'changed',revision}));}catch{ws.close(1008,'Sessão encerrada');}}}
 async fetch(request){const hash=request.headers.get('X-Session-Hash');try{this.session(hash);}catch{return new Response('Entre novamente.',{status:401});}if(request.headers.get('Upgrade')?.toLowerCase()!=='websocket')return new Response('WebSocket esperado.',{status:426});if(this.ctx.getWebSockets().length>=30)return new Response('Limite de telas conectadas.',{status:429});const pair=new WebSocketPair();this.ctx.acceptWebSocket(pair[1]);pair[1].serializeAttachment({hash,lastMessage:0});pair[1].send(JSON.stringify({type:'ready',revision:this.row('SELECT revision FROM workspace').revision}));return new Response(null,{status:101,webSocket:pair[0]});}
 webSocketMessage(ws,message){try{const a=ws.deserializeAttachment();this.session(a?.hash);if(message!=='ping'||Date.now()-a.lastMessage<15000){ws.close(1008,'Mensagem não permitida');return;}a.lastMessage=Date.now();ws.serializeAttachment(a);ws.send('pong');}catch{ws.close(1008,'Sessão encerrada');}}
 webSocketClose(ws,code,reason){ws.close(code,reason);}
 webSocketError(ws){ws.close(1011,'Conexão interrompida');}
}
