// Exercise the built directory and all cross-app menus without network side effects.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=process.env.HOMEPAGE_PREVIEW_ROOT||path.resolve(__dirname,'..');
const origin='https://praia.digital';
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox']});
try{for(const width of [360,768,1280]){
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  await context.route('**/*',async route=>{
    const req=route.request(),url=new URL(req.url());
    if(url.origin!==origin||req.method()!=='GET')return route.abort();
    let file=path.join(root,decodeURIComponent(url.pathname));
    if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
    if(!fs.existsSync(file))return route.fulfill({status:404,body:''});
    const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
    return route.fulfill({body:fs.readFileSync(file),contentType:mime[path.extname(file)]||'application/octet-stream'});
  });
  const page=await context.newPage();
  await page.goto(origin+'/apps/');
  assert.equal(await page.locator('.pd-site-header').count(),1);
  assert.equal(await page.locator('.pd-catalog-card').count(),16);
  await page.locator('.pd-catalog-cta').click();
  assert.equal(new URL(page.url()).hash,'#comprar');
  const links=await page.locator('.pd-catalog-card h3 a').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
  const overflow=async()=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Overflow ${page.url()} ${width}`);
  await overflow();
  await page.screenshot({path:`/tmp/praia-catalog-${width}.png`,fullPage:true});
  for(const link of links){
    await page.goto(origin+link);
    const menu=page.locator('.pd-network details');
    await menu.locator('summary').click();
    assert.equal(await menu.locator('li').count(),15,link);
    await overflow();
    await page.locator('.pd-network a[href="/apps/"]').click();
    assert.equal(new URL(page.url()).pathname,'/apps/');
  }
  await context.close();console.log(`Catalog and 16 return journeys passed at ${width}px`);
}}
finally{await browser.close();}})().catch(error=>{console.error(error);process.exit(1);});
