const {chromium}=require('playwright');
const fs=require('fs'), path=require('path'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium'});
 let checks=0;
 try {
 for(const file of ['contato.html','imoveis.html']) for(const width of [390,1280]){
  const page=await browser.newPage({viewport:{width,height:900}});
  let mode='ok',calls=0,body;
  await page.route('**/*',async route=>{
   const u=new URL(route.request().url());
   if(u.hostname==='formsubmit.co'){
    calls++;body=route.request().postDataJSON();
    if(mode==='network')return route.abort();
    if(mode==='slow')await new Promise(r=>setTimeout(r,200));
    return route.fulfill({status:mode==='500'?500:200,contentType:'application/json',body:mode==='bad'?'oops':JSON.stringify({success: mode==='false'?'false':mode==='missing'?undefined:mode==='string'?'true':true})});
   }
   const f=path.join(root,decodeURIComponent(u.pathname));
   if(u.hostname==='praia.digital'&&fs.existsSync(f)&&fs.statSync(f).isFile())return route.fulfill({path:f});
   return route.abort();
  });
  async function init(){await page.goto('https://praia.digital/'+file+'?private=do-not-capture');await page.locator('[data-pd-lead] button').waitFor();}
  async function fill(){await page.locator('#nome').fill('Teste Fictício');await page.locator('#email').fill('teste@example.com');await page.locator('#interesse').selectOption('comprar');await page.locator('[name=consentimento]').check();}
  await init();await page.locator('[data-pd-lead] button').click();assert.equal(calls,0);checks++;
  await fill();await page.locator('[name=consentimento]').uncheck();await page.locator('[data-pd-lead] button').click();assert.equal(calls,0);checks++;
  for(mode of ['false','missing','bad','500','network']){
   await fill();await page.locator('[data-pd-lead] button').click();await page.waitForFunction(()=>document.querySelector('[data-lead-status]').textContent.includes('Não conseguimos'));
   assert.equal(await page.locator('#nome').inputValue(),'Teste Fictício');assert.equal(await page.locator('[data-pd-lead] button').isDisabled(),false);checks++;
  }
  mode='slow';let before=calls;await fill();await page.locator('[data-pd-lead]').evaluate(f=>{f.requestSubmit();f.requestSubmit();});
  await page.waitForFunction(()=>document.querySelector('[data-lead-status]').textContent.includes('aceita'));
  assert.equal(calls,before+1);assert.equal(body.origem,'/'+file);assert.ok(!JSON.stringify(body).includes('do-not-capture'));assert.equal(await page.locator('[data-pd-lead] button').isDisabled(),true);checks+=3;
  await init();mode='string';await fill();await page.locator('[data-pd-lead] button').click();await page.waitForFunction(()=>document.querySelector('[data-lead-status]').textContent.includes('aceita'));checks++;
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);checks++;
  await page.close();
 }
 console.log(checks+' assertions passed, all delivery requests mocked; no external submissions.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
