const {chromium} = require('playwright');
const fs = require('node:fs'), path = require('node:path'), os = require('node:os');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(root, 'automation/marketplaces/informativos-revisados.json')));
const files = ['novidades-airbnb-booking.html', ...data.articles.map(a => a.file)];

(async () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'marketplaces-preview-'));
  for (const file of ['partials/header.html', 'assets/css/pd-navigation.css', 'js/pd-navigation.js', ...files.map(f => 'blog/' + f)]) {
    const target = path.join(temp, file);
    fs.mkdirSync(path.dirname(target), {recursive: true});
    fs.copyFileSync(path.join(root, file), target);
  }
  execFileSync('python3', [path.join(root, 'scripts/build-navigation.py'), '--root', temp]);
  const browser = await chromium.launch({headless: true, executablePath: process.env.CHROMIUM_PATH || undefined, args: ['--no-sandbox']});
  try {
    for (const width of [360, 390, 768, 1280]) {
      const page = await browser.newPage({viewport: {width, height: 900}});
      await page.route('**/*', r => r.abort());
      for (const file of files) {
        await page.setContent(fs.readFileSync(path.join(temp, 'blog', file), 'utf8'));
        await page.addStyleTag({content: fs.readFileSync(path.join(root, 'assets/css/pd-navigation.css'), 'utf8')});
        await page.addScriptTag({content: fs.readFileSync(path.join(root, 'js/pd-navigation.js'), 'utf8')});
        assert.equal(await page.locator('h1').count(), 1, file);
        assert.equal(await page.locator('header').count(), 1, 'One shared header: ' + file);
        assert.equal(await page.locator('form').count(), 0, 'No misleading signup or data collection');
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'No overflow ' + width + ': ' + file);
        if (file === files[0]) {
          assert.equal(await page.locator('#revisados .card').count(), 4);
          for (const id of ['revisados', 'arquivo', 'monitoramento']) assert.equal(await page.locator('#' + id).count(), 1);
          if (width <= 1080) {
            await page.locator('.pd-site-toggle').click();
            assert.equal(await page.locator('.pd-site-menu').isVisible(), true);
            await page.keyboard.press('Escape');
            assert.equal(await page.locator('.pd-site-menu').isVisible(), false);
          }
          if ([390, 1280].includes(width)) await page.screenshot({path: path.join(os.tmpdir(), 'marketplaces-index-' + width + '.png'), fullPage: true});
        } else {
          assert.equal(await page.getByRole('heading', {name: 'Disponibilidade e impacto no Brasil', exact: true}).count(), 1);
          assert.equal(await page.getByRole('heading', {name: 'Fontes e datas', exact: true}).count(), 1);
        }
        if (width === 390 && file === data.articles[0].file) await page.screenshot({path: path.join(os.tmpdir(), 'marketplaces-tools-390.png'), fullPage: true});
      }
      await page.close();
    }
    console.log('Marketplace browser checks passed: 11 pages at 4 widths, published navigation, menu dismissal, sources, and no overflow.');
  } finally {
    await browser.close();
    fs.rmSync(temp, {recursive: true, force: true});
  }
})().catch(error => {console.error(error); process.exit(1);});
