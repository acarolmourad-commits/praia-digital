// Exercise the built directory and all cross-app menus without network side effects.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=process.env.HOMEPAGE_PREVIEW_ROOT||path.resolve(__dirname,'..');
const origin='https://praia.digital';
const problems=[];
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox']});
try{for(const width of [360,768,1280]){
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  await context.route('**/*',async route=>{
    const req=route.request(),url=new URL(req.url());
    if(url.origin!==origin||req.method()!=='GET')return route.abort();
    let file=path.join(root,decodeURIComponent(url.pathname));
    if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
    if(!fs.existsSync(file))return route.fulfill({status:404,body:''});
    const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
    return route.fulfill({body:fs.readFileSync(file),contentType:mime[path.extname(file)]||'application/octet-stream'});
  });
  const page=await context.newPage();
  await page.goto(origin+'/apps/');
  assert.equal(await page.locator('.pd-site-header').count(),1);
  assert.equal(await page.locator('.pd-catalog-group .card').count(),16);
  assert.equal(await page.locator('#guia-premissas').count(),1);
  const visibleCards = page.locator('.pd-catalog-group .card:visible');
  assert.equal(await visibleCards.count(),16);
  const goal = page.locator('#app-goal');
  const costPath = '/apps/custo-de-compra/';
  for (const term of ['ITBI', 'escritura', 'registro']) {
    await page.goto(origin + '/apps/?busca=' + term + '#buscar-apps');
    assert.deepEqual(await visibleCards.evaluateAll(cards => cards.map(card => card.pathname)), [costPath], term);
    const result = page.locator('#app-only-result');
    assert.ok(await result.isVisible(), term);
    await result.click();
    assert.equal(page.url(), new URL(costPath, origin).href, term);
  }
  await page.goto(origin + '/apps/#buscar-apps');
  for (const term of ['SAC', 'Price']) {
    await page.locator('#app-query').fill(term);
    assert.deepEqual(await visibleCards.evaluateAll(cards => cards.map(card => card.pathname)), [
      '/apps/alugar-ou-comprar/', '/apps/calculadora-financiamento/'
    ], term);
    assert.ok(await page.locator('#app-only-result').isHidden());
  }
  await page.locator('#app-clear').click();
  assert.equal(await visibleCards.count(), 16);
  await goal.selectOption('grupo-comparar');
  await page.locator('#app-query').fill('noites');
  assert.deepEqual(await visibleCards.evaluateAll(cards => cards.map(card => card.getAttribute('href'))), [
    '/apps/simulador-roi-temporada/', '/apps/temporada-ou-anual/'
  ]);
  await page.goto(origin + '/apps/?origem=reuniao&objetivo=planejar#buscar-apps');
  assert.equal(await goal.inputValue(), 'grupo-planejar');
  assert.equal(await visibleCards.count(), 6);
  await page.locator('#app-query').fill('entrada');
  const shared = new URL(page.url());
  assert.equal(shared.searchParams.get('objetivo'), 'planejar');
  assert.equal(shared.search.includes('entrada'), false);
  const recipient = await context.newPage();
  await recipient.goto(shared.href);
  assert.equal(await recipient.locator('.pd-catalog-group .card:visible').count(), 6);
  assert.equal(await recipient.locator('#app-query').inputValue(), '');
  await recipient.close();
  await goal.selectOption('grupo-marketplaces');
  assert.equal(new URL(page.url()).searchParams.get('objetivo'), 'marketplaces');
  await page.locator('#app-clear').click();
  assert.equal(new URL(page.url()).search, '?origem=reuniao');
  assert.equal(new URL(page.url()).hash, '#buscar-apps');
  await page.goto(origin + '/apps/?objetivo=desconhecido#buscar-apps');
  assert.equal(await visibleCards.count(), 16);
  // Recover from an empty search without losing the selected objective.
  await page.goto(origin + '/apps/?origem=guia&objetivo=planejar&busca=vistoria#buscar-apps');
  const keepGoal = page.getByRole('button', {name: 'Ver todos deste objetivo'});
  assert.equal(await visibleCards.count(), 0);
  await page.locator('#app-share-query').check();
  await keepGoal.press('Enter');
  assert.equal(await goal.inputValue(), 'grupo-planejar');
  assert.equal(await visibleCards.count(), 6);
  assert.equal(await page.locator('#app-query').inputValue(), '');
  assert.ok(await page.locator('#app-query').evaluate(el => el === document.activeElement));
  assert.equal(await page.locator('#app-share-query').isChecked(), false);
  assert.equal(new URL(page.url()).search, '?origem=guia&objetivo=planejar');
  assert.equal(new URL(page.url()).hash, '#buscar-apps');
  assert.ok(await keepGoal.isHidden());
  // Escape clears an incoming search and its sharing consent, preserving the goal.
  await page.goto(origin + '/apps/?origem=guia&objetivo=planejar&busca=entrada#buscar-apps');
  const search = page.locator('#app-query');
  assert.equal(await visibleCards.count(), 1);
  await page.locator('#app-share-query').check();
  await search.press('Escape');
  assert.equal(await search.inputValue(), '');
  assert.equal(await goal.inputValue(), 'grupo-planejar');
  assert.equal(await visibleCards.count(), 6);
  assert.equal(new URL(page.url()).search, '?origem=guia&objetivo=planejar');
  assert.equal(await page.locator('#app-share-query').isChecked(), false);
  assert.equal(await page.locator('#app-share-link').inputValue(), origin + '/apps/?objetivo=planejar#buscar-apps');
  assert.ok(await search.evaluate(el => el === document.activeElement));
  await search.press('Escape');
  assert.equal(await goal.inputValue(), 'grupo-planejar');
  await search.fill('ITBI');
  await search.dispatchEvent('keydown', {key: 'Escape', isComposing: true});
  assert.equal(await search.inputValue(), 'ITBI');
  assert.equal(await visibleCards.count(), 1);
  assert.equal(await page.locator('#app-only-result').getAttribute('href'), origin + costPath);
  // Copying the objective excludes search words and unrelated URL parameters.
  await page.goto(origin+'/apps/?objetivo=preparar&origem=reuniao#buscar-apps');
  await page.locator('#app-query').fill('vistoria');
  assert.equal(await visibleCards.count(),1);
  const sharedUrl=await page.locator('#app-share-link').inputValue();
  assert.equal(sharedUrl,origin+'/apps/?objetivo=preparar#buscar-apps');
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{document.body.dataset.copiedLink=text;}}}));
  await page.getByRole('button',{name:'Copiar link do objetivo'}).press('Enter');
  await page.locator('#app-copy-status').getByText(/Link copiado/).waitFor();
  assert.equal(await page.locator('body').getAttribute('data-copied-link'),sharedUrl);
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw new Error('Clipboard denied');}}}));
  await page.getByRole('button',{name:'Copiar link do objetivo'}).click();
  await page.locator('#app-copy-status').getByText(/Selecione e copie/).waitFor();
  assert.equal(await page.locator('#app-share-link').evaluate(el=>el===document.activeElement),true,'Manual copy remains available');
  const includeTerm = page.getByRole('checkbox',{name:'Incluir o termo da busca no link'});
  assert.equal(await includeTerm.isChecked(), false);
  await includeTerm.check();
  const filteredUrl = new URL(await page.locator('#app-share-link').inputValue());
  assert.equal(filteredUrl.searchParams.get('objetivo'), 'preparar');
  assert.equal(filteredUrl.searchParams.get('busca'), 'vistoria');
  assert.equal(filteredUrl.searchParams.has('origem'), false);
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{document.body.dataset.copiedLink=value;}}}));
  await page.getByRole('button',{name:'Copiar link da busca'}).press('Enter');
  await page.locator('#app-copy-status').getByText(/Link copiado/).waitFor();
  assert.equal(await page.locator('body').getAttribute('data-copied-link'),filteredUrl.href);
  await page.goto(filteredUrl.href);
  assert.equal(await page.locator('#app-query').inputValue(),'vistoria');
  assert.equal(await visibleCards.count(),1);
  assert.equal(await includeTerm.isChecked(),false);
  await page.locator('#app-query').fill('anúncio');
  await page.waitForURL(url => !url.searchParams.has('busca'));
  assert.equal(await includeTerm.isChecked(),false);
  await page.goto(filteredUrl.href);
  await page.locator('#app-clear').click();
  assert.equal(new URL(page.url()).search,'');
  assert.equal(await includeTerm.isDisabled(),true);
  await page.goto(sharedUrl);
  assert.equal(await visibleCards.count(),4,'The recipient sees all tools in the objective');
  assert.equal(await page.locator('#app-query').inputValue(),'','Search words are not transferred');
  await page.locator('#app-clear').click();
  assert.equal(await page.locator('#app-share-link').inputValue(),origin+'/apps/#buscar-apps');
  assert.equal(await page.locator('#app-copy-status').innerText(),'');
  await page.locator('#app-query').fill('ANÚNCIO');
  assert.equal(await visibleCards.count(),4,'Search matches the accented objective');
  await page.locator('#app-query').fill('shópee');
  assert.equal(await visibleCards.count(),1,'Search ignores case and accents');
  assert.match(await page.locator('#app-results').innerText(),/^1 de 16/);
  const onlyResult = page.locator('#app-only-result');
  assert.equal(await onlyResult.innerText(), 'Abrir Precificação Shopee e TikTok Shop');
  await onlyResult.focus();
  await Promise.all([
    page.waitForURL(origin + '/apps/calculadora-precificacao-shopee/'),
    onlyResult.press('Enter'),
  ]);
  await page.goto(origin + '/apps/?busca=sh%C3%B3pee#buscar-apps');
  assert.ok(await onlyResult.isVisible());
  const printButton = page.getByRole('button',{name:'Imprimir seleção ou salvar em PDF'});
  await page.evaluate(() => { window.print = () => { document.body.dataset.printRequested = 'yes'; }; });
  await printButton.press('Enter');
  assert.equal(await page.locator('body').getAttribute('data-print-requested'),'yes');
  await page.emulateMedia({media:'print'});
  assert.equal(await visibleCards.count(),1,'Only the filtered app is printed');
  assert.equal(await printButton.isVisible(),false);
  assert.equal(await page.locator('#app-results').isVisible(),true);
  assert.match(await visibleCards.first().evaluate(el=>getComputedStyle(el,'::after').content),/praia\.digital/);
  await page.emulateMedia({media:'screen'});
  await page.locator('#app-goal').selectOption('grupo-planejar');
  assert.equal(await printButton.isDisabled(),true);
  assert.equal(await visibleCards.count(),0,'Search and objective combine');
  assert.ok(await onlyResult.isHidden());
  assert.equal(await onlyResult.getAttribute('href'), null);
  assert.ok(await page.locator('#app-empty').isVisible());
  const broaden = page.getByRole('button',{name:'Buscar em todos os objetivos'});
  assert.ok(await broaden.isVisible());
  await broaden.press('Enter');
  assert.equal(await goal.inputValue(),'');
  assert.equal(await page.locator('#app-query').inputValue(),'shópee');
  assert.ok(await page.locator('#app-query').evaluate(el => el === document.activeElement));
  assert.equal(await visibleCards.count(),1);
  assert.equal(new URL(page.url()).searchParams.has('objetivo'),false);
  assert.equal(await printButton.isEnabled(),true);
  await page.locator('#app-query').fill('zzzinexistente');
  assert.ok(await page.locator('#app-empty').isVisible());
  assert.equal(await broaden.isVisible(),false);
  await page.locator('#app-query').press('Enter');
  assert.equal(new URL(page.url()).pathname,'/apps/','Enter does not submit or navigate');
  await page.locator('#app-clear').click();
  assert.equal(await visibleCards.count(),16);
  assert.equal(await page.locator('#app-query').evaluate(el=>el===document.activeElement),true);
  await page.emulateMedia({media:'print'});
  assert.equal(await visibleCards.count(),16,'Clearing the filters prints the full directory');
  assert.ok(await onlyResult.isHidden());
  await page.emulateMedia({media:'screen'});
  await page.locator('#app-goal').selectOption('grupo-planejar');
  assert.equal(await visibleCards.count(),6);
  await page.locator('#objetivos-apps a[href="#grupo-marketplaces"]').click();
  assert.equal(await visibleCards.count(),16,'Objective links restore hidden targets');
  await page.locator('#app-query').fill('<img src=x onerror=alert(1)>');
  assert.equal(await visibleCards.count(),0);
  assert.equal(await page.locator('#app-results img').count(),0,'Search stays text only');
  await page.locator('#app-clear').click();
  const links=await page.locator('.pd-catalog-group .card').evaluateAll(nodes=>nodes.map(a=>a.getAttribute('href')));
  const overflow=async()=>{
    const spill=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].filter(el=>{const b=el.getBoundingClientRect();return b.width>0&&(b.left< -1||b.right>innerWidth+1)&&getComputedStyle(el).position!=='absolute';}).slice(0,8).map(el=>({tag:el.tagName,id:el.id,cls:el.className,width:el.getBoundingClientRect().width}))}));
    if(spill.scroll>width+1){problems.push({url:page.url(),...spill});console.log(JSON.stringify(problems.at(-1)));}
  };
  await overflow();
  await page.screenshot({path:`/tmp/praia-catalog-${width}.png`,fullPage:true});
  for(const link of links){
    await page.goto(origin+link);
    assert.equal(await page.locator('.pd-workflow h3').count(),1,link);
    assert.equal(await page.locator('.pd-workflow dd').count(),2,link);
    assert.ok(await page.locator('.pd-workflow').isVisible(),link);
    if(link==='/apps/revisor-anuncios/' && process.env.HOMEPAGE_QA_OUTPUT){
      fs.mkdirSync(process.env.HOMEPAGE_QA_OUTPUT,{recursive:true});
      await page.locator('.pd-workflow').screenshot({path:path.join(process.env.HOMEPAGE_QA_OUTPUT,`app-guidance-${width}.png`)});
    }
    const menu=page.locator('.pd-network details');
    await menu.locator('summary').click();
    assert.equal(await menu.locator('li').count(),15,link);
    await overflow();
    await page.locator('.pd-network a[href="/apps/"]').click();
    assert.equal(new URL(page.url()).pathname,'/apps/');
  }
  const dailyPath='/ferramentas/calculadora-diaria-ideal-airbnb-2026.html';
  const dailyCard=page.getByRole('navigation',{name:'Outros recursos'}).getByRole('link',{name:/Calculadora de diária de temporada/});
  await dailyCard.press('Enter');
  assert.equal(new URL(page.url()).pathname,dailyPath);
  assert.equal(new URL(page.url()).hash,'#form-calculo');
  assert.ok(await page.locator('#form-calculo').isVisible());
  await overflow();
  const nextSteps=page.getByRole('navigation',{name:'Compare o próximo cenário da temporada'});
  for(const [ordinal,[name,target]] of [
    [/Projetar receita/, '/apps/simulador-roi-temporada/'],
    [/Comparar temporada/, '/apps/temporada-ou-anual/'],
    [/Voltar ao catálogo/, '/apps/'],
  ].entries()){
    if(ordinal>0){
      const response=await page.goto(origin+dailyPath+'#form-calculo');
      assert.equal(response?.status(),200,dailyPath);
    }
    await nextSteps.getByRole('link',{name}).press('Enter');
    assert.equal(new URL(page.url()).pathname,target);
    assert.ok(await page.locator('h1').isVisible(), target);
  }
  await context.close();console.log(`Catalog, 16 return journeys and seasonal paths passed at ${width}px`);
}assert.deepEqual(problems,[],'All app pages must fit the viewport');}
finally{await browser.close();}})().catch(error=>{console.error(error);process.exit(1);});

