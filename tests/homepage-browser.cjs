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

async function offlineContext(browser, width) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, serviceWorkers: 'block' });
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

async function homepage(page, width) {
  await page.goto(origin + '/', { waitUntil: 'load' });
  const header = page.locator('.pd-site-header');
  await header.waitFor();
  assert.equal(await header.count(), 1, 'use the navigation-built artifact');
  assert.equal(await page.locator('main').count(), 1);
  assert.equal(await page.locator('h1').count(), 1);
  assert.equal(await page.locator('#produtos-comparacao').count(), 1);
  assert.equal(await page.locator('#planos-praia-digital').count(), 0, 'legacy plan injection must not duplicate comparison');
  assert.equal(await page.locator('#apps').count(), 0, 'legacy apps injection must not duplicate curated home content');
  assert.equal(await page.locator('#analise a[href="/apps/"]').count(), 1);
  assert.match(await page.locator('#produtos-comparacao').innerText(), /39\s*\/\s*imóvel\s*\/\s*mês/);
  assert.match(await page.locator('#produtos-comparacao').innerText(), /499\s*\/\s*anúncio\s*\/\s*plataforma/);
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
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await firstGroup.getAttribute('aria-expanded'), 'false');
  }
  await page.screenshot({ path: path.join(output, `home-hero-${width}.png`) });
}

async function searchJourney(page, width) {
  const query = 'apartamento em Santos com 2 quartos até R$ 500 mil';
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
}

async function contactAndCases(page, width) {
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
  assert.match(text, /Hipótese:/i);
  assert(!/métricas verificáveis/i.test(text), 'illustrative cases must not imply verified metrics');
  await noOverflow(page, `illustrative cases ${width}px`);
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
        await contactAndCases(page, width);
        assert.deepEqual(sideEffects, [], 'no external navigation or non-GET requests');
        assert.deepEqual(errors, [], 'no uncaught JavaScript errors');
        results.push({ width, status: 'passed', checks: ['home layout', 'responsive footer', 'menu escape/repeat', 'single product comparison', 'search parse/zero/positive', 'reload/back/forward/reset', 'legacy query', 'contextual contact', 'optional payment', 'illustrative cases'] });
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
