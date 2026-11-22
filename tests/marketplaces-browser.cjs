const {chromium} = require('playwright');
const fs = require('node:fs'), path = require('node:path'), os = require('node:os');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(root, 'automation/marketplaces/informativos-revisados.json')));
const files = ['novidades-airbnb-booking.html', ...data.articles.map(a => a.file)];

async function checkSellerHelp(browser) {
  const markup = fs.readFileSync(path.join(root, 'suporte-marketplaces.html'), 'utf8');
  for (const width of [320, 390, 1280]) {
    const page = await browser.newPage({viewport: {width, height: 900}, hasTouch: width <= 390});
    await page.route('**/*', route => route.abort());
    await page.setContent(markup);
    const search = page.getByRole('searchbox', {name: 'Buscar nas perguntas frequentes'});
    const status = page.getByRole('status');
    const rows = page.locator('#lista details');
    const clear = page.getByRole('button', {name: 'Limpar', exact: true});
    const firstSummary = rows.first().locator('summary');
    assert.equal(await status.textContent(), '13 perguntas disponíveis.');
    assert.equal(await page.locator('#lista details:visible').count(), 13);
    assert.equal(await rows.locator('summary:visible').count(), 13);
    await firstSummary.focus();
    await page.keyboard.press('Enter');
    assert.equal(await firstSummary.evaluate(el => el.parentElement.open), true);
    await search.fill('  CEST  ');
    assert.equal(await status.textContent(), '1 pergunta encontrada.');
    assert.equal(await page.locator('#lista details:visible').count(), 1);
    const visibleSummary = page.locator('#lista details:visible summary');
    assert.match(await visibleSummary.textContent(), /NCM, CEST e CFOP/);
    await visibleSummary.focus();
    await page.keyboard.press('Enter');
    assert.equal(await visibleSummary.evaluate(el => !el.parentElement.open && document.activeElement === el), true);
    await search.fill('  prazo   estoque ');
    assert.match(await page.locator('#lista details:visible summary').textContent(), /primeiro pedido/);
    await search.fill('documentacao');
    assert.equal(await status.textContent(), '1 pergunta encontrada.');
    await search.fill('termo inexistente zz');
    assert.equal(await page.locator('#lista details:visible').count(), 0);
    assert.match(await status.textContent(), /Nenhuma pergunta encontrada/);
    if (width <= 390) await clear.tap();
    else {
      await search.focus();
      await page.keyboard.press('Tab');
      assert.equal(await clear.evaluate(el => document.activeElement === el), true);
      await page.keyboard.press('Enter');
    }
    assert.equal(await search.inputValue(), '');
    assert.equal(await search.evaluate(el => document.activeElement === el), true);
    assert.equal(await status.textContent(), '13 perguntas disponíveis.');
    assert.equal(await page.locator('#lista details[open]').count(), 1);
    assert.equal(await firstSummary.evaluate(el => el.parentElement.open), true);
    assert.equal(await page.locator('header .logo').getAttribute('href'), '/');
    assert.equal(await page.locator('footer a').first().getAttribute('href'), '/apps/guia-de-uso.html#vender');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'Seller help overflow at ' + width);
    await page.close();
  }
  const page = await browser.newPage({javaScriptEnabled: false, viewport: {width: 320, height: 900}});
  await page.route('**/*', route => route.abort());
  await page.setContent(markup);
  assert.equal(await page.locator('#faq-search').isVisible(), false);
  assert.equal(await page.locator('#lista details:visible').count(), 13);
  await page.locator('#lista summary').first().click();
  assert.equal(await page.locator('#lista details[open]').count(), 1);
  await page.close();
  console.log('Seller help: 13 FAQs, label and live status, token filters, keyboard/touch reset, 320/390/1280 px, no-JS accordion.');
}

(async () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'marketplaces-preview-'));
  for (const file of ['partials/header.html', 'assets/css/pd-navigation.css', 'js/pd-navigation.js', ...files.map(f => 'blog/' + f)]) {
    const target = path.join(temp, file);
    fs.mkdirSync(path.dirname(target), {recursive: true});
    fs.copyFileSync(path.join(root, file), target);
  }
  execFileSync('python3', [path.join(root, 'scripts/build-navigation.py'), '--root', temp]);
  const browser = await chromium.launch({headless: true, executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    for (const width of [360, 390, 768, 1280]) {
      const page = await browser.newPage({viewport: {width, height: 900}});
      await page.route('**/*', r => r.abort());
      for (const file of files) {
        await page.setContent(fs.readFileSync(path.join(temp, 'blog', file), 'utf8'));
        await page.addStyleTag({content: fs.readFileSync(path.join(root, 'assets/css/pd-navigation.css'), 'utf8')});
        await page.addScriptTag({content: fs.readFileSync(path.join(root, 'js/pd-navigation.js'), 'utf8')});
        assert.equal(await page.locator('h1').count(), 1, file);
        assert.equal(await page.locator('header').count(), 1, 'One shared header: ' + file);
        assert.equal(await page.locator('form').count(), 0, 'No misleading signup or data collection');
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'No overflow ' + width + ': ' + file);
        if (file === files[0]) {
          assert.equal(await page.locator('#revisados .card').count(), 4);
          for (const id of ['revisados', 'arquivo', 'monitoramento']) assert.equal(await page.locator('#' + id).count(), 1);
          if (width <= 1080) {
            await page.locator('.pd-site-toggle').click();
            assert.equal(await page.locator('.pd-site-menu').isVisible(), true);
            await page.keyboard.press('Escape');
            assert.equal(await page.locator('.pd-site-menu').isVisible(), false);
          }
          if ([390, 1280].includes(width)) await page.screenshot({path: path.join(os.tmpdir(), 'marketplaces-index-' + width + '.png'), fullPage: true});
        } else {
          assert.equal(await page.getByRole('heading', {name: 'Disponibilidade e impacto no Brasil', exact: true}).count(), 1);
          assert.equal(await page.getByRole('heading', {name: 'Fontes e datas', exact: true}).count(), 1);
        }
        if (width === 390 && file === data.articles[0].file) await page.screenshot({path: path.join(os.tmpdir(), 'marketplaces-tools-390.png'), fullPage: true});
      }
      await page.close();
    }
    await checkSellerHelp(browser);
    console.log('Marketplace browser checks passed: 11 pages at 4 widths, published navigation, menu dismissal, sources, and no overflow.');
  } finally {
    await browser.close();
    fs.rmSync(temp, {recursive: true, force: true});
  }
})().catch(error => {console.error(error); process.exit(1);});
