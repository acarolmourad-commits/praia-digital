// Serves only repository files via interception. No live requests or email.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {execFileSync}=require('node:child_process');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..'),origin='https://praia.digital',route='/ia/marketplaces/piloto/';
const built=execFileSync('python3',['-c',`import importlib.util,pathlib
r=pathlib.Path(${JSON.stringify(root)})
s=importlib.util.spec_from_file_location('nav',r/'scripts/build-navigation.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
print(m.transform((r/'ia/marketplaces/piloto/index.html').read_text(),(r/'partials/header.html').read_text())[0])`],{encoding:'utf8'});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const width of [320,390,1280]){
   const ctx=await browser.newContext({viewport:{width,height:900}}),unexpected=[],errors=[];
   await ctx.route('**/*',r=>{
    const u=new URL(r.request().url());
    if(u.origin!==origin||r.request().method()!=='GET'){unexpected.push(r.request().url());return r.abort();}
    const file=path.join(root,decodeURIComponent(u.pathname));
    if(u.pathname===route)return r.fulfill({contentType:'text/html',body:built});
    if(!fs.existsSync(file)||!fs.statSync(file).isFile()){unexpected.push(u.pathname);return r.abort();}
    const type=/\.m?js$/.test(file)?'application/javascript':file.endsWith('.css')?'text/css':file.endsWith('.svg')?'image/svg+xml':'application/octet-stream';
    return r.fulfill({contentType:type,body:fs.readFileSync(file)});
   });
   const p=await ctx.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(origin+route);
   await p.locator('#run').waitFor();await p.waitForFunction(()=>!document.getElementById('run').disabled);
   assert.ok(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   await p.keyboard.press('Tab');assert.equal(await p.locator('.skip-link').evaluate(e=>e===document.activeElement),true);
   await p.locator('#run').click();assert.match(await p.locator('#check-count').innerText(),/10\/10/);
   assert.equal(await p.locator('#inventory tr').count(),3);
   await p.screenshot({path:`/tmp/marketplaces-pilot-${width}.png`,fullPage:true});
   await p.locator('#reset').click();await p.locator('#reserve-form button[type=submit]').click();
   assert.equal(await p.locator('#orders li').count(),1);
   await p.locator('#replay').click();assert.equal(await p.locator('#orders li').count(),1);assert.match(await p.locator('#feedback').innerText(),/já aplicado/);
   await p.locator('#quantity').fill('149');await p.locator('#reserve-form button[type=submit]').click();assert.match(await p.locator('#feedback').innerText(),/insuficiente/);
   await p.getByRole('button',{name:/Confirmar saída DEMO-PM1/}).click();assert.match(await p.locator('#orders').innerText(),/Expedido/);
   const download=p.waitForEvent('download');await p.locator('#download').click();
   const d=await download,report=JSON.parse(fs.readFileSync(await d.path(),'utf8'));assert.equal(report.productionValidated,false);assert.equal(report.reconciled,true);assert.equal(report.orders.length,1);
   await p.reload();assert.equal(await p.locator('#orders li').count(),0);
   assert.deepEqual(errors,[]);assert.deepEqual(unexpected,[]);await ctx.close();console.log(`PASS ${width}px: layout, keyboard, scenario, duplicate, rejection, shipment, report, reset`);
  }
  const ctx=await browser.newContext({javaScriptEnabled:false});await ctx.route('**/*',r=>r.request().url()===origin+route?r.fulfill({contentType:'text/html',body:built}):r.fulfill({body:''}));
  const p=await ctx.newPage();await p.goto(origin+route);assert.ok(await p.locator('noscript').isVisible());assert.ok(await p.locator('#run').isDisabled());await ctx.close();
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
