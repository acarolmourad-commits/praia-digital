import {AppError,CHANNELS,text,integer,uuid,nextStock} from './domain.mjs';

export function migrateOrders(room){
 room.sql.exec(`CREATE TABLE IF NOT EXISTS connections(id TEXT PRIMARY KEY,name TEXT NOT NULL,channel TEXT NOT NULL,seller_id TEXT NOT NULL,key_hash TEXT NOT NULL,active INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL,last_received TEXT);
CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY,source_id TEXT NOT NULL,channel TEXT NOT NULL,reference TEXT NOT NULL,seller_id TEXT NOT NULL,status TEXT NOT NULL,version INTEGER NOT NULL DEFAULT 1,external_version INTEGER NOT NULL DEFAULT 0,external_hash TEXT NOT NULL DEFAULT '',created_at TEXT NOT NULL,updated_at TEXT NOT NULL,UNIQUE(channel,reference));
CREATE TABLE IF NOT EXISTS order_lines(order_id TEXT NOT NULL,product_id TEXT NOT NULL,sku TEXT NOT NULL,quantity INTEGER NOT NULL CHECK(quantity>0),PRIMARY KEY(order_id,product_id));
CREATE INDEX IF NOT EXISTS order_status ON orders(status,seller_id);
CREATE TABLE IF NOT EXISTS order_events(id TEXT PRIMARY KEY,order_id TEXT NOT NULL,status TEXT NOT NULL,actor TEXT NOT NULL,note TEXT NOT NULL,created_at TEXT NOT NULL);`);
}
function channel(v){if(!CHANNELS.includes(v))throw new AppError('Escolha o canal.');return v;}
function seller(room,id,active=true){if(id==='owner')return id;uuid(id);const m=room.row('SELECT active FROM members WHERE id=?',id);if(!m||(active&&!m.active))throw new AppError('Influenciador não disponível.',409);return id;}
function replay(room,id,hash,owner){uuid(id);const old=room.row('SELECT * FROM operations WHERE id=?',id);if(!old)return;if(old.member_id!==owner)throw new AppError('Tentativa pertencente a outro acesso.',403);if(old.payload_hash!==hash)throw new AppError('Tentativa já utilizada com outros dados.',409);return {...JSON.parse(old.response),replayed:true};}
function capacity(room){if(room.row('SELECT COUNT(*) AS n FROM operations').n>=100000)throw new AppError('Limite do piloto atingido. Exporte o histórico e contate a Praia Digital.',409);}
function finish(room,op,hash,owner,result){room.sql.exec('UPDATE workspace SET revision=revision+1');const r={ok:true,...result,revision:room.row('SELECT revision FROM workspace').revision};room.sql.exec('INSERT INTO operations(id,payload_hash,response,member_id) VALUES(?,?,?,?)',op,hash,JSON.stringify(r),owner);return r;}
function publish(room,r){if(r.ok&&!r.replayed){room.broadcast(r.revision);room.ctx.waitUntil(room.schedule());}return r;}

export function connectionWrite(room,hash,b,payloadHash){return publish(room,room.safe(()=>{
 const session=room.session(hash);room.admin(session);const old=replay(room,b.operation_id,payloadHash,session.member_id);if(old)return old;
 return room.ctx.storage.transactionSync(()=>{capacity(room);const id=uuid(b.id);
  if(b.revoke){if(!room.row('SELECT id FROM connections WHERE id=?',id))throw new AppError('Conexão não encontrada.',404);room.sql.exec('UPDATE connections SET active=0 WHERE id=?',id);}
  else{
   if(room.row('SELECT COUNT(*) AS n FROM connections WHERE active=1').n>=20)throw new AppError('Limite de 20 conexões ativas.',409);
   if(room.row('SELECT id FROM connections WHERE id=?',id))throw new AppError('Conexão já cadastrada.',409);
   if(!/^[a-f0-9]{64}$/.test(b.key_hash||''))throw new AppError('Chave de integração inválida.');
   room.sql.exec('INSERT INTO connections(id,name,channel,seller_id,key_hash,created_at) VALUES(?,?,?,?,?,?)',id,text(b.name,60),channel(b.channel),seller(room,b.seller_id||'owner'),b.key_hash,new Date().toISOString());
  }
  return finish(room,b.operation_id,payloadHash,session.member_id,{id});
 });
}));}

function linesInput(room,items){
 if(!Array.isArray(items)||!items.length||items.length>30)throw new AppError('Informe de 1 a 30 itens por pedido.');
 const seen=new Set();return items.map(item=>{const sku=text(item?.sku,50).toUpperCase(),quantity=integer(item.quantity,1);const p=room.row('SELECT * FROM products WHERE sku=? AND archived=0',sku);if(!p)throw new AppError('SKU não encontrado ou arquivado: '+sku,409);if(seen.has(p.id))throw new AppError('Agrupe as quantidades de um mesmo SKU.');seen.add(p.id);return {product_id:p.id,sku:p.sku,quantity};}).sort((a,b)=>a.product_id.localeCompare(b.product_id));
}
function sameLines(old,items){return JSON.stringify(old.map(l=>[l.product_id,l.quantity]).sort())===JSON.stringify(items.map(l=>[l.product_id,l.quantity]).sort());}
export function changeOrder(room,session,b,{source,api=false,keyHash=null,productionId=null}={}){
 const now=new Date().toISOString();let order,items,reference,selectedChannel,selectedSeller;
 if(api){
  reference=text(b.reference,80);selectedChannel=source.channel;selectedSeller=source.seller_id;
  order=room.row('SELECT * FROM orders WHERE channel=? AND reference=?',selectedChannel,reference);
  if(order&&order.source_id!==source.id)throw new AppError('Pedido já registrado por outra origem. Confira antes de integrar.',409);
  items=linesInput(room,b.items);integer(b.revision,1,Number.MAX_SAFE_INTEGER);
 }else if(b.id){
  order=room.row('SELECT * FROM orders WHERE id=?',uuid(b.id));if(!order)throw new AppError('Pedido não encontrado.',404);
  if(session.role!=='admin'&&order.seller_id!==session.member_id)throw new AppError('Este pedido pertence a outro responsável.',403);
  if(order.source_id!=='manual'&&room.row('SELECT active FROM connections WHERE id=?',order.source_id)?.active)throw new AppError('Este pedido é atualizado pela integração. Pause a conexão antes de intervir.',409);
  items=room.sql.exec('SELECT * FROM order_lines WHERE order_id=? ORDER BY product_id',order.id).toArray();
 }else{
  reference=text(b.reference,80);selectedChannel=channel(b.channel);selectedSeller=session.role==='admin'?(b.seller_id||'owner'):session.member_id;
  if(session.role!=='admin'&&b.seller_id&&b.seller_id!==session.member_id)throw new AppError('Você só pode criar seus próprios pedidos.',403);
  if(room.row('SELECT id FROM orders WHERE channel=? AND reference=?',selectedChannel,reference))throw new AppError('Este pedido já está cadastrado neste canal. Confira a lista de pedidos.',409);
  items=linesInput(room,b.items);
 }
 if(!order){const prod=room.row('SELECT id FROM production WHERE channel=? AND reference=?',selectedChannel,reference);if(prod&&prod.id!==productionId)throw new AppError('Referência já cadastrada em Sob demanda.',409);}
 const status=b.status;if(!['reserved','fulfilled','cancelled'].includes(status))throw new AppError('Escolha reservar, confirmar saída ou cancelar.');
 let oldItems;if(order){
  oldItems=room.sql.exec('SELECT * FROM order_lines WHERE order_id=?',order.id).toArray();
  if(!sameLines(oldItems,items))throw new AppError('Os itens do pedido não podem mudar. Confira o pedido na origem.',409);
  if(api&&b.revision<=order.external_version){if(b.revision===order.external_version&&keyHash===order.external_hash)return {id:order.id,order_status:order.status,unchanged:true};throw new AppError('Evento desatualizado ou revisão conflitante. Consulte o pedido atual na origem.',409);}
  if(!api&&order.version!==integer(b.expected_version,1,1000000000))throw new AppError('O pedido mudou. Atualize a lista antes de confirmar.',409);
  if(order.status!==status&&order.status!=='reserved')throw new AppError('Pedido já encerrado. Devoluções exigem conferência física e movimentação própria.',409);
 }else{
  seller(room,selectedSeller,!productionId);if(room.row('SELECT COUNT(*) AS n FROM orders').n>=20000)throw new AppError('Limite de 20.000 pedidos por espaço.',409);
  order={id:crypto.randomUUID(),source_id:source?.id||'manual',channel:selectedChannel,reference,seller_id:selectedSeller,status:null};
  room.sql.exec('INSERT INTO orders(id,source_id,channel,reference,seller_id,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',order.id,order.source_id,order.channel,order.reference,order.seller_id,status,now,now);
  for(const line of items)room.sql.exec('INSERT INTO order_lines VALUES(?,?,?,?)',order.id,line.product_id,line.sku,line.quantity);
 }
 const type=order.status===status?null:!order.status?(status==='reserved'?'reserve':status==='fulfilled'?'sale':null):status==='fulfilled'?'fulfill':'release';
 const note=api?'Pedido recebido pela API':text(b.note||'',200,false);
 if(type)for(const line of items){
  const p=room.row('SELECT * FROM products WHERE id=? AND archived=0',line.product_id);if(!p)throw new AppError('Produto arquivado ou ausente. Confira o pedido.',409);
  const next=nextStock(p,{type,quantity:line.quantity});
  room.sql.exec('UPDATE products SET physical=?,reserved=?,version=version+1,updated_at=? WHERE id=?',next.physical,next.reserved,now,p.id);
  room.sql.exec('INSERT INTO movements(id,product_id,type,quantity,delta_physical,delta_reserved,after_physical,after_reserved,channel,reference,note,actor,created_at,member_id,seller_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',crypto.randomUUID(),p.id,type,line.quantity,next.physical-p.physical,next.reserved-p.reserved,next.physical,next.reserved,order.channel,'EV:'+order.id,`Pedido ${order.reference}${note?' · '+note:''}`,session.actor,now,session.member_id,order.seller_id);
  room.evaluateAlert(p.id,now);
 }
 room.sql.exec('UPDATE orders SET status=?,version=version+1,external_version=?,external_hash=?,updated_at=? WHERE id=?',status,api?b.revision:(order.external_version||0),api?keyHash:(order.external_hash||''),now,order.id);
 room.sql.exec('INSERT INTO order_events VALUES(?,?,?,?,?,?)',crypto.randomUUID(),order.id,status,session.actor,note,now);
 if(api)room.sql.exec('UPDATE connections SET last_received=? WHERE id=?',now,source.id);
 return {id:order.id,order_status:status};
}
export function orderWrite(room,hash,b,payloadHash){return publish(room,room.safe(()=>{const s=room.session(hash);const old=replay(room,b.operation_id,payloadHash,s.member_id);if(old)return old;return room.ctx.storage.transactionSync(()=>{capacity(room);return finish(room,b.operation_id,payloadHash,s.member_id,changeOrder(room,s,b));});}));}
export function integrationWrite(room,id,tokenHash,b,payloadHash,contentHash){return publish(room,room.safe(()=>{
 const c=room.row('SELECT * FROM connections WHERE id=? AND key_hash=? AND active=1',uuid(id),tokenHash);if(!c)throw new AppError('Chave de integração inválida ou revogada.',401);seller(room,c.seller_id);
 const s={actor:'Integração: '+c.name,member_id:'integration:'+c.id,role:'integration'};
 const old=replay(room,b.event_id,payloadHash,s.member_id);if(old)return old;
 return room.ctx.storage.transactionSync(()=>{capacity(room);return finish(room,b.event_id,payloadHash,s.member_id,changeOrder(room,s,b,{source:c,api:true,keyHash:contentHash}));});
}));}
export function ordersPage(room,hash,{before=1000000000,status='',q=''}={}){return room.safe(()=>{
 const s=room.session(hash);integer(before,1,1000000000);q=text(q,80,false);if(status&&!['reserved','fulfilled','cancelled'].includes(status))throw new AppError('Filtro inválido.');
 const args=[before],where=['o.rowid<?'];if(s.role!=='admin'){where.push('o.seller_id=?');args.push(s.member_id);}if(status){where.push('o.status=?');args.push(status);}if(q){where.push('instr(lower(o.reference),lower(?))>0');args.push(q);}
 const rows=room.sql.exec("SELECT o.rowid AS cursor,o.*,COALESCE(m.name,'Gestão da marca') AS seller_name,COALESCE(c.active,0) AS connection_active,c.name AS connection_name FROM orders o LEFT JOIN members m ON m.id=o.seller_id LEFT JOIN connections c ON c.id=o.source_id WHERE "+where.join(' AND ')+' ORDER BY o.rowid DESC LIMIT 50',...args).toArray();
 for(const o of rows){o.items=room.sql.exec('SELECT l.*,p.name FROM order_lines l JOIN products p ON p.id=l.product_id WHERE order_id=?',o.id).toArray();delete o.external_hash;}
 return {ok:true,orders:rows,next_cursor:rows.length===50?rows.at(-1).cursor:null};
});}
export function connectionsList(room,hash){return room.safe(()=>{room.admin(room.session(hash));return {ok:true,connections:room.sql.exec("SELECT c.id,c.name,c.channel,c.seller_id,c.active,c.created_at,c.last_received,COALESCE(m.name,'Gestão da marca') AS seller_name FROM connections c LEFT JOIN members m ON m.id=c.seller_id ORDER BY c.rowid DESC LIMIT 100").toArray()};});}
