import {AppError,text,integer,uuid,nextStock} from './domain.mjs';
import {changeOrder} from './orders.mjs';
export const brazilDate=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo'}).format(new Date());
export function productionDue(date){if(typeof date!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(date)||!Number.isFinite(Date.parse(date))||new Date(date).toISOString().slice(0,10)!==date)throw new AppError('Informe uma data de pagamento válida.');const d=new Date(date+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+20);return d.toISOString().slice(0,10);}
export function migrateProduction(room){room.sql.exec(`CREATE TABLE IF NOT EXISTS production(id TEXT PRIMARY KEY,product_id TEXT NOT NULL,sku TEXT NOT NULL,quantity INTEGER NOT NULL CHECK(quantity>0),channel TEXT NOT NULL,reference TEXT NOT NULL,seller_id TEXT NOT NULL,status TEXT NOT NULL,paid_date TEXT NOT NULL DEFAULT '',due_date TEXT NOT NULL DEFAULT '',order_id TEXT,version INTEGER NOT NULL DEFAULT 1,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,UNIQUE(channel,reference)); CREATE TABLE IF NOT EXISTS production_events(id TEXT PRIMARY KEY,production_id TEXT NOT NULL,status TEXT NOT NULL,actor TEXT NOT NULL,note TEXT NOT NULL,created_at TEXT NOT NULL);`);}
export function productionWrite(room,hash,b,payloadHash){const result=room.safe(()=>{const s=room.session(hash);room.admin(s);uuid(b.operation_id);const old=room.row('SELECT * FROM operations WHERE id=?',b.operation_id);if(old){if(old.member_id!==s.member_id||old.payload_hash!==payloadHash)throw new AppError('Tentativa já utilizada com outros dados.',409);return {...JSON.parse(old.response),replayed:true};}
 return room.ctx.storage.transactionSync(()=>{
 if(room.row('SELECT COUNT(*) n FROM operations').n>=100000)throw new AppError('Limite de operações atingido.',409);
 const now=new Date().toISOString();let p,id,orderId=null;
 if(b.action==='create'){
  if(room.row('SELECT COUNT(*) n FROM production').n>=20000)throw new AppError('Limite de encomendas atingido.',409);
  const product=room.row('SELECT * FROM products WHERE id=? AND archived=0',uuid(b.product_id));if(!product)throw new AppError('Produto indisponível.',409);
  const reference=text(b.reference,80),channel=text(b.channel,40);if(!['Manual','TikTok Shop','Instagram','Facebook','Shopee','Mercado Livre','Loja física','Outro'].includes(channel))throw new AppError('Canal inválido.');
  if(room.row('SELECT id FROM production WHERE channel=? AND reference=?',channel,reference)||room.row('SELECT id FROM orders WHERE channel=? AND reference=?',channel,reference))throw new AppError('Referência já cadastrada. Confira os pedidos e a produção.',409);
  const seller=b.seller_id||'owner';if(seller!=='owner'&&!room.row('SELECT id FROM members WHERE id=? AND active=1',uuid(seller)))throw new AppError('Responsável indisponível.',409);
  id=crypto.randomUUID();room.sql.exec("INSERT INTO production(id,product_id,sku,quantity,channel,reference,seller_id,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,'awaiting_payment',?,?)",id,product.id,product.sku,integer(b.quantity,1),channel,reference,seller,now,now);
 }else{
  id=uuid(b.id);p=room.row('SELECT * FROM production WHERE id=?',id);if(!p)throw new AppError('Encomenda não encontrada.',404);
  if(p.version!==integer(b.expected_version,1,1000000000))throw new AppError('A encomenda mudou. Atualize antes de continuar.',409);
  if(b.action==='pay'){
   if(p.status!=='awaiting_payment')throw new AppError('Pagamento já registrado ou encomenda encerrada.',409);
   if(b.payment_confirmed!==true)throw new AppError('Confirme que o pagamento foi conferido.');
   const due=productionDue(b.paid_date);if(b.paid_date>brazilDate())throw new AppError('Pagamento não pode estar no futuro.');
   room.sql.exec("UPDATE production SET paid_date=?,due_date=?,status='in_production',version=version+1,updated_at=? WHERE id=?",b.paid_date,due,now,id);
  }else if(b.action==='complete'){
   if(p.status!=='in_production')throw new AppError('Somente produção paga pode ser concluída.',409);
   if(b.available_confirmed!==true)throw new AppError('Confirme que as unidades estão prontas e disponíveis para expedição.');
   const product=room.row('SELECT * FROM products WHERE id=? AND archived=0',p.product_id);if(!product)throw new AppError('Produto indisponível.',409);
   const n=nextStock(product,{type:'entry',quantity:p.quantity});
   room.sql.exec('UPDATE products SET physical=?,version=version+1,updated_at=? WHERE id=?',n.physical,now,p.product_id);
   room.sql.exec('INSERT INTO movements(id,product_id,type,quantity,delta_physical,delta_reserved,after_physical,after_reserved,channel,reference,note,actor,created_at,member_id,seller_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',crypto.randomUUID(),p.product_id,'entry',p.quantity,p.quantity,0,n.physical,product.reserved,p.channel,'PROD:'+id,'Produção concluída e reservada para '+p.reference,s.actor,now,s.member_id,p.seller_id);
   const created=changeOrder(room,s,{reference:p.reference,channel:p.channel,seller_id:p.seller_id,status:'reserved',items:[{sku:p.sku,quantity:p.quantity}],note:'Produção sob demanda concluída'},{productionId:id});orderId=created.id;
   room.sql.exec("UPDATE production SET order_id=?,status='completed',version=version+1,updated_at=? WHERE id=?",orderId,now,id);
  }else if(b.action==='cancel'){
   if(!['awaiting_payment','in_production'].includes(p.status))throw new AppError('Encomenda encerrada. Confira o pedido de saída vinculado.',409);
   text(b.note,200);room.sql.exec("UPDATE production SET status='cancelled',version=version+1,updated_at=? WHERE id=?",now,id);
  }else throw new AppError('Ação inválida.');
 }
 const current=room.row('SELECT status FROM production WHERE id=?',id);room.sql.exec('INSERT INTO production_events VALUES(?,?,?,?,?,?)',crypto.randomUUID(),id,current.status,s.actor,text(b.note||'',200,false),now);
 room.sql.exec('UPDATE workspace SET revision=revision+1');const response={ok:true,id,order_id:orderId,revision:room.row('SELECT revision FROM workspace').revision};room.sql.exec('INSERT INTO operations(id,payload_hash,response,member_id) VALUES(?,?,?,?)',b.operation_id,payloadHash,JSON.stringify(response),s.member_id);return response;
 });});if(result.ok&&!result.replayed){room.broadcast(result.revision);room.ctx.waitUntil(room.schedule());}return result;}
export function productionPage(room,hash,{before=1000000000,status=''}={}){return room.safe(()=>{room.admin(room.session(hash));integer(before,1,1000000000);if(status&&!['awaiting_payment','in_production','completed','cancelled'].includes(status))throw new AppError('Filtro inválido.');const rows=room.sql.exec("SELECT r.rowid cursor,r.*,p.name,COALESCE(m.name,'Gestão da marca') seller_name,o.status order_status FROM production r JOIN products p ON p.id=r.product_id LEFT JOIN members m ON m.id=r.seller_id LEFT JOIN orders o ON o.id=r.order_id WHERE r.rowid<? AND (?='' OR r.status=?) ORDER BY r.rowid DESC LIMIT 50",before,status,status).toArray();for(const r of rows)r.events=room.sql.exec('SELECT status,actor,note,created_at FROM production_events WHERE production_id=? ORDER BY rowid DESC',r.id).toArray();return {ok:true,production:rows,next_cursor:rows.length===50?rows.at(-1).cursor:null,today:brazilDate()};});}
