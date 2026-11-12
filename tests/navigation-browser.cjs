// Run with Playwright installed in NODE_PATH; no network or deployment required.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const file of ['index.html', 'cidades/bertioga.html']) {
      for (const width of [375, 768, 1080, 1280]) {
        const page = await browser.newPage({ viewport: { width, height: 900 } });
        await page.route('**/*', route => route.abort());
        await page.setContent(fs.readFileSync(path.join(process.env.NAV_PREVIEW_ROOT || root, file), 'utf8'));
        await page.addStyleTag({ content: fs.readFileSync(path.join(root, 'assets/css/pd-navigation.css'), 'utf8') });
        await page.addScriptTag({ content: fs.readFileSync(path.join(root, 'js/pd-navigation.js'), 'utf8') });
        const header = page.locator('.pd-site-header');
        assert.equal(await header.count(), 1);
        assert.equal(await header.locator('.pd-site-group').count(), 5);
        assert.equal(await header.locator('a').count(), 28);
        const toggle = header.locator('.pd-site-toggle');
        const menu = header.locator('.pd-site-menu');
        if (width <= 1080) {
          assert.equal(await menu.isVisible(), false);
          await toggle.click();
          assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
          assert.equal(await menu.isVisible(), true);
          const label = header.locator('.pd-site-label').first();
          await label.click();
          assert.equal(await label.getAttribute('aria-expanded'), 'true');
          assert.equal(await header.locator('.pd-site-submenu').first().isVisible(), true);
          await page.keyboard.press('Escape');
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          await page.keyboard.press('Escape');
          assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
          await toggle.click();
          await toggle.click();
          assert.equal(await menu.isVisible(), false);
        } else {
          assert.equal(await toggle.isVisible(), false);
          assert.equal(await menu.isVisible(), true);
          const label = header.locator('.pd-site-label').last();
          await label.hover();
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          await label.click();
          assert.equal(await label.getAttribute('aria-expanded'), 'true');
          assert.equal(await header.locator('.pd-site-submenu').last().isVisible(), true);
          await label.click();
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          await label.focus();
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          await page.keyboard.press('Enter');
          assert.equal(await label.getAttribute('aria-expanded'), 'true');
          await page.keyboard.press('Escape');
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          assert.equal(await header.locator('.pd-site-submenu').last().isVisible(), false);
          await page.keyboard.press('Space');
          assert.equal(await label.getAttribute('aria-expanded'), 'true');
          await page.keyboard.press('Tab');
          assert.equal(await header.locator('.pd-site-submenu').last().locator('a').first().evaluate(el => el === document.activeElement), true);
          await page.keyboard.press('Escape');
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          await label.click();
          await header.locator('.pd-site-label').first().click();
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          assert.equal(await header.locator('.pd-site-label').first().getAttribute('aria-expanded'), 'true');
          await page.locator('main').click({ position: { x: 5, y: 100 } });
          assert.equal(await header.locator('.pd-site-label').first().getAttribute('aria-expanded'), 'false');
        }
        const bounds = await header.boundingBox();
        assert(bounds.width <= width, 'header overflows viewport');
        console.log(`${file}: ${width}px passed`);
        await page.close();
      }
    }
    // Real legacy pages previously had duplicate, offscreen links to a missing #main.
    for (const file of ['automacao-imobiliarias.html', 'blog/10-artigos-seo-litoral-paulista-2026.html']) {
      for (const width of [375, 1280]) {
        const page = await browser.newPage({ viewport: { width, height: 900 } });
        const url = `https://navigation.test/${file}`;
        await page.route('**/*', route => {
          if (route.request().url() === url && route.request().method() === 'GET') {
            return route.fulfill({
              contentType: 'text/html; charset=utf-8',
              body: fs.readFileSync(path.join(process.env.NAV_PREVIEW_ROOT || root, file), 'utf8')
            });
          }
          return route.abort();
        });
        await page.goto(url, { waitUntil: 'load' });
        await page.addStyleTag({ content: fs.readFileSync(path.join(root, 'css/style.css'), 'utf8') });
        await page.addStyleTag({ content: fs.readFileSync(path.join(root, 'assets/css/pd-navigation.css'), 'utf8') });
        await page.addScriptTag({ content: fs.readFileSync(path.join(root, 'js/pd-navigation.js'), 'utf8') });
        const skip = page.locator('a.skip-link[href="#main"]');
        assert.equal(await skip.count(), 1, 'one keyboard shortcut precedes navigation');
        await page.keyboard.press('Tab');
        assert.equal(await skip.evaluate(el => el === document.activeElement), true, 'first Tab reaches skip link');
        const box = await skip.boundingBox();
        assert(box && box.x >= 0 && box.y >= 0 && box.x + box.width <= width + 1 && box.height > 20,
          `${file}: focused skip link must be readable inside ${width}px viewport`);
        await page.keyboard.press('Enter');
        await page.waitForFunction(() => location.hash === '#main' && document.activeElement.id === 'main');
        assert.equal(new URL(page.url()).hash, '#main');
        await page.keyboard.press('Tab');
        assert.equal(await page.evaluate(() => {
          const target = document.getElementById('main');
          const active = document.activeElement;
          return active !== document.body && active !== target && !active.closest('.pd-site-header')
            && Boolean(target.compareDocumentPosition(active) & Node.DOCUMENT_POSITION_FOLLOWING);
        }), true, 'next Tab enters content after the skip target, bypassing navigation');
        console.log(`${file}: skip link ${width}px passed`);
        await page.close();
      }
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
