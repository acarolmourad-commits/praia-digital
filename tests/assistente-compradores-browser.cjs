'use strict';
const { chromium } = require('playwright');
const fs = require('node:fs'), path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
(async()=>{const browser=await chromium.launch({headless:true});try {
for(const width of [320,390,768,1280]){
const context=await browser.newContext({viewport:{width,height:900}});
let outbound=[];
await context.route('**/*',route=>{
const u=new URL(route.request().url());if(u.origin!=='https://praia.digital'){outbound.push(u.origin);return route.abort();}
const f=path.resolve(root,'.'+u.pathname+(u.pathname.endsWith('/')?'index.html':''));
if(!f.startsWith(root+path.sep)||!fs.existsSync(f))return route.fulfill({status:404,body:'Missing'});
return route.fulfill({body:fs.readFileSync(f),contentType:({'.html':'text/html','.js':'application/javascript','.css':'text/css'})[path.extname(f)]||'application/octet-stream'});
});
const page=await context.newPage(), errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('https://praia.digital/ferramentas/assistente-virtual.html');
await page.locator('#buyer-city').fill('Bertioga, Indaiá');await page.locator('#buyer-budget').fill('2000000');await page.locator('#buyer-type').selectOption({label:'Casa'});
await page.getByRole('button',{name:'Preparar resumo',exact:true}).click();assert.match(await page.locator('#buyer-summary').inputValue(),/2\.000\.000/);
assert.ok(await page.locator('#buyer-preview').isVisible());
await page.locator('#msg').fill('Procuro casa em Bertioga para temporada');await page.locator('#buyer-ask').click();assert.equal(await page.locator('.msg.bot').count(),2);
await page.locator('#msg').fill('<img src=x onerror=alert(1)>');await page.locator('#buyer-ask').click();assert.equal(await page.locator('#chat img').count(),0);
assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow '+width);
assert.deepEqual(errors,[]);assert.ok(!outbound.some(x=>/wa.me|formsubmit/.test(x)),'No contact or newsletter sent');
const dest=process.env.ASSISTENTE_QA_OUTPUT||'/tmp/assistente-qa';fs.mkdirSync(dest,{recursive:true});await page.screenshot({path:path.join(dest,'assistente-'+width+'.png'),fullPage:true});
await page.locator('#buyer-clear').click();assert.equal(await page.locator('#chat').textContent(),'');assert.equal(await page.locator('#buyer-summary').inputValue(),'');
await context.close();}
console.log('Browser flows passed at 320, 390, 768 and 1280px. No external submissions.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
