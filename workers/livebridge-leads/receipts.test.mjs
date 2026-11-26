import test from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import worker from './worker.mjs';
import {enqueueReceipts, sendReceipts} from './receipts.mjs';

const now = new Date('2026-11-17T18:00:00.000Z');
const before = '2026-11-17T00:00:00.000Z';
function setup() {
  const db = new DatabaseSync(':memory:');
  for (const file of ['schema.sql','receipt-migration.sql']) db.exec(readFileSync(new URL(file,import.meta.url),'utf8'));
  const env = {LEAD_LIMITER:{limit:async()=>({success:true})},RECEIPTS_MODE:'test',
    RECEIPTS_START_AT:before,RESEND_API_KEY:'offline-test-only',
    LEADS_DB:{prepare(sql){return {bind(...params){return {
      async run(){const r=db.prepare(sql).run(...params);return {success:true,meta:{changes:Number(r.changes)}};},
      async first(){return db.prepare(sql).get(...params);},
      async all(){return {results:db.prepare(sql).all(...params)};}
    };}};}}};
  env.LEADS_DB.batch = async statements => {
    db.exec('BEGIN');
    try {const results=[];for(const s of statements)results.push(await s.run());db.exec('COMMIT');return results;}
    catch(e){db.exec('ROLLBACK');throw e;}
  };
  return {db,env};
}
const payload = (extra={}) => ({submission_id:crypto.randomUUID(),service:'Estoque Vivo',name:'Teste fictício',
  email:'comercial@praia.digital',phone:'',business:'Empresa fictícia',source:'Ainda não faço lives',
  marketplaces:[],destinations:[],goal:'BRIEFING PRIVADO NÃO ENVIAR',website:'',consent:true,
  consent_version:'livebridge-contact-2026-11-12',...extra});
const request = b => new Request('https://worker.test/leads',{method:'POST',headers:{Origin:'https://praia.digital','Content-Type':'application/json'},body:JSON.stringify(b)});
async function save(env,db,extra={}) {
  const body=payload(extra), mode=env.RECEIPTS_MODE;
  env.RECEIPTS_MODE='off';
  const response=await worker.fetch(request(body),env);
  env.RECEIPTS_MODE=mode;
  assert.equal(response.status,201);
  db.prepare('UPDATE leads SET created_at=? WHERE id=?').run(now.toISOString(),body.submission_id);
  return body;
}
const ok = async () => Response.json({id:'mock-provider-id'});
const status = (db,id) => db.prepare('SELECT status FROM receipt_delivery WHERE lead_id=?').get(id)?.status;

test('receipt uses committed data, minimal content, fixed recipient in pilot and stable key',async()=>{
  const {env,db}=setup(), b=await save(env,db), messages=[];
  await enqueueReceipts(env,b.submission_id,now);
  await sendReceipts(env,b.submission_id,async(url,options)=>{messages.push({url,options});return ok();},now);
  assert.equal(messages.length,1);
  const {url,options}=messages[0], body=JSON.parse(options.body);
  assert.equal(url,'https://api.resend.com/emails');
  assert.deepEqual(body.to,['comercial@praia.digital']);assert.equal(body.reply_to,'comercial@praia.digital');
  assert.match(body.subject,/TESTE INTERNO/);assert.match(body.text,new RegExp(b.submission_id));
  assert.ok(!options.body.includes(b.goal));assert.ok(!options.body.includes(b.business));
  assert.equal(options.headers['Idempotency-Key'],`service-receipt-v1/${b.submission_id}`);
  assert.equal(status(db,b.submission_id),'accepted');
  assert.equal(db.prepare("SELECT status FROM notification_outbox WHERE kind='receipt'").get().status,'accepted');
});
test('duplicate submission and concurrent dispatch send only once',async()=>{
  const {env,db}=setup(),b=await save(env,db);let calls=0;
  await Promise.all([enqueueReceipts(env,b.submission_id,now),enqueueReceipts(env,b.submission_id,now)]);
  const transport=async()=>{calls++;await new Promise(resolve=>setTimeout(resolve,5));return ok();};
  await Promise.all([sendReceipts(env,'',transport,now),sendReceipts(env,'',transport,now)]);
  env.RECEIPTS_MODE='off';assert.equal((await worker.fetch(request(b),env)).status,200);env.RECEIPTS_MODE='test';
  await enqueueReceipts(env,b.submission_id,now);await sendReceipts(env,'',transport,now);
  assert.equal(calls,1);assert.equal(db.prepare('SELECT count(*) n FROM leads').get().n,1);
  assert.equal(db.prepare('SELECT count(*) n FROM receipt_delivery').get().n,1);
});
test('provider 503, rejection, malformed success and timeout preserve leads and require review',async()=>{
  for(const response of [()=>Response.json({}, {status:503}),()=>Response.json({}, {status:429}),
    ()=>Response.json({}, {status:401}),()=>Response.json({}),()=>{throw new Error('private provider detail');}]) {
    const {env,db}=setup(),b=await save(env,db);let calls=0;
    await enqueueReceipts(env,b.submission_id,now);
    const transport=async()=>{calls++;return response();};
    await sendReceipts(env,'',transport,now);await sendReceipts(env,'',transport,now);
    assert.equal(calls,1);assert.equal(status(db,b.submission_id),'review_required');
    assert.equal(db.prepare('SELECT count(*) n FROM leads').get().n,1);
  }
});
test('disabled provider, missing secret or invalid cutover never call network or queue notices',async()=>{
  for(const extra of [{RECEIPTS_MODE:'off'},{RESEND_API_KEY:''},{RECEIPTS_START_AT:''},{RECEIPTS_MODE:'typo'}]) {
    const {env,db}=setup();await save(env,db);Object.assign(env,extra);
    assert.equal(await enqueueReceipts(env,'',now),'pending_setup');
    await sendReceipts(env,'',async()=>assert.fail('network forbidden'),now);
    assert.equal(db.prepare('SELECT count(*) n FROM receipt_delivery').get().n,0);
  }
});
test('pilot excludes visitors, historical notices, technical records and invalid consent',async()=>{
  const {env,db}=setup();
  const other=await save(env,db,{email:'person@example.invalid'});
  const old=await save(env,db);db.prepare('UPDATE leads SET created_at=? WHERE id=?').run('2026-11-13T13:23:00.000Z',old.submission_id);
  const tech=await save(env,db);db.prepare("UPDATE leads SET status='teste_tecnico' WHERE id=?").run(tech.submission_id);
  const revoked=await save(env,db);db.prepare("UPDATE leads SET consent_version='withdrawn' WHERE id=?").run(revoked.submission_id);
  await enqueueReceipts(env,'',now);assert.equal(db.prepare('SELECT count(*) n FROM receipt_delivery').get().n,0);
  env.RECEIPTS_MODE='live';await enqueueReceipts(env,'',now);
  assert.equal(db.prepare('SELECT lead_id FROM receipt_delivery').get().lead_id,other.submission_id);
});
test('recipient quota and global quota hold messages without losing protocols',async()=>{
  const {env,db}=setup();const leads=[];
  for(let i=0;i<4;i++)leads.push(await save(env,db));
  await Promise.all([enqueueReceipts(env,'',now),enqueueReceipts(env,'',now)]);
  assert.equal(db.prepare('SELECT count(*) n FROM receipt_delivery').get().n,3);
  assert.equal(db.prepare("SELECT count(*) n FROM notification_outbox WHERE kind='receipt' AND status='quota_hold'").get().n,1);
  env.RECEIPTS_MODE='live';
  for(let i=0;i<90;i++)await save(env,db,{email:`offline${i}@example.invalid`});
  await enqueueReceipts(env,'',now);
  assert.equal(db.prepare('SELECT count(*) n FROM receipt_delivery').get().n,90);
});
test('interrupted or old jobs are held and never automatically resent',async()=>{
  const {env,db}=setup(),b=await save(env,db);
  await enqueueReceipts(env,'',now);
  db.prepare("UPDATE receipt_delivery SET status='sending',started_at=?").run('2026-11-17T17:55:00.000Z');
  await sendReceipts(env,'',async()=>assert.fail('network forbidden'),now);
  assert.equal(status(db,b.submission_id),'review_required');
  const second=await save(env,db);await enqueueReceipts(env,second.submission_id,now);
  await sendReceipts(env,'',async()=>assert.fail('network forbidden'),new Date(+now+24*3600000));
  assert.equal(status(db,second.submission_id),'review_required');
});
test('service storage failure rolls back lead and both notification rows',async()=>{
  const {env,db}=setup();env.RECEIPTS_MODE='off';
  db.exec("CREATE TRIGGER fail_service BEFORE INSERT ON service_requests BEGIN SELECT RAISE(ABORT,'simulated write failure'); END;");
  const r=await worker.fetch(request(payload()),env);
  assert.equal(r.status,503);
  for(const table of ['leads','notification_outbox','receipt_delivery'])assert.equal(db.prepare(`SELECT count(*) n FROM ${table}`).get().n,0);
});
test('invalid consent causes neither registration nor either email',async()=>{
  const {env,db}=setup();env.EMAIL_NOTIFICATIONS_ENABLED='true';env.EMAIL={send:async()=>assert.fail('send forbidden')};
  assert.equal((await worker.fetch(request(payload({consent:false})),env)).status,422);
  await enqueueReceipts(env,'',now);await sendReceipts(env,'',async()=>assert.fail('send forbidden'),now);
  assert.equal(db.prepare('SELECT count(*) n FROM leads').get().n,0);
});

test('accepted form keeps its protocol and team notice when receipt provider is unavailable',async()=>{
  const {env,db}=setup();let team=0,receipts=0;
  env.EMAIL_NOTIFICATIONS_ENABLED='true';env.EMAIL={send:async()=>{team++;return {messageId:'team-mock'};}};
  const original=globalThis.fetch;
  globalThis.fetch=async()=>{
    receipts++;assert.equal(db.prepare('SELECT count(*) n FROM service_requests').get().n,1);
    assert.equal(db.prepare('SELECT count(*) n FROM leads').get().n,1);
    return Response.json({}, {status:503});
  };
  try {
    const b=payload();const r=await worker.fetch(request(b),env);
    assert.equal(r.status,201);assert.equal((await r.json()).id,b.submission_id);
    const repeated=await worker.fetch(request(b),env);
    assert.equal((await repeated.json()).email_status,'review_required');
    assert.equal(receipts,1);assert.equal(team,1);
    assert.equal(status(db,b.submission_id),'review_required');
  } finally {globalThis.fetch=original;}
});
test('missing receipt migration does not invalidate an accepted registration or team notice',async()=>{
  const {env,db}=setup();db.exec('DROP TABLE receipt_delivery');let team=0;
  env.EMAIL_NOTIFICATIONS_ENABLED='true';env.EMAIL={send:async()=>{team++;return {messageId:'team-mock'};}};
  const r=await worker.fetch(request(payload()),env);
  assert.equal(r.status,201);assert.equal((await r.json()).email_status,'pending_setup');assert.equal(team,1);
});
test('persistence failure after provider acceptance does not cause an automatic resend',async()=>{
  const {env,db}=setup(),b=await save(env,db);let calls=0;
  await enqueueReceipts(env,'',now);
  db.exec("CREATE TRIGGER fail_accept BEFORE UPDATE OF status ON receipt_delivery WHEN NEW.status='accepted' BEGIN SELECT RAISE(ABORT,'simulated failure'); END;");
  const transport=async()=>{calls++;return ok();};
  await sendReceipts(env,'',transport,now);await sendReceipts(env,'',transport,now);
  assert.equal(calls,1);assert.equal(status(db,b.submission_id),'review_required');
});

test('isolated QA is closed without its secret and cannot send CRM login emails',async()=>{
  const {env,db}=setup(),body=payload();env.QA_MODE='true';env.RECEIPTS_MODE='off';
  env.QA_ACCESS_TOKEN='offline-qa-access-token';env.QA_SUBMISSION_ID=body.submission_id;
  assert.equal((await worker.fetch(request(body),env)).status,404);
  const authorized=b=>{const r=request(b);r.headers.set('Authorization','Bearer '+env.QA_ACCESS_TOKEN);return r;};
  assert.equal((await worker.fetch(authorized({...body,email:'outsider@example.invalid'}),env)).status,422);
  assert.equal((await worker.fetch(authorized(payload()),env)).status,422);
  assert.equal(db.prepare('SELECT count(*) n FROM leads').get().n,0);
  assert.equal((await worker.fetch(new Request('https://worker.test/crm/login',{method:'POST',headers:{Authorization:'Bearer '+env.QA_ACCESS_TOKEN}}),env)).status,404);
  assert.equal((await worker.fetch(authorized(body),env)).status,201);
  assert.equal((await worker.fetch(authorized(body),env)).status,200);
});
