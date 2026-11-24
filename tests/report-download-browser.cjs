// Read-only local routes and fictitious input; no provider or email requests.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const deadline = setTimeout(() => { console.error('Report download test timed out'); process.exit(1); }, 120000);
(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    for (const width of [320, 390, 1280]) {
      const context = await browser.newContext({viewport:{width,height:900}});
      await context.route('**/*', route => {
        const url = new URL(route.request().url());
        assert.equal(route.request().method(), 'GET');
        if (url.origin !== 'https://praia.digital') return route.abort();
        const file = path.resolve(root, '.' + url.pathname + (url.pathname.endsWith('/') ? 'index.html' : ''));
        if (!file.startsWith(root + path.sep) || !fs.existsSync(file)) return route.fulfill({status:404,body:'Missing'});
        const types = {'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json'};
        return route.fulfill({body:fs.readFileSync(file),contentType:types[path.extname(file)] || 'application/octet-stream'});
      });
      const page = await context.newPage();
      page.setDefaultTimeout(15000);
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto('https://praia.digital/apps/checklist-vistoria/#pendencias-da-vistoria');
      await page.locator('#pendencias-da-vistoria a[href="/apps/relatorio-imovel/#evidencias-da-visita"]').press('Enter');
      await page.waitForURL('**/apps/relatorio-imovel/#evidencias-da-visita');
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      await page.getByRole('link', {name:'Conferir a pauta de retorno'}).press('Enter');
      await page.waitForURL('**/#pauta-de-retorno');
      const copy = page.getByRole('button', {name:'Copiar pauta completa'});
      await copy.waitFor({state:'visible'});
      assert.ok(await copy.isDisabled());
      await page.getByRole('link', {name:'Voltar aos campos de fontes e pendências'}).press('Enter');
      await page.waitForURL('**/#evidencias-da-visita');
      await page.locator('#pending').fill('A vaga atende à unidade em visita?');
      await page.locator('#contact').fill('Contato de teste');
      const pdf = await page.pdf({preferCSSPageSize:true});
      assert.equal((pdf.toString('latin1').match(/\/Type \/Page\b/g) || []).length,1);
      await context.grantPermissions(['clipboard-read','clipboard-write']);
      await copy.focus();
      await copy.press('Enter');
      await page.waitForFunction(()=>document.getElementById('agenda-copy-status').textContent === 'Pauta copiada.');
      assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'Pauta de retorno\n\nPontos a confirmar\nA vaga atende à unidade em visita?');
      await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true}));
      await copy.click();
      assert.equal(await page.locator('#agenda-text').evaluate(el=>el===document.activeElement && el.selectionEnd-el.selectionStart===el.value.length),true);
      await page.locator('#pending').fill('');
      assert.ok(await copy.isDisabled());
      assert.equal(await page.locator('#agenda-copy-status').textContent(),'');
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('#load-example').click();
      await page.locator('#pending').fill('Confirmar área privativa\nResponsável: equipe fictícia');
      const downloadText = async () => {
        const waiting = page.waitForEvent('download');
        await page.locator('#download-report').click();
        const file = await waiting;
        assert.equal(await file.failure(), null);
        return {name:file.suggestedFilename(),text:fs.readFileSync(await file.path(),'utf8')};
      };
      const example = await downloadText();
      assert.equal(example.name, 'relatorio-imovel-exemplo-ficticio.txt');
      assert.match(example.text,/EXEMPLO FICTÍCIO/);
      assert.match(example.text,/Confirmar área privativa\nResponsável: equipe fictícia/);
      assert.match(example.text,/America\/Sao_Paulo/);
      assert.match(example.text,/Fontes e datas de confirmação/);
      page.once('dialog', dialog => dialog.accept());
      await page.locator('#clear-report').click();
      const blank = await downloadText();
      assert.equal(blank.name,'relatorio-imovel.txt');
      assert.equal((blank.text.match(/\nA confirmar/g)||[]).length,17);
      assert.doesNotMatch(blank.text,/EXEMPLO FICTÍCIO|equipe fictícia/);
      assert.deepEqual(errors,[]);
      const disabledPage = await context.newPage();
      await disabledPage.goto('https://praia.digital/');
      const homeLink = disabledPage.locator('a[href="/apps/relatorio-imovel/#guardar-relatorio"]');
      assert.equal(await homeLink.count(),1);
      assert.match(await homeLink.textContent(),/em texto/);
      await homeLink.click();
      await disabledPage.waitForURL('**/apps/relatorio-imovel/#guardar-relatorio');
      assert.ok(await disabledPage.locator('#download-report').isEnabled());
      await context.close();
      console.log(`TXT content, reset and homepage link passed at ${width}px`);
    }
  } finally { await browser.close(); clearTimeout(deadline); }
})().catch(error => { clearTimeout(deadline); console.error(error); process.exit(1); });
