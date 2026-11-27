// Exercise the built directory and all cross-app menus without network side effects.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=process.env.HOMEPAGE_PREVIEW_ROOT||path.resolve(__dirname,'..');
const origin='https://praia.digital';
const problems=[];
(async()=>{const browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE||undefined,args:['--no-sandbox']});
try{for(const width of [360,768,1280]){
  const context=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});
  const routeSite=async route=>{
    const req=route.request(),url=new URL(req.url());
    if(url.origin!==origin||req.method()!=='GET')return route.abort();
    let file=path.join(root,decodeURIComponent(url.pathname));
    if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
    if(!fs.existsSync(file))return route.fulfill({status:404,body:''});
    const mime={'.html':'text/html','.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml'};
    return route.fulfill({body:fs.readFileSync(file),contentType:mime[path.extname(file)]||'application/octet-stream'});
  };
  await context.route('**/*',routeSite);
  const page=await context.newPage();
  await page.goto(origin+'/apps/');
  assert.equal(await page.locator('.pd-site-header').count(),1);
  assert.equal(await page.locator('.pd-catalog-group .card').count(),16);
  assert.equal(await page.locator('#guia-premissas').count(),1);
  const visibleCards = page.locator('.pd-catalog-group .card:visible');
  assert.equal(await visibleCards.count(),16);
  const goal = page.locator('#app-goal');
  const inspectionPath = '/apps/checklist-vistoria/';
  for (const term of ['entrega das chaves', 'vistoria de saída']) {
    await page.goto(origin + '/apps/?busca=' + encodeURIComponent(term) + '#buscar-apps');
    assert.deepEqual(await visibleCards.evaluateAll(cards => cards.map(card => card.pathname)), [inspectionPath], term);
    await page.locator('#app-only-result').press('Enter');
    assert.equal(new URL(page.url()).pathname, inspectionPath);
  }
  await page.goto(origin + '/');
  await page.locator('a[href="/apps/checklist-vistoria/#entrega-das-chaves"]').press('Enter');
  await page.waitForURL(origin + inspectionPath + '#entrega-das-chaves');
  const handover = page.getByRole('region', {name: 'Como comparar a vistoria de entrada com a de saída'});
  await handover.waitFor({state: 'visible'});
  await handover.getByRole('link', {name:'Relatório do imóvel'}).press('Enter');
  await page.waitForURL(origin + '/apps/relatorio-imovel/#evidencias-da-visita');
  await page.locator('#evidencias-da-visita').waitFor({state: 'visible'});
  const roiPath = '/apps/simulador-roi-temporada/';
  const marketPath = '/apps/calculadora-precificacao-shopee/';
  const dailyResource = '/ferramentas/calculadora-diaria-ideal-airbnb-2026.html#form-calculo';
  const bookingResource = '/blog/novidades-airbnb-booking.html';
  await page.goto(origin+'/apps/#buscar-apps');
  const finder = page.getByRole('searchbox', {name:'O que você quer fazer?'});
  const related = page.locator('#app-resource-results');
  const relatedLinks = related.getByRole('link');
  const appPaths = () => visibleCards.evaluateAll(cards => cards.map(card => card.getAttribute('href')));
  const resourcePaths = () => relatedLinks.evaluateAll(links => links.map(link => link.getAttribute('href')));
  for (const word of ['rentabilidade','  RENTABILIDÁDE  ','taxa da plataforma']) {
    await finder.fill(word);
    assert.deepEqual(await appPaths(),[roiPath],word);
    assert.match(await page.locator('#app-results').innerText(),/^1 de 16/);
    assert.ok(await related.isHidden());
  }
  await finder.fill('taxa');
  assert.deepEqual(await appPaths(),[roiPath, marketPath]);
  await finder.fill('temporada');
  assert.deepEqual(await appPaths(),[roiPath, '/apps/temporada-ou-anual/']);
  assert.deepEqual(await resourcePaths(),[dailyResource]);
  await finder.fill('Airbnb');
  assert.deepEqual(await appPaths(),[]);
  assert.deepEqual(await resourcePaths(),[dailyResource,bookingResource]);
  assert.match(await page.locator('#app-results').innerText(),/0 de 16.*2 recursos complementares/);
  assert.ok(await page.locator('#app-empty').isHidden());
  assert.ok(await page.locator('#app-only-result').isHidden());
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  await related.getByRole('link',{name:/Calculadora de diária/}).press('Enter');
  await page.waitForURL(origin+dailyResource);
  assert.ok(await page.locator('#form-calculo').isVisible());
  await page.goto(origin+'/apps/?objetivo=planejar&busca=Booking#buscar-apps');
  assert.ok(await related.isHidden());
  assert.match(await page.locator('#app-results').innerText(),/recurso complementar em outro objetivo/);
  await page.getByRole('button',{name:'Buscar em todos os objetivos'}).press('Enter');
  assert.equal(await finder.inputValue(),'Booking');
  assert.ok(await finder.evaluate(el=>el===document.activeElement));
  assert.deepEqual(await resourcePaths(),[bookingResource]);
  await finder.press('Escape');
  assert.ok(await related.isHidden());
  assert.equal(await visibleCards.count(),16);
  await finder.fill('Booking');
  await related.getByRole('link',{name:'Novidades Airbnb e Booking'}).press('Enter');
  await page.waitForURL(origin+bookingResource);
  assert.ok(await page.getByRole('heading',{name:'Novidades Airbnb e Booking',exact:true}).isVisible());
  await page.goto(origin+'/apps/#buscar-apps');
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
  const jump = page.getByRole('button', {name: 'Ir ao primeiro resultado'});
  assert.ok(await jump.isHidden());
  for (const term of ['SAC', 'Price']) {
    await page.locator('#app-query').fill(term);
    assert.deepEqual(await visibleCards.evaluateAll(cards => cards.map(card => card.pathname)), [
      '/apps/alugar-ou-comprar/', '/apps/calculadora-financiamento/'
    ], term);
    assert.ok(await page.locator('#app-only-result').isHidden());
    await jump.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('href'), '/apps/alugar-ou-comprar/');
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').getAttribute('href'), '/apps/calculadora-financiamento/');
  }
  await page.locator('#app-clear').click();
  assert.equal(await visibleCards.count(), 16);
  await goal.selectOption('grupo-comparar');
  await page.locator('#app-query').fill('noites');
  await jump.click();
  assert.equal(await page.locator(':focus').getAttribute('href'), '/apps/simulador-roi-temporada/');
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
  const marketplaceNav = page.locator('#objetivos-apps a[href="#grupo-marketplaces"]');
  await page.locator('#app-query').fill('entrada');
  const originalUrl = page.url();
  for (const modifier of ['ctrlKey','metaKey','shiftKey','altKey']) {
    await marketplaceNav.evaluate((link,key)=>{
      document.addEventListener('click',event=>event.preventDefault(),{once:true});
      link.dispatchEvent(new MouseEvent('click',{[key]:true,bubbles:true,cancelable:true}));
    }, modifier);
    assert.equal(page.url(), originalUrl, modifier);
    assert.equal(await goal.inputValue(), 'grupo-planejar', modifier);
    assert.equal(await page.locator('#app-query').inputValue(), 'entrada', modifier);
  }
  await marketplaceNav.click();
  assert.equal(await visibleCards.count(),16,'Objective links restore hidden targets');
  await page.goto(origin + '/apps/?origem=guia&objetivo=planejar&busca=entrada#grupo-marketplaces');
  await page.locator('#grupo-marketplaces').waitFor({state:'visible'});
  assert.equal(await visibleCards.count(),16,'Direct conflicting group fragments still reveal the heading');
  assert.equal(new URL(page.url()).search,'?origem=guia');
  assert.equal(new URL(page.url()).hash,'#grupo-marketplaces');
  await page.goto(origin + '/apps/?origem=guia&objetivo=planejar&busca=entrada#grupo-planejar');
  assert.equal(await visibleCards.count(),1,'Matching direct group fragments keep the intentional filter');
  assert.equal(await goal.inputValue(),'grupo-planejar');
  assert.equal(await page.locator('#app-query').inputValue(),'entrada');
  await page.locator('#app-query').fill('<img src=x onerror=alert(1)>');
  assert.equal(await visibleCards.count(),0);
  assert.equal(await page.locator('#app-results img').count(),0,'Search stays text only');
  await page.locator('#app-clear').click();
  const links = await page.locator('.pd-catalog-group .card').evaluateAll(nodes => nodes.map(card => ({
    link: card.getAttribute('href'),
    group: card.closest('.pd-catalog-group').getAttribute('aria-labelledby'),
  })));
  const overflow=async()=>{
    const spill=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,elements:[...document.querySelectorAll('body *')].filter(el=>{const b=el.getBoundingClientRect();return b.width>0&&(b.left< -1||b.right>innerWidth+1)&&getComputedStyle(el).position!=='absolute';}).slice(0,8).map(el=>({tag:el.tagName,id:el.id,cls:el.className,width:el.getBoundingClientRect().width}))}));
    if(spill.scroll>width+1){problems.push({url:page.url(),...spill});console.log(JSON.stringify(problems.at(-1)));}
  };
  await overflow();
  await page.screenshot({path:`/tmp/praia-catalog-${width}.png`,fullPage:true});
  for (const {link, group} of links) {
    await page.goto(origin+link);
    const shortcut = page.getByRole('link', {name: 'Ver aplicativos relacionados', exact: true});
    assert.ok(await shortcut.isVisible(), link);
    assert.ok((await shortcut.boundingBox()).height >= 44, link);
    await shortcut.press('Enter');
    assert.equal(await page.evaluate(() => document.activeElement.id), 'pd-network-title', link);
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
    assert.ok(await page.locator('.pd-network a[href="/apps/"]').isVisible(), link);
    const objective = group.slice('grupo-'.length);
    await page.locator(`.pd-network a[href="/apps/?objetivo=${objective}#${group}"]`).press('Enter');
    await page.waitForURL(origin + '/apps/?objetivo=' + objective + '#' + group);
    await page.waitForFunction(expected => document.getElementById('app-goal')?.value === expected, group);
    assert.equal(new URL(page.url()).hash, '#' + group);
    assert.equal(await goal.inputValue(), group);
    assert.equal(await page.locator('.pd-catalog-group:visible').count(), 1);
    assert.ok(await page.locator('#' + group).isVisible());
  }
  // The checklist works by keyboard and label, with a single live canonical.
  const checklistPath = '/assets/ferramentas/checklist-automatizacao-corretores-litoral-2026.html';
  await page.getByRole('link', {name: 'checklist de automação para corretores'}).click();
  assert.equal(new URL(page.url()).pathname, checklistPath);
  assert.deepEqual(await page.locator('link[rel="canonical"]').evaluateAll(nodes => nodes.map(n => n.href)), [origin + checklistPath]);
  const firstTask = page.getByRole('checkbox', {name: /Conferi os dados do imóvel/});
  assert.equal(await page.getByRole('checkbox').count(), 16);
  await firstTask.focus();
  await firstTask.press('Space');
  assert.equal(await page.locator('#progress').textContent(), '1 de 16 pontos conferidos');
  await page.getByText(/Conferi os dados do imóvel com a fonte/, {exact: false}).click();
  assert.equal(await page.locator('#progress').textContent(), '0 de 16 pontos conferidos');
  await overflow();
  await page.getByRole('link', {name: 'Revisor de anúncios', exact: true}).click();
  assert.equal(new URL(page.url()).pathname, '/apps/revisor-anuncios/');
  await page.goto(origin + '/apps/');
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
  await context.close();
  const noJs=await browser.newContext({javaScriptEnabled:false,viewport:{width,height:900}});
  await noJs.route('**/*',routeSite);
  const plain=await noJs.newPage();
  await plain.goto(origin+'/apps/?busca=Airbnb#buscar-apps');
  assert.equal(await plain.locator('.pd-catalog-group .card:visible').count(),16);
  assert.ok(await plain.locator('#catalog-search-form').isHidden());
  assert.ok(await plain.getByRole('navigation',{name:'Outros recursos'}).getByRole('link',{name:/Calculadora de diária de temporada para Airbnb/}).isVisible());
  assert.ok(await plain.getByRole('link',{name:'Novidades Airbnb e Booking',exact:true}).isVisible());
  await noJs.close();
  console.log(`Catalog, 16 return journeys and seasonal paths passed at ${width}px`);
}assert.deepEqual(problems,[],'All app pages must fit the viewport');}
finally{await browser.close();}})().catch(error=>{console.error(error);process.exit(1);});

