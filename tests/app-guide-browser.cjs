const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const {screenshot} = require('./screenshot.cjs');
const root = path.resolve(__dirname, '..');
const output = path.join(process.env.RUNNER_TEMP || '/tmp', 'app-guide-qa');
(async () => {
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({headless: true});
  try {
    for (const width of [320, 390, 1280]) {
      const context = await browser.newContext({viewport: {width, height: 900}});
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.hostname !== 'praia.digital' || route.request().method() !== 'GET') return route.abort();
        let file = path.resolve(root, '.' + url.pathname);
        if (!file.startsWith(root + path.sep)) return route.abort();
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file)) return route.abort();
        const ext = path.extname(file);
        return route.fulfill({body: fs.readFileSync(file), contentType: {'.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg'}[ext] || 'text/html'});
      });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto('https://praia.digital/apps/guia-de-uso.html');
      assert.equal(await page.locator('.guide-route').count(), 4);
      assert.equal(await page.locator('input[type=checkbox]').count(), 12);
      await page.locator('input[type=checkbox]').first().check();
      assert.match(await page.locator('#guide-progress').innerText(), /^1 de 12/);
      await page.locator('#guide-reset').click();
      assert.equal(await page.locator('input:checked').count(), 0);
      assert.match(await page.locator('#guide-progress').innerText(), /^0 de 12/);
      await page.evaluate(() => {window.print = () => {window.printCalled = true;};});
      await page.locator('#guide-print').click();
      assert.equal(await page.evaluate(() => window.printCalled), true);
      const groups = JSON.parse(fs.readFileSync(path.join(root, 'data/app-network.json'), 'utf8'));
      for (const app of groups.flatMap(g => g.apps)) assert.ok(await page.locator(`a[href="/apps/${app.slug}/"]`).count());
      for (const anchor of ['comprar','locar','anunciar','vender']) {
        await page.locator(`.guide-toc a[href="#${anchor}"]`).click();
        assert.equal(new URL(page.url()).hash, '#' + anchor);
      }
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      assert.deepEqual(errors, []);
      await page.emulateMedia({media:'print'});
      assert.equal(await page.locator('.guide-route:visible').count(), 4);
      assert.equal(await page.locator('#guide-actions').isVisible(), false);
      await page.emulateMedia({media:'screen'});
      await page.goto('https://praia.digital/apps/guia-de-uso.html');
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.className), 'pd-skip');
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash, '#conteudo');
      await screenshot(page, {path:path.join(output, `guide-${width}.png`),fullPage:true});
      await context.close();
    }
    const nojs = await browser.newContext({javaScriptEnabled:false});
    const page = await nojs.newPage();
    await page.goto('file://' + path.join(root,'apps/guia-de-uso.html'));
    assert.equal(await page.locator('.guide-route').count(),4);
    assert.equal(await page.locator('#guide-actions').isVisible(),false);
    await page.locator('input[type=checkbox]').first().check();
    assert.equal(await page.locator('input:checked').count(),1);
    await nojs.close();
    console.log('Guide passed at 320,390,1280px: links to 16 apps, anchors, checklist/reset, keyboard, print, no-JS.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
