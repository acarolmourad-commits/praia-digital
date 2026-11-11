// Offline QA: every request is intercepted. Forms, payments and WhatsApp are never submitted.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const root = path.resolve(process.env.SERVICES_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = path.join(process.env.RUNNER_TEMP || '/tmp', 'service-promotion-qa');
const pages = ['/servicos.html', '/servicos/propaganda-imobiliaria.html', '/servico-fotografia-edicao.html'];
const payment = 'https://buy.stripe.com/bJe28sd4c0XdfxZ19e4ZR1Y';
function luminance(rgb) {
  const c = rgb.map(v => {v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;});
  return c[0]*0.2126 + c[1]*0.7152 + c[2]*0.0722;
}
function contrast(a,b) {const x=luminance(a),y=luminance(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);}
(async () => {
  fs.mkdirSync(output,{recursive:true});
  const browser = await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {})});
  try {
    for (const width of [320,390,768,1280]) {
      const context = await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
      const sideEffects=[];
      await context.route('**/*', async route => {
        const request=route.request(), url=new URL(request.url());
        if (!['GET','HEAD'].includes(request.method())) {sideEffects.push(request.method()+' '+url.pathname);return route.abort();}
        if(url.origin !== 'https://praia.digital') return route.abort();
        let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
        if(!file.startsWith(root+path.sep))return route.abort();
        if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
        if(!fs.existsSync(file))return route.fulfill({status:404,body:'Not found'});
        return route.fulfill({body:fs.readFileSync(file),contentType:file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':'text/html'});
      });
      for(const url of pages) {
        const page=await context.newPage();
        await page.goto('https://praia.digital'+url,{waitUntil:'load'});
        assert.equal(await page.locator('.pd-site-header').count(),1,'navigation build required');
        assert.equal(await page.locator('h1').count(),1);
        assert.equal(await page.locator('main').count(),1);
        const overflow=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth,offenders:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&r.right>innerWidth+1&&r.left>=0}).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,60)})).slice(0,8)}));
        assert.ok(overflow.width<=width+1,url+' '+JSON.stringify(overflow));
        if(url==='/servicos.html') {
          await page.getByLabel('Seu nome',{exact:true}).waitFor();
          await page.getByLabel('Seu e-mail',{exact:true}).waitFor();
          const hero=await page.locator('.hero .lead').evaluate(e=>({color:getComputedStyle(e).color,opacity:getComputedStyle(e).opacity}));
          assert.equal(hero.color,'rgb(255, 255, 255)');assert.equal(hero.opacity,'1');
          assert.ok(contrast([255,255,255],[7,89,133])>=4.5);
          assert.ok(contrast([255,255,255],[10,61,46])>=4.5);
          assert.ok(contrast([3,105,161],[255,255,255])>=4.5);
          const faq=page.locator('.faq details').nth(3), summary=faq.locator('summary');
          await summary.focus();await page.keyboard.press('Enter');assert.equal(await faq.evaluate(e=>e.open),true);
          await page.keyboard.press('Enter');assert.equal(await faq.evaluate(e=>e.open),false);
          assert.equal(await page.locator('.affiliate-block').evaluate(e=>e.open),false);
          assert.equal(await page.locator('a[href="'+payment+'"]').count(),1);
          await page.getByLabel('Seu e-mail',{exact:true}).scrollIntoViewIfNeeded();
          await page.screenshot({path:path.join(output,`hub-newsletter-${width}.png`)});
          await page.evaluate(()=>scrollTo(0,0));
          if(width<=1080){const toggle=page.locator('.pd-site-toggle');await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');await toggle.click();await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');}
        }
        if(url.includes('propaganda')) {
          assert.equal(await page.locator('a[href="'+payment+'"]').count(),1);
          await page.getByLabel('Seu nome (obrigatório)',{exact:true}).waitFor();
          assert.ok((await page.locator('body').innerText()).includes('Ziontechgroup'));
        }
        if(url.includes('fotografia')) {
          assert.equal(await page.locator('nav.navbar').count(),0);
          await page.locator('a[href="#contato"]').click();
          await page.getByLabel('Nome completo',{exact:true}).waitFor();
          assert.equal(await page.locator('#formStatus').getAttribute('role'),'status');
          await page.evaluate(()=>scrollTo(0,0));
        }
        await page.screenshot({path:path.join(output,`${path.basename(url,'.html')}-${width}.png`),fullPage:true});
        await page.close();
      }
      assert.deepEqual(sideEffects,[]);
      await context.close();
    }
    console.log('Services hub: 3 pages at 320/390/768/1280; no overflow; labels, FAQ keyboard, mobile menu, contrast, payment URLs and zero submissions passed.');
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
