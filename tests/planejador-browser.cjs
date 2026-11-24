const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/planejador-entrada/');
const click=()=>page.locator('#calcular').click();
assert(await page.locator('#res').isHidden());assert.equal(await page.locator('#rend').inputValue(),'0');
const aporte = page.locator('#mensal');
const initialUrl = page.url();
await aporte.press('Enter');
assert.equal(await page.locator('#tempo').textContent(), '30 mês(es)');
await aporte.fill('5000');
assert(await page.locator('#res').isHidden());
await aporte.press('Enter');
assert.equal(await page.locator('#tempo').textContent(), '15 mês(es)');
await aporte.fill('');
await aporte.press('Enter');
assert(await page.locator('#erro').isVisible());
assert.equal(await aporte.evaluate(el => el === document.activeElement), true);
assert.equal(page.url(), initialUrl);
await aporte.fill('2500');
await click();
assert.equal(await page.locator('#tempo').textContent(), '30 mês(es)');
for(const id of ['valor','pct','guardado','mensal','rend']){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill('');assert(await page.locator('#res').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(old);await click();assert(await page.locator('#res').isVisible());}
await page.locator('#mensal').fill('-1');await click();assert(await page.locator('#erro').isVisible());await page.locator('#mensal').fill('0');await page.locator('#guardado').fill('90000');await click();assert((await page.locator('#tempo').textContent()).includes('0 meses'));
await page.locator('#guardado').fill('100');await page.locator('#valor').fill('121');await page.locator('#pct').fill('100');await page.locator('#rend').fill('10');await click();assert.equal(await page.locator('#tempo').textContent(),'2 mês(es)');
await page.locator('#valor').fill('1200');await page.locator('#guardado').fill('0');await page.locator('#mensal').fill('1');await page.locator('#rend').fill('0');await click();assert.equal(await page.locator('#tempo').textContent(),'1200 mês(es)');
await page.locator('#valor').fill('90000');await click();assert((await page.locator('#tempo').textContent()).includes('Não atingida'));assert((await page.locator('#saldo').textContent()).includes('1.200,00'));
await page.locator('#pct').fill('0');await click();await click();assert((await page.locator('#tempo').textContent()).includes('0 meses'));assert(!/NaN|Infinity/.test(await page.locator('#res').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
const body=await page.locator('body').innerText();for(const text of ['13,6%','13,75%','Preço típico','CDBs','baixo risco','Meta alcançável!'])assert(!body.includes(text));
const links=await page.locator('a[href^="/"]').evaluateAll(es=>es.map(e=>e.getAttribute('href').split('#')[0]));for(const l of links){let p=path.join(root,l);if(l.endsWith('/'))p=path.join(p,'index.html');assert(fs.existsSync(p),l);}
await page.close();
}await browser.close();console.log('PASS planner desktop/mobile, validation, zero contributions, exact/unreached horizon, repeated flows, stale results and links');
})().catch(e=>{console.error(e);process.exit(1)});
