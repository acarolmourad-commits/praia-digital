// Offline: route all site requests to disk, block external requests and submissions.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(process.env.GUIDE_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = path.resolve(process.env.GUIDE_QA_OUTPUT || path.join(root, '.audit/guide-qa'));
const origin = 'https://praia.digital';
const hub = '/bairros/index.html';
const reviewed = JSON.parse(fs.readFileSync(path.join(root,'data/neighborhood-editorial-review.json'),'utf8')).pages;
const articles = ['/blog/riviera-sao-lourenco-seguranca-infraestrutura-valorizacao-2026.html', '/blog/estudo-rental-yield-apartamentos-1-2-dormitorios-praia-grande-2026.html'];
const mime = {'.html':'text/html; charset=utf-8','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp'};
async function context(browser,width,javaScriptEnabled=true) {
  const ctx=await browser.newContext({viewport:{width,height:900},javaScriptEnabled,serviceWorkers:'block'});
  await ctx.route('**/*',async route=>{
    const req=route.request(),url=new URL(req.url());
    assert(['GET','HEAD'].includes(req.method()),'No submissions');
    if(url.origin!==origin) return route.abort();
    let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
    if(!file.startsWith(root+path.sep)) return route.fulfill({status:403,body:'Forbidden'});
    const preview=process.env.GUIDE_BUILT_ROOT && path.resolve(process.env.GUIDE_BUILT_ROOT,'.'+decodeURIComponent(url.pathname));
    if(preview && fs.existsSync(preview) && fs.statSync(preview).isFile()) file=preview;
    if(!fs.existsSync(file)||!fs.statSync(file).isFile()) return route.fulfill({status:404,body:'Not found'});
    return route.fulfill({status:200,contentType:mime[path.extname(file)]||'application/octet-stream',body:fs.readFileSync(file)});
  });
  return ctx;
}
async function textContrast(page,selector) {
  const values=await page.locator(selector).evaluateAll(nodes=>nodes.map(el=>{
    const style=getComputedStyle(el);let parent=el,bg=style.backgroundColor;
    while(bg==='rgba(0, 0, 0, 0)' && parent.parentElement){parent=parent.parentElement;bg=getComputedStyle(parent).backgroundColor;}
    return {color:style.color,background:bg,opacity:style.opacity};
  }));
  assert(values.length,'Missing contrast target: '+selector);
  function luminance(css){const rgb=css.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4;});return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;}
  for(const value of values){const a=luminance(value.color),b=luminance(value.background);assert((Math.max(a,b)+.05)/(Math.min(a,b)+.05)>=4.5,JSON.stringify({selector,...value}));assert.equal(value.opacity,'1');}
}
async function overflow(page) {
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`overflow at ${page.url()}`);
}
(async()=>{
  fs.mkdirSync(output,{recursive:true});
  const browser=await chromium.launch({headless:true,...(process.env.GUIDE_BROWSER_CHANNEL?{channel:process.env.GUIDE_BROWSER_CHANNEL}:{})});
  const results=[];
  try {
    for(const width of [375,390,1280]) {
      const ctx=await context(browser,width),page=await ctx.newPage();
      const errors=[];page.on('pageerror',e=>errors.push(e.message));
      await page.goto(origin+hub);await page.locator('#guide-tools').waitFor({state:'visible'});
      assert.equal(await page.locator('.neighborhood-links a').count(),123);
      assert.equal(await page.locator('.city-card').count(),12);
      assert.equal(await page.locator('.related-entry').count(),2);
      await overflow(page);
      await page.screenshot({path:path.join(output,`hub-${width}.png`),fullPage:true});
      const search=page.locator('#guide-search');
      for(const term of ['São Sebastião','sao sebastiao']) {
        await search.fill(term);assert.equal(await page.locator('.city-card:visible').count(),1);
        assert.equal(await page.locator('#sao-sebastiao').isVisible(),true);
      }
      await search.fill('riviera');assert.equal(await page.locator('.neighborhood-links li:visible').count(),1);assert.equal(await page.locator('.related-entry:visible').count(),1);
      await search.fill('aluguel');assert.equal(await page.locator('.related-entry:visible').count(),1);assert.equal(await page.locator('.neighborhood-links li:visible').count(),0);
      await page.locator('#guide-city').selectOption('bertioga');assert(await page.locator('#guide-empty').isVisible());
      await page.locator('#guide-clear').click();assert.equal(await page.locator('.city-card:visible').count(),12);assert(await search.evaluate(el=>el===document.activeElement));
      await page.locator('#guide-collapse').click();assert.equal(await page.locator('.city-card details[open]').count(),0);
      await page.locator('#guide-expand').click();assert.equal(await page.locator('.city-card details[open]').count(),12);
      const summary=page.locator('.city-card summary').first();await summary.focus();await page.keyboard.press('Enter');assert.equal(await page.locator('.city-card details[open]').count(),11);
      await page.keyboard.press('Enter');assert.equal(await page.locator('.city-card details[open]').count(),12);
      await search.fill('zzzznonexistent');assert(await page.locator('#guide-empty').isVisible());await overflow(page);
      await page.locator('.city-nav a[href="#bertioga"]').click();assert(await page.locator('#bertioga').isVisible());
      await page.locator('#bertioga .related-entry a').click();assert.equal(new URL(page.url()).pathname,articles[0]);
      for(let i=0;i<articles.length;i++) {
        await page.goto(origin+articles[i]);await page.locator('.reading').waitFor();
        assert.equal(await page.locator('h1').count(),1);await overflow(page);
        await page.screenshot({path:path.join(output,`article-${i}-${width}.png`),fullPage:true});
        for(const link of await page.locator('main a[href^="#"]').all()) { const id=await link.getAttribute('href');assert.equal(await page.locator(id).count(),1); }
        await page.locator('.breadcrumbs a').nth(1).click();assert.equal(new URL(page.url()).pathname,hub);
        assert(await page.locator(i===0?'#bertioga':'#praia-grande').isVisible());
      }
      for (const item of reviewed) {
        await page.goto(origin+'/'+item.path);await page.locator('main[data-editorial-review]').waitFor();
        assert.equal(await page.locator('main h1').count(),1);await overflow(page);
        await textContrast(page,'main .lead');await textContrast(page,'main .cta');
        assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),item.canonical);
        const ranks=await page.locator('main h1,main h2,main h3,main h4,main h5,main h6').evaluateAll(nodes=>nodes.map(n=>Number(n.tagName.slice(1))));
        for(let i=1;i<ranks.length;i++) assert(ranks[i]<=ranks[i-1]+1,'Heading rank');
        for(const id of ['name','email','phone']) {
          assert.equal(await page.locator('label[for="'+id+'"]').count(),1);
          await page.locator('#'+id).focus();assert(await page.locator('#'+id).evaluate(el=>el===document.activeElement));
        }
        assert(await page.locator('#formStatus[role="status"]').count());
        assert.equal(await page.locator('main a[href^="https://semil.sp.gov.br/dh/travessias"]').count(),0);
        const schemas=await page.locator('script[type="application/ld+json"]').allTextContents();
        assert(!schemas.some(s=>s.includes('RealEstateListing')));
        await page.screenshot({path:path.join(output,item.path.replaceAll('/','-')+'-'+width+'.png'),fullPage:true});
      }
      await page.goto(origin+'/bairros/praia-grande/index.html');
      await page.locator('#booking-heading').waitFor();await overflow(page);
      await textContrast(page,'#booking-affiliate-root h2, #booking-affiliate-root p, #booking-affiliate-root a');
      await textContrast(page,'main .affiliate-disclosure');await textContrast(page,'main .cta');
      assert.equal(await page.locator('main .grid.grid-3').count(),3);
      assert.equal(await page.locator('main #booking-affiliate-root').count(),1);
      for(const id of ['name','phone']){assert.equal(await page.locator('label[for="'+id+'"]').count(),1);await page.locator('#'+id).fill(id==='name'?'Teste':'11999999999');await textContrast(page,'#'+id);}
      assert.equal(await page.locator('#formStatus[role="status"]').count(),1);
      await page.screenshot({path:path.join(output,'praia-grande-hub-'+width+'.png'),fullPage:true});
      assert.equal(await page.locator('[href*="aid=XXXXXX"]').count(),0);
      assert.equal(await page.locator('.affiliate-disclosure').count(),1);
      assert.equal(await page.locator('#booking-affiliate-root input').count(),0);
      await page.goto(origin+hub);
      await page.locator('#guide-search').fill('nome a confirmar');
      assert.equal(await page.locator('.neighborhood-links li:visible').count(),2);
      await page.locator('#guide-clear').click();
      await page.locator('#guide-search').fill('balneario camburi');
      assert.equal(await page.locator('.neighborhood-links li:visible').count(),1);
      assert.deepEqual(errors,[]);results.push({width,reviewedGuides:reviewed.length,passed:true});await ctx.close();
    }
    const ctx=await context(browser,390,false),page=await ctx.newPage();await page.goto(origin+hub);
    assert.equal(await page.locator('.neighborhood-links a:visible').count(),123);assert.equal(await page.locator('.related-entry:visible').count(),2);await overflow(page);
    await ctx.close();results.push({javascript:false,passed:true});
    fs.writeFileSync(path.join(output,'results.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
