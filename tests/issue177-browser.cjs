// Offline UI tests for issue #177. Every request is served locally or intercepted.
// The lead endpoint is simulated; no message is sent and no live reservation is made.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const output=process.env.ISSUE177_QA_OUTPUT || '/tmp/issue177-qa';
const origin='https://praia.digital';
const detail=origin+'/casa-condominio-fechado-bertioga.html';
const mime={'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml'};
fs.mkdirSync(output,{recursive:true});
(async()=>{
  const browser=await chromium.launch({headless:true});
  const results=[];
  try {
    for(const width of [390,1440]) {
      const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
      const posts=[];const qrRequests=[];const errors=[];let accepted=false;
      await context.route('**/*',async route=>{
        const request=route.request();const url=new URL(request.url());
        if(url.href==='https://academy.praia.digital/leads' && request.method()==='POST') {
          posts.push(request.postDataJSON());
          return route.fulfill({status:accepted?200:503,contentType:'application/json',body:JSON.stringify({ok:accepted})});
        }
        if(url.hostname==='api.qrserver.com'){qrRequests.push(url);return route.abort();}
        if(request.method()!=='GET' || url.origin!==origin)return route.abort();
        let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
        if(!file.startsWith(root+path.sep))return route.abort();
        if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
        if(!fs.existsSync(file)||!fs.statSync(file).isFile())return route.fulfill({status:404,body:''});
        return route.fulfill({contentType:mime[path.extname(file)]||'application/octet-stream',body:fs.readFileSync(file)});
      });
      const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
      await page.goto(origin+'/imoveis.html');
      await page.locator('#busca').fill('comprar casa em Bertioga com 2 quartos até R$ 600 mil sala de jogos');
      await page.waitForFunction(()=>document.querySelectorAll('#lista-imoveis .property-card').length===1);
      const card=page.locator('#lista-imoveis .property-card');
      const wa=new URL(await card.locator('.btn-whatsapp').getAttribute('href'));
      assert(wa.searchParams.get('text').includes(detail));assert(wa.searchParams.get('text').includes('R$ 595.000'));
      await card.screenshot({path:path.join(output,`search-${width}.png`)});
      await page.locator('#busca').fill('comprar casa em Bertioga com 2 suítes até R$ 600 mil');
      await page.waitForFunction(()=>document.getElementById('search-status').textContent.includes('suítes não verificada'));
      assert.equal(await page.locator('#lista-imoveis .property-card').count(),0);
      await page.reload();assert.match(await page.locator('#search-status').innerText(),/suítes não verificada/);
      await page.locator('#limpar-busca').click();assert((await page.locator('#lista-imoveis .property-card').count())>0);
      await page.goto(origin+'/encontrar-imovel.html');
      assert.equal(await page.getByRole('link',{name:'🔍 Abrir busca com filtros',exact:true}).getAttribute('href'),'/imoveis.html');
      await page.locator('#destaque-bertioga').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(output,`guide-${width}.png`)});
      await page.goto(origin+'/home-classica.html');
      await page.locator('#qrListingId').fill('25');
      await page.getByRole('button',{name:'🎯 Gerar QR Code',exact:true}).click();
      await page.waitForFunction(()=>document.getElementById('qrStatus').textContent.includes('Não foi possível carregar'));
      assert.equal(await page.locator('#qrResultUrl').getAttribute('href'),detail);
      assert.equal(qrRequests.at(-1).searchParams.get('data'),detail);
      await page.locator('#qrListingId').fill('999');
      await page.getByRole('button',{name:'🎯 Gerar QR Code',exact:true}).click();
      assert.equal(await page.locator('#qrResultUrl').getAttribute('href'),null);
      await page.locator('#qrListingId').fill('25');
      await page.getByRole('button',{name:'🎯 Gerar QR Code',exact:true}).click();
      await page.locator('.qr-card').filter({has:page.locator('#qrListingId')}).screenshot({path:path.join(output,`qr-fallback-${width}.png`)});
      await page.locator('#qrResultUrl').click();assert.equal(page.url(),detail);
      assert.match(await page.locator('h1').innerText(),/Casa com 2 quartos/);
      const hero=page.locator('.bertioga-listing .hero');
      assert.match(await hero.innerText(),/2 banheiros · 1 vaga/);
      await hero.screenshot({path:path.join(output,`house-${width}.png`)});
      const direct=new URL(await hero.locator('.btn-whatsapp').getAttribute('href'));
      assert(direct.searchParams.get('text').includes(detail));
      await page.getByLabel('Nome*',{exact:true}).fill('Teste local offline');
      await page.getByLabel('WhatsApp com DDD*',{exact:true}).fill('11900000000');
      await page.getByRole('button',{name:'Enviar meu interesse',exact:true}).click();
      await page.waitForFunction(()=>!document.getElementById('interestFallback').hidden);
      assert.match(await page.locator('#formStatus').innerText(),/Não foi possível confirmar/);
      const fallback=new URL(await page.locator('#interestFallback').getAttribute('href'));
      assert(fallback.searchParams.get('text').includes(detail));
      assert.equal(posts[0].property_url,detail);assert.equal(posts[0].property_price,'R$ 595.000');
      await page.locator('#leadForm').locator('..').screenshot({path:path.join(output,`contact-failure-${width}.png`)});
      accepted=true;await page.getByRole('button',{name:'Enviar meu interesse',exact:true}).click();
      await page.waitForFunction(()=>document.getElementById('formStatus').textContent.includes('aceitou'));
      assert.equal(await page.locator('#interestFallback').isVisible(),false);
      assert.equal(posts.length,2);
      // Only changed interactive regions are measured; the large legacy page has unrelated content.
      for(const selector of ['#leadForm','.bertioga-listing .hero']){
        const box=await page.locator(selector).boundingBox();assert(box.x>=-1&&box.x+box.width<=width+1,`overflow ${selector} at ${width}`);
      }
      results.push({width,status:'passed',mockLeadRequests:posts.length,qrDestination:qrRequests.at(-1).searchParams.get('data'),pageErrors:errors});
      await context.close();
    }
    fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2));
    console.log(JSON.stringify(results,null,2));
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
