'use strict';

// Run: NODE_PATH=/tmp/pd-compra-qa/node_modules node tests/alugar-comprar-dom.cjs
// These checks execute only local calculator code. No ads, shared scripts,
// external requests, browser telemetry or submitted user data are involved.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM, VirtualConsole } = require('jsdom');
const root = path.resolve(__dirname, '..');
const canonical = 'https://praia.digital/apps/alugar-ou-comprar/';
const html = fs.readFileSync(path.join(root, 'apps/alugar-ou-comprar/index.html'), 'utf8');
const source = {
  core: fs.readFileSync(path.join(root, 'js/alugar-comprar-core.js'), 'utf8'),
  ui: fs.readFileSync(path.join(root, 'js/alugar-comprar-ui.js'), 'utf8')
};
const referenceCore = require('../js/alugar-comprar-core.js');
const ids = { ...Object.fromEntries(Object.entries(referenceCore.fields).map(([key, field]) => [key, field.id])),
  rateType: 'tipoTaxa', amortization: 'sistema' };
const normalize = text => text.replace(/\s+/g, ' ').trim();
const money = value => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })
  .format(Math.abs(value) < 0.005 ? 0 : value);

function load({ core = true, ui = true } = {}) {
  const errors = [];
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('jsdomError', error => errors.push(error));
  const dom = new JSDOM(html, { runScripts: 'outside-only', url: canonical, virtualConsole });
  const w = dom.window;
  const d = w.document;
  const scrolls = [];
  w.HTMLElement.prototype.scrollIntoView = function (options) { scrolls.push({ id: this.id, options }); };
  if (core) w.eval(source.core);
  if (ui) w.eval(source.ui);
  const get = id => d.getElementById(id);
  const set = (id, value, event = 'input') => {
    get(id).value = String(value);
    get(id).dispatchEvent(new w.Event(event, { bubbles: true }));
  };
  const setParams = overrides => Object.entries(overrides).forEach(([key, value]) => set(ids[key], value));
  const submit = () => {
    const event = new w.Event('submit', { bubbles: true, cancelable: true });
    get('rent-buy-form').dispatchEvent(event);
    assert.equal(event.defaultPrevented, true, 'No native submission may escape the calculator');
  };
  const restore = () => get('restore-example').click();
  const read = () => Object.fromEntries(Object.entries(ids).map(([key, id]) => [key, get(id).value]));
  return { dom, w, d, get, set, setParams, submit, restore, read, errors, scrolls };
}
function uiTest(name, fn) {
  test(name, async () => {
    const app = load();
    try { await fn(app); assert.deepEqual(app.errors, []); }
    finally { app.w.close(); }
  });
}
function assertValid(app) {
  assert.equal(app.get('res').hidden, false);
  assert.equal(app.get('error-summary').hidden, true);
  assert.equal(app.d.querySelectorAll('[aria-invalid="true"]').length, 0);
  assert.doesNotMatch(app.get('res').textContent, /NaN|Infinity|undefined/);
}
const zeroScenario = {
  price: 120000, downPayment: 120000, rent: 0, annualInterest: 0,
  loanYears: 1, horizonYears: 1, appreciation: 0, rentGrowth: 0,
  investmentReturn: 0, purchaseCostPct: 0, saleCostPct: 0, annualMaintenance: 0,
  ownerMonthly: 0, renterMonthly: 0, expenseGrowth: 0, loanMonthly: 0,
  balanceIndex: 0, saleTax: 0, rateType: 'nominal', amortization: 'PRICE'
};

test('no-JavaScript markup cannot submit financial scenario values in a query string', () => {
  const app = load({ core: false, ui: false });
  try {
    const form = app.get('rent-buy-form');
    assert.equal(form.querySelector('[type="submit"]').disabled, true);
    assert.equal(form.querySelectorAll('[name]').length, 0);
    assert.equal([...new app.w.FormData(form).entries()].length, 0);
    assert.equal(app.get('res').hidden, true);
    assert.match(app.d.querySelector('noscript').textContent, /Ative JavaScript/);
    assert.ok(app.get('pd-guide-title'));
  } finally { app.w.close(); }
});

test('partial script failure leaves native submission disabled', () => {
  for (const options of [{ core: false, ui: true }, { core: true, ui: false }]) {
    const app = load(options);
    try {
      assert.equal(app.get('rent-buy-form').querySelector('[type="submit"]').disabled, true);
      assert.equal(app.get('res').hidden, true);
      assert.deepEqual(app.errors, []);
    } finally { app.w.close(); }
  }
});

uiTest('initial example agrees with every core default and does not steal focus', app => {
  assertValid(app);
  for (const [key, id] of Object.entries(ids)) assert.equal(app.get(id).value, String(referenceCore.defaults[key]), id);
  assert.equal(app.get('result-label').textContent, 'Exemplo ilustrativo');
  assert.equal(app.d.activeElement, app.d.body);
  assert.equal(app.scrolls.length, 0);
  assert.equal(app.get('rent-buy-form').querySelector('[type="submit"]').disabled, false);
  assert.equal(app.get('yearly-body').rows.length, referenceCore.defaults.horizonYears);
  assert.equal(app.get('sensitivity-body').rows.length, 5);
  assert.match(app.get('result-live').textContent, /Exemplo carregado/);
});

uiTest('numeric fields, limits, labels, hints and error associations match the model', app => {
  const allIds = [...app.d.querySelectorAll('[id]')].map(element => element.id);
  assert.equal(new Set(allIds).size, allIds.length, 'All document IDs must be unique');
  for (const [key, id] of Object.entries(ids)) {
    const field = app.get(id);
    assert.ok(field);
    assert.equal(field.labels.length, 1, id);
    assert.ok(field.labels[0].textContent.trim(), id);
    const descriptions = field.getAttribute('aria-describedby').split(/\s+/);
    assert.ok(descriptions.includes(`${id}-hint`), id);
    assert.ok(descriptions.includes(`${id}-error`), id);
    descriptions.forEach(description => assert.ok(app.get(description), description));
    if (referenceCore.fields[key]) {
      const specification = referenceCore.fields[key];
      assert.equal(field.type, 'number', id);
      assert.equal(field.required, true, id);
      assert.equal(Number(field.min), specification.min, id);
      assert.equal(Number(field.max), specification.max, id);
      if (specification.integer) assert.equal(field.step, '1', id);
    }
  }
});

uiTest('formatted metrics faithfully represent the numerical result', app => {
  const result = referenceCore.calculate(app.read());
  const metrics = {
    'owner-wealth': 'ownerWealth', 'renter-wealth': 'renterWealth',
    'initial-cash': 'initialCash', 'purchase-costs': 'purchaseCosts', 'financed': 'financed',
    'rParc': 'firstPayment', 'first-owner-cost': 'firstOwnerCost', 'first-renter-cost': 'firstRenterCost',
    'rAlug': 'totalRent', 'owner-outlay': 'ownerOutlay', 'renter-outlay': 'renterOutlay',
    'total-loan': 'totalLoanPayments', 'total-interest': 'totalInterest', 'total-indexation': 'totalIndexation',
    'rImovel': 'property', 'remaining-debt': 'debt', 'sale-costs': 'sellingCosts', 'sale-tax': 'saleTax',
    'owner-contributions': 'ownerContributions', 'renter-contributions': 'renterContributions'
  };
  for (const [id, key] of Object.entries(metrics)) assert.equal(app.get(id).textContent, money(result[key]), id);
  assert.match(app.get('rVerdict').textContent, new RegExp(result.outcome === 'buy' ? '^Comprar' : '^Alugar e investir'));
  assert.ok(app.get('rVerdict').textContent.includes(money(Math.abs(result.difference))));
});

uiTest('submission changes the example label, uses the chosen horizon and focuses the results', app => {
  app.set('horizonte', 1);
  app.submit();
  assertValid(app);
  assert.equal(app.get('result-label').textContent, 'Cenário informado');
  assert.equal(app.get('result-title').textContent, 'Patrimônio ao fim de 1 ano');
  assert.equal(app.d.activeElement.id, 'result-title');
  assert.equal(app.scrolls.at(-1).id, 'result-title');
  assert.equal(app.get('yearly-body').rows.length, 1);
  assert.match(app.get('result-live').textContent, /Comparação atualizada/);
});

uiTest('repeated submissions replace rows rather than duplicating results', app => {
  for (let index = 0; index < 3; index += 1) app.submit();
  assert.equal(app.get('yearly-body').rows.length, referenceCore.defaults.horizonYears);
  assert.equal(app.get('sensitivity-body').rows.length, 5);
  assert.equal(app.get('error-list').children.length, 0);
});

uiTest('editing any numeric assumption immediately hides stale results', app => {
  for (const field of Object.values(referenceCore.fields)) {
    app.restore();
    app.set(field.id, field.value);
    assert.equal(app.get('res').hidden, true, field.id);
    assert.match(app.get('result-live').textContent, /Premissas alteradas/, field.id);
    assert.doesNotMatch(app.get('result-live').textContent, /termina com/, field.id);
  }
});

uiTest('change events from both selectors hide stale results without assuming an input event', app => {
  for (const [id, value] of [['sistema', 'SAC'], ['tipoTaxa', 'effective']]) {
    app.restore();
    app.set(id, value, 'change');
    assert.equal(app.get('res').hidden, true, id);
    assert.match(app.get('result-live').textContent, /Compare novamente/);
    app.submit();
    assertValid(app);
  }
});

uiTest('Restore example restores all defaults, clears errors and replaces the previous result', app => {
  app.setParams({ horizonYears: 1, price: 800000, amortization: 'SAC', rateType: 'effective', saleTax: 10000 });
  app.submit();
  app.set('custoCompra', '');
  app.submit();
  assert.equal(app.get('error-summary').hidden, false);
  app.restore();
  assertValid(app);
  for (const [key, id] of Object.entries(ids)) assert.equal(app.get(id).value, String(referenceCore.defaults[key]), id);
  assert.equal(app.get('result-label').textContent, 'Exemplo ilustrativo');
  assert.equal(app.get('yearly-body').rows.length, referenceCore.defaults.horizonYears);
  assert.equal(app.d.activeElement.id, 'result-title');
  assert.equal(app.get('error-list').children.length, 0);
  for (const id of Object.values(ids)) assert.equal(app.get(`${id}-error`).textContent, '');
});

uiTest('native form reset cannot leave the previous scenario visible against restored inputs', async app => {
  app.set('valor', 800000);
  app.submit();
  app.get('rent-buy-form').reset();
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.equal(app.get('valor').value, String(referenceCore.defaults.price));
  if (!app.get('res').hidden) {
    const expected = referenceCore.calculate(referenceCore.defaults);
    assert.equal(app.get('owner-wealth').textContent, money(expected.ownerWealth));
    assert.equal(app.get('renter-wealth').textContent, money(expected.renterWealth));
  }
  assert.equal(app.get('error-summary').hidden, true);
});

uiTest('blank numeric values never silently reuse defaults, including zero-valued advanced fields', app => {
  for (const field of Object.values(referenceCore.fields)) {
    app.restore();
    app.set(field.id, '');
    app.submit();
    assert.equal(app.get('res').hidden, true, field.id);
    assert.equal(app.get(field.id).getAttribute('aria-invalid'), 'true', field.id);
    assert.match(app.get(`${field.id}-error`).textContent, /número válido/, field.id);
    assert.equal(app.d.activeElement.id, field.id, field.id);
  }
});

uiTest('minimum and maximum violations render accessible errors for every numeric field', app => {
  for (const field of Object.values(referenceCore.fields)) {
    for (const value of [field.min - 1, field.max + 1]) {
      app.restore();
      app.set(field.id, value);
      app.submit();
      assert.equal(app.get('res').hidden, true, field.id);
      assert.equal(app.get(field.id).getAttribute('aria-invalid'), 'true', `${field.id}: ${value}`);
      assert.match(app.get(`${field.id}-error`).textContent, /entre/, field.id);
    }
  }
});

uiTest('entry greater than price and fractional year values are rejected', app => {
  app.set('entrada', referenceCore.defaults.price + 1);
  app.submit();
  assert.match(app.get('entrada-error').textContent, /não pode superar/);
  for (const id of ['anos', 'horizonte']) {
    app.restore();
    app.set(id, 1.5);
    app.submit();
    assert.match(app.get(`${id}-error`).textContent, /inteiro/);
    assert.equal(app.get('res').hidden, true);
  }
});

uiTest('unsupported selectors have explicit errors rather than falling back silently', app => {
  for (const id of ['sistema', 'tipoTaxa']) {
    app.restore();
    app.set(id, 'invalid', 'change');
    app.submit();
    assert.equal(app.get(id).getAttribute('aria-invalid'), 'true');
    assert.match(app.get(`${id}-error`).textContent, /opção válida/);
  }
});

uiTest('negative growth and return assumptions are accepted with finite visible results', app => {
  app.setParams({ appreciation: -25, investmentReturn: -15, rentGrowth: -10, expenseGrowth: -10 });
  app.submit();
  assertValid(app);
  assert.match(app.get('rImovel').textContent, /R\$/);
});

uiTest('zero rates and cash purchase are valid and do not retain loan fees or interest', app => {
  app.setParams({ ...zeroScenario, annualInterest: 100, loanMonthly: 1000000, balanceIndex: 30 });
  app.submit();
  assertValid(app);
  for (const id of ['financed', 'rParc', 'remaining-debt', 'total-interest', 'total-loan', 'total-indexation']) {
    assert.equal(app.get(id).textContent, money(0), id);
  }
  assert.match(app.get('rate-description').textContent, /Compra à vista/);
  assert.match(app.get('rVerdict').textContent, /Patrimônios próximos/);
});

uiTest('hidden advanced errors open the appropriate section and focus the first invalid field', app => {
  for (const [id, details] of [['indexador', 'advanced-finance'], ['impostoVenda', 'advanced-costs']]) {
    app.restore();
    app.get(details).open = false;
    app.set(id, -1);
    app.submit();
    assert.equal(app.get(details).open, true, id);
    assert.equal(app.d.activeElement.id, id);
    assert.equal(app.get('error-summary').hidden, false);
    assert.equal(app.get('error-list').children.length, 1);
    assert.match(app.get('result-live').textContent, /Não foi possível comparar/);
  }
});

uiTest('error-summary links reopen advanced sections and focus their target field', app => {
  app.setParams({ price: 0, balanceIndex: -1, saleTax: -1 });
  app.submit();
  assert.equal(app.d.activeElement.id, 'valor');
  assert.equal(app.get('error-list').children.length, 3);
  app.get('advanced-costs').open = false;
  app.get('error-list').querySelector('a[href="#impostoVenda"]').click();
  assert.equal(app.get('advanced-costs').open, true);
  assert.equal(app.d.activeElement.id, 'impostoVenda');
  app.set('valor', referenceCore.defaults.price);
  assert.equal(app.get('error-summary').hidden, true);
  assert.equal(app.d.querySelectorAll('[aria-invalid="true"]').length, 0);
  assert.equal(app.get('res').hidden, true);
});

uiTest('nominal capitalization and effective rates are clearly distinguished', app => {
  assert.match(app.get('rate-description').textContent, /nominais, com capitalização mensal/);
  assert.match(app.get('tipoTaxa-hint').textContent, /anual ÷ 12/);
  app.setParams({ amortization: 'SAC', rateType: 'effective', annualInterest: 12, balanceIndex: 4 });
  app.submit();
  assertValid(app);
  assert.match(app.get('rate-description').textContent, /^SAC/);
  assert.match(app.get('rate-description').textContent, /12% a.a. efetivos/);
  assert.match(app.get('rate-description').textContent, /correção do saldo de 4%/);
  assert.match(app.get('indexador-hint').textContent, /Zero ignora correção/);
});

uiTest('tax provision is disclosed as an estimate and zero does not imply exemption', app => {
  assert.match(app.get('impostoVenda-hint').textContent, /Zero significa não provisionado/);
  assert.match(app.get('net-warning').textContent, /não provisionado/);
  assert.match(app.get('net-warning').textContent, /Zero não significa isenção/);
  app.set('impostoVenda', 10000);
  app.submit();
  assert.equal(app.get('sale-tax').textContent, money(10000));
  assert.match(app.get('net-warning').textContent, /não um cálculo tributário/);
});

uiTest('negative final equity is displayed with a deficit warning and never hidden or floored', app => {
  app.setParams({ ...zeroScenario, downPayment: 0, loanYears: 50,
    appreciation: -50, saleCostPct: 30, saleTax: 1000000 });
  app.submit();
  assertValid(app);
  assert.match(app.get('net-warning').textContent, /não cobre/);
  assert.match(app.get('net-warning').textContent, /déficit foi mantido/);
  assert.match(app.get('owner-wealth').textContent, /^-R\$/);
  assert.match(app.get('rVerdict').textContent, /^Alugar e investir/);
});

uiTest('buy, rent and close conclusions come from net wealth rather than a yield threshold', app => {
  app.setParams({ ...zeroScenario, rent: 100 });
  app.submit();
  assert.match(app.get('rVerdict').textContent, /^Comprar/);
  assert.match(app.get('yield-info').textContent, /não determina a conclusão/);
  app.set('impostoVenda', 10000);
  app.submit();
  assert.match(app.get('rVerdict').textContent, /^Alugar e investir/);
  app.setParams({ rent: 0, saleTax: 0 });
  app.submit();
  assert.match(app.get('rVerdict').textContent, /Patrimônios próximos/);
});

uiTest('sensitivity out-of-domain endpoints clearly report unavailable calculations', app => {
  app.setParams({ appreciation: -50, investmentReturn: 100 });
  app.submit();
  assertValid(app);
  const rows = [...app.get('sensitivity-body').rows];
  assert.equal(rows.length, 5);
  assert.equal(rows.filter(row => row.textContent.includes('Não calculado')).length, 2);
  assert.match(app.get('sensitivity-body').textContent, /Fora dos limites de taxa/);
  assert.doesNotMatch(app.get('sensitivity-body').textContent, /NaN|undefined|Infinity/);
});

uiTest('largest supported values and 50-year tables render without NaN or duplicate rows', app => {
  const high = Object.fromEntries(Object.entries(referenceCore.fields).map(([key, field]) => [key, field.max]));
  app.setParams({ ...high, downPayment: 0 });
  app.submit();
  assertValid(app);
  assert.equal(app.get('yearly-body').rows.length, 50);
  assert.equal(app.get('sensitivity-body').rows.length, 5);
  app.restore();
  assert.equal(app.get('yearly-body').rows.length, referenceCore.defaults.horizonYears);
});

uiTest('live status, table semantics and keyboard navigation targets are accessible', app => {
  const live = app.get('result-live');
  assert.equal(live.getAttribute('role'), 'status');
  assert.equal(live.getAttribute('aria-live'), 'polite');
  assert.equal(live.getAttribute('aria-atomic'), 'true');
  assert.equal(live.closest('[hidden]'), null);
  assert.equal(app.get('error-summary').getAttribute('role'), 'alert');
  assert.equal(app.get('res').getAttribute('aria-labelledby'), 'result-title');
  assert.equal(app.get('result-title').getAttribute('tabindex'), '-1');
  assert.ok(app.d.querySelector('a.skip-link[href="#main"]'));
  assert.equal(app.get('main').getAttribute('tabindex'), '-1');
  for (const table of app.d.querySelectorAll('#res table')) {
    assert.ok(table.caption && table.caption.textContent.trim());
    for (const cell of table.querySelectorAll('thead th')) assert.equal(cell.scope, 'col');
    for (const row of table.tBodies[0].rows) assert.equal(row.cells[0].scope, 'row');
  }
  const scroll = app.d.querySelector('.rb-table-scroll');
  assert.equal(scroll.getAttribute('role'), 'region');
  assert.equal(scroll.getAttribute('tabindex'), '0');
  assert.ok(scroll.getAttribute('aria-label'));
});

uiTest('FAQ structured data matches all visible questions and answers verbatim', app => {
  const schemas = [...app.d.querySelectorAll('script[type="application/ld+json"]')].map(node => JSON.parse(node.textContent));
  assert.equal(schemas.filter(schema => schema['@type'] === 'FAQPage').length, 1);
  const faq = schemas.find(schema => schema['@type'] === 'FAQPage');
  const visible = [...app.get('faq-title').parentElement.querySelectorAll('details')];
  assert.equal(faq.mainEntity.length, visible.length);
  visible.forEach((detail, index) => {
    assert.equal(faq.mainEntity[index]['@type'], 'Question');
    assert.equal(normalize(faq.mainEntity[index].name), normalize(detail.querySelector('summary').textContent));
    assert.equal(faq.mainEntity[index].acceptedAnswer['@type'], 'Answer');
    assert.equal(normalize(faq.mainEntity[index].acceptedAnswer.text),
      normalize([...detail.querySelectorAll('p')].map(node => node.textContent).join(' ')));
  });
  const appSchema = schemas.find(schema => schema['@type'] === 'WebApplication');
  assert.equal(appSchema.url, canonical);
  assert.equal(appSchema.offers.price, '0');
  assert.equal(appSchema.offers.priceCurrency, 'BRL');
});

uiTest('canonical, social metadata, locale and primary heading are consistent', app => {
  assert.equal(app.d.documentElement.lang, 'pt-BR');
  assert.equal(app.d.querySelectorAll('h1').length, 1);
  assert.match(app.d.querySelector('h1').textContent, /Alugar ou comprar/);
  assert.equal(app.d.querySelectorAll('link[rel="canonical"]').length, 1);
  assert.equal(app.d.querySelector('link[rel="canonical"]').href, canonical);
  assert.equal(app.d.querySelector('meta[property="og:url"]').content, canonical);
  assert.match(app.d.title, /Comparador Patrimonial/);
  assert.match(app.d.querySelector('meta[name="description"]').content, /patrimônio/);
  assert.match(app.d.querySelector('meta[name="viewport"]').content, /width=device-width/);
});

uiTest('all local links, hash targets and local script/style assets exist', app => {
  const references = [...app.d.querySelectorAll('a[href], script[src], link[rel="stylesheet"]')];
  for (const element of references) {
    const raw = element.getAttribute(element.tagName === 'SCRIPT' ? 'src' : 'href');
    assert.ok(raw && raw !== '#', element.outerHTML);
    assert.doesNotMatch(raw, /^javascript:/i);
    const url = new URL(raw, canonical);
    if (url.origin !== new URL(canonical).origin) {
      assert.equal(url.protocol, 'https:', raw);
      continue; // HTTP availability is a browser/network check, not a DOM assertion.
    }
    const local = path.join(root, decodeURIComponent(url.pathname));
    const target = url.pathname.endsWith('/') ? path.join(local, 'index.html') : local;
    assert.ok(fs.existsSync(target), `Missing local target: ${raw}`);
    if (url.hash) {
      const targetHtml = url.pathname === new URL(canonical).pathname ? app.d :
        new JSDOM(fs.readFileSync(target, 'utf8')).window.document;
      assert.ok(targetHtml.getElementById(decodeURIComponent(url.hash.slice(1))), `Missing fragment: ${raw}`);
      if (targetHtml !== app.d) targetHtml.defaultView.close();
    }
  }
});

uiTest('methodology discloses equal budgets, nominal values, timing, uncertainty and tax limits', app => {
  const guide = normalize(app.get('pd-guide-title').parentElement.textContent);
  assert.match(guide, /Mesmo capital inicial/);
  assert.match(guide, /maior custo de moradia/);
  assert.match(guide, /não comprova capacidade de pagamento/);
  assert.match(guide, /antes dos aportes no fim do mês/);
  assert.match(guide, /no início do mês/);
  assert.match(guide, /corrige o saldo antes dos juros/);
  assert.match(guide, /saldo corrigido dividido pelos meses restantes/);
  assert.match(guide, /não previsões/);
  assert.match(guide, /ganho de capital/);
  assert.match(guide, /CET/);
  assert.match(normalize(app.d.querySelector('.rb-hero').textContent), /reais nominais.*sem descontar inflação/);
  assert.match(app.get('rendimento-hint').textContent, /líquida de impostos e tarifas/);
});

uiTest('legacy yield recommendations, fabricated current rates and city rankings are absent', app => {
  const allText = normalize(app.d.documentElement.textContent);
  assert.doesNotMatch(allText, /Selic em 13,75|Selic efetiva: 13,66|IPCA em 12 meses: 4,22|IGP-M em 12 meses: apenas 0,95/);
  assert.doesNotMatch(allText, /acima de ~?8%|abaixo de ~?6%|comprar ganha em horizontes|alugar tende a vencer|conservadora litoral paulista 6[–-]8%/i);
  assert.doesNotMatch(allText, /Estimativas Praia Digital com base em anúncios ativos|menor taxa nominal em agosto|cenário em setembro de 2026/);
  assert.doesNotMatch(source.ui, /razao\s*[<>]|yield\s*[<>]|badge\s*b-buy|badge\s*b-rent/);
  const sources = normalize(app.get('sources-title').parentElement.textContent);
  assert.match(sources, /hipóteses ilustrativas/);
  assert.match(sources, /Não há atualização automática/);
  assert.match(sources, /não substituem uma proposta individual/);
  assert.match(sources, /não uma regra automática de decisão/);
  assert.match(app.get('rVerdict').parentElement.textContent, /Não é recomendação/);
});
