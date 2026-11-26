// End-to-end requests use the real Worker with in-memory SQLite and a fake email binding.
// Every browser request is intercepted: no customer data, live writes, or messages.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {pathToFileURL}=require('node:url');
const {DatabaseSync}=require('node:sqlite');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'), origin='https://praia.digital';
const built=JSON.parse(execFileSync('python3',['-c',`
import importlib.util,json,pathlib
r=pathlib.Path(${JSON.stringify(root)})
s=importlib.util.spec_from_file_location('nav',r/'scripts/build-navigation.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
h=(r/'partials/header.html').read_text()
print(json.dumps({p:m.transform((r/p).read_text(),m.header_for_page(p,h))[0] for p in ['servicos-ia.html','solicitar-servico.html']}))
`],{encoding:'utf8'}));
const services=['Atendimento e relacionamento','Automação de processos','Conteúdo e comunicação','Conhecimento e apoio à equipe','Diagnóstico e capacitação','Projeto personalizado'];
const formURL=service=>origin+'/solicitar-servico.html?servico='+encodeURIComponent(service);
async function fillContact(page){
 await page.locator('#lead-name').fill('Teste fictício de QA');
 await page.locator('#business').fill('Empresa fictícia');
 await page.locator('#lead-email').fill('qa@example.invalid');
 await page.locator('#lead-consent').check();
}
async function noOverflow(page){assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),page.url());}
(async()=>{
 const {default:worker}=await import(pathToFileURL(path.join(root,'workers/livebridge-leads/worker.mjs')));
 const db=new DatabaseSync(':memory:');db.exec(fs.readFileSync(path.join(root,'workers/livebridge-leads/schema.sql'),'utf8'));
 const messages=[];
 const env={
  LEAD_LIMITER:{limit:async()=>({success:true})},
  EMAIL_NOTIFICATIONS_ENABLED:'true',
  EMAIL:{send:async m=>{messages.push(m);return{messageId:'mock-'+messages.length}}},
  LEADS_DB:{prepare(sql){return{bind(...params){return{
   async run(){const result=db.prepare(sql).run(...params);return{success:true,meta:{changes:Number(result.changes)}}},
   async first(){return db.prepare(sql).get(...params)},
   async all(){return{results:db.prepare(sql).all(...params)}}
  }}}}}
 };

  env.LEADS_DB.batch = async statements => {
    db.exec('BEGIN');
    try { const results=[]; for (const stmt of statements) results.push(await stmt.run()); db.exec('COMMIT'); return results; }
    catch (error) { db.exec('ROLLBACK'); throw error; }
  };

 const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {})});
 let mode='normal',requests=[],external=[];
 async function route(r){
  const req=r.request(),u=new URL(req.url());
  if(u.hostname==='praia-livebridge-leads.kleber-f63.workers.dev'&&req.method()==='OPTIONS')return r.fulfill({status:204,headers:{'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type'}});
  if(u.hostname==='praia-livebridge-leads.kleber-f63.workers.dev'&&u.pathname==='/leads'&&req.method()==='POST'){
   const body=req.postDataJSON();requests.push(body);
   if(mode==='network')return r.abort('failed');
   if(mode==='unconfirmed')return r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({ok:true,id:'wrong-id'})});
   const response=await worker.fetch(new Request(req.url(),{method:'POST',headers:{Origin:origin,'Content-Type':'application/json'},body:JSON.stringify(body)}),env);
   if(mode==='lost-receipt')return r.abort('failed');
   if(mode.startsWith('email:')){const body=await response.json();body.email_status=mode.slice(6);return r.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:JSON.stringify(body)})}
   return r.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:await response.text()});
  }
  if(req.method()!=='GET'||u.origin!==origin){external.push(req.url());return r.abort()}
  const rel=decodeURIComponent(u.pathname).replace(/^\//,''),f=path.join(root,rel);
  const type=f.endsWith('.css')?'text/css':f.endsWith('.js')?'application/javascript':f.endsWith('.png')?'image/png':f.endsWith('.ico')?'image/x-icon':'text/html';
  if(!built[rel]&&!fs.existsSync(f)){external.push('missing:'+rel);return r.abort()}
  return r.fulfill({body:built[rel]||fs.readFileSync(f),contentType:type});
 }
 try{
  for(const width of [320,390,768,1280]){
   const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});await context.route('**/*',route);
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto(origin+'/servicos-ia.html');await noOverflow(page);
   await page.keyboard.press('Tab');assert.equal(await page.locator('.skip-link').evaluate(e=>e===document.activeElement),true);
   const q=page.locator('summary').first();await q.focus();await page.keyboard.press('Enter');assert.equal(await q.evaluate(e=>e.parentElement.open),true);await page.keyboard.press('Enter');
   assert.equal(await page.locator('.pd-site-header').count(),1);
   assert.equal(await page.locator('.pd-site-cta').getAttribute('href'),'/solicitar-servico.html?servico=Projeto%20personalizado');
   await page.screenshot({path:'/tmp/ia-services-'+width+'.png',fullPage:true});
   await page.locator('.hero .button').click();assert.equal(await page.locator('#lead-service').inputValue(),'Projeto personalizado');
   await noOverflow(page);assert.equal(await page.locator('#project-fields').isVisible(),true);assert.equal(await page.locator('#live-fields').isVisible(),false);
   await page.screenshot({path:'/tmp/ia-services-form-'+width+'.png',fullPage:true});
   for(const service of services){await page.goto(formURL(service));assert.equal(await page.locator('#lead-service').inputValue(),service);assert.equal(await page.locator('#marketplace-fields').isVisible(),false);assert.equal(await page.locator('#source').isDisabled(),true)}
   await page.goto(formURL('LiveBridge AI'));assert.equal(await page.locator('#live-fields').isVisible(),true);assert.equal(await page.locator('#project-fields').isVisible(),false);
   await page.locator('[name=marketplace][value=Shopee]').check();await page.locator('[name=destination][value=Instagram]').check();await page.locator('#source').selectOption('OBS ou outro estúdio');
   await page.locator('#lead-service').selectOption('Estoque Vivo');assert.equal(await page.locator('#marketplace-fields').isVisible(),true);assert.equal(await page.locator('#live-fields').isVisible(),false);
   await page.locator('#lead-service').selectOption('Automação de processos');await fillContact(page);
   await page.locator('#process').fill('Organizar pedidos');await page.locator('#tools').fill('Planilha e e-mail');await page.locator('#volume').fill('20 por semana');await page.locator('#goal').fill('Acompanhar cada retorno');
   const before=requests.length;await page.locator('#lead-submit').click();await page.locator('#brief-result').waitFor({state:'visible'});
   assert.equal(requests.length,before+1);const payload=requests.at(-1);assert.equal(payload.service,'Automação de processos');assert.deepEqual(payload.destinations,[]);assert.deepEqual(payload.marketplaces,[]);assert.equal(payload.source,'Ainda não faço lives');
   const row=db.prepare('SELECT * FROM leads WHERE id=?').get(payload.submission_id);assert.match(row.goal,/Processo: Organizar pedidos/);assert.match(row.goal,/Ferramentas: Planilha e e-mail/);assert.match(row.goal,/Volume ou frequência: 20 por semana/);assert.match(row.goal,/Objetivo: Acompanhar cada retorno/);
   assert.equal(await page.locator('#lead-receipt').innerText(),payload.submission_id);assert.equal(await page.locator('#lead-success-title').evaluate(e=>e===document.activeElement),true);
   assert.match(messages.at(-1).text,/Automação de processos/);assert.equal(messages.at(-1).to,'comercial@praia.digital');assert.equal(db.prepare("SELECT status FROM notification_outbox WHERE lead_id=? AND kind='receipt'").get(payload.submission_id).status,'pending_setup');
   assert.equal(await page.locator('#brief-result [data-service-return]').getAttribute('href'),'/servicos-ia.html');
   await noOverflow(page);assert.deepEqual(errors,[]);await context.close();
   console.log('PASS '+width+'px: layout, keyboard, all service choices, context filtering, private storage, mocked team notice, receipt');
  }
  const context=await browser.newContext();await context.route('**/*',route);const page=await context.newPage();
  await page.goto(formURL('LiveBridge AI'));await fillContact(page);await page.locator('#source').selectOption('Celular / câmera');await page.locator('[name=marketplace][value=Shopee]').check();await page.locator('[name=destination][value=Instagram]').check();await page.locator('#goal').fill('Testar uma live');await page.locator('#lead-submit').click();await page.locator('#brief-result').waitFor({state:'visible'});assert.deepEqual(requests.at(-1).destinations,['Instagram']);assert.deepEqual(requests.at(-1).marketplaces,['Shopee']);assert.equal(requests.at(-1).source,'Celular / câmera');assert.equal(await page.locator('#brief-result [data-service-return]').getAttribute('href'),'/ia/marketplaces/');
  await page.goto(formURL('Estoque Vivo'));await fillContact(page);await page.locator('[name=marketplace][value=Outros]').check();await page.locator('#lead-submit').click();await page.locator('#brief-result').waitFor({state:'visible'});assert.deepEqual(requests.at(-1).marketplaces,['Outros']);assert.deepEqual(requests.at(-1).destinations,[]);
  await page.goto(formURL('Projeto personalizado'));await fillContact(page);await page.locator('#lead-name').fill('   ');const n=requests.length;await page.locator('#lead-submit').click();assert.equal(requests.length,n);await page.locator('#lead-name').fill('QA fictício');
  mode='unconfirmed';await page.locator('#lead-submit').click();await page.locator('#lead-error').waitFor({state:'visible'});assert.equal(await page.locator('#brief-result').isVisible(),false);assert.equal(await page.locator('#lead-submit').innerText(),'Enviar solicitação');assert.equal(await page.locator('#source').isDisabled(),true);
  mode='lost-receipt';await page.locator('#lead-submit').click();await page.locator('#lead-submit').waitFor({state:'visible'});await page.waitForFunction(()=>document.getElementById('lead-submit').disabled===false);const id=requests.at(-1).submission_id;const messageCount=messages.length;
  mode='normal';await page.locator('#lead-submit').click();await page.locator('#brief-result').waitFor({state:'visible'});assert.equal(requests.at(-1).submission_id,id);assert.equal(db.prepare('SELECT count(*) n FROM leads WHERE id=?').get(id).n,1);assert.equal(messages.length,messageCount);
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);await page.locator('#copy-receipt').click();await page.waitForFunction(()=>document.getElementById('copy-status').textContent.includes('copiado'));assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),id);
  for(const [state,expected] of [['queued','fila de envio'],['sending','processada'],['accepted','não comprova a entrega'],['review_required','não é necessário reenviar'],['quota_hold','aguardando disponibilidade'],['__proto__','Não foi possível confirmar a situação']]) {
    mode='email:'+state;await page.goto(formURL('Projeto personalizado'));await fillContact(page);
    await page.locator('#lead-submit').click();await page.locator('#brief-result').waitFor({state:'visible'});
    assert.ok((await page.locator('#lead-email-status').innerText()).includes(expected));
    assert.ok((await page.locator('#lead-receipt').innerText()).length===36);
  }
  mode='normal';
  console.log('PASS separate registration/email statuses and untrusted status fallback.');
  await context.close();
  const nojs=await browser.newContext({javaScriptEnabled:false});await nojs.route('**/*',route);const plain=await nojs.newPage();await plain.goto(formURL('Projeto personalizado'));assert.equal(await plain.locator('#lead-submit').isDisabled(),true);assert.equal(await plain.locator('noscript').isVisible(),true);await nojs.close();
  assert.deepEqual(external,[]);console.log('PASS LiveBridge and stock compatibility; validation, rejected receipt, retry without duplicate, copy and no-JS fallback. No live writes or emails.');
 }finally{await browser.close();db.close()}
})().catch(e=>{console.error(e);process.exit(1)});
