// Run: NODE_PATH=<playwright node_modules> node tests/city-comparator-browser.cjs
const assert=require('node:assert/strict');
const http=require('node:http');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const server=http.createServer((req,res)=>{
 let rel=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(rel.endsWith('/'))rel+='index.html';
 const target=path.resolve(root,'.'+rel);
 if(!target.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 fs.readFile(target,(error,body)=>{if(error){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.html':'text/html','.css':'text/css','.js':'text/javascript'})[path.extname(target)]||'application/octet-stream');res.end(body);});
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.CHROMIUM_EXECUTABLE_PATH}:{})});
 try{
  for(const width of [320,375,768,1280]){
   const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',error=>errors.push(error.message));
   await page.goto(origin+'/apps/comparador-cidades/');
   assert.equal(await page.locator('#tbody tr').count(),12);
   assert(await page.getByText('Referências históricas, ainda não revalidadas',{exact:true}).isVisible());
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),`Document overflow at ${width}`);
   for(const [name,first] of [['🏖️ Renda de temporada','São Sebastião'],['🏠 Morar bem','São Vicente'],['💰 Investidor','Bertioga']]){
    await page.getByRole('button',{name,exact:true}).click();
    assert.equal(await page.locator('#tbody tr').first().locator('th').textContent(),first);
    assert.equal(await page.locator('.prof[aria-pressed="true"]').count(),1);
    assert((await page.getByRole('status').textContent()).includes('1 sem score'));
    assert((await page.locator('#tbody tr').last().textContent()).includes('Sem score'));
   }
   await page.getByRole('button',{name:'🏠 Morar bem',exact:true}).focus();await page.keyboard.press('Enter');
   assert.equal(await page.locator('.prof[aria-pressed="true"]').textContent(),'🏠 Morar bem');
   assert(await page.getByRole('button',{name:'🏠 Morar bem',exact:true}).evaluate(el=>el===document.activeElement));
   if(width<=375){
    for(const [index,region] of (await page.locator('.table-scroll').all()).entries()){
     assert(await region.evaluate(el=>el.scrollWidth>el.clientWidth));
     await region.focus();await page.keyboard.press('ArrowRight');
     await page.waitForFunction(i=>document.querySelectorAll('.table-scroll')[i].scrollLeft>0,index);
     assert(await region.evaluate(el=>el.scrollLeft>0),'Keyboard horizontal scrolling');
    }
   }
   const out=process.env.COMPARATOR_SCREENSHOTS;if(out){fs.mkdirSync(out,{recursive:true});await page.screenshot({path:path.join(out,`comparador-${width}.png`),fullPage:true});}
   assert.deepEqual(errors,[]);await page.close();
  }
  const nojs=await browser.newPage({javaScriptEnabled:false});await nojs.goto(origin+'/apps/comparador-cidades/');
  assert.equal(await nojs.locator('.reference-table tr').count(),13);assert(await nojs.locator('noscript').isVisible());await nojs.close();
  console.log('PASS: desktop/tablet/mobile 1280/768/375/320px, all profiles, keyboard/focus, overflow containment, 12 cities, missing-data state, no-JS fallback, no page errors.');
 }finally{await browser.close();server.close();}
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
