// Local-file routing only; no live forms, provider requests or publication.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname,'..');
async function route(page, failSearch=false) {
  await page.route('**/*', async request => {
    const url = new URL(request.request().url());
    if (url.hostname !== 'praia.test') return request.abort();
    if (failSearch && url.pathname === '/data/content-search.json') return request.fulfill({status:503,body:'Unavailable'});
    let file = path.resolve(root,'.'+decodeURIComponent(url.pathname));
    if (!file.startsWith(root+path.sep) && file!==root) return request.abort();
    if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file=path.join(file,'index.html');
    if (!fs.existsSync(file)) return request.fulfill({status:404,body:'Missing'});
    const type={'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json'}[path.extname(file)] || 'application/octet-stream';
    await request.fulfill({status:200,body:fs.readFileSync(file),contentType:type});
  });
}
(async()=>{
 const browser=await chromium.launch({headless:true});
 try {
  for (const width of [375,768,1280]) {
   const page=await browser.newPage({viewport:{width,height:900}}); await route(page);
   const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto('https://praia.test/sitemap.html');
   assert(await page.locator('.pd-site-search').isVisible(),'search is reachable with the menu closed');
   assert.equal(await page.locator('#directory .directory-list a').count(),100);
   await page.locator('#content-query').fill('sao sebastiao');
   await page.locator('#content-search button[type=submit]').click();
   await page.waitForFunction(()=>document.getElementById('results-list').children.length>0);
   assert((await page.locator('#results-list').innerText()).toLowerCase().includes('são sebastião'));
   assert.equal(new URL(page.url()).searchParams.get('q'),'sao sebastiao');
   await page.locator('#content-category').selectOption({label:'Cidades e bairros'});
   await page.waitForFunction(()=>!document.getElementById('search-status').textContent.includes('Carregando'));
   for(const label of await page.locator('#results-list span').allTextContents()) assert.equal(label,'Cidades e bairros');
   await page.locator('#content-query').fill('zzzinexistente987');
   await page.locator('#content-search button[type=submit]').click();
   await page.waitForFunction(()=>document.getElementById('search-status').textContent.includes('Nenhum resultado'));
   await page.locator('#content-clear').click();
   await page.waitForFunction(()=>document.getElementById('results-list').children.length===30);
   await page.locator('#load-more').click();assert.equal(await page.locator('#results-list li').count(),60);
   assert(await page.locator('#results-list li').nth(30).locator('a').evaluate(el=>el===document.activeElement));
   await page.goBack();await page.waitForFunction(()=>document.getElementById('search-status').textContent.includes('Nenhum resultado'));
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal overflow');
   await page.goto('https://praia.test/guias/auditoria-fotos-descricao-temporada.html');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'guide stays within viewport');
   assert.equal(await page.locator('h1').count(),1);assert.deepEqual(errors,[]);
   console.log(`Search, history, pagination, guide and navigation: ${width}px passed`);await page.close();
  }
  const offline=await browser.newPage({javaScriptEnabled:false});await route(offline);
  await offline.goto('https://praia.test/sitemap.html');assert.equal(await offline.locator('#directory .directory-list a').count(),100);
  await offline.getByRole('link',{name:'Próxima página →'}).click();assert(offline.url().endsWith('/explorar/pagina-2.html'));
  assert.equal(await offline.locator('#directory .directory-list a').count(),100);await offline.close();
  const failure=await browser.newPage();await route(failure,true);
  await failure.goto('https://praia.test/sitemap.html?q=bertioga');
  await failure.waitForFunction(()=>document.getElementById('search-status').textContent.includes('Não foi possível'));
  assert.equal(await failure.locator('#directory .directory-list a').count(),100);await failure.close();
  console.log('No-JavaScript navigation and failed-fetch fallback passed');
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
