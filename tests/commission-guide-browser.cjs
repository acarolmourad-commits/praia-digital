// NODE_PATH must point to an installed Playwright package directory.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const target = '/corretores/comissao-atrasada.html';
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHANNEL ? {channel: process.env.PLAYWRIGHT_CHANNEL} : {}) });
  try {
    const page = await browser.newPage();
    await page.route('**/*', route => route.abort());
    await page.setContent(fs.readFileSync(path.join(root, target), 'utf8'));
    await page.addStyleTag({content: fs.readFileSync(path.join(root, 'css/comissao-corretores.css'), 'utf8')});
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('main').count(), 1);
    assert.equal(await page.locator('html').getAttribute('lang'), 'pt-BR');
    const ids = await page.locator('[id]').evaluateAll(els => els.map(e => e.id));
    assert.equal(ids.length, new Set(ids).size, 'Unique anchor IDs');
    for (const href of await page.locator('a[href^="#"]').evaluateAll(els => els.map(e => e.getAttribute('href')))) {
      assert.ok(ids.includes(href.slice(1)), `Anchor resolves: ${href}`);
    }
    for (const href of await page.locator('a[href^="/"]').evaluateAll(els => els.map(e => e.getAttribute('href')))) {
      const file = href.endsWith('/') ? href.slice(1) + 'index.html' : href.slice(1);
      const tracked = execFileSync('git', ['ls-tree', '--name-only', 'HEAD', '--', file], {cwd: root, encoding: 'utf8'}).trim();
      assert.equal(tracked, file, `Internal target exists: ${file}`);
    }
    const schema = JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
    assert.equal(schema.mainEntityOfPage, await page.locator('link[rel="canonical"]').getAttribute('href'));
    for (const width of [320, 375, 768, 1280]) {
      await page.setViewportSize({width, height: 900});
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `No overflow at ${width}px`);
      assert.ok(await page.locator('.topbar nav').isVisible(), 'Navigation remains visible');
    }
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').textContent(), 'Pular para o conteúdo');
    await page.locator('summary').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('details').getAttribute('open'), '');
    for (const file of ['profissionais/index.html', 'corretores/cadastrar-imovel.html', 'hub/ia-corretores-litoral/index.html']) {
      assert.ok(fs.readFileSync(path.join(root, file), 'utf8').includes(`href="${target}"`), `Entry point: ${file}`);
    }
    assert.equal(fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8').split(`https://praia.digital${target}`).length - 1, 1);
    if (process.env.COMMISSION_SCREENSHOT) {
      await page.setViewportSize({width: 1280, height: 900});
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({path: process.env.COMMISSION_SCREENSHOT});
    }
    console.log('PASS: landmarks, metadata, anchors, internal targets, 4 responsive widths, keyboard controls, 3 entry points and sitemap.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
