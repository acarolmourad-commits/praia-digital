// Offline mobile checks against a disposable copy built by the deployment script.
// No form is submitted; every request is fulfilled locally or blocked.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const origin = 'https://praia.digital';
const output = path.resolve(process.env.EDITORIAL_QA_OUTPUT || path.join(os.tmpdir(), 'praia-editorial-qa'));
const pages = [
  'blog/index.html',
  'anfitrioes/index.html',
  'blog/diagnostico-anuncio-temporada-litoral-2026.html',
  'blog/sincronizar-calendario-airbnb-booking-ical.html',
  'blog/briefing-criacao-anuncio-airbnb-booking.html',
  'blog/google-sheets-gestao-imoveis-litoral.html',
  'blog/mensuracao-attribution-marketing-imobiliario-local-litoral-2026.html',
  'blog/como-gerar-avaliacoes-google-imobiliarias-litoral-2026.html',
];
const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.woff2': 'font/woff2' };

function prepare() {
  const preview = fs.mkdtempSync(path.join(os.tmpdir(), 'praia-editorial-preview-'));
  for (const file of [...pages, 'partials/header.html']) {
    const destination = path.join(preview, file);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.copyFileSync(path.join(root, file), destination);
  }
  fs.mkdirSync(output, { recursive: true });
  execFileSync('python3', [path.join(root, 'scripts/build-navigation.py'), '--root', preview, '--report', path.join(output, 'navigation.json')], { stdio: 'inherit' });
  return preview;
}

async function offlineContext(browser, preview, width) {
  const context = await browser.newContext({ viewport: { width, height: 900 }, isMobile: true, hasTouch: true, serviceWorkers: 'block' });
  const sideEffects = [];
  await context.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (!['GET', 'HEAD'].includes(request.method())) {
      sideEffects.push(`${request.method()} ${url.origin}${url.pathname}`);
      return route.abort();
    }
    if (url.origin !== origin) {
      if (request.isNavigationRequest()) sideEffects.push(`External navigation: ${url.origin}${url.pathname}`);
      return route.abort();
    }
    let relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
    if (!relative || relative.endsWith('/')) relative += 'index.html';
    let filename = path.resolve(root, relative);
    if (!filename.startsWith(root + path.sep)) return route.fulfill({ status: 403, body: 'Forbidden' });
    if (fs.existsSync(filename) && fs.statSync(filename).isDirectory()) relative += '/index.html';
    filename = path.join(fs.existsSync(path.join(preview, relative)) ? preview : root, relative);
    if (!fs.existsSync(filename) || !fs.statSync(filename).isFile()) return route.fulfill({ status: 404, body: 'Not found' });
    return route.fulfill({ status: 200, contentType: mime[path.extname(filename)] || 'application/octet-stream', body: fs.readFileSync(filename) });
  });
  return { context, sideEffects };
}

async function noOverflow(page, label) {
  const sizes = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
  const expectedWidth = page.viewportSize().width;
  assert(sizes.viewport <= expectedWidth + 1 && sizes.document <= expectedWidth + 1 && sizes.body <= expectedWidth + 1, `${label}: horizontal overflow ${JSON.stringify(sizes)}`);
  return sizes;
}

async function keyboardFocus(page, locator, label) {
  // Tab out and back uses real keyboard modality rather than forcing :focus-visible.
  await locator.focus();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  await locator.scrollIntoViewIfNeeded();
  const result = await locator.evaluate(element => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return {
      active: element === document.activeElement,
      focusVisible: element.matches(':focus-visible'),
      outlineStyle: style.outlineStyle,
      outlineWidth: parseFloat(style.outlineWidth),
      outlineColor: style.outlineColor,
      visible: rect.width > 0 && rect.height > 0 && rect.bottom > 0 && rect.top < innerHeight,
      text: element.textContent.trim().slice(0, 90),
    };
  });
  assert(result.active && result.focusVisible && result.visible, `${label}: keyboard focus not visible ${JSON.stringify(result)}`);
  assert(!['none', 'hidden'].includes(result.outlineStyle) && result.outlineWidth >= 2, `${label}: missing focus outline`);
  return { label, ...result };
}

async function mobileMenu(page) {
  const toggle = page.locator('.pd-site-toggle');
  await toggle.click();
  assert.equal(await toggle.getAttribute('aria-expanded'), 'true');
  await page.locator('.pd-site-label').first().click();
  assert.equal(await page.locator('.pd-site-submenu').first().isVisible(), true);
  await noOverflow(page, 'expanded mobile menu');
  await page.keyboard.press('Escape');
  await page.keyboard.press('Escape');
  assert.equal(await toggle.getAttribute('aria-expanded'), 'false');
}

async function search(page) {
  const input = page.locator('#pdBlogSearch');
  const list = page.locator('#pdBlogList li:not([hidden])');
  const total = await list.count();
  assert(total > 100, 'the deferred search indexes the full selected catalog');
  await input.fill('sao vicente');
  assert((await list.count()) > 0 && (await list.count()) < total, 'unaccented city search filters guides');
  await input.fill('zzzz-sem-correspondencia-qa');
  assert.equal(await list.count(), 0);
  assert(await page.locator('#pdBlogEmpty').isVisible());
  await page.locator('#pdBlogClear').click();
  assert.equal(await input.inputValue(), '');
  assert.equal(await input.evaluate(element => element === document.activeElement), true);
  assert.equal(await list.count(), total);
  await input.fill('calendario booking');
  const result = list.locator('a[href="/blog/sincronizar-calendario-airbnb-booking-ical.html"]');
  assert.equal(await result.count(), 1);
  await result.click();
  await page.waitForURL(origin + '/blog/sincronizar-calendario-airbnb-booking-ical.html');
  assert.match(await page.locator('h1').innerText(), /Airbnb e Booking/);
  return total;
}

(async () => {
  const preview = prepare();
  if (process.argv.includes('--prepare-only')) {
    console.log(`Prepared ${pages.length} navigation-built pages successfully`);
    fs.rmSync(preview, { recursive: true, force: true });
    return;
  }
  const { chromium } = require('playwright');
  const results = [];
  const failures = [];
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    for (const width of [390, 768]) {
      for (const file of pages) {
        const { context, sideEffects } = await offlineContext(browser, preview, width);
        const page = await context.newPage();
        page.setDefaultTimeout(7000);
        const record = { file, width, focus: [] };
        try {
          const response = await page.goto(origin + '/' + file, { waitUntil: 'load' });
          assert.equal(response.status(), 200);
          assert.equal(await page.locator('.pd-site-header').count(), 1, 'official navigation is present');
          assert.equal(await page.locator('main').count(), 1);
          assert.equal(await page.locator('h1').count(), 1);
          await page.locator('footer nav a').first().waitFor();
          record.dimensions = await noOverflow(page, `${file} ${width}px`);
          await mobileMenu(page);
          record.focus.push(await keyboardFocus(page, page.locator('main a').first(), 'main link'));
          if (file === 'anfitrioes/index.html') {
            record.focus.push(await keyboardFocus(page, page.locator('.hero a').first(), 'dark hero'));
            record.focus.push(await keyboardFocus(page, page.locator('.cta a').first(), 'dark CTA'));
            const summary = page.locator('details summary').first();
            await summary.focus();
            await page.keyboard.press('Enter');
            assert.equal(await summary.evaluate(element => element.parentElement.open), true);
          } else if (file !== 'blog/index.html') {
            record.focus.push(await keyboardFocus(page, page.locator('.toc a').first(), 'table of contents'));
            record.focus.push(await keyboardFocus(page, page.locator('.cta-box .button'), 'article CTA'));
            const anchor = page.locator('.toc a').first();
            const fragment = await anchor.getAttribute('href');
            assert(await page.locator(fragment).count(), `missing target ${fragment}`);
            await anchor.click();
            assert.equal(new URL(page.url()).hash, fragment);
            await noOverflow(page, 'article after anchor navigation');
          }
          record.focus.push(await keyboardFocus(page, page.locator('footer nav a').first(), 'dark footer'));
          if (file === 'blog/index.html') {
            record.searchGuides = await search(page);
            await page.goto(origin + '/' + file, { waitUntil: 'load' });
          }
          await noOverflow(page, `${file} after interactions`);
          await page.screenshot({ path: path.join(output, `${file.replace(/[^a-z0-9-]/gi, '_')}-${width}.png`), fullPage: true });
          assert.deepEqual(sideEffects, [], 'no external navigation or mutating request');
          record.status = 'passed';
          console.log(`${file}: ${width}px passed`);
        } catch (error) {
          record.status = 'failed';
          record.error = String(error.message);
          failures.push(`${file} ${width}px: ${error.message}`);
          await page.screenshot({ path: path.join(output, `failure-${file.replace(/[^a-z0-9-]/gi, '_')}-${width}.png`), fullPage: true }).catch(() => {});
        } finally {
          results.push(record);
          await context.close();
        }
      }
    }
    assert.equal(failures.length, 0, failures.join('\n'));
  } finally {
    fs.writeFileSync(path.join(output, 'results.json'), JSON.stringify({ pages: pages.length, widths: [390, 768], results, failures }, null, 2));
    await browser?.close();
    fs.rmSync(preview, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exit(1); });
