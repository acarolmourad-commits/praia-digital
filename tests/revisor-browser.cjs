const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
(async()=>{const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});try{
for(const width of [390,1280]){
 const context=await browser.newContext({viewport:{width,height:900}});
 await context.route('**/*',route=>{
  const url=new URL(route.request().url());
  if(url.origin!=='https://praia.digital')return route.abort();
  let file=path.resolve(root,'.'+url.pathname+(url.pathname.endsWith('/')?'index.html':''));
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file))return route.fulfill({status:404,body:'Missing'});
  return route.fulfill({body:fs.readFileSync(file),contentType:({'.html':'text/html','.js':'application/javascript','.css':'text/css'})[path.extname(file)]||'text/plain'});
 });
 const page=await context.newPage(); const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('https://praia.digital/apps/revisor-anuncios/');
 assert.equal(await page.locator('h1').count(),1);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 await page.getByRole('button',{name:'Carregar exemplo fictício'}).click();
 await page.getByRole('button',{name:'Comparar as versões'}).click();
 assert.equal(await page.locator('#different-count').textContent(),'3');
 assert.equal(await page.locator('#pending-count').textContent(),'2');
 assert.equal(await page.locator('#report').isVisible(),true);
 page.once('dialog',d=>d.dismiss());await page.locator('#clear').click();
 assert.equal(await page.locator('#ref-price').inputValue(),'600.000,00');assert.equal(await page.locator('#report').isVisible(),true);
 page.once('dialog',d=>d.dismiss());await page.locator('#example').click();assert.equal(await page.locator('#report').isVisible(),true);
 await page.locator('#ref-price').fill('700.000,00');assert.equal(await page.locator('#report').isVisible(),false);
 page.once('dialog',d=>d.dismiss());await page.locator('#example').click();assert.equal(await page.locator('#ref-price').inputValue(),'700.000,00');
 page.once('dialog',d=>d.accept());await page.locator('#example').click();assert.equal(await page.locator('#ref-price').inputValue(),'600.000,00');
 await page.getByRole('button',{name:'Comparar as versões'}).click();
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 fs.mkdirSync('/tmp/revisor-qa',{recursive:true});await page.screenshot({path:`/tmp/revisor-qa/revisor-${width}.png`,fullPage:true});
 page.once('dialog',d=>d.accept());await page.locator('#clear').click();assert.equal(await page.locator('#ref-price').inputValue(),'');assert.equal(await page.locator('#report').isVisible(),false);
 assert.deepEqual(errors,[]);await context.close();
}
console.log('Desktop/mobile, example, comparison, cancel/confirm clear and overwrite, invalidation and overflow passed.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
