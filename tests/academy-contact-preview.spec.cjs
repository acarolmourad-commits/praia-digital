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
   await route.fulfill({status:200,contentType:file.endsWith('.css')?'text/css':file.endsWith('.js')?'text/javascript':'text/html',body:fs.readFileSync(file)});
  });
  await page.goto('https://academy-preview.test/'+publicPath);
  assert.equal(await page.locator('[data-kit]').count(),62);
  assert.equal(await page.locator('[data-bundle]').count(),8);
  assert.equal(await page.locator('.copy-order').count(),70);
  // Every copied request must preserve the original mailto, including accents,
  // line breaks and its unique material reference. No message is sent here.
  await page.evaluate(async () => {
   window.copiedRequests=[];
   Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.copiedRequests.push(text)}});
   for(const button of document.querySelectorAll('.copy-order')){
    button.click();
    await Promise.resolve();
   }
  });
  const copied=await page.evaluate(()=>window.copiedRequests);
  const expected=await page.locator('[data-kit] a.cta,[data-bundle] a.cta').evaluateAll(links=>links.map(a=>{
   const u=new URL(a.href);return `Para: comercial@praia.digital\nAssunto: ${u.searchParams.get('subject')}\n\n${u.searchParams.get('body')}`;
  }));
  assert.deepEqual(copied,expected);
  assert.equal(await page.locator('.order-status:visible').count(),70);
  assert.ok((await page.locator('.order-status').first().innerText()).includes('O pedido ainda não foi enviado'));
  // Cover both unavailable API and rejected permission, then retry successfully.
  await page.evaluate(width=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:width===390?undefined:{writeText:async()=>{throw new Error('Permission denied');}}}),width);
  const copyButton=page.locator('.copy-order').first();
  await copyButton.focus();await page.keyboard.press('Enter');
  const fallback=page.locator('.order-copy-text').first();await fallback.waitFor({state:'visible'});
  assert.equal(await fallback.inputValue(),expected[0]);
  assert.equal(await fallback.getAttribute('readonly'),'');
  assert.ok(await fallback.evaluate(el=>document.activeElement===el&&el.selectionStart===0&&el.selectionEnd===el.value.length));
  assert.ok((await page.locator('.order-status').first().innerText()).includes('A cópia automática não está disponível'));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  await page.screenshot({path:path.join(out,'copy-fallback-'+width+'.png'),fullPage:false});
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{}}}));
  await copyButton.click();await fallback.waitFor({state:'hidden'});
  // Reset focus to exercise the page's original skip link from the start.
  await page.reload();
  assert.equal(await page.locator('a[href*="stripe"]').count(),0);
  assert.ok((await page.locator('body').innerText()).includes('não instantâneas'));
  assert.ok((await page.locator('body').innerText()).includes('antes do pagamento'));
  await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').getAttribute('href'),'#main');
  await page.screenshot({path:path.join(out,'catalog-'+width+'.png'),fullPage:false});
  const references = new Set();
  for(const a of await page.locator('[data-kit] a,[data-bundle] a').all()){
   const href=await a.getAttribute('href');assert.ok(href.startsWith('mailto:comercial@praia.digital?'));
   const url=new URL(href);assert.ok(url.searchParams.get('subject').startsWith('Solicitar compra'));
   assert.ok(!href.includes('+'), 'Spaces in mailto headers must use percent encoding');
   const body = url.searchParams.get('body');
   assert.ok(body.includes('Antes do pagamento'));
   const match = body.match(/Referência do material: ([a-z0-9-]+)\./);
   assert.ok(match, 'Missing offer reference');
   const sku = match[1];
   assert.ok(!references.has(sku), 'Duplicate offer reference');
   references.add(sku);
  }
  await page.locator('#kit-search').fill('PriceLabs');assert.equal(await page.locator('[data-kit]:visible').count(),1);
  assert.equal(await page.locator('#kit-count').innerText(),'Resultados: 1 kit e 0 trilhas.');
  await page.locator('[data-kit]:visible').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(out,'selected-'+width+'.png'),fullPage:false});
  await page.locator('#kit-search').fill('zzznothing');assert.equal(await page.locator('[data-kit]:visible').count(),0);assert.equal(await page.locator('[data-bundle]:visible').count(),0);assert.ok(await page.locator('#empty').isVisible());
  await page.locator('#catalog-clear').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('[data-kit]:visible').count(),62);assert.equal(await page.locator('[data-bundle]:visible').count(),8);
  assert.equal(await page.locator(':focus').getAttribute('id'),'kit-search');
  assert.equal(await page.locator('#kit-count').innerText(),'Resultados: 62 kits e 8 trilhas.');
  assert.ok(await page.locator('#catalog-clear').isHidden());
  await page.locator('#kit-search').fill('marketing');
  assert.ok(await page.locator('[data-kit]:visible').count()>0);assert.ok(await page.locator('[data-bundle]:visible').count()>0);
  await page.locator('#kit-search').fill('documentação');
  const accented=await page.locator('[data-kit]:visible h2,[data-bundle]:visible h3').allTextContents();assert.ok(accented.length>0);
  await page.locator('#kit-search').fill('  DOCUMENTACAO  ');
  assert.deepEqual(await page.locator('[data-kit]:visible h2,[data-bundle]:visible h3').allTextContents(),accented);
  // A multi-word query matches only when all its words occur in the offer.
  await page.locator('#kit-search').fill('trilha   avaliação');
  assert.equal(await page.locator('[data-kit]:visible').count(),0);assert.equal(await page.locator('[data-bundle]:visible').count(),1);
  assert.ok(await page.locator('#empty').isHidden());
  // Operational copy-status text must not become searchable editorial content.
  await page.locator('[data-bundle]:visible .copy-order').click();
  await page.locator('#kit-search').fill('Pedido ainda não foi enviado');
  assert.equal(await page.locator('[data-kit]:visible,[data-bundle]:visible').count(),0);
  await page.locator('#catalog-clear').click();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  const bundle=page.locator('[data-bundle]').first();
  assert.ok((await bundle.innerText()).includes('mesmos kits vendidos individualmente'));
  const details=bundle.locator('details');await details.locator('summary').click();assert.ok(await details.evaluate(el=>el.open));
  assert.equal(await details.locator('ul li').count(),3);assert.equal(await details.locator('ol li').count(),3);
  await bundle.scrollIntoViewIfNeeded();await page.screenshot({path:path.join(out,'bundle-'+width+'.png'),fullPage:false});
  await bundle.screenshot({path:path.join(out,'bundle-complete-'+width+'.png')});
  await details.locator('summary').click();assert.ok(!(await details.evaluate(el=>el.open)));
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  assert.deepEqual(errors,[]);assert.deepEqual(unexpected,[]);
  await page.close();
 }
 }finally{await browser.close();}
 fs.writeFileSync(path.join(out,'result.json'),JSON.stringify({state:'passed',page:publicPath,sha256:crypto.createHash('sha256').update(html).digest('hex'),viewports:[390,1280],count:62,bundles:8,scope:'Contact only; no mail sent, payment, or private content'},null,2));
 console.log('PASS70 contact-only offers,390/1280,copy exact requests,clipboard denied/unavailable/retry,search,keyboard,no overflow/no checkout');
})().catch(e=>{console.error(e);process.exit(1)});
