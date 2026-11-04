// Offline browser QA against navigation-prepared HTML; no external network/submissions.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),built=process.env.CITY_PREVIEW_ROOT;
const data=require('../data/city-guides.json'),output=path.join(root,'.audit/city-guides/browser');
const origin='https://praia.digital',mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'};
(async()=>{
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.CITY_BROWSER_CHANNEL?{channel:process.env.CITY_BROWSER_CHANNEL}:{})});const results=[];
 try{
 for(const width of [375,1280]){
  const ctx=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  const failed=[];
  await ctx.route('**/*',async route=>{
   const req=route.request(),u=new URL(req.url());assert.equal(req.method(),'GET');
   if(u.origin!==origin)return route.abort();
   let rel=decodeURIComponent(u.pathname);if(rel.endsWith('/'))rel+='index.html';
   let f=path.join(root,rel);if(built&&fs.existsSync(path.join(built,rel)))f=path.join(built,rel);
   if(!fs.existsSync(f)){failed.push(rel);return route.fulfill({status:404,body:'Not found'});}
   return route.fulfill({status:200,contentType:mime[path.extname(f)]||'application/octet-stream',body:fs.readFileSync(f)});
  });
  const page=await ctx.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const c of data.cities){
   await page.goto(origin+`/cidades/${c.slug}.html`);await page.locator('h1').waitFor();
   assert.equal(await page.locator('h1').count(),1);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),c.slug+' overflow');
   await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.textContent.trim()),'Ir para o conteúdo');
   await Promise.all([
    page.waitForURL(url=>url.hash==='#conteudo'),
    page.keyboard.press('Enter')
   ]);
   assert.equal(new URL(page.url()).hash,'#conteudo');
   await page.locator('summary').first().click();assert(await page.locator('details').first().getAttribute('open')!==null);
   if(['bertioga','cubatao','iguape','ilha-comprida'].includes(c.slug)){
    await page.evaluate(()=>scrollTo(0,0));
    await page.screenshot({path:path.join(output,`${c.slug}-${width}.png`),fullPage:true});
   }
   await page.getByRole('link',{name:`Ver imóveis em ${c.name}`,exact:true}).first().click();
   await page.locator('#search-status').waitFor();
   assert.equal(await page.locator('#cidade-filtro').inputValue(),c.name);
   const meta=await page.locator('.property-card .property-meta').allTextContents();
   const cards=await page.locator('.property-card').count();
   for(let i=0;i<cards;i++)assert((await page.locator('.property-card').nth(i).locator('.property-meta').first().textContent()).startsWith(c.name));
   if(['cananeia','cubatao','iguape','ilha-comprida'].includes(c.slug)){assert.equal(cards,0);assert((await page.locator('.imoveis-empty').textContent()).includes('Nenhum imóvel'));}
   if(c.slug==='bertioga'){
    assert.equal(cards,5);
    assert.equal(await page.locator('a[href*="apartamento-alto-padrao-bertioga"]').count(),0);
    await page.locator('#tipo-filtro').selectOption('Aluguel');
    assert.equal(await page.locator('.property-card').count(),0);
    assert(await page.locator('.imoveis-empty').isVisible());
    await page.locator('#tipo-filtro').selectOption('Venda');
    assert.equal(await page.locator('.property-card').count(),5);
   }
   results.push({city:c.name,width,cards,passed:true});
  }
  await page.goto(origin+'/cidades/');assert.equal(await page.locator('.city-card').count(),16);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await page.screenshot({path:path.join(output,`index-${width}.png`),fullPage:true});
  assert.deepEqual(errors,[]);assert.deepEqual(failed,[]);await ctx.close();
 }
 const ctx=await browser.newContext({javaScriptEnabled:false,viewport:{width:375,height:900}});
 await ctx.route('**/*',route=>{
  const u=new URL(route.request().url());if(u.origin!==origin)return route.abort();let rel=u.pathname;if(rel.endsWith('/'))rel+='index.html';
  const f=built&&fs.existsSync(path.join(built,rel))?path.join(built,rel):path.join(root,rel);
  return route.fulfill({contentType:mime[path.extname(f)]||'text/plain',body:fs.readFileSync(f)});
 });
 const page=await ctx.newPage();await page.goto(origin+'/cidades/');assert.equal(await page.locator('.city-card').count(),16);
 await page.goto(origin+'/cidades/bertioga.html');assert.equal(await page.locator('h1').count(),1);assert(await page.locator('#fontes').isVisible());await ctx.close();
 fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({results,noJavaScript:true},null,2));console.log(`${results.length} city/viewport flows and no-JavaScript guides passed.`);
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
