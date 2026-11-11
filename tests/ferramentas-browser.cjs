// Offline browser QA: every request is intercepted. No real form, contact or payment submission.
const {chromium}=require('playwright');
const AxeBuilder=require('@axe-core/playwright').default;
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),out='/tmp/ferramentas-previews';
const routes=['/ferramentas/index.html','/apps/simulador-roi-temporada/'];
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
 try{
 for(const width of [320,390,768,1280]){
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block',reducedMotion:'reduce'}),sideEffects=[];
  await context.route('**/*',async route=>{
   const req=route.request(),url=new URL(req.url());
   if(!['GET','HEAD'].includes(req.method())){sideEffects.push(req.method()+' '+url.href);return route.abort();}
   if(url.origin!=='https://praia.digital')return route.abort();
   let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
   if(!file.startsWith(root+path.sep))return route.abort();
   if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
   if(!fs.existsSync(file))return route.fulfill({status:404,body:''});
   return route.fulfill({body:fs.readFileSync(file),contentType:({'.js':'application/javascript','.css':'text/css','.html':'text/html','.json':'application/json'})[path.extname(file)]||'application/octet-stream'});
  });
  for(const route of routes){
   const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.goto('https://praia.digital'+route,{waitUntil:'networkidle'});
   assert.equal(await page.locator('.pd-site-header').count(),1,'Build navigation before running');
   assert.equal(await page.locator('main').count(),1);assert.equal(await page.locator('h1').count(),1);
   const overflow=async()=>assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' horizontal overflow '+width);
   await overflow();
   await page.keyboard.press('Tab');
   assert.equal(await page.evaluate(()=>document.activeElement.classList.contains('skip-link')),true,'skip link must precede navigation');
   await page.keyboard.press('Enter');
   if(route.includes('/apps/')){
    assert.equal(await page.locator('#result').isVisible(),false);
    await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
    assert.match(await page.locator('#rLiq').innerText(),/18.795,63/);assert.match(await page.locator('#rRoiL').innerText(),/3,2%/);
    assert.equal(await page.locator('#roi-result-title').evaluate(e=>e===document.activeElement),true);
    await page.locator('#ocup').fill('150');assert.equal(await page.locator('#result').isVisible(),false);
    await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
    assert.equal(await page.locator('#result').isVisible(),false);assert.match(await page.locator('#ocup-error').innerText(),/100%/);
    assert.equal(await page.locator('#ocup').getAttribute('aria-invalid'),'true');
    await page.locator('#ocup').fill('55');await page.locator('#ocup').press('Enter');
    await page.locator('#cidade').selectOption('Bertioga');assert.equal(await page.locator('#result').isVisible(),false);
    assert.equal(await page.locator('#adr').inputValue(),'750');assert.equal(await page.locator('#ocup').inputValue(),'55');
    await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
    for(const [id,value]of [['noites','366'],['valor','0'],['custos','-1'],['plataforma','101'],['ir','101']]){
     const before=await page.locator('#'+id).inputValue();await page.locator('#'+id).fill(value);await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
     assert.equal(await page.locator('#result').isVisible(),false);assert.equal(await page.locator('#'+id).getAttribute('aria-invalid'),'true');await page.locator('#'+id).fill(before);
    }
    await page.locator('#ocup').fill('0');await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
    assert.match(await page.locator('#rPayback').innerText(),/Não recuperado/);
    const summary=page.locator('.roi-faq summary').first();await summary.focus();await page.keyboard.press('Enter');assert.equal(await summary.evaluate(e=>e.parentElement.open),true);await page.keyboard.press('Enter');
    await page.locator('#ocup').fill('55');await page.getByRole('button',{name:'Calcular rentabilidade',exact:true}).click();
    await page.locator('#result').screenshot({path:path.join(out,`roi-result-${width}.png`)});
   }else{
    assert.equal(await page.locator('.fh-card').count(),3);
    assert.ok(await page.locator('.fh-kit').evaluate(e=>!!(e.compareDocumentPosition(document.querySelector('footer'))&Node.DOCUMENT_POSITION_FOLLOWING)));
    await page.getByRole('link',{name:'Conhecer o Kit Temporada',exact:true}).waitFor();
    assert.match(await page.locator('.fh-kit').innerText(),/R\$ 39/);
    assert.match(await page.locator('.fh-kit').innerText(),/Assinatura recorrente/);
    await page.getByRole('link',{name:'Calcular ocupação',exact:true}).click();await page.waitForURL('**/calculadora-ocupacao-airbnb-2026.html');
    await page.goBack();await page.waitForLoadState('networkidle');assert.equal(await page.locator('.fh-card').count(),3);
   }
   await overflow();
   const a11y=await new AxeBuilder({page}).include('main').withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
   fs.writeFileSync(path.join(out,`${route.includes('/apps/')?'roi':'hub'}-axe-${width}.json`),JSON.stringify(a11y.violations,null,2));
   assert.deepEqual(a11y.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),[],route+' accessibility');
   await page.evaluate(()=>scrollTo(0,0));
   if(width<=1080){const toggle=page.locator('.pd-site-toggle');await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');await toggle.click();await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');}
   await page.screenshot({path:path.join(out,`${route.includes('/apps/')?'roi':'hub'}-${width}.png`),fullPage:true});
   await page.screenshot({path:path.join(out,`${route.includes('/apps/')?'roi':'hub'}-top-${width}.png`)});
   assert.deepEqual(errors,[]);await page.close();
  }
  assert.deepEqual(sideEffects,[]);await context.close();console.log(`PASS hub and ROI ${width}px: inputs, navigation, semantics, axe, no overflow and screenshots`);
 }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
