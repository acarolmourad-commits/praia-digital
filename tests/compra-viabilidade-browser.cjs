// CI browser regression suite. All resources are served from the checked-out repo.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const artifacts = '/tmp/pd-compra-previews';
fs.mkdirSync(artifacts, { recursive: true });
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of [320, 390, 768, 1280]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.route('**/*', async route => {
        const url = new URL(route.request().url());
        if (url.hostname !== 'pd.test' && !(url.hostname === 'praia.digital' && url.pathname === '/partials/footer.html')) return route.abort();
        const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
        if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) return route.fulfill({ status: 404, body: '' });
        const type = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' }[path.extname(file)] || 'application/octet-stream';
        return route.fulfill({ status: 200, contentType: type, body: fs.readFileSync(file) });
      });
      await page.goto('https://pd.test/ferramentas/vale-a-pena-comprar-2026.html');
      await page.locator('[data-result="owner-month"]').waitFor();
      await page.getByLabel('Seu e-mail para receber novidades', { exact: true }).waitFor();
      assert.equal(await page.locator('.whatsapp-float').isVisible(), false);
      assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), 'auto');
      const overflow = () => page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
      assert.equal(await overflow(), false, `initial horizontal overflow ${width}`);
      assert.ok((await page.locator('[data-result="owner-month"]').innerText()).includes('4.689,65'));
      assert.doesNotMatch(await page.locator('.v-hero').innerText(), /comprar(?=este)|compra(?=cabe)/);
      await page.screenshot({ path: path.join(artifacts, `top-${width}.png`) });
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('.v-skip').evaluate(e => e === document.activeElement), true);
      const skip = await page.locator('.v-skip').boundingBox();
      assert.ok(skip.x >= 0 && skip.y >= 0, `visible skip link ${width}`);
      await page.keyboard.press('Enter');
      assert.equal(await page.locator('#main').evaluate(e => e === document.activeElement), true);
      assert.ok(await page.locator('#price').evaluate(e => parseFloat(getComputedStyle(e).fontSize) >= 16));
      await page.getByLabel('Preço do imóvel (R$)', { exact: true }).fill('');
      assert.equal(await page.locator('.v-result-amount').count(), 0);
      assert.equal(await page.locator('#price').getAttribute('aria-invalid'), 'true');
      await page.getByRole('button', { name: 'Atualizar análise' }).click();
      assert.equal(await page.locator('#price').evaluate(e => e === document.activeElement), true);
      await page.getByLabel('Preço do imóvel (R$)', { exact: true }).fill('500000');
      await page.getByLabel('Entrada (R$)', { exact: true }).fill('600000');
      assert.equal(await page.locator('.v-result-amount').count(), 0);
      await page.getByLabel('Forma de compra', { exact: true }).selectOption('avista');
      assert.equal(await page.locator('#entry').isVisible(), false);
      assert.equal(await page.locator('.v-result-amount').count(), 1);
      await page.getByLabel('Forma de compra', { exact: true }).selectOption('financiado');
      assert.equal(await page.locator('.v-result-amount').count(), 0);
      await page.getByLabel('Entrada (R$)', { exact: true }).fill('100000');
      await page.getByLabel('Qual é o seu objetivo?', { exact: true }).selectOption('temporada');
      assert.ok((await page.locator('#result').innerText()).includes('16,5%'));
      await page.getByLabel('Noites ocupadas por ano', { exact: true }).fill('366');
      assert.equal(await page.locator('.v-result-amount').count(), 0);
      await page.getByLabel('Noites ocupadas por ano', { exact: true }).fill('150');
      await page.getByLabel('Preço do imóvel (R$)', { exact: true }).fill('10000000');
      assert.ok((await page.locator('#result').innerText()).includes('0,83%'));
      assert.equal(await overflow(), false, `large result overflow ${width}`);
      await page.getByLabel('Qual é o seu objetivo?', { exact: true }).selectOption('anual');
      assert.equal(await page.locator('#nights').isVisible(), false);
      assert.equal(await page.locator('#annualRent').isVisible(), true);
      await page.getByRole('button', { name: 'Restaurar exemplo' }).click();
      await page.waitForFunction(() => document.getElementById('goal').value === 'moradia' && document.getElementById('result').textContent.includes('4.689,65'));
      await page.getByRole('button', { name: 'Atualizar análise' }).click();
      assert.equal(await page.locator('#result-title').evaluate(e => e === document.activeElement), true);
      const resultPosition = await page.locator('#result-title').boundingBox();
      assert.ok(resultPosition.y >= 70 && resultPosition.y < 700, `result visible below fixed header ${width}`);
      await page.screenshot({ path: path.join(artifacts, `result-${width}.png`) });
      await page.getByText('Se a valorização mudar?', { exact: true }).click();
      assert.equal(await overflow(), false, `sensitivity overflow ${width}`);
      await page.locator('.v-summary').screenshot({ path: path.join(artifacts, `summary-${width}.png`) });
      if (width <= 768) {
        await page.getByRole('button', { name: 'Abrir menu de navegação' }).click();
        assert.equal(await page.locator('.pd-site-menu').isVisible(), true);
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.pd-site-menu').isVisible(), false);
      }
      assert.deepEqual(errors, [], `JavaScript errors at ${width}`);
      console.log(`PASS ${width}px: layout, keyboard, invalid values, cash/financed, three goals, reset, result focus, menu`);
      await page.close();
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
