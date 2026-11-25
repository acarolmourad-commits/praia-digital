const {checkAppLinkTargets} = require('./check-app-link-targets.cjs');
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/calculadora-consorcio/');
const click=()=>page.locator('#calcular').click();
assert(await page.locator('#result').isHidden());await click();assert(await page.locator('#result').isVisible());
for(const id of ['credito','prazo','taxa','taxaFin']){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill('');assert(await page.locator('#result').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(old);await click();assert(await page.locator('#result').isVisible());}
await page.locator('#lance').fill('');assert(await page.locator('#result').isHidden());await click();assert.equal(await page.locator('#rLance').textContent(),'R$ 0');
await page.locator('#credito').fill('120000');await page.locator('#prazo').fill('120');await page.locator('#taxa').fill('20');await page.locator('#taxaFin').fill('0');await click();assert.equal(await page.locator('#rTotF').textContent(),'R$ 120.000');assert((await page.locator('#rSave').textContent()).includes('-24.000'));
await page.locator('#taxaFin').fill('0.000000000001');await click();assert.equal(await page.locator('#rParcF').textContent(),'R$ 1.000');
for(const [id,value] of [['prazo','1.5'],['lance','101'],['credito','0'],['taxa','-1'],['taxaFin','101']]){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await click();assert(await page.locator('#result').isHidden());assert(await page.locator('#erro').isVisible());await page.locator('#'+id).fill(old);await click();}
await click();assert(await page.locator('#result').isVisible());assert(!/NaN|Infinity/.test(await page.locator('#result').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
await checkAppLinkTargets(page, root);
await page.close();
}await browser.close();console.log('PASS consorcio desktop/mobile validation, zero/tiny rates, optional bid, stale results and internal links');
})().catch(e=>{console.error(e);process.exit(1)});
