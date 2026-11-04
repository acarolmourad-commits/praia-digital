const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),out=process.env.INDAIA_QA_OUTPUT||'/tmp/indaia-qa';fs.mkdirSync(out,{recursive:true});
(async()=>{const browser=await chromium.launch({headless:true});
for(const width of [390,1440]){
 const ctx=await browser.newContext({viewport:{width,height:900}});const errors=[];
 await ctx.route('**/*',async route=>{const u=new URL(route.request().url());if(u.origin!=='https://praia.digital')return route.abort();const p=path.resolve(root,'.'+u.pathname);if(!p.startsWith(root+'/')||!fs.existsSync(p))return route.fulfill({status:404,body:''});return route.fulfill({path:p,contentType:p.endsWith('.html')?'text/html; charset=utf-8':p.endsWith('.js')?'application/javascript':p.endsWith('.jpeg')?'image/jpeg':undefined});});
 const page=await ctx.newPage();page.on('pageerror',e=>errors.push(e.message));
 await page.goto('https://praia.digital/imoveis/apartamento-indaia-88m2.html');
 assert.equal(await page.locator('h1').count(),1);
 assert.match(await page.locator('#rental-results').innerText(),/65.700/);assert.match(await page.locator('#rental-results').innerText(),/35.835/);
 await page.locator('#occupancy').fill('0');assert.match(await page.locator('#rental-results').innerText(),/13.440/);assert.match(await page.locator('#rental-results').innerText(),/Não há retorno/);
 await page.locator('#occupancy').fill('101');assert.ok((await page.locator('#rental-error').innerText()).length>0);assert.equal(await page.locator('#rental-results').innerText(),'');
 await page.locator('#occupancy').fill('30');await page.locator('#rental-form button').click();await page.locator('#rental-form button').click();assert.match(await page.locator('#rental-results').innerText(),/35.835/);
 await page.locator('#price').fill('1000000');assert.match(await page.locator('#value-results').innerText(),/1.159.274/);await page.locator('#price').fill('950000');
 await page.locator('#rate').fill('-3');assert.match(await page.locator('#value-results').innerText(),/815.797/);await page.locator('#rate').fill('3');
 for(const img of await page.locator('img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(el=>el.decode());}
 assert.equal(await page.locator('img').count(),29);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
 await page.locator('.faq summary').first().click();assert.equal(await page.locator('.faq details').first().getAttribute('open'),'');await page.locator('.faq summary').first().click();
 await page.screenshot({path:path.join(out,`${width}-full.png`),fullPage:true});await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,`${width}-hero.png`)});
 assert.deepEqual(errors,[]);await ctx.close();console.log(`${width}px: gallery, calculations, invalid inputs, repeated submit, FAQ, overflow passed`);
}await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
