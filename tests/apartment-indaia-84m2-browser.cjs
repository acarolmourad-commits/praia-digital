// Offline visual and navigation checks. No messages, forms or external requests.
const {chromium} = require('playwright');
const fs = require('node:fs'), path = require('node:path'), assert = require('node:assert/strict');
const root = path.resolve(process.env.INDAIA_84_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = path.join(process.env.INDAIA_QA_OUTPUT || '/tmp/indaia-qa', '84m2');
const origin = 'https://praia.digital';
const detail = '/imoveis/apartamento-indaia-bertioga-84m2.html';
fs.mkdirSync(output, {recursive:true});
(async () => {
 const browser = await chromium.launch({headless:true, ...(process.env.CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.CHROMIUM_EXECUTABLE_PATH} : {})});
 for (const width of [390, 1440]) {
  const context = await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  const sideEffects = [], errors = [];
  await context.route('**/*', async route => {
   const req = route.request(), url = new URL(req.url());
   if (!['GET','HEAD'].includes(req.method()) || url.origin !== origin) {
    if (req.isNavigationRequest() || !['GET','HEAD'].includes(req.method())) sideEffects.push(req.url());
    return route.abort();
   }
   let file = path.resolve(root, '.'+decodeURIComponent(url.pathname));
   if (!file.startsWith(root+path.sep)) return route.fulfill({status:403,body:''});
   if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file,'index.html');
   if (!fs.existsSync(file)) return route.fulfill({status:404,body:''});
   const mime = {'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.jpeg':'image/jpeg','.svg':'image/svg+xml','.png':'image/png','.webp':'image/webp'};
   return route.fulfill({path:file,contentType:mime[path.extname(file)]});
  });
  const page = await context.newPage(); page.on('pageerror', e => errors.push(e.message));
  await page.goto(origin + '/imoveis.html', {waitUntil:'load'});
  const card = page.locator('.property-card').filter({has:page.locator(`a[href="${detail.slice(1)}"]`)});
  await card.waitFor(); assert.equal(await card.count(),1);
  assert.match(await card.innerText(),/960\.000/); assert.match(await card.innerText(),/84 m²/);
  assert.equal(await page.locator('.property-card a[href="imoveis/apartamento-indaia-88m2.html"]').count(),1);
  await card.locator('.btn-secondary').click(); await page.waitForURL(origin + detail);
  assert.equal(await page.locator('h1').count(),1); assert.match(await page.locator('h1').innerText(),/vista parcial/);
  assert.equal(await page.locator('.gallery figure').count(),10);
  await page.locator('a[href="#fotos"]').click(); assert.equal(new URL(page.url()).hash,'#fotos');
  for (const img of await page.locator('img').all()) {await img.scrollIntoViewIfNeeded(); await img.evaluate(el=>el.decode());}
  assert.equal(await page.locator('img').count(),11);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow at ${width}px`);
  const studyLink = page.getByRole('link', {name:'Ver estudo de Airbnb e valorização'});
  await studyLink.focus(); await page.keyboard.press('Enter');
  assert.equal(new URL(page.url()).hash,'#estudo-rentabilidade');
  const study = page.locator('#estudo-rentabilidade');
  assert(await study.isVisible());
  assert.match(await study.innerText(),/Esse piso não entrega 6% de retorno líquido/);
  assert.match(await study.innerText(),/142 noites/); assert.match(await study.innerText(),/101 noites/);
  assert.match(await study.innerText(),/R\$ 824\.384,66/); assert.match(await study.innerText(),/R\$ 1\.112\.903,11/);
  assert.equal(await study.locator('table caption').count(),3);
  assert.equal(await study.locator('form,input,iframe').count(),0);
  for (const region of await study.locator('[role="region"]').all()) {
   assert(await region.getAttribute('aria-label')); assert.equal(await region.getAttribute('tabindex'),'0');
   await region.focus(); assert(await region.evaluate(el=>el===document.activeElement));
   await page.keyboard.press('ArrowRight');
   assert.equal(await region.locator('th:not([scope])').count(),0);
  }
  for (const link of await study.locator('a[href^="https://"]').all()) {
   assert((await link.innerText()).trim().length>4);
   assert.equal(new URL(await link.getAttribute('href')).protocol,'https:');
  }
  await page.locator('a[href="#fonte-airbnb"]').click(); assert.equal(new URL(page.url()).hash,'#fonte-airbnb');
  await page.goBack(); assert.equal(new URL(page.url()).hash,'#estudo-rentabilidade');
  await studyLink.click(); assert.equal(new URL(page.url()).hash,'#estudo-rentabilidade');
  await study.screenshot({path:path.join(output,`${width}-study.png`)});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`study overflow at ${width}px`);
  for (const link of await page.locator('a[href^="https://wa.me/"]').all()) {
   const href = await link.getAttribute('href'); assert.match(href,/5511954346288/); assert(decodeURIComponent(href).includes('84 m²'));
  }
  const popupPromise = context.waitForEvent('page'); await page.locator('.gallery a').first().click();
  const popup = await popupPromise; await popup.waitForLoadState(); assert(popup.url().endsWith('/01-varanda-vista-parcial-mar.jpeg')); await popup.close();
  await page.screenshot({path:path.join(output,`${width}-full.png`),fullPage:true});
  await page.evaluate(()=>scrollTo(0,0)); await page.screenshot({path:path.join(output,`${width}-hero.png`)});
  await page.locator('a.back').click(); await page.waitForURL(origin+'/imoveis.html');
  assert.equal(await page.locator(`.property-card a[href="${detail.slice(1)}"]`).count(),1);
  await page.goBack(); await page.waitForURL(u=>u.pathname===detail); await page.goForward(); await page.waitForURL(origin+'/imoveis.html');
  assert.deepEqual(errors,[]); assert.deepEqual(sideEffects,[]);
  console.log(`${width}px: preserved cards/photos, study math, sources, keyboard, tables, anchors, history and overflow passed`);
  await context.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
