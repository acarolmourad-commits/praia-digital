const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
const file='blog/rentabilidade-imoveis-praia-2026.html';
const html=fs.readFileSync(path.join(root,file),'utf8');
// Synthetic arithmetic fixtures only; not market returns or published forecasts.
assert.equal((120-20)/1000,0.1);
assert.equal((100+1200-1000-100)/(1000+100),200/1100);
assert(Math.abs(((1+0.08)/(1+0.04)-1)-0.03846153846153855)<1e-12);
assert(html.includes('(F + S − K − A) ÷ (K + A)'));
assert(html.includes('(1 + r) ÷ (1 + i) − 1'));
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
  const d=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());assert.equal(d['@type'],'BlogPosting');assert.equal(d.datePublished,undefined);assert.equal(d.dateModified,'2026-11-17');
  const ids=await page.locator('[id]').evaluateAll(es=>es.map(e=>e.id));assert.equal(new Set(ids).size,ids.length);
  const body=await page.locator('body').innerText();assert(!body.includes('completo em breve'));assert(!body.includes('Case De Sucesso'));assert(body.includes('não apresenta médias'));assert(body.includes('não é taxa anual'));assert(body.includes('não os calcula'));assert(body.includes('K + A deve ser positivo'));
  const links=await page.locator('a[href]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
  for(const link of links){if(link.startsWith('#'))assert(ids.includes(link.slice(1)));else if(link.startsWith('/')){let p=path.join(root,link);if(link.endsWith('/'))p=path.join(p,'index.html');assert(fs.existsSync(p),link);}}
  assert.equal(await page.locator('a[href^="https://www.gov.br/receitafederal/"]').count(),1);assert.equal(await page.locator('a[href^="https://www.bcb.gov.br/"]').count(),2);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'horizontal overflow');
  await page.locator('.article-toc a[href="#preco"]').click();assert(new URL(page.url()).hash==='#preco');
  await page.locator('a[href="#conteudo"]').last().click();assert(new URL(page.url()).hash==='#conteudo');
  await page.close();
 }
 await browser.close(); console.log('PASS: Return guide semantic structure, schema, internal paths/fragments, official sources, 390/1280px overflow and anchor navigation');
})().catch(e=>{console.error(e);process.exit(1)});
