// Offline regression tests against the same navigation-built HTML that is deployed.
// Run build-navigation.py first, then NODE_PATH=... node tests/homepage-browser.cjs.
// Every browser request is intercepted; no external forms, payments or messages run.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(process.env.HOMEPAGE_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = path.resolve(process.env.HOMEPAGE_QA_OUTPUT || '/tmp/praia-homepage-qa');
const origin = 'https://praia.digital';
const results = [];
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon', '.woff2': 'font/woff2' };

async function offlineContext(browser, width, options = {}) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, serviceWorkers: 'block', ...options });
  const sideEffects = [];
  await context.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (!['GET', 'HEAD'].includes(request.method())) {
      sideEffects.push(`${request.method()} ${url.origin}${url.pathname}`);
      return route.abort();
    }
    if (url.origin !== origin) {
      if (request.isNavigationRequest()) sideEffects.push(`External navigation: ${url.origin}${url.pathname}`);
      return route.abort();
    }
    let filename = path.resolve(root, '.' + decodeURIComponent(url.pathname));
    if (!filename.startsWith(root + path.sep) && filename !== root) return route.fulfill({ status: 403, body: 'Forbidden' });
    if (fs.existsSync(filename) && fs.statSync(filename).isDirectory()) filename = path.join(filename, 'index.html');
    if (!fs.existsSync(filename) || !fs.statSync(filename).isFile()) return route.fulfill({ status: 404, body: 'Not found' });
    return route.fulfill({ status: 200, contentType: mime[path.extname(filename)] || 'application/octet-stream', body: fs.readFileSync(filename) });
  });
  return { context, sideEffects };
}

async function noOverflow(page, label) {
  const dimensions = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
  assert(dimensions.document <= dimensions.viewport + 1 && dimensions.body <= dimensions.viewport + 1,
    `${label} horizontal overflow: ${JSON.stringify(dimensions)}`);
}

async function turnoverFromHome(page, width) {
  const home = origin + '/#central-airbnb-booking';
  const path = '/anfitrioes/checklists-anfitrioes.html#intervalo-entre-reservas';
  await page.goto(home);
  const feature = page.locator('#central-airbnb-booking').getByRole('link', {name:'Calcule quanto tempo sobra entre reservas', exact:true});
  assert.equal(await page.locator(`a[href="${path}"]`).count(), 1);
  assert.equal(await feature.getAttribute('href'), path);
  assert(await feature.isVisible());
  await feature.press('Enter');
  await page.waitForURL(origin + path);
  assert(await page.getByRole('heading', {name:'Planeje o intervalo entre reservas', exact:true}).isVisible());
  assert(await page.getByRole('button', {name:'Calcular intervalo', exact:true}).isEnabled());
  await noOverflow(page, `intervalo entre reservas ${width}px`);
  await page.goBack();
  assert.equal(page.url(), home);
  console.log(`${width}px: home → estimativa de intervalo entre reservas → voltar`);
}

async function blackFriday(page, width) {
  const special = origin + '/compras/black-friday.html';
  await page.goto(origin + '/#especial-black-friday');
  const feature = page.locator('#especial-black-friday').getByRole('link', { name: 'Explorar o especial Black Friday' });
  assert.equal(await feature.getAttribute('href'), '/compras/black-friday.html');
  await page.keyboard.press('Tab');
  await feature.focus();
  assert.deepEqual(await feature.evaluate(el => {
    const style = getComputedStyle(el);
    return [document.activeElement === el, style.outlineStyle, style.outlineColor];
  }), [true, 'solid', 'rgb(148, 91, 0)'], 'homepage spotlight has the scoped high-contrast focus color');
  await page.screenshot({ path: path.join(output, `black-friday-focus-${width}.png`) });
  await page.keyboard.press('Enter');
  await page.waitForURL(special);

  const disclosure = page.locator('.hero .affiliate-disclosure');
  const campaign = page.getByRole('link', { name: 'Consultar campanha na Amazon Brasil ↗' });
  assert(await disclosure.isVisible() && await campaign.isVisible());
  assert.match(await disclosure.innerText(), /pode receber comissão por compras qualificadas/);
  const order = await disclosure.evaluate(el => {
    const first = el.ownerDocument.querySelector('a[rel~="sponsored"]');
    return !!first && !!(el.compareDocumentPosition(first) & Node.DOCUMENT_POSITION_FOLLOWING) &&
      el.getBoundingClientRect().bottom <= first.getBoundingClientRect().top;
  });
  assert(order, 'disclosure appears visually and in reading order before the first affiliate link');
  assert.equal(await page.locator('a[rel~="sponsored"]').count(), 49, 'one campaign and 48 products');
  assert.equal(await page.locator('.summer .item').count(), 48);
  assert.equal(await page.getByRole('link', { name: /^Comparar na Amazon Brasil — .+ \(abre nova aba\)$/ }).count(), 48);
  await noOverflow(page, `Black Friday ${width}px`);
  await page.locator('.summer .hero').screenshot({ path: path.join(output, `black-friday-disclosure-${width}.png`) });

  // Focus the campaign link, but never follow a retailer link.
  await campaign.focus();
  assert.equal(await campaign.evaluate(el => el === document.activeElement && getComputedStyle(el).outlineStyle === 'solid'), true);
  const themes = page.getByRole('navigation', { name: 'Temas da Black Friday' });
  const ids = ['viagens', 'praia', 'temporada', 'presentes', 'decoracao', 'festas', 'comparar'];
  assert.deepEqual(await themes.locator('a').evaluateAll(nodes => nodes.map(a => a.hash)), ids.map(id => '#' + id));
  for (const id of ids) {
    const jump = themes.locator(`a[href="#${id}"]`);
    await jump.focus();
    await page.keyboard.press('Enter');
    await page.waitForURL(special + '#' + id);
    await page.waitForFunction(target => {
      const title = document.getElementById(target);
      const header = document.querySelector('.pd-site-header');
      if (!title || !header) return false;
      const bounds = title.getBoundingClientRect();
      return getComputedStyle(title).scrollMarginTop === '110px' &&
        bounds.top >= header.getBoundingClientRect().bottom && bounds.bottom <= innerHeight;
    }, id, { timeout: 5000 });
  }
  await page.screenshot({ path: path.join(output, `black-friday-anchor-${width}.png`) });
}

async function appCatalog(browser, page, width) {
  await page.goto(origin + '/apps/');
  assert.equal(await page.locator('main').count(), 1);
  const catalog = page.locator('#catalogo-apps');
  const cards = catalog.locator('.pd-catalog-group a.card[href^="/apps/"]');
  assert.equal(await cards.count(), 16);
  assert.equal(await catalog.locator('a.card[href="/apps/guia-de-uso.html"]').count(), 1);
  await page.keyboard.press('Tab');
  assert.equal(await page.locator('.pd-skip').evaluate(el => {
    const box = el.getBoundingClientRect();
    return el === document.activeElement && box.top >= 0 && box.bottom < innerHeight &&
      document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2) === el;
  }), true, 'first keyboard target is visible above the header');
  await page.screenshot({path:path.join(output,`app-catalog-skip-${width}.png`)});
  await page.keyboard.press('Enter');
  assert.equal(await catalog.evaluate(el => el === document.activeElement), true);
  for (const group of ['grupo-planejar', 'grupo-comparar', 'grupo-preparar', 'grupo-marketplaces']) {
    const jump = page.locator('#objetivos-apps a[href="#' + group + '"]');
    await jump.focus();
    assert.equal(await jump.evaluate(el => getComputedStyle(el).outlineStyle), 'solid');
    assert((await jump.boundingBox()).height >= 44);
    await page.keyboard.press('Enter');
    await page.waitForURL(origin + '/apps/#' + group);
    const title = page.locator('#' + group);
    const bounds = await title.boundingBox();
    const headerBottom = await page.locator('.pd-site-header').evaluate(el => el.getBoundingClientRect().bottom);
    assert(bounds.y >= headerBottom && bounds.y + bounds.height < 900, 'objective heading is visible below sticky header');
    assert.equal(await title.evaluate(el => el === document.activeElement), true, 'fragment transfers keyboard focus to heading');
    const section = page.locator('.pd-catalog-group').filter({has:title});
    await page.keyboard.press('Tab');
    assert.equal(await section.locator('.card').first().evaluate(el => el === document.activeElement), true, 'next Tab enters the selected group');
    await section.locator('.catalog-return a').focus();
    await page.keyboard.press('Enter');
    await page.waitForURL(origin + '/apps/#objetivos-apps');
    assert.equal(await page.locator('#objetivos-apps').evaluate(el => el === document.activeElement), true);
  }
  const columns = await page.locator('.pd-catalog-group:first-child .card').evaluateAll(nodes => nodes.map(n => n.getBoundingClientRect().x));
  assert.equal(columns[0] === columns[1], width < 640, 'catalog stacks on mobile');
  await noOverflow(page, 'app catalog ' + width);
  await catalog.screenshot({path:path.join(output,`app-catalog-${width}.png`)});
  await page.locator('#catalogo-apps a[href="/apps/comparador-cidades/"]').click();
  await page.waitForURL(origin + '/apps/comparador-cidades/');
  await page.locator('.pd-network-nav a[href="/apps/"]').click();
  await page.waitForURL(origin + '/apps/');
  assert.equal(await cards.count(),16,'return from app keeps complete catalog');
  const offline = await offlineContext(browser, width, {javaScriptEnabled:false});
  try {
    const plain = await offline.context.newPage();
    await plain.goto(origin + '/apps/');
    assert.equal(await plain.locator('#catalogo-apps .pd-catalog-group a.card[href^="/apps/"]').count(),16);
    assert.equal(await plain.locator('a.card[href="/apps/guia-de-uso.html"]').count(),1);
    await plain.locator('#objetivos-apps a[href="#grupo-marketplaces"]').focus();
    await plain.keyboard.press('Enter');
    await plain.waitForURL(origin + '/apps/#grupo-marketplaces');
    await plain.locator('.pd-catalog-group').filter({has:plain.locator('#grupo-marketplaces')}).locator('.card').click();
    await plain.waitForURL(origin + '/apps/calculadora-precificacao-shopee/');
    assert.deepEqual(offline.sideEffects,[]);
  } finally { await offline.context.close(); }
}

async function homepage(page, width) {
  await page.goto(origin + '/', { waitUntil: 'load' });
  const header = page.locator('.pd-site-header');
  await header.waitFor();
  assert.equal(await header.count(), 1, 'use the navigation-built artifact');
  assert.equal(await page.locator('main').count(), 1);
  assert.equal(await page.locator('h1').count(), 1);
  assert.equal(await page.locator('#produtos-comparacao').count(), 1);
  assert.equal(await page.locator('#planos-praia-digital').count(), 0, 'legacy plan injection must not duplicate comparison');
  assert.equal(await page.locator('section#apps').count(), 1, 'one curated app journey section');
  assert.equal(await page.locator('[id=apps]').count(), 1, 'no duplicated app anchor');
  const journeys = page.locator('#jornadas-apps');
  assert.equal(await journeys.locator('article').count(), 4);
  const cards = await journeys.locator('article').evaluateAll(nodes => nodes.map(n => n.getBoundingClientRect().x));
  assert.equal(cards[0] === cards[1], width <= 640, 'journeys stack on mobile');
  const firstApp = journeys.locator('.app-steps a').first();
  await firstApp.focus();
  assert.equal(await firstApp.evaluate(el => getComputedStyle(el).outlineStyle), 'solid');
  assert((await firstApp.boundingBox()).height >= 44, 'touch target');
  await page.locator('section#apps').screenshot({path:path.join(output,`app-journeys-${width}.png`)});
  await page.keyboard.press('Enter');
  await page.waitForURL(origin + '/apps/comparador-cidades/');
  for (const anchor of ['apps', 'jornadas-apps']) {
    await page.goto(origin + '/#' + anchor);
    await journeys.waitFor();
    await page.waitForFunction(() => {
      const title = document.querySelector('#apps-titulo').getBoundingClientRect();
      return title.top >= document.querySelector('.pd-site-header').getBoundingClientRect().bottom && title.bottom < innerHeight;
    });
    await page.screenshot({path:path.join(output,`app-anchor-${anchor}-${width}.png`)});
  }
  await page.locator('#produtos-comparacao summary').focus();
  await page.keyboard.press('Enter');
  assert.equal(await page.locator('#produtos-comparacao details').evaluate(el=>el.open),true);
  assert.match(await page.locator('#academy').innerText(), /62 kits e 8 trilhas/);
  assert.match(await page.locator('#academy').innerText(), /compra assistida/);
  await page.locator('#academy').scrollIntoViewIfNeeded();
  await page.screenshot({path:path.join(output,`academy-${width}.png`)});
  assert.equal(await page.locator('#analise a[href="/apps/"]').count(), 1);
  const products = page.locator('#produtos-comparacao');
  assert.doesNotMatch(await products.innerText(), /R\$\s*\d/);
  for (const href of ['/entrega-kit-temporada.html', '/entrega-descricoes-ia.html', '/servicos/anuncios-airbnb-booking.html', '/planos.html']) {
    assert(await products.locator(`a[href="${href}"]`).isVisible(), href);
  }
  await noOverflow(page, `home ${width}px`);
  await page.locator('footer').scrollIntoViewIfNeeded();
  await noOverflow(page, `footer ${width}px`);
  const footerBounds = await page.locator('footer .cols').boundingBox();
  assert(footerBounds.x >= -1 && footerBounds.x + footerBounds.width <= width + 1, 'footer columns fit viewport');
  await page.screenshot({ path: path.join(output, `home-footer-${width}.png`) });
  await page.evaluate(() => scrollTo(0, 0));
  const toggle = header.locator('.pd-site-toggle');
  const firstGroup = header.locator('.pd-site-label').first();
  if (width <= 1080) {
    await toggle.click();
    assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
    await firstGroup.click();
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'true');
    await noOverflow(page, `open menu ${width}px`);
    await page.keyboard.press('Escape');
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'false');
    await page.keyboard.press('Escape');
    assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
    await toggle.click();
    await toggle.click();
    assert.equal(await toggle.getAttribute('aria-expanded'), 'false', 'repeated open/close stays consistent');
  } else {
    assert.equal(await toggle.isVisible(), false);
    await firstGroup.focus();
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'false');
    await page.keyboard.press('Enter');
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'false');
  }
  await page.screenshot({ path: path.join(output, `home-hero-${width}.png`) });
}

async function searchJourney(page, width) {
  const query = 'apartamento em Santos com 2 quartos até R$ 500 mil';
  await page.locator('#finalidade').selectOption('Venda');
  await page.locator('#smartsearch input[name="q"]').fill(query);
  await Promise.all([page.waitForURL(url => url.pathname === '/imoveis.html'), page.locator('#smartsearch button[type="submit"]').click()]);
  await page.locator('#lista-imoveis .imoveis-empty').waitFor();
  assert.equal(new URL(page.url()).searchParams.get('q'), query);
  assert.equal(await page.locator('#busca').inputValue(), query);
  assert.equal(await page.locator('#cidade-filtro').inputValue(), 'Santos');
  assert.equal(await page.locator('#categoria-filtro').inputValue(), 'apartamento');
  assert.equal(await page.locator('#quartos-filtro').inputValue(), '2');
  assert.equal(await page.locator('#preco-filtro').inputValue(), '500000');
  assert.equal(await page.locator('#lista-imoveis .property-card').count(), 0);
  await noOverflow(page, `zero results ${width}px`);
  await page.reload({ waitUntil: 'load' });
  assert.equal(await page.locator('#busca').inputValue(), query, 'reload preserves query');
  await page.locator('#busca').fill('casa em Bertioga até R$ 3 milhões');
  await page.locator('#lista-imoveis .property-card').first().waitFor();
  assert.equal(await page.locator('#cidade-filtro').inputValue(), 'Bertioga');
  assert.equal(await page.locator('#categoria-filtro').inputValue(), 'casa');
  const positiveCount = await page.locator('#lista-imoveis .property-card').count();
  assert(positiveCount > 0, 'matching criteria should show listings');
  await page.locator('#cidade-filtro').selectOption('Santos');
  assert.equal(new URL(page.url()).searchParams.get('cidade'), 'Santos');
  await page.goBack();
  await page.waitForFunction(() => document.getElementById('cidade-filtro').value === 'Bertioga');
  assert.equal(await page.locator('#lista-imoveis .property-card').count(), positiveCount);
  await page.goForward();
  await page.waitForFunction(() => document.getElementById('cidade-filtro').value === 'Santos');
  await page.locator('#limpar-busca').click();
  assert.equal(await page.locator('#busca').inputValue(), '');
  assert.equal(await page.locator('#cidade-filtro').inputValue(), '');
  assert.equal(await page.locator('#quartos-filtro').inputValue(), '');
  assert.equal(await page.locator('#preco-filtro').inputValue(), '');
  assert((await page.locator('#lista-imoveis .property-card').count()) >= positiveCount);
  await page.locator('#limpar-busca').click();
  await noOverflow(page, `catalog ${width}px`);
  const legacyQuery = '?q=casa%20em%20Bertioga&preco_max=3000000';
  await page.goto(origin + '/encontrar-imovel.html' + legacyQuery, { waitUntil: 'load' });
  await page.waitForURL(url => url.pathname === '/imoveis.html');
  assert.equal(new URL(page.url()).searchParams.get('q'), 'casa em Bertioga');
  assert.equal(new URL(page.url()).searchParams.get('preco_max'), '3000000');
  assert.match(await page.locator('#search-status').innerText(), /Finalidade pendente/);
  await page.goto(origin+'/imoveis.html?q='+encodeURIComponent('apartamento de 2 quartos até R$ 700 mil em Bertioga'));
  assert.equal(await page.locator('.property-card').count(),0);
  await page.locator('#tipo-filtro').selectOption('Venda');
  // The three authorized apartments match 2 bedrooms in Bertioga below R$ 700k.
  assert.equal(await page.locator('.property-card').count(),3);
  const matchingApartments = await page.locator('.property-card a[href^="imoveis/"]').evaluateAll(links => links.map(link => link.getAttribute('href')).sort());
  assert.deepEqual(matchingApartments, [
    'imoveis/apartamento-bertioga-70m2.html',
    'imoveis/apartamento-vicente-carvalho-ii-saoc-45m2.html',
    'imoveis/apartamento-vista-linda-65m2.html'
  ]);
  await page.locator('#tipo-filtro').selectOption('Aluguel');
  assert.equal(await page.locator('#preco-filtro').inputValue(),'');
  assert(!/700/.test(await page.locator('#busca').inputValue()),'old purchase budget is removed from the query');
  assert.match(await page.locator('#preco-label').innerText(), /R\$\/mês/);
  await page.locator('#preco-filtro').fill('9000');
  await page.locator('#preco-filtro').press('Tab');
  // The owner withdrew Bertioga's old rental; budget handling must still work.
  assert.equal(await page.locator('.property-card').count(),0);
  assert(await page.locator('.imoveis-empty').isVisible());
  await page.screenshot({path:path.join(output,`rental-search-${width}.png`)});
  await page.reload();
  assert.equal(await page.locator('#preco-filtro').inputValue(),'9000');
  await page.locator('#busca').fill('apartamento em Bertioga');
  assert.equal(await page.locator('#tipo-filtro').inputValue(),'Aluguel');
  await page.goto(origin+'/');
  const questions=await page.locator('.ai-q').evaluateAll(links=>links.map(a=>({url:a.href,question:a.textContent.split('"')[1]})));
  assert.equal(new Set(questions.map(q=>q.url)).size,4);
  for(const q of questions){
    await page.goto(q.url);
    assert.equal(await page.locator('label[for="msg"]').count(),1,'one accessible label for the question');
    assert.equal(await page.getByRole('textbox',{name:'Sua pergunta',exact:true}).count(),1);
    assert.equal(await page.locator('#msg').inputValue(),q.question);
    assert.equal(await page.locator('#chat .user').count(),0,'prefill never submits');
  }
}

async function contactAndCases(page, width) {
  await page.goto(origin + '/captura-leads.html', { waitUntil: 'load' });
  assert(!/Lead registrado|Finalizar pagamento/.test(await page.locator('body').innerText()));
  await page.getByRole('link', { name: 'Solicitar avaliação gratuita', exact: true }).click();
  await page.waitForURL('**/interesse.html?produto=avaliacao');
  assert.equal(await page.locator('#produto').inputValue(), 'avaliacao');
  assert.equal(await page.locator('#pagamento-opcional').isVisible(), false);

  for (const product of ['pricelabs', 'airbnb-booking', 'avaliacao']) {
    await page.goto(origin + '/interesse.html?produto=' + product, { waitUntil: 'load' });
    assert.equal(await page.locator('#produto').inputValue(), product);
    assert.equal(await page.locator('#pagto').getAttribute('required'), null);
    assert.equal(await page.locator('#pagamento-opcional').isVisible(), product !== 'avaliacao');
    assert.equal(await page.locator('#pagto').isDisabled(), product === 'avaliacao');
    await page.locator('#nome').fill('Teste local');
    await page.locator('#cidade').selectOption('Bertioga');
    assert.equal(await page.locator('#f').evaluate(form => form.checkValidity()), true, 'payment is optional');
    // Validate only: never submit this form or click its WhatsApp button.
    await noOverflow(page, `contact ${product} ${width}px`);
  }
  await page.locator('#produto').selectOption('pricelabs');
  await page.locator('#pagto').selectOption('Pix');
  await page.locator('#produto').selectOption('avaliacao');
  assert.equal(await page.locator('#pagto').inputValue(), '', 'free interest clears stale payment');
  assert.equal(await page.locator('#pagto').isDisabled(), true);
  await page.goto(origin + '/interesse.html?produto=%3Cscript%3Ealert(1)%3C%2Fscript%3E', { waitUntil: 'load' });
  assert.equal(await page.locator('#produto').inputValue(), '', 'unknown context ignored');
  await page.goto(origin + '/cases.html', { waitUntil: 'load' });
  assert.match(await page.locator('h1').innerText(), /Exemplos ilustrativos/i);
  const text = await page.locator('body').innerText();
  const indicators = page.locator('.metric').filter({ hasText: /^Métrica a observar:/i });
  assert.equal(await indicators.count(), 5, 'five illustrative scenarios describe indicators to observe');
  for (const indicator of await indicators.all()) assert(await indicator.isVisible());
  assert(!/métricas verificáveis/i.test(text), 'illustrative cases must not imply verified metrics');
  await noOverflow(page, `illustrative cases ${width}px`);
}

async function purposeTransitions(page) {
  const buying='comprar apartamento de 2 quartos em Bertioga até R$ 700 mil';
  const renting='alugar apartamento de 2 quartos em Bertioga até R$ 700 mil';
  for(const source of ['selector','text']) {
    await page.goto(origin+'/');
    await page.locator('#finalidade').selectOption('Venda');
    await page.locator('#q').fill(buying);
    if(source==='selector') await page.locator('#finalidade').selectOption('Aluguel');
    else await page.locator('#q').fill(renting);
    assert.equal(await page.locator('#finalidade').inputValue(),'Aluguel');
    const q=await page.locator('#q').inputValue();
    assert(!q.includes('700'),'home clears purchase budget on '+source+' change');
    assert(q.includes('Bertioga') && q.includes('2 quartos'),'home keeps city and bedrooms');
    assert.match(await page.locator('#home-search-status').innerText(),/Orçamento limpo/);
    await page.locator('#smartsearch button').click();
    await page.waitForURL('**/imoveis.html?**');
    assert.equal(await page.locator('#preco-filtro').inputValue(),'');
    assert.equal(await page.locator('#tipo-filtro').inputValue(),'Aluguel');
  }
  await page.goto(origin+'/imoveis.html?q='+encodeURIComponent(buying));
  assert.equal(await page.locator('#preco-filtro').inputValue(),'700000');
  await page.locator('#busca').fill(renting);
  assert.equal(await page.locator('#tipo-filtro').inputValue(),'Aluguel');
  assert.equal(await page.locator('#preco-filtro').inputValue(),'');
  assert.equal(new URL(page.url()).searchParams.get('preco_max'),'');
  assert.match(await page.locator('#search-status').innerText(),/Orçamento limpo/);
  await page.reload();
  assert.equal(await page.locator('#preco-filtro').inputValue(),'');
  // An initial, explicitly monthly rental query remains legitimate.
  await page.goto(origin+'/imoveis.html?q='+encodeURIComponent('alugar apartamento de 2 quartos em Bertioga até R$ 9 mil por mês'));
  assert.equal(await page.locator('#tipo-filtro').inputValue(),'Aluguel');
  assert.equal(await page.locator('#preco-filtro').inputValue(),'9000');
  assert.equal(await page.locator('.property-card').count(),0);
  assert(await page.locator('.imoveis-empty').isVisible());
  await page.locator('#busca').fill('comprar apartamento em Bertioga até R$ 9 mil');
  assert.equal(await page.locator('#tipo-filtro').inputValue(),'Venda');
  assert.equal(await page.locator('#preco-filtro').inputValue(),'');
  await page.goto(origin+'/imoveis.html?q='+encodeURIComponent(buying)+'&finalidade=Aluguel');
  assert.equal(await page.locator('#tipo-filtro').inputValue(),'Aluguel');
  assert.equal(await page.locator('#preco-filtro').inputValue(),'');
  assert.match(await page.locator('#search-status').innerText(),/texto e a finalidade do link eram diferentes/);
}


async function houseListing(page,width){
  await page.goto(origin+'/imoveis/casa-terrea-bertioga-675m2.html',{waitUntil:'load'});
  assert.equal(await page.locator('.gallery img').count(),20);
  assert.match(await page.locator('.price').innerText(),/1\.800\.000/);
  assert.match(await page.locator('#rental-results').innerText(),/44\.100,00/);
  await page.locator('#occupancy').fill('0');
  assert.match(await page.locator('#rental-results').innerText(),/-.*21\.600,00/);
  assert.match(await page.locator('#rental-results').innerText(),/Não há retorno/);
  await page.locator('#rate').fill('-3');
  assert.match(await page.locator('#value-results').innerText(),/1\.545\.721,25/);
  await page.locator('#occupancy').fill('30');
  await page.locator('#rate').fill('3');
  await noOverflow(page,`house listing ${width}px`);
  await page.locator('.gallery img').evaluateAll(images=>images.forEach(img=>{img.loading='eager';}));
  await page.waitForFunction(()=>Array.from(document.querySelectorAll('.gallery img')).every(img=>img.complete&&img.naturalWidth>0));
  const wa=await page.locator('.hero a.cta').first().getAttribute('href');
  assert(wa.startsWith('https://wa.me/5511954346288?text='));
  await page.screenshot({path:path.join(output,`house-${width}.png`)});
  await page.locator('a.back').click();
  await page.waitForURL(url => url.pathname === '/imoveis.html');
  const card = page.locator('#lista-imoveis .property-card').filter({
    has: page.locator('a[href="imoveis/casa-terrea-bertioga-675m2.html"]')
  });
  await card.first().waitFor({ state: 'visible' });
  assert.equal(await card.count(),1);assert.match(await card.innerText(),/1\.800\.000/);
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const launch = { headless: true };
  if (process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE) launch.executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE;
  const browser = await chromium.launch(launch);
  try {
    for (const width of [375, 390, 1280]) {
      const { context, sideEffects } = await offlineContext(browser, width);
      const page = await context.newPage();
      page.setDefaultTimeout(15000);
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      try {
        await homepage(page, width);
        await searchJourney(page, width);
        await purposeTransitions(page);
        await contactAndCases(page, width);
        await houseListing(page,width);
        await appCatalog(browser, page, width);
        await turnoverFromHome(page, width);
        await blackFriday(page, width);
        assert.deepEqual(sideEffects, [], 'no external navigation or non-GET requests');
        assert.deepEqual(errors, [], 'no uncaught JavaScript errors');
        results.push({ width, status: 'passed', checks: ['app catalog objectives, keyboard, return and no-JS', 'home layout', 'interval between reservations discovery', 'Black Friday focus, disclosure, names and seven anchors', 'responsive footer', 'menu escape/repeat', 'single product comparison', 'search parse/zero/positive', 'reload/back/forward/reset', 'legacy query', 'contextual contact', 'optional payment', 'illustrative cases','house catalog/photos/calculators'] });
        console.log(`${width}px: homepage, search, contact and cases passed`);
      } catch (error) {
        results.push({ width, status: 'failed', message: error.message, errors });
        await page.screenshot({ path: path.join(output, `failure-${width}.png`), fullPage: true }).catch(() => {});
        throw error;
      } finally {
        fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify(results, null, 2));
        await context.close();
      }
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

