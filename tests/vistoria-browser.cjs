const {checkAppLinkTargets} = require('./check-app-link-targets.cjs');
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.join(__dirname,'..');
(async()=>{
const browser=await chromium.launch({headless:true});
for(const width of [390,1280]){
const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.route('**/*',async route=>{const u=new URL(route.request().url());if(u.hostname!=='local.test')return route.abort();let p=path.join(root,u.pathname);if(u.pathname.endsWith('/'))p=path.join(p,'index.html');if(!fs.existsSync(p)||!fs.statSync(p).isFile())return route.abort();if(p.endsWith('shared.js')||p.endsWith('related-ads.js'))return route.fulfill({body:''});await route.fulfill({path:p});});
await page.goto('http://local.test/apps/checklist-vistoria/');
const handoff = page.locator('section[aria-labelledby="entrega-das-chaves"]');
assert.equal(await handoff.locator('#entrega-das-chaves').count(), 1);
assert.equal(await handoff.getByRole('heading', {name:'O que registrar na entrega das chaves', level:3}).count(), 1);
assert.equal(await handoff.locator('.pd-key-handoff li').count(), 4);
assert.equal(await handoff.locator('a[href="/apps/relatorio-imovel/#evidencias-da-visita"]').count(), 1);
assert.equal(await handoff.locator('.pd-key-handoff :is(input, textarea, button)').count(), 0);
// Every toggle has a unique accessible name that includes its observation.
const items=page.locator('#groups .item');
assert.equal(await items.count(),26);
for(const item of await items.all()){
  const label=await item.locator('span').innerText();
  for(const action of ['✓ OK','✗ Problema']){
    const toggle=page.getByRole('button',{name:action+' '+label,exact:true});
    assert.equal(await toggle.count(),1);
    const box=await toggle.boundingBox();
    assert(box.width>=44 && box.height>=44);
  }
}
// Resuming moves focus without marking the item, including after a reload.
const resume = page.getByRole('link', {name:'Ir ao primeiro item sem marcação'});
await resume.press('Enter');
assert.equal(await page.evaluate(() => document.activeElement.id), 'vistoria-0_0-ok');
assert.equal(await page.locator('#groups [aria-pressed="true"]').count(), 0);
await page.keyboard.press('Enter');
await page.reload();
await resume.press('Enter');
assert.equal(await page.evaluate(() => document.activeElement.id), 'vistoria-0_1-ok');
await page.locator('#vistoria-0_0-ok').press('Enter');
assert.equal(await resume.getAttribute('href'), '#vistoria-0_0-ok');
const allMarked = Object.fromEntries(await items.evaluateAll(rows => rows.map(row =>
  [row.querySelector('span').id.slice('item-'.length), 'bad'])));
await page.evaluate(state => localStorage.setItem('pd-vistoria-v1',JSON.stringify(state)),allMarked);
await page.reload();
assert.equal(await resume.count(), 0);
assert.match(await page.locator('#verdict').innerText(), /26 com problema e 0 sem marcação/);
page.once('dialog', dialog=>dialog.accept());
await page.locator('#reset').click();
assert.equal(await resume.getAttribute('href'), '#vistoria-0_0-ok');
// Print must keep the final group and identify states even in black and white.
const distance=page.locator('#vistoria-4_0-ok');
const parking=page.locator('#vistoria-4_3-bad');
await distance.press('Enter');
await parking.press('Space');
const problems = page.locator('#visit-problems-list');
const parkingLink = problems.getByRole('link', {name: 'Vagas de garagem conforme anúncio'});
assert.equal(await problems.getByRole('link').count(), 1);
const copy = page.getByRole('button', {name:'Copiar itens a conferir'});
await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{
  writeText: async text => { window.copiedCriteria = text; }
}}));
await copy.press('Enter');
const expected = 'Itens a conferir na vistoria\n• Vagas de garagem conforme anúncio';
await page.waitForFunction(() => document.getElementById('visit-copy-status').textContent.includes('copiados'));
assert.equal(await page.evaluate(() => window.copiedCriteria), expected);
await page.evaluate(() => Object.defineProperty(navigator, 'clipboard', {value:undefined}));
await copy.click();
const manual = page.locator('#visit-copy-text');
assert.equal(await manual.inputValue(), expected);
assert.equal(await manual.evaluate(el => el === document.activeElement && el.selectionEnd === el.value.length), true);
await parkingLink.press('Enter');
assert.equal(await parking.evaluate(el => el === document.activeElement), true);
assert.equal(await page.getByRole('button', {name: '✗ Problema Vagas de garagem conforme anúncio', exact: true}).count(), 1);
await page.reload();
assert.equal(await parkingLink.count(), 1);
await page.emulateMedia({media:'print'});
const printed=page.locator('#groups .item:visible');
assert.equal(await printed.count(),26);
assert.equal(await problems.isVisible(), false);
assert.equal(await resume.isVisible(), false);
assert.equal(await page.locator('#groups .card:visible').count(),5);
for (const [label,state] of [
  ['Distância real da praia conferida','OK'],
  ['Vagas de garagem conforme anúncio','Problema'],
  ['Comércio e serviços próximos','Sem marcação']
]) {
  const item=printed.filter({hasText:label});
  assert.equal(await item.evaluate(el=>getComputedStyle(el,'::after').content),JSON.stringify(state));
}
await page.emulateMedia({media:'screen'});
await distance.press('Enter');
await page.locator('#vistoria-4_3-ok').press('Enter');
assert.equal(await problems.getByRole('link').count(), 0);
assert.equal(await copy.count(), 0);
assert.equal(await manual.isVisible(), false);
assert.equal(await manual.inputValue(), '');
assert.equal(await page.locator('#visit-problems-empty').isVisible(), true);
await page.locator('#vistoria-4_3-ok').press('Enter');
const key='pd-vistoria-v1',first=()=>page.locator('#groups button').first();
// Keep keyboard focus on the same control after updates, including repeated toggles.
const focused=()=>page.evaluate(()=>document.activeElement?.outerHTML);
await first().focus();
await page.keyboard.press('Enter');
assert.equal(await first().evaluate(el=>el===document.activeElement),true,await focused());
assert.equal(await first().getAttribute('aria-pressed'),'true');
await page.keyboard.press('Space');
assert.equal(await first().evaluate(el=>el===document.activeElement),true);
assert.equal(await first().getAttribute('aria-pressed'),'false');
await page.keyboard.press('Tab');
const problem=page.locator('#groups button').nth(1);
assert.equal(await problem.evaluate(el=>el===document.activeElement),true);
await page.keyboard.press('Enter');
assert.equal(await problem.evaluate(el=>el===document.activeElement),true);
assert.equal(await problem.getAttribute('aria-pressed'),'true');
await page.keyboard.press('Enter');
assert.equal(await problem.getAttribute('aria-pressed'),'false');
await page.keyboard.press('Tab');
assert.equal(await page.locator('#groups button').nth(2).evaluate(el=>el===document.activeElement),true);
await page.locator('#reset').focus();
page.once('dialog',d=>d.dismiss());await page.keyboard.press('Enter');
assert.equal(await page.locator('#reset').evaluate(el=>el===document.activeElement),true);
page.once('dialog',d=>d.accept());await page.keyboard.press('Enter');
assert.equal(await page.locator('#reset').evaluate(el=>el===document.activeElement),true);

assert.equal(await page.locator('#score').textContent(),'0%');await first().click();assert((await page.locator('#storage-status').textContent()).includes('salvas'));await page.reload();assert.equal(await first().getAttribute('aria-pressed'),'true');await first().click();assert.equal(await first().getAttribute('aria-pressed'),'false');
for(const raw of ['{','null','{"0_0":"ok","bogus":"ok","0_1":"unknown"}']){
 await page.evaluate(({key,raw})=>localStorage.setItem(key,raw),{key,raw});await page.reload();assert((await page.locator('#storage-status').textContent()).includes('Modo sessão'));await first().click();assert.equal(await page.evaluate(key=>localStorage.getItem(key),key),raw);
 page.once('dialog',d=>d.dismiss());await page.locator('#reset').click();assert.equal(await page.evaluate(key=>localStorage.getItem(key),key),raw);
 page.once('dialog',d=>d.accept());await page.locator('#reset').click();assert.equal(await page.evaluate(key=>localStorage.getItem(key),key),null);assert.equal(await page.locator('#score').textContent(),'0%');
}
await first().click();const saved=await page.evaluate(key=>localStorage.getItem(key),key);
await page.evaluate(()=>{Storage.prototype.setItem=function(){throw new Error('quota');};});await page.locator('#groups button').nth(1).click();assert((await page.locator('#storage-status').textContent()).includes('não foi possível salvar'));assert.equal(await page.evaluate(key=>localStorage.getItem(key),key),saved);
await page.evaluate(()=>{Storage.prototype.removeItem=function(){throw new Error('denied');};});page.once('dialog',d=>d.accept());await page.locator('#reset').click();assert((await page.locator('#storage-status').textContent()).includes('Não foi possível remover'));assert.equal(await page.locator('#score').textContent(),'0%');
await page.reload();await page.evaluate(()=>localStorage.clear());await page.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}});});await page.reload();assert((await page.locator('#storage-status').textContent()).includes('não foi possível ler'));await first().click();assert((await page.locator('#verdict').textContent()).includes('1/26'));
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));assert.deepEqual(errors,[]);assert(!(await page.locator('#verdict').textContent()).includes('pode avançar'));
await checkAppLinkTargets(page, root);
await page.close();
}await browser.close();console.log('PASS checklist mobile/desktop, reload, corrupt/null/unknown, storage exceptions and reset cancel/confirm');
})().catch(e=>{console.error(e);process.exit(1)});
