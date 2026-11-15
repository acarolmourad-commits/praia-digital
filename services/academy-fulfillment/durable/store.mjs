/* SQLite Durable Object ledger. Local candidate, not deployed. New databases
 * only: legacy event schemas require explicit migration review, never an
 * implicit ALTER/backfill of receipts that lack signed-payload evidence. */
export class Ledger {
 constructor(storage) {
  this.s=storage; this.sql=storage.sql;
  storage.transactionSync(()=>{
   this.sql.exec(`CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,type TEXT NOT NULL,object_id TEXT NOT NULL,created INTEGER NOT NULL,payload_sha256 TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'PENDING',due INTEGER NOT NULL DEFAULT 0,attempts INTEGER NOT NULL DEFAULT 0,error TEXT)`);
   const columns=this.rows('PRAGMA table_info(events)').map(row=>row.name);
   if(!columns.includes('payload_sha256'))throw Error('LEDGER_SCHEMA_REVIEW_REQUIRED');
   this.sql.exec(`CREATE TABLE IF NOT EXISTS orders(id TEXT PRIMARY KEY,fingerprint TEXT NOT NULL,payload TEXT NOT NULL,state TEXT NOT NULL,version INTEGER NOT NULL DEFAULT 0,lease TEXT,lease_until INTEGER NOT NULL DEFAULT 0,draft_id TEXT,message_id TEXT,revoked INTEGER NOT NULL DEFAULT 0,attempts INTEGER NOT NULL DEFAULT 0,due INTEGER NOT NULL,error TEXT,hold_reason TEXT)`);
   if(!this.rows('PRAGMA table_info(orders)').some(row=>row.name==='hold_reason'))throw Error('LEDGER_SCHEMA_REVIEW_REQUIRED');
   this.sql.exec('CREATE INDEX IF NOT EXISTS due_orders ON orders(state,due)');
   this.sql.exec('CREATE TABLE IF NOT EXISTS intake_holds(id INTEGER PRIMARY KEY CHECK(id=1),reason TEXT NOT NULL)');
  });
 }
 rows(query,...args){return [...this.sql.exec(query,...args)];}
 intakeHeld(){return this.rows('SELECT reason FROM intake_holds WHERE id=1').length!==0;}
 // Never erase evidence of an effect that may already have begun. Updating the
 // version invalidates any stale pre-effect operation after provider awaits.
 holdOrder(id,reason){
  this.sql.exec("UPDATE orders SET state=CASE WHEN state='DRAFT_CREATING' THEN 'UNCERTAIN' WHEN state IN ('SENDING','UNCERTAIN','SENT') THEN state ELSE 'HELD' END,revoked=1,version=version+1,error=?,hold_reason=? WHERE id=?",reason,reason,id);
 }
 recordEvent(e){
  if(!e||!/^[a-f0-9]{64}$/.test(e.payload_sha256||'')||!Number.isSafeInteger(e.created)||e.created<0)throw Error('INVALID_RECEIPT_PROOF');
  const outcome=this.s.transactionSync(()=>{
   if(this.intakeHeld())return {error:'EVENT_INTAKE_QUARANTINED'};
   this.sql.exec('INSERT OR IGNORE INTO events(id,type,object_id,created,payload_sha256) VALUES(?,?,?,?,?)',e.id,e.type,e.object_id,e.created,e.payload_sha256);
   const found=this.rows('SELECT * FROM events WHERE id=?',e.id)[0];
   if(['type','object_id','created','payload_sha256'].some(k=>found[k]!==e[k])){
    // Conservative account-shard hold, including risk-event conflicts whose
    // related session cannot safely be inferred without more provider reads.
    this.sql.exec("INSERT OR IGNORE INTO intake_holds VALUES(1,'EVENT_CONFLICT')");
    this.sql.exec("UPDATE events SET state='HELD',error='EVENT_CONFLICT' WHERE id=?",e.id);
    for(const row of this.rows('SELECT id FROM orders'))this.holdOrder(row.id,'EVENT_CONFLICT');
    return {error:'EVENT_CONFLICT'};
   }
   return {row:found};
  });
  // Throw AFTER commit: the quarantine must survive the caller's error path.
  if(outcome.error)throw Error(outcome.error);return outcome.row;
 }
 pendingEvents(limit=10,now=Date.now()){
  if(this.intakeHeld())return [];
  return this.rows('SELECT * FROM events WHERE state=? AND due<=? ORDER BY due,created,id LIMIT ?','PENDING',now,Math.min(limit,20));
 }
 retryEvent(id,now,terminal=false){
  if(this.intakeHeld())return;
  const r=this.rows('SELECT attempts FROM events WHERE id=?',id)[0];const attempts=(r?.attempts||0)+1;
  this.sql.exec('UPDATE events SET attempts=?,due=?,state=?,error=? WHERE id=?',attempts,now+Math.min(3600000,60000*2**Math.min(attempts-1,6)),terminal?'HELD':'PENDING',terminal?'POLICY_CONFLICT':'PROVIDER_RETRY',id);
 }
 markEventDone(id){this.sql.exec("UPDATE events SET state='DONE' WHERE id=? AND state='PENDING'",id);}
 acceptVerifiedOrder(o,fingerprint,now){
  const outcome=this.s.transactionSync(()=>{
   if(this.intakeHeld())return {error:'EVENT_INTAKE_QUARANTINED'};
   const row=this.get(o.id);
   if(row){
    if(row.fingerprint!==fingerprint){this.holdOrder(row.id,'ORDER_CONFLICT');return {error:'ORDER_CONFLICT'};}
    return {row};
   }
   this.sql.exec('INSERT INTO orders(id,fingerprint,payload,state,due) VALUES(?,?,?,?,?)',o.id,fingerprint,JSON.stringify(o),'READY',now);
   return {row:this.get(o.id)};
  });
  if(outcome.error)throw Error(outcome.error);return outcome.row;
 }
 get(id){return this.rows('SELECT * FROM orders WHERE id=?',id)[0]||null;}
 claim(id,token,now){return this.s.transactionSync(()=>{
  if(this.intakeHeld())return null;
  const r=this.get(id);if(!r||['SENT','HELD','REVOKED'].includes(r.state)||r.due>now||r.lease_until>now)return null;
  if(['DRAFT_CREATING','SENDING'].includes(r.state))this.sql.exec('UPDATE orders SET state=?,version=version+1,lease=NULL,lease_until=0,error=? WHERE id=?','UNCERTAIN','PROCESS_INTERRUPTED',id);
  this.sql.exec('UPDATE orders SET lease=?,lease_until=?,version=version+1 WHERE id=?',token,now+120000,id);return this.get(id);
 });}
 transition(row,next,fields={}){
  const allowed=new Set(['draft_id','message_id','error','due','attempts']);for(const k of Object.keys(fields))if(!allowed.has(k))throw Error('INVALID_UPDATE');
  return this.s.transactionSync(()=>{
   const r=this.get(row.id);if(!r||r.version!==row.version||r.lease!==row.lease||r.state!==row.state||this.intakeHeld())throw Error('STALE_OPERATION');
   const keys=Object.keys(fields);this.sql.exec(`UPDATE orders SET state=?,version=version+1${keys.map(k=>','+k+'=?').join('')} WHERE id=?`,next,...keys.map(k=>fields[k]),row.id);return this.get(row.id);
  });
 }
 assertWriteAllowed(expected,now){return this.s.transactionSync(()=>{
  const current=this.get(expected.id);
  if(!Number.isSafeInteger(now)||now<0||!current||this.intakeHeld()||current.revoked||current.hold_reason||
    !['DRAFT_CREATING','SENDING'].includes(current.state)||current.state!==expected.state||
    current.version!==expected.version||!expected.lease||current.lease!==expected.lease||current.lease_until<=now)throw Error('DURABLE_WRITE_GUARD_REJECTED');
  return true;
 });}
 release(row){this.sql.exec('UPDATE orders SET lease=NULL,lease_until=0,version=version+1 WHERE id=? AND version=? AND lease=?',row.id,row.version,row.lease);}
 revoke(id){return this.s.transactionSync(()=>{
  const r=this.get(id);if(!r)return;const state=['SENDING','UNCERTAIN','SENT'].includes(r.state)?r.state:'REVOKED';
  this.sql.exec('UPDATE orders SET revoked=1,state=?,version=version+1 WHERE id=?',state,id);
 });}
 recoverSent(id,messageId){this.s.transactionSync(()=>{
  const r=this.get(id);if(!r)throw Error('UNKNOWN_ORDER');if(r.message_id&&r.message_id!==messageId)throw Error('MESSAGE_CONFLICT');
  this.sql.exec('UPDATE orders SET state=?,message_id=?,lease=NULL,lease_until=0,version=version+1 WHERE id=?','SENT',messageId,id);
 });}
 due(now,limit=5){
  if(this.intakeHeld())return [];
  return this.rows("SELECT id FROM orders WHERE state NOT IN ('SENT','HELD','REVOKED') AND due<=? AND lease_until<=? ORDER BY due,id LIMIT ?",now,now,limit);
 }
}
