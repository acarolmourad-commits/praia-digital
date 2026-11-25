const {checkAppLinkTargets} = require('./check-app-link-targets.cjs');
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/custo-de-compra/');
const click=()=>page.locator('#calcular').click();
const values={valor:'500000',itbi:'10000',escritura:'2500',registro:'2000',banco:'1500',outros:'500'};
assert(await page.locator('#res').isHidden());for(const id of Object.keys(values))assert.equal(await page.locator('#'+id).inputValue(),'');await click();assert(await page.locator('#erro').isVisible());
for(const [id,value] of Object.entries(values))await page.locator('#'+id).fill(value);await click();assert((await page.locator('#total').textContent()).includes('16.500,00'));
for(const id of Object.keys(values)){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill('');assert(await page.locator('#res').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(old);await click();}
for(const [id,value] of [['valor','0'],['itbi','-1'],['registro','1000000001']]){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await click();assert(await page.locator('#res').isHidden());assert(await page.locator('#erro').isVisible());await page.locator('#'+id).fill(old);await click();}
for(const id of Object.keys(values).filter(id=>id!=='valor'))await page.locator('#'+id).fill('0');await click();await click();assert((await page.locator('#total').textContent()).includes('0,00'));assert(!/NaN|Infinity/.test(await page.locator('#res').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
assert.equal(await page.locator('#cidade, #financ, #faq').count(),0);const body=await page.locator('body').innerText();for(const text of ['Alíquota típica','~R$3.000','prevalecendo o maior','sem surpresas'])assert(!body.includes(text));
await checkAppLinkTargets(page, root);
await page.close();
}await browser.close();console.log('PASS purchase budget mobile/desktop, blank/zero inputs, limits, error recovery and stale results');
})().catch(e=>{console.error(e);process.exit(1)});
