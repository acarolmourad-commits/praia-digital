const {chromium} = require('playwright');
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH || undefined,args:['--no-sandbox']});try{
for(const width of [320,360,390,768,1280]){
 const page=await browser.newPage({viewport:{width,height:1000}});
 await page.route('**/*',r=>r.abort());
 await page.setContent(fs.readFileSync(path.join(root,'docs/inteligencia/boletim-diario.html'),'utf8'));
 for(const css of ['assets/css/pd-navigation.css','assets/css/boletim.css'])await page.addStyleTag({content:fs.readFileSync(path.join(root,css),'utf8')});
 for(const js of ['js/pd-navigation.js','js/boletim.js'])await page.addScriptTag({content:fs.readFileSync(path.join(root,js),'utf8')});
 const total=await page.locator('.news-item').count();
 assert.equal(await page.locator('.news-item:visible').count(),total);
 if(total){
 const city=await page.locator('.news-item').first().getAttribute('data-city');
 const expected=await page.locator('.news-item').evaluateAll((items,city)=>items.filter(i=>i.dataset.city===city).length,city);
 await page.selectOption('#filter-city',city);assert.equal(await page.locator('.news-item:visible').count(),expected);
 // Inject an unavailable option solely to exercise the accessible empty-state flow.
 await page.locator('#filter-category').evaluate(s=>s.add(new Option('Test empty','__no_match__')));
 await page.selectOption('#filter-category','__no_match__');assert.equal(await page.locator('.news-item:visible').count(),0);assert.equal(await page.locator('#filter-empty').isVisible(),true);
 await page.locator('#filter-reset').click();assert.equal(await page.locator('.news-item:visible').count(),total);assert.equal(await page.locator('#filter-empty').isVisible(),false);await page.locator('#filter-reset').click();assert.equal(await page.locator('.news-item:visible').count(),total);
 } else { assert.equal(await page.locator('.bulletin-filters').isVisible(),false); }
 await page.locator('#copy-rss').click();assert.match(await page.locator('#copy-status').innerText(),/Endereço copiado|Selecione e copie/);await page.locator('#copy-rss').click();assert.equal(await page.locator('#rss-address').inputValue(),'https://praia.digital/docs/inteligencia/feed.xml');
 if(width<=1080){await page.locator('.pd-site-toggle').click();assert.equal(await page.locator('.pd-site-menu').isVisible(),true);await page.locator('.pd-site-label').last().click();await page.keyboard.press('Escape');await page.keyboard.press('Escape');assert.equal(await page.locator('.pd-site-menu').isVisible(),false);}
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,'No horizontal overflow '+width);
 await page.screenshot({path:'/tmp/bulletin-'+width+'.png',fullPage:true});await page.close();
}
const noJs=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:900}});await noJs.route('**/*',r=>r.abort());await noJs.setContent(fs.readFileSync(path.join(root,'docs/inteligencia/boletim-diario.html'),'utf8'));assert.equal(await noJs.locator('.news-item:visible').count(),(fs.readFileSync(path.join(root,'docs/inteligencia/boletim-diario.html'),'utf8').match(/class="bulletin-card news-item"/g)||[]).length);assert.equal(await noJs.locator('#rss-address').inputValue(),'https://praia.digital/docs/inteligencia/feed.xml');await noJs.close();
const page=await browser.newPage({viewport:{width:390,height:900}});await page.route('**/*',r=>r.abort());await page.setContent(fs.readFileSync(path.join(root,'newsletter/assinatura.html'),'utf8'));assert.equal(await page.locator('form').count(),0);assert.equal(await page.locator('a[href="/docs/inteligencia/feed.xml"]').count(),1);
console.log('Bulletin browser checks passed: 5 widths, filters/reset, empty state, repeated RSS copying/fallback, menu dismissal, no overflow, no-JS content, inactive signup.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
