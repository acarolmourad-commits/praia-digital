// Run: node tests/diaria-browser.cjs. Requests are intercepted; no personal data is sent.
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
(async () => {
 const browser = await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {})});
 try {
  for (const width of [320,390,768,1280]) {
   const page = await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});
   const errors=[]; page.on('pageerror', e=>errors.push(e.message));
   let sendCount=0, responseSuccess=true, release=null;
   await page.route('**/*', async route=>{
    const url=new URL(route.request().url());
    if(url.hostname==='formsubmit.co'){
      sendCount++;
      if(release) await release;
      return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({success:responseSuccess})});
    }
    if(!['pd.test','praia.digital'].includes(url.hostname)) return route.abort();
    const file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
    if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()) return route.fulfill({status:404,body:''});
    return route.fulfill({contentType:({'.html':'text/html','.js':'text/javascript','.css':'text/css'})[path.extname(file)]||'text/plain',body:fs.readFileSync(file)});
   });
   await page.goto('https://pd.test/ferramentas/calculadora-diaria-ideal-airbnb-2026.html');
   const visible= id=>page.locator('#'+id).isVisible();
   const calculate=()=>page.locator('#calcular').click();
   const overflow=()=>page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
   assert.equal(await visible('resultado'),false);
   assert.equal(await overflow(),false);
   fs.mkdirSync('/tmp/diaria-previews',{recursive:true});
   await page.screenshot({path:`/tmp/diaria-previews/top-${width}.png`});
   await page.locator('#estadia').focus();await page.keyboard.press('Enter');
   assert.match(await page.locator('#principal').innerText(),/378,77/);
   assert.match(await page.locator('#detalhes').innerText(),/159,59/);
   assert.equal(await page.locator('#resultado').evaluate(e=>e===document.activeElement),true);
   assert.equal(await visible('baixar-relatorio'),true);
   assert.equal(sendCount,0);
   assert.ok(await page.locator('#titulo-resultado').evaluate(e=>e.getBoundingClientRect().top>=document.querySelector('.pd-site-header').getBoundingClientRect().bottom),'Result heading must not be obscured by navigation');
   const a11y=await new AxeBuilder({page}).include('main').withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
   fs.writeFileSync(`/tmp/diaria-previews/axe-${width}.json`,JSON.stringify(a11y.violations,null,2));
   assert.deepEqual(a11y.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);
   await page.screenshot({path:`/tmp/diaria-previews/full-${width}.png`,fullPage:true});
   const downloaded=page.waitForEvent('download');await page.locator('#baixar-relatorio').click();
   const download=await downloaded;
   const report=fs.readFileSync(await download.path(),'utf8');
   assert.match(report,/378,77/);assert.match(report,/não representam mercado observado/);
   assert.doesNotMatch(report,/<li>Comparativo detalhado|<td>Mercado<\/td>/);
   await page.keyboard.press('Tab');
   assert.equal(await overflow(),false);
   fs.mkdirSync('/tmp/diaria-previews',{recursive:true});
   await page.locator('#resultado').screenshot({path:`/tmp/diaria-previews/result-${width}.png`});
   for (const [id,value] of [['custos','1600'],['limpeza','160'],['lucro','3100'],['ocupacao','46'],['estadia','3.5']]) {
    await page.locator('#'+id).fill(value);
    assert.equal(await visible('resultado'),false);assert.equal(await visible('baixar-relatorio'),false);
    assert.equal(await page.evaluate(()=>window.__sim),null);await calculate();
   }
   await page.locator('#cidade').selectOption('Guarujá');assert.equal(await visible('resultado'),false);await calculate();
   for(const [id,value] of [['ocupacao','0'],['ocupacao','150'],['ocupacao','-1'],['custos','-1'],['limpeza','-1'],['lucro','-1'],['estadia','0'],['estadia','366'],['custos','100000001'],['custos',''],['custos','NaN'],['custos','Infinity']]) {
    const old=await page.locator('#'+id).inputValue();
    await page.locator('#'+id).evaluate((e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));},value);
    await calculate();assert.equal(await visible('resultado'),false);assert.equal(await visible('erro-calculo'),true);
    assert.equal(await page.locator('#baixar-relatorio').getAttribute('href'),null);
    assert.equal(await page.locator('#'+id).evaluate(e=>e===document.activeElement),true);
    await page.locator('#'+id).fill(old);await calculate();
   }
   for(const id of ['custos','limpeza','lucro']) await page.locator('#'+id).fill('0');
   await page.locator('#ocupacao').fill('100');await page.locator('#estadia').fill('365');await calculate();
   assert.match(await page.locator('#principal').innerText(),/0,00/);
   await page.locator('#lead-email').fill('invalid');await page.locator('#enviar-simulacao').click();assert.equal(sendCount,0);
   await page.locator('#lead-email').fill('test@example.com');responseSuccess=false;
   await page.locator('#enviar-simulacao').click();await page.waitForFunction(()=>document.querySelector('#status-envio').textContent.includes('Não foi possível'));
   assert.equal(await visible('baixar-relatorio'),true);
   responseSuccess=true;
   await page.locator('#enviar-simulacao').click();await page.waitForFunction(()=>document.querySelector('#status-envio').textContent.includes('confirmou a aceitação'));
   let resolve;release=new Promise(r=>resolve=r);
   await page.locator('#enviar-simulacao').click();
   await page.locator('#custos').fill('1500');await calculate();resolve();
   await page.waitForFunction(()=>!document.querySelector('#enviar-simulacao').disabled);
   assert.equal(await visible('pos-envio'),false);
   assert.equal(await page.locator('#status-envio').innerText(),'');
   assert.equal(await overflow(),false);
   // Accelerate only the calculator timeout; network is still intercepted.
   await page.evaluate(()=>{
    const realTimeout=window.setTimeout;
    window.setTimeout=(fn,ms,...args)=>realTimeout(fn,ms===15000?100:ms,...args);
   });
   let finishTimeout;release=new Promise(r=>finishTimeout=r);
   const beforeTimeout=sendCount;
   await page.locator('#enviar-simulacao').click();
   await page.waitForFunction(()=>document.querySelector('#status-envio').textContent.includes('resultado do envio é incerto'));
   assert.equal(await page.locator('#enviar-simulacao').isDisabled(),false);
   assert.match(await page.locator('#status-envio').innerText(),/Não reenviamos automaticamente/);
   assert.equal(sendCount,beforeTimeout+1);
   assert.equal(await visible('baixar-relatorio'),true);
   finishTimeout();release=null;
   assert.deepEqual(errors,[]);
   await page.close(); console.log(`PASS diária ${width}px: calculation, validation, download, keyboard, edit invalidation, email and race`);
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
