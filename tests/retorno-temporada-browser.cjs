// Run: NODE_PATH=<playwright node_modules> node tests/retorno-temporada-browser.cjs
const {chromium}=require('playwright');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../ferramentas-gratuitas/imobiliarias/analise-retorno-temporada-litoral.html'),'utf8');
(async()=>{
 const browser=await chromium.launch({...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {}),headless:true,args:['--no-sandbox']});
 let count=0;
 for(const width of [390,1280]) {
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.route('**/*',r=>r.abort()); // no analytics, provider requests or data submission
  await page.setContent(html);
  const run=async(values,expected)=>{
   for(const [i,id] of ['diaria','dias','taxa'].entries()) await page.locator('#'+id).fill(values[i]);
   await page.locator('#calcular').click();
   assert.match(await page.locator('.result').innerText(),expected);count++;
  };
  await run(['800','45','70'],/25\.200,00/);
  await run(['800','45','0'],/R\$ 0,00/);
  await run(['800','45','100'],/36\.000,00/);
  await run(['800.50','1','50'],/400,25/);
  await run(['800','0','70'],/R\$ 0,00/);
  for(const values of [['','45','70'],['0','45','70'],['-1','45','70'],['800','366','70'],['800','1.5','70'],['800','45','101'],['800','45','-1']]) await run(values,/Informe diária positiva/);
  await run(['9007199254740991','365','100'],/excede o limite/);
  await run(['800','45','70'],/25\.200,00/); // recovery after invalid input
  await page.locator('#calcular').click();assert.match(await page.locator('.result').innerText(),/25\.200,00/);count++;
  assert.equal(await page.locator('a:has-text("Avaliação de preço")').getAttribute('href'),'/ferramentas/avaliacao-preco.html');
  assert.equal(await page.locator('label[for]').count(),3);
  assert.equal(await page.locator('.result').getAttribute('aria-live'),'polite');
  await page.close();
 }
 const page=await browser.newPage({javaScriptEnabled:false});await page.route('**/*',r=>r.abort());await page.setContent(html);assert.equal(await page.locator('#calcular').isDisabled(),true);count++;
 await browser.close();console.log(`${count} browser checks passed (390/1280px, invalid inputs, repeated calculation, no-JS)`);
})().catch(e=>{console.error(e);process.exit(1)});
