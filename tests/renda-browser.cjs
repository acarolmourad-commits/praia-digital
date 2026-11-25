const {checkAppLinkTargets} = require('./check-app-link-targets.cjs');
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/renda-para-financiar/');
const click=()=>page.locator('#calcular').click();
await click();assert(await page.locator('#res').isVisible());
await page.locator('#pct').fill('-1');assert(await page.locator('#res').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#pct').getAttribute('aria-invalid'),'true');
await page.locator('#pct').fill('30');await page.locator('#taxa').fill('0');await click();assert.equal(await page.locator('#sac1').textContent(),await page.locator('#price').textContent());
await page.locator('#entrada').fill('100');await click();assert((await page.locator('#dica').textContent()).includes('não há saldo'));assert((await page.locator('#price').textContent()).includes('0,00'));
await page.locator('#entrada').fill('20');await page.locator('#taxa').fill('12');await page.locator('#tipoTaxa').selectOption('efetiva');assert(await page.locator('#res').isHidden());await click();await click();assert(await page.locator('#res').isVisible());
for(const [id,value] of [['prazo','1.5'],['valor',''],['pct','0']]){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await click();assert(await page.locator('#erro').isVisible());assert(await page.locator('#res').isHidden());await page.locator('#'+id).fill(old);}
await click();assert(await page.locator('#res').isVisible());assert(!/NaN|Infinity/.test(await page.locator('#res').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
const body=await page.locator('body').innerText();for(const text of ['11,19','13,75','Na prática, sim','Renda mínima por faixa'])assert(!body.includes(text));
await checkAppLinkTargets(page, root);
await page.close();
}await browser.close();console.log('PASS renda desktop/mobile validation, repeated flow, zero rates, full entry, stale-results and internal links');
})().catch(e=>{console.error(e);process.exit(1)});
