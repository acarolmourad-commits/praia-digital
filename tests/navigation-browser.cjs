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
        assert.equal(await header.locator('a').count(), 26);
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
          assert.equal(await label.getAttribute('aria-expanded'), 'true');
          assert.equal(await header.locator('.pd-site-submenu').last().isVisible(), true);
          await label.focus();
          await page.keyboard.press('Escape');
          assert.equal(await label.getAttribute('aria-expanded'), 'false');
          assert.equal(await header.locator('.pd-site-submenu').last().isVisible(), false);
        }
        const bounds = await header.boundingBox();
        assert(bounds.width <= width, 'header overflows viewport');
        console.log(`${file}: ${width}px passed`);
        await page.close();
      }
    }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });
