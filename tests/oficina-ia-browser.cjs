// Offline regression: no real customer data or network submissions.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const origin = 'https://oficina.test';
const appUrl = `${origin}/apps/oficina-ia-imobiliaria/`;

async function fixture(browser, { javaScriptEnabled = true, failModule = false } = {}) {
  const context = await browser.newContext({ javaScriptEnabled, viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  const documents = [];
  const unexpected = [];
  page.on('request', request => {
    if (request.isNavigationRequest() && request.frame() === page.mainFrame()) documents.push(request.url());
  });
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    if (url.origin !== origin || url.search || route.request().method() !== 'GET') {
      unexpected.push({ url: url.href, method: route.request().method() });
      return route.abort();
    }
    if (failModule && url.pathname.endsWith('/core.mjs')) return route.abort();
    const rel = url.pathname.endsWith('/') ? `${url.pathname}index.html` : url.pathname;
    const file = path.resolve(root, `.${rel}`);
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      return route.fulfill({ status: 404, body: '' });
    }
    const contentType = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css' }[path.extname(file)] || 'application/octet-stream';
    return route.fulfill({ contentType, body: fs.readFileSync(file) });
  });
  await page.goto(appUrl, { waitUntil: 'networkidle' });
  return { context, page, documents, unexpected };
}

async function assertNoNavigation(page, documents, unexpected) {
  // Give an accidental native navigation a frame to begin before checking it.
  await page.waitForTimeout(100);
  assert.equal(page.url(), appUrl);
  assert.deepEqual(documents, [appUrl]);
  assert.deepEqual(unexpected, []);
}

(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.CHROMIUM_EXECUTABLE_PATH } : {}) });
  try {
    for (const mode of [{ javaScriptEnabled: false }, { failModule: true }]) {
      const { context, page, documents, unexpected } = await fixture(browser, mode);
      try {
        assert.equal(await page.locator('[data-oficina-control]:enabled').count(), 0);
        assert(await page.locator('#startup-status').isVisible());
        assert(await page.locator('#startup-status a').isVisible());
        if (mode.javaScriptEnabled === false) assert(await page.locator('noscript').isVisible());
        // Exercise the second defense independently, including submit() which bypasses listeners.
        await page.evaluate(() => {
          for (const control of document.querySelectorAll('[data-oficina-control]')) control.disabled = false;
          for (const control of document.querySelectorAll('input, textarea')) control.value = 'Synthetic privacy regression';
        });
        for (const id of ['listing', 'followup']) {
          await page.locator(`#${id} button[type=submit]`).click();
          await assertNoNavigation(page, documents, unexpected);
          await page.locator(`#${id}`).evaluate(form => HTMLFormElement.prototype.requestSubmit.call(form));
          await assertNoNavigation(page, documents, unexpected);
          await page.locator(`#${id}`).evaluate(form => HTMLFormElement.prototype.submit.call(form));
          await assertNoNavigation(page, documents, unexpected);
        }
        await page.locator('#listing input[name=tipo]').press('Enter');
        await assertNoNavigation(page, documents, unexpected);
        console.log(`PASS: ${mode.javaScriptEnabled === false ? 'JavaScript disabled' : 'module import failed'} — disabled controls, visible help, no native submission or query string`);
      } finally { await context.close(); }
    }

    const { context, page, documents, unexpected } = await fixture(browser);
    try {
      assert.equal(await page.locator('[data-oficina-control]:disabled').count(), 0);
      assert.equal(await page.locator('#startup-status').isVisible(), false);
      await page.getByLabel('Tipo do imóvel', { exact: true }).fill('Apartamento');
      await page.getByLabel('Cidade', { exact: true }).fill('Bertioga');
      await page.getByLabel('Finalidade', { exact: true }).fill('Venda');
      const literal = '<img src="x" onerror="alert(1)">';
      await page.getByLabel('Diferenciais confirmados', { exact: true }).fill(literal);
      await page.getByRole('button', { name: 'Montar briefing e prompt', exact: true }).click();
      const output = await page.locator('#output').inputValue();
      assert.match(output, /4 de 12 campos preenchidos/);
      assert.match(output, /NÃO INFORMADO/);
      assert(output.includes(literal));
      assert.equal(await page.locator('img[src="x"]').count(), 0);
      assert(await page.locator('#output').evaluate(element => element === document.activeElement));
      await page.getByRole('button', { name: 'Conferir campos faltantes', exact: true }).click();
      assert.match(await page.locator('#output').inputValue(), /REVISÃO DE COMPLETUDE/);
      await page.getByLabel('Contexto confirmado', { exact: true }).fill('Teste fictício de encerramento.');
      await page.locator('#followup select[name="etapa"]').selectOption('encerrar');
      await page.getByRole('button', { name: 'Preparar modelo de e-mail', exact: true }).click();
      assert.match(await page.locator('#output').inputValue(), /NÃO ENVIADO/);
      assert.match(await page.locator('#output').inputValue(), /não enviar novas mensagens/);
      await page.getByRole('button', { name: 'Limpar tudo', exact: true }).click();
      assert.equal(await page.locator('#output').inputValue(), '');
      assert.equal(await page.getByLabel('Cidade', { exact: true }).inputValue(), '');
      assert.equal(await page.getByLabel('Contexto confirmado', { exact: true }).inputValue(), '');
      assert.equal(await page.locator('[data-oficina-control]:disabled').count(), 0);
      await assertNoNavigation(page, documents, unexpected);
      console.log('PASS: initialized app — briefing, literal rendering, missing fields, follow-up draft, focus and reset stay local');
    } finally { await context.close(); }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
