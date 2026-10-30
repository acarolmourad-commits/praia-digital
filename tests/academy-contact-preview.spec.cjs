const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict'),crypto=require('node:crypto');
(async()=>{
 const root=process.cwd(),out=path.join(process.env.RUNNER_TEMP||os.tmpdir(),'academy-contact-qa');fs.mkdirSync(out,{recursive:true});
 const publicPath='education/kits-2026.html',html=fs.readFileSync(path.join(root,publicPath),'utf8');
 for(const token of ['drive.google.com','buy.stripe.com','artifact-manifest','private_output_dir','workspace/shared','course-learning-plans','ready_for_sale'])assert.ok(!html.includes(token),'Disallowed private/payment marker: '+token);
 assert.ok(!/<form\b/i.test(html),'No payment/data collection form');
 for(const p of ['education/index.html','education/cursos/index.html'])assert.ok(fs.readFileSync(path.join(root,p),'utf8').includes('/education/kits-2026.html'),'Entry link missing');
 const browser=await chromium.launch({headless:true});
 try{
 for(const width of [390,1280]){
  const page=await browser.newPage({viewport:{width,height:900}}),errors=[],unexpected=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/*',async route=>{
   const u=new URL(route.request().url());
   if(u.origin!=='https://academy-preview.test'){unexpected.push(u.origin);return route.abort();}
   const rel=decodeURIComponent(u.pathname).replace(/^\//,''),file=path.resolve(root,rel);
   if(!file.startsWith(root+path.sep)||!fs.existsSync(file))return route.fulfill({status:404,body:'Missing local fixture'});
   await route.fulfill({status:200,contentType:file.endsWith('.css')?'text/css':'text/html',body:fs.readFileSync(file)});
  });
  await page.goto('https://academy-preview.test/'+publicPath);
  assert.equal(await page.locator('[data-kit]').count(),62);
  assert.equal(await page.locator('a[href*="stripe"]').count(),0);
  assert.ok((await page.locator('body').innerText()).includes('não instantâneas'));
  assert.ok((await page.locator('body').innerText()).includes('antes do pagamento'));
  await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('href'),'#main');
  await page.screenshot({path:path.join(out,'catalog-'+width+'.png'),fullPage:false});
  for(const a of await page.locator('[data-kit] a').all()){
   const href=await a.getAttribute('href');assert.ok(href.startsWith('mailto:comercial@praia.digital?'));
   const url=new URL(href);assert.ok(url.searchParams.get('subject').startsWith('Solicitar compra'));
   assert.ok(url.searchParams.get('body').includes('Antes do pagamento'));
  }
  await page.locator('#kit-search').fill('PriceLabs');assert.equal(await page.locator('[data-kit]:visible').count(),1);
  assert.equal(await page.locator('#kit-count').innerText(),'1 kit encontrado');
  await page.locator('[data-kit]:visible').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'selected-'+width+'.png'),fullPage:false});
  await page.locator('#kit-search').fill('zzznothing');assert.equal(await page.locator('[data-kit]:visible').count(),0);assert.ok(await page.locator('#empty').isVisible());
  await page.locator('#kit-search').fill('');assert.equal(await page.locator('[data-kit]:visible').count(),62);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(unexpected,[]);
  await page.close();
 }
 }finally{await browser.close();}
 fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({state:'passed',page:publicPath,sha256:crypto.createHash('sha256').update(html).digest('hex'),viewports:[390,1280],count:62,scope:'Contact only; no mail sent, payment, or private content'},null,2));
 console.log('PASS62 contact-only offers,390/1280,search/empty/recovery,keyboard,contextual mailto,no overflow/no checkout');
})().catch(e=>{console.error(e);process.exit(1)});
