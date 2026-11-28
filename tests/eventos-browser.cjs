const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
const file='eventos-litoral-paulista-2026-2027.html';
const html=fs.readFileSync(path.join(root,file),'utf8');
(async()=>{
 const browser=await chromium.launch({headless:true});
 for(const width of [390,1280]) {
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.route('**/*',async route=>{
   const u=new URL(route.request().url());
   if(u.hostname!=='local.test') return route.abort();
   const p=path.join(root,decodeURIComponent(u.pathname));
   if(!p.startsWith(root)||!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();
   await route.fulfill({path:p});
  });
  await page.goto('http://local.test/'+file);
  for(const t of ['html','head','body','main','article','h1','title'])assert.equal(await page.locator(t).count(),1,t);
  assert.equal(await page.locator('script[type="application/ld+json"]').count(),1);
  const d=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());assert.equal(d['@type'],'Article');assert.equal(d.datePublished,undefined);assert.equal(d.dateModified,'2026-11-17');
  const ids=await page.locator('[id]').evaluateAll(es=>es.map(e=>e.id));assert.equal(new Set(ids).size,ids.length);
  const body=await page.locator('body').innerText();
  for(const phrase of ['não é um calendário confirmado','não fornece atualização em tempo real','não comprova demanda','data a confirmar'])assert(body.includes(phrase),phrase);
  for(const phrase of ['Compre antes do evento','Receber calendário','valorização consistente','Temporada rentável'])assert(!body.includes(phrase),phrase);
  const links=await page.locator('a[href]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
  for(const link of links){if(link.startsWith('#'))assert(ids.includes(link.slice(1)));else if(link.startsWith('/')){let p=path.join(root,link);if(link.endsWith('/'))p=path.join(p,'index.html');assert(fs.existsSync(p),link);}}
  assert.equal(await page.locator('a[href="https://www.turismosantos.com.br/pt-br"]').count(),1);
  assert.equal(await page.locator('a[href="https://www.bertioga.sp.gov.br/"]').count(),1);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'horizontal overflow');
  await page.locator('.article-toc a[href="#status"]').click();assert(new URL(page.url()).hash==='#status');
  await page.locator('a[href="#conteudo"]').last().click();assert(new URL(page.url()).hash==='#conteudo');
  await page.goto('http://local.test/eventos-litoral-paulista-2026-2027/agenda-eventos-bertioga.html');
  const agendaLink=page.getByRole('link',{name:'Dezembro de 2026',exact:true});
  await agendaLink.press('Enter');
  assert.equal(new URL(page.url()).hash,'#dezembro-2026');
  const december=page.locator('#dezembro-2026');
  assert.equal(await december.getByRole('link',{name:'Comunicado da Prefeitura sobre O Cortiço',exact:true}).getAttribute('href'),'https://www.bertioga.sp.gov.br/turma-adulta-de-teatro-da-casa-da-cultura-apresenta-espetaculo-o-cortico-com-entrada-gratuita');
  assert.equal(await december.getByRole('link',{name:'Programação de Natal da Prefeitura de Bertioga',exact:true}).getAttribute('href'),'https://bertioga.sp.gov.br/bertioga-celebra-o-natal-com-ballet-circo-shows-e-grandes-eventos-de-4-a-23-de-dezembro');
  assert.equal(await december.locator('li').count(),3);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Bertioga December agenda horizontal overflow');
  for(const city of ['bertioga','guaruja']){
   const slug='eventos-litoral-paulista-2026-2027';
   await page.goto('http://local.test/'+slug+'/carnaval-'+city+'.html');
   assert.equal(await page.getByRole('heading',{level:1}).count(),1);
   await page.getByRole('link',{name:'Perguntas frequentes',exact:true}).press('Enter');
   assert.equal(new URL(page.url()).hash,'#perguntas');
   assert.equal(await page.locator('a[href^="mailto:comercial@praia.digital?"]').count(),1);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'horizontal overflow: '+city);
   const events=page.locator('a[href="/'+slug+'/agenda-eventos-'+city+'.html"]');
   await events.press('Enter');
   await page.waitForURL('http://local.test/'+slug+'/agenda-eventos-'+city+'.html');
   assert.match(await page.locator('h1').innerText(),/onde conferir a programação/);
  }
  await page.close();
 }
 await browser.close(); console.log('PASS: Events planning guide semantic structure, schema, internal paths/fragments, official sources, 390/1280px overflow and anchor navigation');
})().catch(e=>{console.error(e);process.exit(1)});
