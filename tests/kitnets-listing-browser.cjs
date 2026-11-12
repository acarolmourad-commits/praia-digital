// Offline checks for this listing only; no external requests or messages.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(process.env.KITNETS_PREVIEW_ROOT || path.join(__dirname, '..'));
const output = process.env.KITNETS_QA_OUTPUT || '/tmp/kitnets-listing-qa';
const origin = 'https://praia.digital';
const detail = '/imoveis/residencial-4-kitnets-864m2.html';
const asset = '/assets/residencial-4-kitnets-864m2/';
fs.mkdirSync(output, { recursive: true });
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const width of [375, 1280]) {
      const context = await browser.newContext({ viewport: { width, height: 900 }, serviceWorkers: 'block' });
      const errors = [], blocked = [], missing = [];
      await context.route('**/*', async route => {
        const request = route.request(), url = new URL(request.url());
        if (!['GET', 'HEAD'].includes(request.method()) || url.origin !== origin) {
          blocked.push(request.url());
          return route.abort();
        }
        const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
        if (!file.startsWith(root + path.sep)) return route.fulfill({ status: 403, body: '' });
        if (!fs.existsSync(file) || !fs.statSync(file).isFile()) {
          missing.push(url.pathname);
          return route.fulfill({ status: 404, body: '' });
        }
        const mime = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.css': 'text/css', '.js': 'application/javascript' };
        return route.fulfill({ path: file, contentType: mime[path.extname(file)] || 'application/octet-stream' });
      });
      try {
        const page = await context.newPage();
        page.setDefaultTimeout(15000);
        page.on('pageerror', error => errors.push(error.message));
        await page.goto(origin + detail, { waitUntil: 'load' });
        assert.equal(await page.locator('h1').count(), 1);
        assert.match(await page.locator('h1').innerText(), /4 kitnets/i);
        assert.match(await page.locator('.hero .price').innerText(), /R\$\s*2\.000\.000/);
        assert.match(await page.locator('.facts').innerText(), /864 m²/);
        assert.match(await page.locator('.facts').innerText(), /terreno/i);
        assert.equal(await page.locator('.gallery figure').count(), 12);
        assert.equal(await page.locator('.gallery img').count(), 12);
        assert.equal(await page.locator('img').count(), 13); // cover + gallery
        const body = await page.locator('body').innerText();
        assert(!/LOCALIZACAO_CONFIRMAR|LEGENDA_CONFIRMAR/.test(body), 'Unresolved draft placeholders');
        const robots = await page.locator('meta[name="robots"]').getAttribute('content');
        assert(!/noindex/i.test(robots), 'Listing must be indexable after final review');
        const schema = JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
        assert.equal(schema.offers.price, '2000000');
        assert.equal(schema.offers.priceCurrency, 'BRL');
        assert.equal(schema.image.length, 12);
        assert(!schema.floorSize, 'Do not describe land area as built floor area');
        assert.equal(await page.locator('.gallery a').count(), 12);
        for (let i = 0; i < 12; i++) {
          const expected = asset + String(i + 1).padStart(2, '0') + '.webp';
          const img = page.locator('.gallery img').nth(i);
          assert.equal(await img.getAttribute('src'), expected);
          assert.equal(await page.locator('.gallery a').nth(i).getAttribute('href'), expected);
          assert((await img.getAttribute('alt') || '').trim().length > 10);
          await img.scrollIntoViewIfNeeded();
          await img.evaluate(el => el.decode());
          assert(await img.evaluate(el => el.naturalWidth > 0 && el.naturalHeight > 0));
        }
        const ctas = page.locator('a[href^="https://wa.me/"]');
        assert.equal(await ctas.count(), 2);
        for (const link of await ctas.all()) {
          const url = new URL(await link.getAttribute('href'));
          assert.equal(url.pathname, '/5511954346288');
          assert.match(url.searchParams.get('text'), /4 kitnets/i);
          assert.match(url.searchParams.get('text'), /2\.000\.000/);
        }
        // Never click WhatsApp links; verify the href only.
        await page.locator('a[href="#fotos"]').click();
        assert.equal(new URL(page.url()).hash, '#fotos');
        const popupPromise = context.waitForEvent('page');
        await page.locator('.gallery a').first().click();
        const popup = await popupPromise;
        await popup.waitForLoadState();
        assert.equal(new URL(popup.url()).pathname, asset + '01.webp');
        await popup.close();
        for (const faq of await page.locator('.faq details').all()) {
          await faq.locator('summary').click();
          assert(await faq.getAttribute('open') !== null);
          await faq.locator('summary').click();
        }
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Horizontal overflow at ${width}px`);
        await page.screenshot({ path: path.join(output, `${width}-full.png`), fullPage: true });
        await page.evaluate(() => scrollTo(0, 0));
        await page.screenshot({ path: path.join(output, `${width}-hero.png`) });
        assert.deepEqual(errors, []);
        assert.deepEqual(blocked, [], 'Unexpected external request');
        assert.deepEqual(missing, [], 'Missing local resource');
        console.log(`${width}px: gallery, decoded photos, price, metadata, CTA, FAQ and overflow passed`);
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
