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
        if (file !== root && !file.startsWith(root + path.sep)) return route.abort();
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file)) return route.abort();
        const ext = path.extname(file);
        return route.fulfill({body: fs.readFileSync(file), contentType: {'.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg'}[ext] || 'text/html'});
      });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto('https://praia.digital/');
      const buyGuide=page.locator('article[aria-labelledby="roteiro-orcamento"]').getByRole('link',{name:'abra o roteiro de compra'});
      await buyGuide.press('Enter');
      assert.equal(new URL(page.url()).pathname, '/apps/guia-de-uso.html');
      assert.equal(new URL(page.url()).hash, '#comprar');
      assert.equal(await page.locator('#comprar input[type=checkbox]').count(), 3);
      await page.waitForFunction(() => {
        const target = document.getElementById('comprar');
        const header = document.querySelector('.pd-site-header');
        return Boolean(target && header && target.getBoundingClientRect().top >= header.getBoundingClientRect().bottom
          && target.getBoundingClientRect().top < innerHeight);
      });
      await page.goto('https://praia.digital/#rede-apps');
      await page.getByRole('link', {name: 'Separe as comodidades de cada categoria das áreas comuns'}).press('Enter');
      assert.equal(new URL(page.url()).hash, '#comodidades-por-categoria');
      await page.waitForFunction(() => {
        const target = document.getElementById('comodidades-por-categoria');
        const header = document.querySelector('.pd-site-header');
        return Boolean(target && header && target.getBoundingClientRect().top >= header.getBoundingClientRect().bottom
          && target.getBoundingClientRect().top < innerHeight);
      });
      await page.goto('https://praia.digital/apps/guia-de-uso.html');
      assert.equal(await page.locator('.guide-route').count(), 4);
      assert.equal(await page.locator('input[type=checkbox]').count(), 12);
      await page.locator('input[type=checkbox]').first().check();
      assert.match(await page.locator('#guide-progress').innerText(), /^1 de 12/);
      // A restored document may have checked fields without a change event.
      await page.evaluate(() => {
        const boxes = document.querySelectorAll('.guide-route input[type=checkbox]');
        boxes[0].checked = false;
        boxes[1].checked = true;
        boxes[2].checked = true;
        window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted:true}));
      });
      assert.match(await page.locator('#guide-progress').innerText(), /^2 de 12/);
      // Export the actual restored state, including unchecked items and route links.
      const downloadPromise = page.waitForEvent('download');
      await page.getByRole('button', {name:'Baixar checklist em texto'}).press('Enter');
      const download = await downloadPromise;
      assert.match(download.suggestedFilename(), /^praia-digital-checklist-\d{4}-\d{2}-\d{2}\.txt$/);
      const exportedPath = path.join(output, `checklist-${width}.txt`);
      await download.saveAs(exportedPath);
      const exported = fs.readFileSync(exportedPath, 'utf8');
      assert.equal((exported.match(/\[x\] Marcado nesta consulta/g) || []).length, 2);
      assert.equal((exported.match(/\[ \] A conferir \(não marcado\)/g) || []).length, 10);
      assert.match(exported, /America\/Sao_Paulo/);
      assert.match(exported, /Não comprovam aprovação, execução ou resultado/);
      for (const anchor of ['comprar','locar','anunciar','vender']) {
        assert.ok(exported.includes(`https://praia.digital/apps/guia-de-uso.html#${anchor}`));
      }
      assert.equal((exported.match(/Responsável: não identificado/g) || []).length, 4);
      // A focused export contains just that route, while preserving all page markings.
      for (const anchor of ['comprar','locar','anunciar','vender']) {
        await page.getByLabel('Roteiros para salvar').selectOption(anchor);
        const focusedPromise = page.waitForEvent('download');
        await page.locator('#guide-download').press('Enter');
        const focusedDownload = await focusedPromise;
        assert.ok(focusedDownload.suggestedFilename().startsWith(`praia-digital-checklist-${anchor}-`));
        await focusedDownload.saveAs(exportedPath);
        const focused = fs.readFileSync(exportedPath, 'utf8');
        assert.equal((focused.match(/Responsável: não identificado/g) || []).length, 1);
        for (const other of ['comprar','locar','anunciar','vender']) {
          assert.equal(focused.includes(`guia-de-uso.html#${other}`), other === anchor);
        }
        assert.equal((focused.match(/Marcado nesta consulta/g) || []).length, anchor === 'comprar' ? 2 : 0);
        assert.equal((focused.match(/A conferir \(não marcado\)/g) || []).length, anchor === 'comprar' ? 1 : 3);
        assert.equal(await page.locator('input:checked').count(), 2);
        assert.ok((await page.locator('#guide-download-status').innerText()).includes(await page.locator(`#${anchor} h2`).innerText()));
      }
      // Print each selected route without losing marks in the other routes.
      for (const anchor of ['comprar','locar','anunciar','vender']) {
        await page.getByLabel('Roteiros para salvar').selectOption(anchor);
        await page.evaluate(() => window.dispatchEvent(new Event('beforeprint')));
        await page.emulateMedia({media:'print'});
        assert.equal(await page.locator('.guide-route:visible').count(), 1);
        assert.equal(await page.locator(`#${anchor}`).isVisible(), true);
        assert.equal(await page.locator('main > .guide-example:visible').count(), 0);
        assert.equal(await page.locator('input:checked').count(), 2);
        assert.ok((await page.locator('.guide-print-scope').innerText()).includes(await page.locator(`#${anchor} h2`).innerText()));
        if (width === 1280) {
          const pdf = await page.pdf({path:path.join(output, `roteiro-${anchor}.pdf`), format:'A4'});
          assert.equal(pdf.subarray(0,4).toString(), '%PDF');
          assert.ok(pdf.length > 1000);
        }
        await page.evaluate(() => window.dispatchEvent(new Event('afterprint')));
        await page.emulateMedia({media:'screen'});
        assert.equal(await page.locator('.guide-route:visible').count(), 4);
        assert.equal(await page.locator('input:checked').count(), 2);
        assert.equal(await page.locator('.guide-print-scope').isVisible(), false);
      }
      await page.getByLabel('Roteiros para salvar').selectOption('');

      await page.evaluate(() => window.dispatchEvent(new PageTransitionEvent('pageshow', {persisted:true})));
      assert.match(await page.locator('#guide-progress').innerText(), /^2 de 12/);
      await page.locator('#guide-reset').click();
      assert.equal(await page.locator('input:checked').count(), 0);
      assert.match(await page.locator('#guide-progress').innerText(), /^0 de 12/);
      const resetDownloadPromise = page.waitForEvent('download');
      await page.locator('#guide-download').click();
      const resetDownload = await resetDownloadPromise;
      await resetDownload.saveAs(exportedPath);
      const resetExport = fs.readFileSync(exportedPath, 'utf8');
      assert.equal((resetExport.match(/\[x\]/g) || []).length, 0);
      assert.equal((resetExport.match(/\[ \] A conferir/g) || []).length, 12);
      const undo = page.getByRole('button', {name: 'Desfazer limpeza'});
      await undo.press('Enter');
      assert.equal(await page.locator('#guide-reset').evaluate(el => el === document.activeElement), true);
      const checkedIndices = () => page.locator('.guide-route input[type=checkbox]').evaluateAll(
        boxes => boxes.flatMap((box, i) => box.checked ? [i] : [])
      );
      assert.deepEqual(await checkedIndices(), [1, 2]);
      assert.equal(await undo.isVisible(), false);
      await page.locator('#guide-reset').press('Enter');
      assert.equal(await undo.evaluate(el => el === document.activeElement), true);
      await page.locator('.guide-route input[type=checkbox]').first().check();
      assert.equal(await undo.isVisible(), false);
      assert.deepEqual(await checkedIndices(), [0]);
      await page.locator('#guide-reset').click();
      await page.evaluate(() => {window.print = () => {window.printCalled = true;};});
      await page.locator('#guide-print').click();
      assert.equal(await page.evaluate(() => window.printCalled), true);
      const groups = JSON.parse(fs.readFileSync(path.join(root, 'data/app-network.json'), 'utf8'));
      for (const app of groups.flatMap(g => g.apps)) assert.ok(await page.locator(`a[href="/apps/${app.slug}/"]`).count());
      for (const anchor of ['comprar','locar','anunciar','vender']) {
        await page.locator(`.guide-toc a[href="#${anchor}"]`).click();
        assert.equal(new URL(page.url()).hash, '#' + anchor);
        await page.waitForFunction(id => Math.abs(document.getElementById(id).getBoundingClientRect().top - 96) < 2, anchor);
        assert.ok(await page.evaluate(id => document.getElementById(id).getBoundingClientRect().top >= document.querySelector('.pd-site-header').getBoundingClientRect().bottom, anchor));
      }
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
      assert.deepEqual(errors, []);
      await page.emulateMedia({media:'print'});
      assert.equal(await page.locator('.guide-route:visible').count(), 4);
      assert.equal(await page.locator('#guide-actions').isVisible(), false);
      await page.emulateMedia({media:'screen'});
      await page.goto('https://praia.digital/apps/guia-de-uso.html');
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.matches('a.pd-skip[href="#conteudo"]')), true);
      await page.keyboard.press('Enter');
      await page.waitForURL('**/apps/guia-de-uso.html#conteudo');
      assert.equal(await page.locator('#conteudo').count(), 1);
      await screenshot(page, {path:path.join(output, `guide-${width}.png`),fullPage:true});
      await context.close();
    }
    // Compare the current candidate with the PR base. Baseline removes the pageshow listener and anchor-margin fix only;
    // all other production code matches base a8ef91f7.
    const layoutResults = {};
    for (const variant of ['base-a8ef91f7', 'candidate']) {
      const context = await browser.newContext({viewport:{width:320,height:900}});
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.hostname !== 'praia.digital' || route.request().method() !== 'GET') return route.abort();
        let file = path.resolve(root, '.' + url.pathname);
        if (!file.startsWith(root + path.sep)) return route.abort();
        if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
        if (!fs.existsSync(file)) return route.abort();
        let body = fs.readFileSync(file);
        if (variant === 'base-a8ef91f7' && url.pathname === '/js/app-guide.js') {
          body = Buffer.from(body.toString().replace("  // Back/forward navigation can restore checkbox state without firing change.\n  window.addEventListener('pageshow', update);\n", ''));
        }
        if (variant === 'base-a8ef91f7' && url.pathname === '/css/app-guide.css') {
          body = Buffer.from(body.toString().replace('\n/* Keep skip-link and route targets below the shared fixed header. */\n#conteudo.guide-width,.guide-route{scroll-margin-top:6rem}\n', ''));
        }
        return route.fulfill({body,contentType:{'.css':'text/css','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg'}[path.extname(file)]||'text/html'});
      });
      const page = await context.newPage();
      await page.goto('https://praia.digital/apps/guia-de-uso.html');
      await page.evaluate(() => document.fonts.ready);
      const metrics = () => page.evaluate(() => ({
        scrollY, viewport:innerWidth, width:document.documentElement.scrollWidth,
        headerBottom:document.querySelector('.pd-site-header').getBoundingClientRect().bottom,
        elements:[...document.querySelectorAll('.pd-network-nav, .guide-hero, #conteudo')].map(el => {
          const r=el.getBoundingClientRect(); return {class:el.className,top:r.top,bottom:r.bottom,left:r.left,right:r.right};
        })
      }));
      layoutResults[variant] = {initial:await metrics()};
      await screenshot(page,{path:path.join(output, `compare-${variant}-320-initial.png`)});
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.matches('a.pd-skip[href="#conteudo"]')),true);
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash,'#conteudo');
      // Let native smooth scrolling finish before observing fixed/sticky layout.
      await page.waitForFunction(() => window.scrollY > 0);
      await page.evaluate(() => new Promise(resolve => {
        let previous=scrollY, stable=0;
        const check=()=>{stable=Math.abs(scrollY-previous)<0.1?stable+1:0;previous=scrollY;
          if(stable>=30)resolve();else requestAnimationFrame(check);};requestAnimationFrame(check);
      }));
      layoutResults[variant].anchor=await metrics();
      await screenshot(page,{path:path.join(output, `compare-${variant}-320-anchor.png`)});
      await screenshot(page,{path:path.join(output, `compare-${variant}-320-stable-full.png`),fullPage:true});
      await context.close();
    }
    assert.deepEqual(layoutResults.candidate.initial,layoutResults['base-a8ef91f7'].initial);
    assert.ok(layoutResults['base-a8ef91f7'].anchor.elements[2].top < layoutResults['base-a8ef91f7'].anchor.headerBottom, 'Baseline reproduces hidden anchor target');
    assert.ok(layoutResults.candidate.anchor.elements[2].top >= layoutResults.candidate.anchor.headerBottom, 'Candidate target clears the fixed header');
    fs.writeFileSync(path.join(output,'compare-320-metrics.json'),JSON.stringify(layoutResults,null,2));
    console.log('320px initial layout unchanged; baseline anchor hidden and candidate anchor clear after scrolling settles.');
    const nojs = await browser.newContext({javaScriptEnabled:false});
    const page = await nojs.newPage();
    const templatePath = '/downloads/ficha-acomodacao.txt';
    const guidePath = '/apps/guia-de-uso.html';
    const server = require('node:http').createServer((request, response) => {
      const file = request.url;
      if (file !== templatePath && file !== guidePath) {
        response.writeHead(404).end();
        return;
      }
      response.setHeader('Content-Type', file === templatePath ? 'text/plain;charset=utf-8' : 'text/html;charset=utf-8');
      response.end(fs.readFileSync(path.join(root, file)));
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    try {
      await page.goto(`http://127.0.0.1:${server.address().port}${guidePath}#qual-arquivo-guardar`);
      const files = page.locator('#qual-arquivo-guardar');
      const downloadReady = page.waitForEvent('download');
      await files.getByRole('link',{name:'baixe a ficha em branco em TXT'}).press('Enter');
      const template = await downloadReady;
      assert.equal(template.suggestedFilename(),'ficha-acomodacao.txt');
      assert.deepEqual(fs.readFileSync(await template.path()),fs.readFileSync(path.join(root,'downloads/ficha-acomodacao.txt')));
      await files.getByRole('link',{name:'opções de impressão e download'}).press('Enter');
      assert.equal(new URL(page.url()).hash,'#salvar-conferencias');
      assert.equal(await page.locator('#salvar-conferencias').isVisible(),true);
      assert.equal(await page.locator('.guide-route').count(),4);
      assert.equal(await page.locator('#guide-actions').isVisible(),false);
      await page.locator('input[type=checkbox]').first().check();
      assert.equal(await page.locator('input:checked').count(),1);
    } finally {
      server.close();
    }
    await nojs.close();
    console.log('Guide passed at 320,390,1280px: links to 16 apps, anchors, checklist/reset, keyboard, print, no-JS.');
  } finally { await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
