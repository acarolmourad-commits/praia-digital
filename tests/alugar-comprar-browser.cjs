// Regression suite for CI. Only checked-out fixtures are served; no user data leaves the browser.
const { chromium } = require('playwright');
const { AxeBuilder } = require('@axe-core/playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const artifacts = '/tmp/pd-rent-buy-previews';
fs.mkdirSync(artifacts, { recursive: true });
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of [320, 390, 768, 1280]) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, locale: 'pt-BR', reducedMotion: 'reduce' });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.hostname !== 'pd.test') return route.abort();
        const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
        if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return route.fulfill({ status: 404, body: '' });
        const contentType = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' }[path.extname(file)] || 'application/octet-stream';
        return route.fulfill({ status: 200, contentType, body: fs.readFileSync(file) });
      });
      await page.goto('https://pd.test/apps/alugar-ou-comprar/index.html');
      await page.locator('#res').waitFor({ state: 'visible' });
      assert.equal(await page.getByRole('button', { name: 'Comparar patrimônios' }).isEnabled(), true);
      assert.match(await page.locator('#rParc').innerText(), /4\.964,46/);
      assert.match(await page.locator('#owner-wealth').innerText(), /470\.301,80/);
      assert.match(await page.locator('#renter-wealth').innerText(), /624\.733,08/);
      const overflow = () => page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
      assert.equal(await overflow(), false, `initial horizontal overflow at ${width}px`);
      await page.screenshot({ path: path.join(artifacts, `top-${width}.png`) });
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('.rb-skip').evaluate(element => element === document.activeElement), true);
      const skip = await page.locator('.rb-skip').boundingBox();
      assert.ok(skip.x >= 0 && skip.y >= 0, `visible skip link at ${width}px`);
      await page.keyboard.press('Enter');
      assert.equal(await page.locator('#main').evaluate(element => element === document.activeElement), true);
      assert.ok(await page.locator('#valor').evaluate(element => parseFloat(getComputedStyle(element).fontSize) >= 16));
      await page.getByLabel('Valor do imóvel (R$)', { exact: true }).fill('0');
      assert.equal(await page.locator('#res').isVisible(), false);
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.equal(await page.locator('#valor').getAttribute('aria-invalid'), 'true');
      assert.equal(await page.locator('#valor').evaluate(element => element === document.activeElement), true);
      assert.doesNotMatch(await page.locator('#result-live').innerText(), /Infinity|NaN/);
      await page.getByRole('button', { name: 'Restaurar exemplo' }).click();
      await page.getByLabel('Prazo do financiamento (anos)', { exact: true }).fill('-1');
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.equal(await page.locator('#res').isVisible(), false);
      await page.getByRole('button', { name: 'Restaurar exemplo' }).click();
      await page.getByLabel('Entrada disponível (R$)', { exact: true }).fill('700000');
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.match(await page.locator('#entrada-error').innerText(), /não pode superar/);
      await page.getByLabel('Entrada disponível (R$)', { exact: true }).fill('595000');
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.match(await page.locator('#rate-description').innerText(), /Compra à vista/);
      assert.match(await page.locator('#rParc').innerText(), /0,00/);
      await page.getByRole('button', { name: 'Restaurar exemplo' }).click();
      await page.getByText('Financiamento: sistema, taxa, correção e seguros', { exact: true }).click();
      await page.getByLabel('Sistema de amortização', { exact: true }).selectOption('SAC');
      await page.getByLabel('Tipo de taxa anual', { exact: true }).selectOption('effective');
      await page.getByLabel('Correção anual do saldo devedor (%)', { exact: true }).fill('2');
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.match(await page.locator('#rate-description').innerText(), /SAC.*efetivos.*2%/);
      assert.equal(await page.locator('#result-title').evaluate(element => element === document.activeElement), true);
      const resultPosition = await page.locator('#result-title').boundingBox();
      assert.ok(resultPosition.y >= 70 && resultPosition.y < 700, `result focus below header at ${width}px`);
      await page.getByText('Como o resultado muda com as taxas?', { exact: true }).click();
      assert.equal(await overflow(), false, `sensitivity overflow at ${width}px`);
      assert.equal(await page.locator('#sensitivity-body tr:first-child td:nth-child(2)').evaluate(element => getComputedStyle(element).whiteSpace), 'nowrap');
      const sensitivityRegion = page.getByRole('region', { name: 'Tabela de sensibilidade das taxas, com rolagem horizontal' });
      await sensitivityRegion.scrollIntoViewIfNeeded();
      await sensitivityRegion.screenshot({ path: path.join(artifacts, `sensitivity-${width}.png`) });
      if (width < 520) {
        await sensitivityRegion.focus();
        await page.keyboard.press('End');
        await page.keyboard.press('ArrowRight');
        assert.ok(await sensitivityRegion.evaluate(element => element.scrollWidth > element.clientWidth), 'sensitivity stays in a local scroll region');
        await sensitivityRegion.evaluate(element => { element.scrollLeft = element.scrollWidth; });
        assert.ok(await sensitivityRegion.evaluate(element => element.scrollLeft > 0), 'remaining columns are reachable');
        await sensitivityRegion.screenshot({ path: path.join(artifacts, `sensitivity-end-${width}.png`) });
      }
      await page.locator('#res').screenshot({ path: path.join(artifacts, `result-${width}.png`) });
      await page.getByText('Acompanhar patrimônio ano a ano', { exact: true }).click();
      assert.equal(await overflow(), false, `yearly table leaks beyond its container at ${width}px`);
      assert.equal(await page.locator('#yearly-body tr').count(), 10);
      await page.getByText('Custos de aquisição, manutenção e venda', { exact: true }).click();
      await page.getByLabel('Custos de aquisição (% do preço)', { exact: true }).fill('31');
      await page.getByText('Custos de aquisição, manutenção e venda', { exact: true }).click();
      await page.getByRole('button', { name: 'Comparar patrimônios' }).click();
      assert.equal(await page.locator('#advanced-costs').evaluate(element => element.open), true);
      assert.equal(await page.locator('#custoCompra').evaluate(element => element === document.activeElement), true);
      await page.getByRole('button', { name: 'Restaurar exemplo' }).click();
      assert.equal(await page.locator('#result-label').innerText(), 'Exemplo ilustrativo');
      // Show every accordion so the accessibility audit covers advanced controls and tables.
      for (const details of await page.locator('#main details').all()) {
        if (!(await details.evaluate(element => element.open))) await details.locator('summary').click();
      }
      const accessibility = await new AxeBuilder({ page }).include('#main').withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      fs.writeFileSync(path.join(artifacts, `accessibility-${width}.json`), JSON.stringify(accessibility, null, 2));
      assert.deepEqual(accessibility.violations.map(issue => ({ id: issue.id, nodes: issue.nodes.map(node => node.target) })), [], `WCAG A/AA checks at ${width}px`);
      if (width <= 768) {
        await page.getByRole('button', { name: 'Abrir menu de navegação' }).click();
        assert.equal(await page.locator('.pd-site-menu').isVisible(), true);
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.pd-site-menu').isVisible(), false);
      }
      assert.deepEqual(errors, [], `JavaScript errors at ${width}px`);
      console.log(`PASS ${width}px: layout, keyboard, validation, cash/financing, SAC, effective rate, indexation, tables, reset, menu, axe`);
      await context.close();
    }
    const nojs = await browser.newPage({ javaScriptEnabled: false });
    await nojs.route('**/*', route => {
      const url = new URL(route.request().url());
      if (url.hostname !== 'pd.test') return route.abort();
      const file = path.resolve(root, '.' + url.pathname);
      if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return route.fulfill({ status: 404, body: '' });
      return route.fulfill({ contentType: file.endsWith('.css') ? 'text/css' : 'text/html', body: fs.readFileSync(file) });
    });
    await nojs.goto('https://pd.test/apps/alugar-ou-comprar/index.html');
    assert.equal(await nojs.getByRole('button', { name: 'Comparar patrimônios' }).isEnabled(), false);
    assert.match(await nojs.locator('noscript').innerText(), /Ative JavaScript/);
    assert.equal(await nojs.locator('#rent-buy-form [name]').count(), 0);
    await nojs.close();
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
