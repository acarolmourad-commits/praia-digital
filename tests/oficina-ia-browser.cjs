// Offline regression: no real customer data or network submissions.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const origin = 'https://oficina.test';
const appUrl = `${origin}/apps/oficina-ia-imobiliaria/`;
const moduleVersion = '?v=' + createHash('sha256').update(fs.readFileSync(path.join(root, 'apps/oficina-ia-imobiliaria/app.mjs'))).digest('hex').slice(0, 12);
const networkStyleVersion = '?v=' + createHash('sha256').update(fs.readFileSync(path.join(root, 'css/app-network.css'))).digest('hex').slice(0, 12);

async function fixture(browser, { javaScriptEnabled = true, failModule = false, width = 390, legacyMarkup = false } = {}) {
  const context = await browser.newContext({ javaScriptEnabled, viewport: { width, height: 844 } });
  const page = await context.newPage();
  const documents = [];
  const unexpected = [];
  page.on('request', request => {
    if (request.isNavigationRequest() && request.frame() === page.mainFrame()) documents.push(request.url());
  });
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    const versionedModule = url.pathname === '/apps/oficina-ia-imobiliaria/app.mjs' && url.search === moduleVersion;
    const versionedStyle = url.pathname === '/css/app-network.css' && url.search === networkStyleVersion;
    if (url.origin !== origin || (url.search && !versionedModule && !versionedStyle) || route.request().method() !== 'GET') {
      unexpected.push({ url: url.href, method: route.request().method() });
      return route.abort();
    }
    if (failModule && url.pathname.endsWith('/core.mjs')) return route.abort();
    // A cached legacy URL must never satisfy a fresh page's module request.
    if (url.pathname.endsWith('/app.mjs') && !versionedModule) {
      return route.fulfill({ contentType: 'text/javascript', body: '// Simulated stale cached module: no new handlers.' });
    }
    const rel = url.pathname.endsWith('/') ? `${url.pathname}index.html` : url.pathname;
    const file = path.resolve(root, `.${rel}`);
    if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      return route.fulfill({ status: 404, body: '' });
    }
    const contentType = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css' }[path.extname(file)] || 'application/octet-stream';
    const body = legacyMarkup && file.endsWith('oficina-ia-imobiliaria/index.html')
      ? fs.readFileSync(file, 'utf8').replace(/<span id="result-kind">.*?<\/span>/, '')
      : fs.readFileSync(file);
    return route.fulfill({ contentType, body });
  });
  await page.goto(appUrl, { waitUntil: 'networkidle' });
  assert.equal(await page.locator('.pd-route-link a').evaluate(el => getComputedStyle(el).minHeight), '44px', 'The current shared style must load for the route link.');
  return { context, page, documents, unexpected };
}

async function assertNoNavigation(page, documents, unexpected) {
  // Give an accidental native navigation a frame to begin before checking it.
  await page.waitForTimeout(100);
  assert.equal(page.url(), appUrl);
  assert.deepEqual(documents, [appUrl]);
  assert.deepEqual(unexpected, []);
}

async function assertCurrentExports(browser, width) {
  const { context, page, documents, unexpected } = await fixture(browser, { width });
  const downloads = [];
  page.on('download', download => downloads.push(download));
  try {
    // Intercept only the local clipboard; no permission prompts or real contacts.
    await page.evaluate(() => {
      window.testCopies = [];
      window.rejectCopy = false;
      window.deferCopy = false;
      Object.defineProperty(navigator, 'clipboard', { configurable: true, value: {
        writeText: async text => {
          if (window.rejectCopy) throw new Error('Synthetic clipboard denial');
          if (window.deferCopy) await new Promise(resolve => { window.resolveCopy = resolve; });
          window.testCopies.push(text);
        }
      } });
    });
    const copy = page.getByRole('button', { name: 'Copiar texto', exact: true });
    const download = page.getByRole('button', { name: 'Baixar TXT', exact: true });
    const generate = page.getByRole('button', { name: 'Montar briefing e prompt', exact: true });
    const output = page.locator('#output');
    const status = page.locator('#status');
    await copy.click();
    assert.match(await status.textContent(), /Gere um resultado antes de copiar/);
    await page.getByLabel('Tipo do imóvel', { exact: true }).fill('Apartamento fictício');
    await page.getByLabel('Cidade', { exact: true }).fill('Bertioga');
    await page.getByLabel('Finalidade', { exact: true }).fill('Venda fictícia');
    const price = page.getByLabel('Preço e periodicidade', { exact: true });
    await price.fill('R$ 600.000 — teste');
    await generate.click();
    const oldText = await output.inputValue();
    await price.fill('R$ 700.000 — teste');
    assert.match(await status.textContent(), /foram alterados/);
    assert.equal(await output.inputValue(), oldText, 'preserve the draft for review');
    await copy.click();
    await download.click();
    await page.waitForTimeout(100);
    assert.deepEqual(await page.evaluate(() => window.testCopies), []);
    assert.equal(downloads.length, 0, 'outdated result must not create a download');

    // Editing the old output alone must not bypass the changed source fields.
    await output.fill('Revisão manual fictícia');
    await copy.click();
    assert.deepEqual(await page.evaluate(() => window.testCopies), []);
    await generate.click();
    assert.match(await output.inputValue(), /R\$ 700\.000/);
    assert.doesNotMatch(await output.inputValue(), /R\$ 600\.000/);
    await copy.click();
    assert.equal(await page.evaluate(() => window.testCopies.at(-1)), await output.inputValue());

    // Editing the other form does not invalidate a briefing.
    await page.getByLabel('Contexto confirmado', { exact: true }).fill('Contexto fictício.');
    await copy.click();
    assert.match(await status.textContent(), /Texto copiado/);
    const edited = (await output.inputValue()) + '\nRevisão manual fictícia.';
    await output.fill(edited);
    const downloadEvent = page.waitForEvent('download');
    await download.click();
    const file = await downloadEvent;
    assert.equal(fs.readFileSync(await file.path(), 'utf8'), edited);
    assert.equal(file.suggestedFilename(), 'praia-digital-briefing.txt');
    assert.equal(await page.locator('#result-kind').textContent(), 'Briefing e prompt');

    // A rejected clipboard request keeps the manual-copy fallback functional.
    await page.evaluate(() => { window.rejectCopy = true; });
    await copy.click();
    assert.match(await status.textContent(), /Selecionei o texto/);
    assert.deepEqual(await output.evaluate(el => [el.selectionStart, el.selectionEnd]), [0, edited.length]);
    await page.evaluate(() => { window.rejectCopy = false; window.deferCopy = true; });
    await copy.click();
    await price.fill('R$ 800.000 — teste');
    await page.evaluate(() => window.resolveCopy());
    assert.match(await status.textContent(), /foram alterados/, 'pending copy cannot erase a newer warning');
    await page.evaluate(() => { window.deferCopy = false; });

    // Reverting the source values restores the existing manually reviewed text.
    await price.fill('R$ 700.000 — teste');
    await copy.click();
    assert.equal(await page.evaluate(() => window.testCopies.at(-1)), edited);
    await page.getByRole('button', { name: 'Conferir campos faltantes', exact: true }).click();
    const checklistEvent = page.waitForEvent('download');
    await download.click();
    const checklistFile = await checklistEvent;
    assert.equal(checklistFile.suggestedFilename(), 'praia-digital-checklist.txt');
    assert.equal(fs.readFileSync(await checklistFile.path(), 'utf8'), await output.inputValue());
    await price.fill('');
    await copy.click();
    assert.match(await status.textContent(), /foram alterados/);

    // Each valid email stage still generates a draft; switching stages invalidates it.
    const stages = ['primeiro', 'retorno', 'interesse', 'encerrar'];
    for (const stage of stages) {
      await page.locator('#followup select').selectOption(stage);
      await page.getByRole('button', { name: 'Preparar modelo de e-mail', exact: true }).click();
      assert.match(await output.inputValue(), /MODELO PARA REVISAR — NÃO ENVIADO/);
      assert.match(await page.locator('#result-kind').textContent(), /^Modelo de e-mail:/);
      const emailEvent = page.waitForEvent('download');
      await download.click();
      const emailFile = await emailEvent;
      assert.equal(emailFile.suggestedFilename(), `praia-digital-email-${stage}.txt`);
      assert.equal(fs.readFileSync(await emailFile.path(), 'utf8'), await output.inputValue());
      await page.getByLabel('Cidade', { exact: true }).fill('Santos');
      await copy.click();
      assert.match(await status.textContent(), /Texto copiado/);
      const count = await page.evaluate(() => window.testCopies.length);
      await page.locator('#followup select').selectOption(stage === 'primeiro' ? 'retorno' : 'primeiro');
      await copy.click();
      assert.equal(await page.evaluate(() => window.testCopies.length), count);
      assert.match(await status.textContent(), /foram alterados/);
    }
    const generatedEmail = await output.inputValue();
    page.once('dialog', dialog => dialog.dismiss());
    await page.getByRole('button', { name: 'Limpar tudo', exact: true }).click();
    assert.equal(await output.inputValue(), generatedEmail);
    page.once('dialog', dialog => dialog.accept());
    await page.getByRole('button', { name: 'Limpar tudo', exact: true }).click();
    assert.equal(await output.inputValue(), '');
    assert.equal(await page.locator('#result-kind').textContent(), 'Nenhum resultado gerado');
    assert(await page.getByLabel('Tipo do imóvel', { exact: true }).evaluate(element => element === document.activeElement));
    await output.fill('   ');
    await download.click();
    assert.match(await status.textContent(), /Gere um resultado antes de baixar/);
    assert.equal(downloads.length, 6);
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `no horizontal overflow at ${width}px`);
    await assertNoNavigation(page, documents, unexpected);
    console.log(`PASS: ${width}px — stale drafts blocked, fresh/edited TXT and copy work, source isolation, clipboard fallback, four stages and reset`);
  } finally { await context.close(); }
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
      page.once('dialog', dialog => dialog.accept());
      await page.getByRole('button', { name: 'Limpar tudo', exact: true }).click();
      assert.equal(await page.locator('#output').inputValue(), '');
      assert.equal(await page.getByLabel('Cidade', { exact: true }).inputValue(), '');
      assert.equal(await page.getByLabel('Contexto confirmado', { exact: true }).inputValue(), '');
      assert(await page.getByLabel('Tipo do imóvel', { exact: true }).evaluate(element => element === document.activeElement));
      assert.equal(await page.locator('[data-oficina-control]:disabled').count(), 0);
      await assertNoNavigation(page, documents, unexpected);
      console.log('PASS: initialized app — briefing, literal rendering, missing fields, follow-up draft, focus and reset stay local');
    } finally { await context.close(); }
    for (const width of [320, 390, 1280]) await assertCurrentExports(browser, width);
    const legacy = await fixture(browser, { legacyMarkup: true });
    try {
      await legacy.page.getByLabel('Tipo do imóvel', { exact: true }).fill('Apartamento fictício');
      await legacy.page.getByLabel('Cidade', { exact: true }).fill('Bertioga');
      await legacy.page.getByLabel('Finalidade', { exact: true }).fill('Venda fictícia');
      await legacy.page.getByRole('button', { name: 'Montar briefing e prompt', exact: true }).click();
      assert.match(await legacy.page.locator('#status').textContent(), /Resultado pronto/);
      legacy.page.once('dialog', dialog => dialog.accept());
      await legacy.page.getByRole('button', { name: 'Limpar tudo', exact: true }).click();
      assert.equal(await legacy.page.locator('#output').inputValue(), '');
      await assertNoNavigation(legacy.page, legacy.documents, legacy.unexpected);
      console.log('PASS: versioned module bypasses stale URL; legacy markup can generate and reset');
    } finally { await legacy.context.close(); }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
