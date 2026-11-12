const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const files = ['avaliacao', 'conteudo', 'imagens', 'investidores', 'marketing', 'videos', 'portais'].map(name => `ia/ia-${name}.html`);
const checks = [];
function scripts(file) {
  return [...fs.readFileSync(path.join(root, file), 'utf8').matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
    .filter(match => !/ld\+json|\bsrc\s*=/.test(match[1])).map(match => match[2]);
}
function setup(file, marker, values = {}) {
  const elements = new Map(), alerts = [], copied = [];
  function element(id) {
    if (!elements.has(id)) {
      let html = '';
      elements.set(id, {
        value: values[id] ?? '', textContent: '', children: [],
        get innerHTML() { return html; },
        set innerHTML(value) { html = value; this.children = []; },
        classList: { values: new Set(), add(value) { this.values.add(value); }, remove(value) { this.values.delete(value); } },
        appendChild(child) { this.children.push(child); }, scrollIntoView() {}
      });
    }
    return elements.get(id);
  }
  const context = {
    document: { getElementById: element, createElement: () => ({ value: '', textContent: '' }) },
    navigator: { clipboard: { async writeText(value) { copied.push(value); } } },
    alert: value => alerts.push(value), Number, Math, Object, String
  };
  context.window = context;
  vm.createContext(context);
  const source = scripts(file).find(script => script.includes(marker));
  assert(source, `Missing application script: ${file}`);
  vm.runInContext(source, context, { filename: file });
  return { context, element, alerts, copied, run: source => vm.runInContext(source, context) };
}
function test(name, run) { run(); checks.push(name); }
async function testAsync(name, run) { await run(); checks.push(name); }
function noInvalidNumber(html) { assert(!/NaN|Infinity|∞|undefined/.test(html), html); }

async function main() {
  test('all seven application pages have parseable inline JavaScript', () => {
    for (const file of files) for (const source of scripts(file)) new vm.Script(source, { filename: file });
  });

  const valuation = setup(files[0], 'function runValuation(', { valTipo: 'apartamento', valCidade: 'santos', valArea: '100', valPreco: '1600000', valDiferencial: 'vista mar' });
  test('valuation computes finite illustrative output using the entered area', () => {
    valuation.context.runValuation();
    const html = valuation.element('valuationResult').innerHTML;
    assert(html.includes('1.610.000'));
    assert(html.includes('1.481.200'));
    assert(html.includes('1.738.800'));
    assert(html.includes('NÃO CONSTITUI PTAM'));
    noInvalidNumber(html);
  });
  test('valuation does not classify an omitted price as within range', () => {
    valuation.element('valPreco').value = '';
    valuation.element('valDiferencial').value = '<img src=x onerror=alert(1)>';
    valuation.context.runValuation();
    const html = valuation.element('valuationResult').innerHTML;
    assert(html.includes('Preço não informado'));
    assert(html.includes('&lt;img'));
    assert(!html.includes('<img'));
  });
  for (const [field, value] of [['valArea', ''], ['valArea', '-1'], ['valArea', 'Infinity'], ['valArea', 'invalid'], ['valPreco', '-1'], ['valCidade', 'invalid']]) {
    test(`valuation rejects ${field}=${JSON.stringify(value)}`, () => {
      const previous = valuation.element(field).value;
      valuation.element(field).value = value;
      const before = valuation.alerts.length;
      valuation.context.runValuation();
      assert.equal(valuation.alerts.length, before + 1);
      assert(!valuation.element('valuationResult').classList.values.has('visible'));
      valuation.element(field).value = previous;
    });
  }
  test('valuation rejects finite inputs that overflow or exceed safe derived values', () => {
    const previous = valuation.element('valArea').value;
    const previousOutput = valuation.element('valuationResult').innerHTML;
    for (const area of ['1e308', '1e14']) {
      valuation.element('valArea').value = area;
      const before = valuation.alerts.length;
      valuation.context.runValuation();
      assert.equal(valuation.alerts.length, before + 1);
      assert(valuation.alerts.at(-1).includes('limites numéricos'));
      assert(!valuation.element('valuationResult').classList.values.has('visible'));
      assert.equal(valuation.element('valuationResult').innerHTML, previousOutput);
    }
    valuation.element('valArea').value = previous;
  });

  const content = setup(files[1], 'function generate(');
  for (const type of ['noticia', 'guia', 'bairro', 'investidor', 'seo']) {
    test(`content generates the ${type} template`, () => {
      content.context.generate(type);
      assert(content.element('contentResult').innerHTML.length > 150);
      assert(content.element('contentResult').classList.values.has('visible'));
      noInvalidNumber(content.element('contentResult').innerHTML);
    });
  }
  test('content handles unknown and inherited property names without executing them', () => {
    for (const type of ['unknown', 'constructor', '__proto__']) {
      content.context.generate(type);
      assert(content.element('contentResult').innerHTML.includes('Escolha um tipo de conteúdo.'));
    }
  });
  await testAsync('content copies the full text and recovers when clipboard is unavailable', async () => {
    await content.context.copyText({ previousElementSibling: { innerText: 'Texto completo\nSegunda linha' } });
    assert.equal(content.copied.at(-1), 'Texto completo\nSegunda linha');
    content.context.navigator.clipboard = undefined;
    await content.context.copyText({});
    assert(content.alerts.at(-1).includes('manualmente'));
  });

  const images = setup(files[2], 'function runImages(', { iTipo: 'casa', iCidade: 'santos', iCanal: 'anuncio' });
  for (const channel of ['anuncio', 'banner', 'rede']) {
    test(`images generate three concepts for ${channel}`, () => {
      images.element('iCanal').value = channel;
      images.context.runImages();
      const html = images.element('imgResult').innerHTML;
      assert.equal((html.match(/class="preview"/g) || []).length, 3);
      assert(html.includes('Santos'));
      noInvalidNumber(html);
    });
  }
  test('images reject invalid selection values', () => {
    images.element('iCidade').value = '<img src=x>';
    images.context.runImages();
    assert(images.alerts.at(-1).includes('válidos'));
    assert(!images.element('imgResult').classList.values.has('visible'));
  });

  const investor = setup(files[3], 'function calcInvestor(', { invPrice: '800000', invDown: '200000', invRent: '4000', invExp: '1000', invCity: 'santos' });
  test('investor scenario produces the entered cash flow before financing', () => {
    investor.context.calcInvestor();
    const html = investor.element('kpis').innerHTML;
    for (const value of ['3.000', '36.000', '18.00%', '4.50%', '5.6 anos']) assert(html.includes(value), value);
    assert(html.includes('antes do financiamento'));
    noInvalidNumber(html);
  });
  for (const [field, value] of [['invPrice', ''], ['invPrice', '-1'], ['invPrice', 'Infinity'], ['invDown', '900000'], ['invDown', '0'], ['invRent', ''], ['invRent', '-1'], ['invExp', '-1'], ['invExp', 'invalid'], ['invCity', 'constructor']]) {
    test(`investor rejects ${field}=${JSON.stringify(value)}`, () => {
      const previous = investor.element(field).value;
      investor.element(field).value = value;
      const before = investor.alerts.length;
      investor.context.calcInvestor();
      assert.equal(investor.alerts.length, before + 1);
      assert(!investor.element('investorResult').classList.values.has('visible'));
      investor.element(field).value = previous;
    });
  }
  test('investor rejects overflowing amounts and unsafe ratios from tiny positive inputs', () => {
    const previousOutput = investor.element('kpis').innerHTML;
    for (const values of [{ invRent: '1e308' }, { invRent: '1e15' }, { invDown: '1e-308' }, { invRent: '1e-308', invExp: '0' }]) {
      const previous = Object.fromEntries(Object.keys(values).map(field => [field, investor.element(field).value]));
      for (const [field, value] of Object.entries(values)) investor.element(field).value = value;
      const before = investor.alerts.length;
      investor.context.calcInvestor();
      assert.equal(investor.alerts.length, before + 1);
      assert(investor.alerts.at(-1).includes('limites numéricos'));
      assert(!investor.element('investorResult').classList.values.has('visible'));
      assert.equal(investor.element('kpis').innerHTML, previousOutput);
      for (const [field, value] of Object.entries(previous)) investor.element(field).value = value;
    }
  });
  test('investor handles zero and negative operating income without infinite payback', () => {
    for (const rent of ['1000', '0']) {
      investor.element('invRent').value = rent;
      investor.context.calcInvestor();
      const html = investor.element('kpis').innerHTML;
      noInvalidNumber(html);
      assert(html.includes('>—</div>'));
      assert(investor.element('investorResult').classList.values.has('visible'));
    }
  });

  const marketing = setup(files[4], 'function runMarketing(', { mkCanal: 'instagram', mkFormat: 'post', mkCidade: 'santos', mkPublico: 'comprador', mkDiferencial: '<img src=x onerror=alert(1)>', mkObjetivo: 'visitas' });
  for (const channel of ['instagram', 'facebook', 'linkedin', 'tiktok', 'youtube', 'email', 'meta', 'google']) {
    test(`marketing generates and refreshes formats for ${channel}`, () => {
      marketing.element('mkCanal').value = channel;
      marketing.context.refreshFormats();
      const formats = marketing.element('mkFormat').children.map(item => item.value);
      if (channel === 'email') assert.deepEqual(formats, ['sequencia', 'one-mail']);
      else if (['meta', 'google'].includes(channel)) assert.deepEqual(formats, ['ad', 'campaign']);
      else assert.equal(formats.length, 5);
      marketing.context.runMarketing();
      const html = marketing.element('marketingResult').innerHTML;
      assert(html.includes('Santos'));
      assert(html.includes('&lt;img'));
      assert(!html.includes('<img'));
      noInvalidNumber(html);
      for (const match of html.matchAll(/onclick="([^"]+)"/g)) new vm.Script(match[1]);
    });
  }
  await testAsync('marketing copy buttons copy one complete block and the complete package', async () => {
    marketing.element('mkCanal').value = 'instagram';
    marketing.context.runMarketing();
    const handlers = [...marketing.element('marketingResult').innerHTML.matchAll(/onclick="([^"]+)"/g)].map(match => match[1]);
    await marketing.run(handlers[0]);
    assert.equal(marketing.copied.at(-1), marketing.context.__mkBlocks[0].value);
    assert(marketing.copied.at(-1).length > 1);
    await marketing.run(handlers.at(-1));
    assert.equal(marketing.copied.at(-1), marketing.context.__mkCopyText);
    marketing.context.navigator.clipboard.writeText = async () => { throw new Error('denied'); };
    await marketing.run(handlers[0]);
    assert(marketing.alerts.at(-1).includes('manualmente'));
  });
  test('marketing rejects invalid selections without generating undefined text', () => {
    marketing.element('mkPublico').value = 'constructor';
    marketing.context.runMarketing();
    assert(marketing.alerts.at(-1).includes('válidos'));
    assert(!marketing.element('marketingResult').classList.values.has('visible'));
  });

  const video = setup(files[5], 'function runVideo(', { vFormato: 'reel', vCidade: 'santos' });
  for (const format of ['reel', 'tour', 'apresentacao', 'narrado']) {
    test(`video generates the ${format} script`, () => {
      video.element('vFormato').value = format;
      video.context.runVideo();
      assert(video.element('videoResult').innerHTML.length > 200);
      noInvalidNumber(video.element('videoResult').innerHTML);
    });
  }
  test('video handles an invalid format and rejects an invalid city', () => {
    video.element('vFormato').value = 'constructor';
    video.context.runVideo();
    assert(video.element('videoResult').innerHTML.includes('Escolha um formato.'));
    video.element('vCidade').value = '<img src=x>';
    video.context.runVideo();
    assert(video.alerts.at(-1).includes('válida'));
    assert(!video.element('videoResult').classList.values.has('visible'));
  });
  await testAsync('video copies the entire script and recovers from clipboard denial', async () => {
    await video.context.copyText({ previousElementSibling: { innerText: 'Roteiro completo\nCena final' } });
    assert.equal(video.copied.at(-1), 'Roteiro completo\nCena final');
    video.context.navigator.clipboard.writeText = async () => { throw new Error('denied'); };
    await video.context.copyText({});
    assert(video.alerts.at(-1).includes('manualmente'));
  });
  const seo = setup(files[6], 'function runSEO(', { seoTipo: 'apartamento', seoCidade: 'santos', seoBairro: 'Gonzaga', seoDorms: '2', seoPreco: '850000', seoDiferencial: 'vista mar' });
  seo.element('seoCidade').options = [{ value: 'santos', text: 'Santos' }];
  seo.element('seoCidade').selectedIndex = 0;
  test('portal SEO generates metadata with the entered price and a proposed slug only', () => {
    seo.context.runSEO();
    const html = seo.element('seoResult').innerHTML;
    assert(html.includes('850.000'));
    assert(html.includes('apto 2q em Gonzaga — Santos'));
    assert(html.includes('URL sugerida (não publicada): /apartamento-2q-gonzaga-santos.html'));
    assert(!html.includes('<a '));
    noInvalidNumber(html);
  });
  test('portal SEO accepts blank optional fields without inventing price or bedrooms', () => {
    for (const field of ['seoBairro', 'seoDorms', 'seoPreco', 'seoDiferencial']) seo.element(field).value = '';
    seo.context.runSEO();
    const html = seo.element('seoResult').innerHTML;
    assert(!html.includes('R$'));
    assert(!html.includes('• Quartos:'));
    assert(html.includes('/apartamento-santos.html'));
    noInvalidNumber(html);
  });
  test('portal SEO rejects invalid amounts, bedrooms and selection values', () => {
    for (const [field, value] of [['seoPreco', '-1'], ['seoPreco', 'invalid'], ['seoPreco', '1e308'], ['seoDorms', '-1'], ['seoDorms', '1.5'], ['seoDorms', '<img>'], ['seoDorms', '1e308'], ['seoTipo', 'unknown'], ['seoCidade', 'unknown']]) {
      const previous = seo.element(field).value;
      const before = seo.alerts.length;
      seo.element(field).value = value;
      seo.context.runSEO();
      assert.equal(seo.alerts.length, before + 1);
      assert(!seo.element('seoResult').classList.values.has('visible'));
      seo.element(field).value = previous;
    }
    seo.element('seoCidade').selectedIndex = -1;
    seo.context.runSEO();
    assert(!seo.element('seoResult').classList.values.has('visible'));
    seo.element('seoCidade').selectedIndex = 0;
  });
  test('portal SEO escapes user text in metadata, keywords and description', () => {
    seo.element('seoBairro').value = '<img src=x onerror=alert(1)>&';
    seo.element('seoDiferencial').value = '<script>alert(1)</script>';
    seo.context.runSEO();
    const html = seo.element('seoResult').innerHTML;
    assert(!html.includes('<img'));
    assert(!html.includes('<script>'));
    for (const className of ['meta-title', 'meta-desc', 'keywords']) {
      const block = html.match(new RegExp(`<div class="${className}">([\\s\\S]*?)</div>`));
      assert(block && block[1].includes('&lt;img'));
      assert(block[1].includes('&amp;'));
    }
    assert(html.includes('&lt;script&gt;'));
  });
  await testAsync('portal SEO copies the full package and recovers from absent or denied clipboard', async () => {
    await seo.context.copyText(seo.context.__seoCopyText);
    assert.equal(seo.copied.at(-1), seo.context.__seoCopyText);
    assert(seo.copied.at(-1).includes('URL sugerida (não publicada):'));
    seo.context.navigator.clipboard.writeText = async () => { throw new Error('denied'); };
    await seo.context.copyText(seo.context.__seoCopyText);
    assert(seo.alerts.at(-1).includes('manualmente'));
    seo.context.navigator.clipboard = undefined;
    await seo.context.copyText(seo.context.__seoCopyText);
    assert(seo.alerts.at(-1).includes('manualmente'));
  });
  console.log(JSON.stringify({ checks: checks.length, passed: checks.length, pages: files.length }));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
