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
        for (const target of [guide, study]) {
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
        await page.goto('https://praia.digital/');
        await page.locator('#apps a[href="' + guide + '"]').click();
        await page.waitForURL('**' + guide);
        await page.locator('main a[href="/apps/guia-de-uso.html"]').first().click();
        await page.waitForURL('**/apps/guia-de-uso.html');
        await page.locator('a[href="' + guide + '"]').click();
        await page.waitForURL('**' + guide);
        await page.locator('main a[href="' + study + '"]').click();
        await page.waitForURL('**' + study);
        await context.close();
      }
    }
    console.log('Guide/study passed at 360/390/768/1280, with/without JS: evidence tables, anchors, menu, navigation loop, no overflow; screenshots saved.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
