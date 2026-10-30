// Offline public Academy browsing; no external request, purchase, message or enrollment.
const {chromium}=require('playwright');
const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');
const output=path.join(process.env.RUNNER_TEMP||'/tmp','academy-qa');fs.mkdirSync(output,{recursive:true});
const root=path.resolve(__dirname,'..');const catalog=require('../education/assets/catalog.json');
(async()=>{const browser=await chromium.launch({headless:true});try{
 for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',async route=>{
   const req=route.request(),url=new URL(req.url());assert.equal(req.method(),'GET');
   if(url.origin!=='https://praia.digital')return route.abort();
   const file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
   if(!file.startsWith(root+path.sep)||!fs.existsSync(file))return route.fulfill({status:404,body:'Missing'});
   const types={'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json'};
   return route.fulfill({body:fs.readFileSync(file),contentType:types[path.extname(file)]||'text/plain'});
  });
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const paths=['/education/index.html','/education/cursos/index.html','/education/formacoes/index.html',...catalog.map(x=>x.path)];
  for(const p of paths){await page.goto('https://praia.digital'+p);assert.equal(await page.locator('h1').count(),1,p);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${width}:${p}`);assert.ok((await page.title()).length<160);}
  for(const course of catalog.filter(c=>c.kind==='Curso curto digital')){
   await page.goto('https://praia.digital/docs/academy/delivery/'+course.slug+'.html');
   assert.equal(await page.getByRole('heading',{name:'Procedimento demonstrado',exact:true}).count(),1);
   assert.equal(await page.getByRole('heading',{name:'Quando o plano falha',exact:true}).count(),1);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`delivery:${width}:${course.slug}`);
  }
  await page.goto('https://praia.digital/education/cursos/index.html');await page.screenshot({path:path.join(output,`catalog-${width}.png`),fullPage:false});await page.getByLabel('Buscar por assunto').fill('pricelabs');assert.ok(await page.locator('[data-course]:visible').count()>=1);await page.getByLabel('Buscar por assunto').fill('imoveis');assert.ok(await page.locator('[data-course]:visible').count()>1);await page.getByLabel('Buscar por assunto').fill('zzzz-no-such-course');assert.equal(await page.locator('[data-course]:visible').count(),0);await page.getByLabel('Buscar por assunto').fill('');assert.ok(await page.locator('[data-course]:visible').count()>50);
  await page.goto('https://praia.digital/education/cursos/airbnb-do-zero/index.html');await page.screenshot({path:path.join(output,`course-${width}.png`),fullPage:true});await page.getByRole('link',{name:'Ler amostra gratuita'}).click();assert.ok(page.url().endsWith('amostra.html'));await page.goBack();assert.ok(page.url().endsWith('index.html'));await page.getByRole('link',{name:'Solicitar matrícula',exact:true}).click();await page.locator('#selected-course').waitFor({state:'visible'});await page.screenshot({path:path.join(output,`checkout-${width}.png`),fullPage:true});assert.ok((await page.locator('#course-title').textContent()).includes('Airbnb'));await page.goBack();assert.ok(page.url().includes('airbnb-do-zero/index.html'));assert.deepEqual(errors,[]);await context.close();
 }
 console.log('Academy desktop/mobile all catalog pages, search, sample and enrollment navigation passed');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
