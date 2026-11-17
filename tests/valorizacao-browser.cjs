const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/calculadora-valorizacao/');
const click=()=>page.locator('#calcular').click();
assert(await page.locator('#res').isHidden());await click();assert((await page.locator('#dica').textContent()).includes('mesmo valor'));
for(const id of ['valor','taxa','anos','cdi']){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill('');assert(await page.locator('#res').isHidden());await click();assert(await page.locator('#erro').isVisible());assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(old);await click();}
await page.locator('#cenario').selectOption('5');assert(await page.locator('#res').isHidden());assert.equal(await page.locator('#taxa').inputValue(),'5');await click();
await page.locator('#taxa').fill('-100');assert.equal(await page.locator('#cenario').inputValue(),'custom');await click();assert((await page.locator('#vfImo').textContent()).includes('0,00'));
for(const [id,value] of [['taxa','-200'],['cdi','-200'],['anos','1.5'],['valor','0'],['anos','51']]){const old=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await click();assert(await page.locator('#res').isHidden());assert(await page.locator('#erro').isVisible());await page.locator('#'+id).fill(old);await click();}
await page.locator('#cdi').fill('-100');await click();assert((await page.locator('#dica').textContent()).includes('mesmo valor'));
await page.locator('#cenario').selectOption('0');await page.locator('#cdi').fill('0');await click();await click();assert((await page.locator('#dica').textContent()).includes('mesmo valor'));assert(!/NaN|Infinity/.test(await page.locator('#res').innerText()));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);
const body=await page.locator('body').innerText();for(const text of ['15,2%','Médio litoral','13,5%','Faixa típica','Regra prática:','maior valorização 12m'])assert(!body.includes(text));
const links=await page.locator('a[href^="/"]').evaluateAll(es=>es.map(e=>e.getAttribute('href').split('#')[0]));for(const l of links){let p=path.join(root,l);if(l.endsWith('/'))p=path.join(p,'index.html');assert(fs.existsSync(p),l);}
await page.close();
}await browser.close();console.log('PASS valorizacao desktop/mobile, negative/zero rates, tie, presets, invalid/stale results and links');
})().catch(e=>{console.error(e);process.exit(1)});
