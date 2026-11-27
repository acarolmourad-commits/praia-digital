// Offline publication verification. No forms, email, payments or provider calls.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const { screenshot } = require('./screenshot.cjs');
const root = path.resolve(__dirname, '..');
const guide = '/guias/usar-apps-com-evidencias.html';
const study = '/cases/rede-aplicativos-praia-digital.html';
const output = path.join(process.env.RUNNER_TEMP || '/tmp', 'app-guide-qa');

// Node-side deadline also covers page.evaluate and disabled page timers.
let phase = 'launch';
const deadline = setTimeout(() => {
  console.error('Browser evidence exceeded 5 minutes at: ' + phase);
  process.exit(1);
}, 300000);

async function verifyValueEstimator(page, width) {
  const errors = [];
  const onError = error => errors.push(error.message);
  page.on('pageerror', onError);
  await page.goto('https://praia.digital/apps/?objetivo=comparar#grupo-comparar');
  await page.locator('#grupo-comparar a.card[href="/apps/valor-imovel/"]').press('Enter');
  await page.waitForURL('**/apps/valor-imovel/');
  const area = page.getByRole('spinbutton', { name: 'Área construída (m²)' });
  const city = page.getByLabel('Cidade', { exact: true });
  const result = page.locator('#res');
  const error = page.locator('#area-erro[role="alert"]');
  assert.match(await city.locator('option:checked').innerText(), /Bertioga/);
  assert.equal(await city.getByRole('option', { name: /Caraguatatuba/ }).count(), 0);
  assert.match(await page.locator('#tabela-nota').innerText(), /Caraguatatuba aparece só nesta tabela/);
  assert.equal(await result.isVisible(), false);

  await area.press('Enter');
  assert.equal(await page.locator('#valor').innerText(), 'R$ 352.800');
  assert.equal(await page.locator('#range').innerText(), 'Faixa ilustrativa (±7%): R$ 328.104 — R$ 377.496');
  assert.equal(await result.evaluate(node => node === document.activeElement), true);

  for (const [input, message] of [
    ['', /maior que zero/], ['0', /maior que zero/], ['-1', /maior que zero/],
    ['1e308', /não permite calcular/], ['3e12', /não permite calcular/], ['1e-20', /não permite calcular/],
  ]) {
    // Recalculate successfully before each error to expose stale output.
    await area.fill('105');
    await area.press('Enter');
    assert.ok(await result.isVisible());
    await area.fill(input);
    await area.press('Enter');
    assert.equal(await result.isVisible(), false);
    assert.equal(await result.locator('#valor, #range, #bd').allTextContents().then(text => text.join('')), '');
    assert.match(await error.innerText(), message);
    assert.equal(await area.getAttribute('aria-invalid'), 'true');
    assert.equal(await area.evaluate(node => node === document.activeElement), true);
  }

  await area.fill('105.5');
  await page.getByRole('checkbox', { name: /Frente para o mar/ }).check();
  await page.getByRole('checkbox', { name: /A até 200m da praia/ }).check();
  await page.getByRole('button', {name: /Estimar valor/}).press('Enter');
  assert.equal(await area.getAttribute('aria-invalid'), null);
  assert.equal(await error.textContent(), '');
  assert.equal(await page.locator('#valor').innerText(), 'R$ 535.974');
  assert.match(await page.locator('#bd').innerText(), /Frente mar \+35%/);
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Estimator overflow at ${width}px`);
  assert.deepEqual(errors, []);
  page.off('pageerror', onError);
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of [360, 390, 768, 1280]) {
      for (const javaScriptEnabled of [true, false]) {
        const context = await browser.newContext({ viewport: { width, height: 900 }, javaScriptEnabled });
        await context.route('**/*', async route => {
          assert.equal(route.request().method(), 'GET');
          const url = new URL(route.request().url());
          if (url.hostname !== 'praia.digital') return route.abort();
          let file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
          if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
          if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return route.fulfill({ status: 404, body: 'Not found' });
          const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.jpg': 'image/jpeg', '.png': 'image/png' };
          return route.fulfill({ body: fs.readFileSync(file), contentType: types[path.extname(file)] || 'application/octet-stream' });
        });
        const page = await context.newPage();
        context.setDefaultTimeout(15000);
        context.setDefaultNavigationTimeout(15000);
        for (const target of [guide, study]) {
          phase = `${width}px js=${javaScriptEnabled} document ${target}`;
          console.log(phase);
          const errors = [];
          const onError = error => errors.push(error.message);
          page.on('pageerror', onError);
          await page.goto('https://praia.digital' + target);
          await page.keyboard.press('Tab');
          assert.equal(await page.evaluate(() => document.activeElement.matches('a.skip-link[href="#conteudo"]')), true);
          await page.keyboard.press('Enter');
          await page.waitForURL(url => url.hash === '#conteudo');
          assert.equal(new URL(page.url()).hash, '#conteudo');
          assert.equal(await page.locator('h1').count(), 1);
          assert.equal(await page.locator('header.pd-site-header').count(), 1);
          assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${target} overflow at ${width}`);
          const ids = await page.locator('[id]').evaluateAll(els => els.map(el => el.id));
          assert.equal(ids.length, new Set(ids).size);
          for (const href of await page.locator('main a[href^="#"]').evaluateAll(els => els.map(el => el.getAttribute('href')))) assert.ok(ids.includes(href.slice(1)));
          if (target === guide) {
            assert.equal(await page.locator("table").count(), 2);
            assert.equal(await page.locator(".table-wrap").evaluateAll(els => els.every(el => el.scrollWidth <= el.clientWidth + 1)), true);
            assert.ok(await page.locator('main a[href="/apps/guia-de-uso.html"]').count());
            await page.locator('a[href="#conferencia"]').click();
            assert.ok(page.url().endsWith('#conferencia'));
          }
          if (javaScriptEnabled && width === 390) {
            const toggle = page.locator('.pd-site-toggle');
            await toggle.click(); assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
            await page.keyboard.press('Escape'); assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
          }
          if (javaScriptEnabled && [390, 1280].includes(width)) {
            await page.evaluate(() => scrollTo(0, 0));
            await screenshot(page, { path: path.join(output, `${path.basename(target, '.html')}-${width}.png`), fullPage: true });
          }
          assert.deepEqual(errors, []);
          page.off('pageerror', onError);
        }
        phase = `${width}px js=${javaScriptEnabled} pricing/laboratory round trip`;
        console.log(phase);
        await page.goto('https://praia.digital/apps/guia-de-uso.html#vender');
        const pilotLink = page.locator('#vender a[href="/ia/marketplaces/piloto/"]');
        assert.equal(await pilotLink.count(), 1);
        // Fragment navigation scrolls smoothly. Wait on Node-side geometry before
        // Playwright's click stability check, including with page JavaScript disabled.
        let lastPilotBox = null;
        let stablePilotSamples = 0;
        const pilotDeadline = Date.now() + 5000;
        while (stablePilotSamples < 3 && Date.now() < pilotDeadline) {
          const current = await pilotLink.boundingBox();
          assert.ok(current, 'Pilot link must be visible in layout');
          stablePilotSamples = lastPilotBox && ['x', 'y', 'width', 'height'].every(key => Math.abs(current[key] - lastPilotBox[key]) < 0.5) ? stablePilotSamples + 1 : 0;
          lastPilotBox = current;
          await new Promise(resolve => setTimeout(resolve, 100));
        }
        assert.equal(stablePilotSamples, 3, 'Pilot link must stabilize before click');
        await pilotLink.click();
        await page.waitForURL('**/ia/marketplaces/piloto/');
        const returnToPricing = page.getByRole('link', { name: 'Voltar ao roteiro de precificação', exact: true });
        assert.equal(await returnToPricing.getAttribute('href'), '/apps/guia-de-uso.html#vender');
        await returnToPricing.click();
        await page.waitForURL('**/apps/guia-de-uso.html#vender');
        assert.equal(await page.locator('input[type=checkbox]').count(), 12);
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        // Discovery links are complementary, not a seventeenth filtered app.
        for (const source of ['/', '/apps/']) {
          phase = `${width}px js=${javaScriptEnabled} discovery ${source}`;
          console.log(phase);
          await page.goto('https://praia.digital' + source);
          const link = page.locator('a[href="/ia/marketplaces/piloto/"]');
          assert.equal(await link.count(), 1);
          assert.match(await link.innerText(), /Laboratório Estoque Vivo/);
          const block = source === '/' ? page.locator('aside[aria-labelledby="guia-apps-home"]') : link;
          assert.match(await block.innerText(), /produtos fictícios/);
          assert.match((await block.innerText()).toLowerCase(), /sem conexão com lojas ou estoque real/);
          if (source === '/apps/') assert.equal(await page.locator('.pd-catalog-group .card').count(), 16);
          await link.scrollIntoViewIfNeeded();
          // Poll layout from Node: page animation callbacks do not run with JS disabled.
          phase += ' stable layout';
          let previousBox = null;
          let stableSamples = 0;
          const stableDeadline = Date.now() + 5000;
          while (stableSamples < 2 && Date.now() < stableDeadline) {
            const currentBox = await link.boundingBox();
            assert.ok(currentBox, 'Discovery link must have a layout box');
            stableSamples = previousBox && ['x', 'y', 'width', 'height'].every(key => Math.abs(currentBox[key] - previousBox[key]) < 0.5) ? stableSamples + 1 : 0;
            previousBox = currentBox;
            await new Promise(resolve => setTimeout(resolve, 100));
          }
          assert.equal(stableSamples, 2, 'Layout failed to stabilize: ' + phase);
          phase += ' screenshot/navigation';
          assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Pilot discovery overflow ${source} ${width}`);
          const box = await link.boundingBox();
          assert.ok(box.width > 0 && box.x >= 0 && box.x + box.width <= width + 1);
          await screenshot(page, { path: path.join(output, `pilot-link-${source === '/' ? 'home' : 'catalog'}-${width}-${javaScriptEnabled ? 'js' : 'nojs'}.png`) });
          await link.click();
          await page.waitForURL('**/ia/marketplaces/piloto/');
          assert.match(await page.locator('h1').innerText(), /Um saldo confiável/);
          await page.goBack();
          assert.equal(new URL(page.url()).pathname, source);
        }
        if (width === 390) {
          phase = `${width}px js=${javaScriptEnabled} homepage/portfolio discovery`;
          console.log(phase);
          const casePath = '/cases.html#caso-estoque-vivo';
          await page.goto('https://praia.digital/');
          const portfolioLink = page.locator('#apps a[href="' + casePath + '"]');
          assert.equal(await portfolioLink.count(), 1);
          await portfolioLink.click();
          await page.waitForURL('**' + casePath);
          const portfolioCase = page.locator('#caso-estoque-vivo');
          assert.match(await portfolioCase.locator('h2').innerText(), /estoque fictício/);
          assert.match(await portfolioCase.innerText(), /não comprova integração nem resultado comercial/);
          assert.equal(await portfolioCase.getByRole('link', { name: 'roteiro de precificação' }).getAttribute('href'), '/apps/guia-de-uso.html#vender');
          assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Portfolio overflow at 390 px');
          const laboratoryLink = portfolioCase.getByRole('link', { name: 'Experimentar o laboratório com estoque fictício' });
          // The incoming fragment can still be scrolling when the assertions above pass.
          // Use Node-side geometry checks, which also run when page JS is disabled.
          let lastLaboratoryBox = null;
          let stableLaboratorySamples = 0;
          const laboratoryDeadline = Date.now() + 5000;
          while (stableLaboratorySamples < 3 && Date.now() < laboratoryDeadline) {
            const current = await laboratoryLink.boundingBox();
            assert.ok(current, 'Portfolio laboratory link must have a layout box');
            stableLaboratorySamples = lastLaboratoryBox && ['x', 'y', 'width', 'height'].every(key => Math.abs(current[key] - lastLaboratoryBox[key]) < 0.5) ? stableLaboratorySamples + 1 : 0;
            lastLaboratoryBox = current;
            await new Promise(resolve => setTimeout(resolve, 100));
          }
          assert.equal(stableLaboratorySamples, 3, 'Portfolio laboratory link must stabilize before click');
          await laboratoryLink.click();
          await page.waitForURL('**/ia/marketplaces/piloto/#laboratorio');
          assert.equal(await page.locator('#laboratorio').count(), 1);
        }
        await page.goto('https://praia.digital/');
        await page.locator('#apps a[href="' + guide + '"]').click();
        await page.waitForURL('**' + guide);
        await page.locator('main a[href="/apps/guia-de-uso.html"]').first().click();
        await page.waitForURL('**/apps/guia-de-uso.html');
        await page.locator('a[href="' + guide + '"]').click();
        await page.waitForURL('**' + guide);
        await page.locator('main a[href="' + study + '"]').click();
        await page.waitForURL('**' + study);
        phase = `${width}px js=${javaScriptEnabled} pauta de retorno`;
        await page.getByRole('region', { name: 'Da visita às perguntas para o proprietário' })
          .getByRole('link', { name: 'Relatório do imóvel', exact: true }).click();
        await page.waitForURL('**/apps/relatorio-imovel/#pauta-de-retorno');
        const panel = page.locator('#pauta-de-retorno');
        if (javaScriptEnabled) {
          assert.ok(await page.locator('#agenda-text').isVisible());
          await page.locator('#pending').fill('A vaga é privativa?');
          await page.locator('#contact').fill('Contato privado fictício');
          assert.equal(await page.locator('#agenda-text').inputValue(), 'Pauta de retorno\n\nPontos a confirmar\nA vaga é privativa?');
          assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        } else {
          if (!await panel.evaluate(node => node.open)) await panel.locator('summary').press('Enter');
          assert.match(await panel.innerText(), /montar a pauta manualmente/);
        }
        if (javaScriptEnabled && [390, 1280].includes(width)) {
          phase = `${width}px Estimador de Valor – catalog, calculation, validation and recovery`;
          console.log(phase);
          await verifyValueEstimator(page, width);
        }
        await context.close();
      }
    }
    console.log('Guide/study passed at 360/390/768/1280, with/without JS: evidence tables, anchors, menu, navigation loop, no overflow; screenshots saved.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => clearTimeout(deadline));
