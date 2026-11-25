const {checkAppLinkTargets} = require('./check-app-link-targets.cjs');
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/temporada-ou-anual/');
const click=()=>page.locator('#calcular').click();
assert(await page.locator('#res').isHidden());await click();assert((await page.locator('#la').textContent()).includes('2.400,00'));
for(const id of ['valor','diaria','noites','taxa','custos','anual','custosAnual']){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill('');assert(await page.locator('#res').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(old);await click();}
for(const [id,value] of [['valor','0'],['noites','32'],['noites','1.5'],['taxa','101'],['custosAnual','-1']]){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await click();assert(await page.locator('#res').isHidden());assert(await page.locator('#erro').isVisible());await page.locator('#'+id).fill(old);await click();}
await page.locator('#noites').fill('0');await page.locator('#anual').fill('0');await click();assert((await page.locator('#lt').textContent()).includes('-'));assert((await page.locator('#la').textContent()).includes('-'));
await page.locator('#custos').fill('400');await click();assert((await page.locator('#dica').textContent()).includes('iguais'));
await page.locator('#custos').fill('0');await page.locator('#custosAnual').fill('0');await click();await click();assert((await page.locator('#dica').textContent()).includes('iguais'));assert(!/NaN|Infinity/.test(await page.locator('#res').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
const body=await page.locator('body').innerText();for(const text of ['1,8–2,5','ocupação real de plataformas','40%+','Yield anual'])assert(!body.includes(text));
await checkAppLinkTargets(page, root);
await page.close();
}await browser.close();console.log('PASS rental comparison desktop/mobile, expenses both sides, zero/negative/tie balances, invalid/stale results and links');
})().catch(e=>{console.error(e);process.exit(1)});
