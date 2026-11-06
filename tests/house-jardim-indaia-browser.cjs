// Offline visual and navigation checks. No messages, forms or external requests.
const {chromium} = require('playwright');
const fs = require('node:fs'), path = require('node:path'), assert = require('node:assert/strict');
const root = path.resolve(process.env.HOUSE_INDAIA_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = path.join(process.env.INDAIA_QA_OUTPUT || '/tmp/indaia-qa', 'house-indaia');
const origin = 'https://praia.digital';
const detail = '/imoveis/casa-jardim-indaia-180m2.html';
fs.mkdirSync(output, {recursive:true});
(async () => {
 const browser = await chromium.launch({headless:true});
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
  const page = await context.newPage(); page.setDefaultTimeout(15000); page.setDefaultNavigationTimeout(30000); page.on('pageerror', e => errors.push(e.message));
  await page.goto(origin + '/imoveis.html', {waitUntil:'load'});
  const card = page.locator('.property-card').filter({has:page.locator(`a[href="${detail.slice(1)}"]`)});
  await card.waitFor(); assert.equal(await card.count(),1);
  assert(!/quartos|undefined|null|Bertioga/.test(await card.innerText()),'Unknown counts and exact location must stay omitted');
  await page.locator('#quartos-filtro').selectOption('2');
  assert.equal(await card.count(),0,'Unknown bedroom count must not match a bedroom filter');
  await page.locator('#quartos-filtro').selectOption('');
  assert.match(await card.innerText(),/400\.000/); assert.match(await card.innerText(),/109,91 m²/);
  assert.equal(await page.locator('.property-card a[href="imoveis/apartamento-indaia-88m2.html"]').count(),1);
  await card.locator('.btn-secondary').click(); await page.waitForURL(origin + detail);
  assert.equal(await page.locator('h1').count(),1); assert.match(await page.locator('h1').innerText(),/Jardim Indaiá/);
  assert.equal(await page.locator('.gallery figure').count(),11);
  await page.locator('a[href="#fotos"]').click(); assert.equal(new URL(page.url()).hash,'#fotos');
  for (const img of await page.locator('img').all()) {await img.scrollIntoViewIfNeeded(); await img.evaluate(el=>el.decode());}
  assert.equal(await page.locator('img').count(),12);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow at ${width}px`);
  for (const link of await page.locator('a[href^="https://wa.me/"]').all()) {
   const href = await link.getAttribute('href'); assert.match(href,/5511954346288/); assert(decodeURIComponent(href).includes('180 m²'));
  }
  const popupPromise = context.waitForEvent('page'); await page.locator('.gallery a').first().click();
  const popup = await popupPromise; await popup.waitForLoadState(); assert(popup.url().endsWith('/01-vista-da-casa.jpeg')); await popup.close();
  await page.screenshot({path:path.join(output,`${width}-full.png`),fullPage:true});
  await page.evaluate(()=>scrollTo(0,0)); await page.screenshot({path:path.join(output,`${width}-hero.png`)});
  await page.locator('a.back').click(); await page.waitForURL(origin+'/imoveis.html');
  assert.equal(await page.locator(`.property-card a[href="${detail.slice(1)}"]`).count(),1);
  await page.goBack(); await page.waitForURL(u=>u.pathname===detail); await page.goForward(); await page.waitForURL(origin+'/imoveis.html');
  assert.deepEqual(errors,[]); assert.deepEqual(sideEffects,[]);
  console.log(`${width}px: new and existing cards, page, 11 photos, popup, back/forward, CTA and overflow passed`);
  await context.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
