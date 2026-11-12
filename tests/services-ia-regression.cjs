'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

// Run the pages' real inline handlers offline. A mailto value is inspected,
// never followed; any attempt to post customer data fails this test.
function load(file) {
  const html = fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
  const nodes = new Map();
  for (const [, id] of html.matchAll(/\bid=["']([^"']+)["']/g)) {
    const classes = new Set();
    const listeners = {};
    let markup = '', text = '';
    nodes.set(id, {
      value: '', style: {}, listeners,
      get innerHTML() { return markup; },
      set innerHTML(value) { markup = value; text = ''; },
      get textContent() { return text; },
      set textContent(value) { text = value; markup = ''; },
      classList: { add(value) { classes.add(value); }, contains(value) { return classes.has(value); } },
      addEventListener(event, handler) { listeners[event] = handler; },
    });
  }
  let networkCalls = 0;
  const context = vm.createContext({
    document: { getElementById(id) { return nodes.get(id) || null; } },
    fetch() { networkCalls++; throw new Error('Draft preparation must not POST data'); },
  });
  context.window = context;
  context.location = { href: '' };
  for (const [, attrs, code] of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/\bsrc\s*=|application\/ld\+json/i.test(attrs)) continue;
    new vm.Script(code, { filename: file }).runInContext(context);
  }
  return { context, nodes, networkCalls: () => networkCalls,
    set(values) { for (const [id, value] of Object.entries(values)) nodes.get(id).value = String(value); },
  };
}

let passed = 0;
function check(name, fn) { fn(); passed++; console.log(`PASS ${name}`); }

for (const [file, suffix] of [
  ['servicos-ia-imobiliarias.html', 'Plan'],
  ['servicos-ia-investidores.html', 'PlanInvest'],
]) {
  const page = load(file);
  const submit = page.nodes.get(`b2bLeadForm${suffix}`).listeners.submit;
  const valid = { Nome: 'Teste & Cia', Fone: '11999990000', Cidade: 'São Vicente', Perfil: 'imobiliaria', Plano: 'Starter' };
  const fill = values => page.set(Object.fromEntries(Object.entries(values).map(([key, value]) => [`b2b${key}${suffix}`, value])));
  for (const field of Object.keys(valid)) {
    check(`${file}: missing ${field} cannot prepare or send`, () => {
      fill({ ...valid, [field]: field === 'Nome' || field === 'Fone' || field === 'Cidade' ? '   ' : '' });
      let prevented = false;
      submit({ preventDefault() { prevented = true; } });
      assert.equal(prevented, true);
      assert.equal(page.context.location.href, '');
      assert.match(page.nodes.get(`b2bFeedback${suffix}`).textContent, /Preencha/);
      assert.equal(page.networkCalls(), 0);
    });
  }
  check(`${file}: valid fields create the exact manual email draft`, () => {
    fill(valid);
    submit({ preventDefault() {} });
    const url = new URL(page.context.location.href);
    assert.equal(url.protocol, 'mailto:');
    assert.equal(url.pathname, 'comercial@praia.digital');
    assert.equal(url.searchParams.get('subject'), 'Solicita proposta B2B');
    assert.equal(url.searchParams.get('body'), 'Nome: Teste & Cia\nTelefone: 11999990000\nCidade: São Vicente\nPerfil: imobiliaria\nPlano: Starter\n');
    const feedback = page.nodes.get(`b2bFeedback${suffix}`);
    assert.match(feedback.textContent, /Rascunho preparado/);
    assert.match(feedback.textContent, /nenhum pedido foi registrado automaticamente/);
    assert.equal(feedback.style.display, 'block');
    assert.equal(page.networkCalls(), 0);
  });
}

const investor = load('servicos-ia-investidores.html');
check('investor: positive price preserves the existing illustrative calculation', () => {
  investor.set({ siCity: 'Santos', siPrice: '1200000' });
  investor.context.calcInvest();
  const result = investor.nodes.get('simKpi').innerHTML;
  assert.match(result, /R\$ 1\.200\.000/);
  assert.match(result, /5\.0% a\.a\./);
  assert.match(result, /Yield do cenário/);
  assert.match(result, />5\.000<\/div>/);
  assert.equal(investor.nodes.get('simResult').classList.contains('visible'), true);
  assert.doesNotMatch(result, /undefined|NaN|Infinity/);
});
check('investor: clearly identifies preset values as illustrative', () => {
  const html = fs.readFileSync(path.join(__dirname, '..', 'servicos-ia-investidores.html'), 'utf8');
  assert.match(html, /Os preços e as taxas predefinidos são ilustrativos/);
  assert.match(html, /substituídos ou validados com dados reais/);
  assert.match(html, /não é uma estimativa de mercado e não inclui custos/);
  assert.doesNotMatch(html, /Yield médio/);
});
check('investor: blank price keeps each existing city scenario', () => {
  const scenarios = {
    'São Vicente': ['720.000', '6.1'], Santos: ['1.250.000', '5.0'],
    'Guarujá': ['950.000', '4.6'], 'Praia Grande': ['780.000', '5.8'],
    'Itanhaém': ['880.000', '6.4'], 'Mongaguá': ['750.000', '6.9'],
    'Peruíbe': ['920.000', '7.2'], Bertioga: ['860.000', '5.1'],
  };
  for (const [city, [price, yieldValue]] of Object.entries(scenarios)) {
    investor.set({ siCity: city, siPrice: '' });
    investor.context.calcInvest();
    const result = investor.nodes.get('simKpi').innerHTML;
    assert(result.includes(`R$ ${price}`));
    assert(result.includes(`${yieldValue}% a.a.`));
  }
});
for (const badPrice of ['0', '-1', 'abc', 'Infinity', '1e309', '1e308']) {
  check(`investor: rejects invalid price ${badPrice} and removes stale KPIs`, () => {
    investor.set({ siPrice: badPrice });
    investor.context.calcInvest();
    assert.match(investor.nodes.get('simKpi').textContent, /valor estimado válido, maior que zero/);
    assert.equal(investor.nodes.get('simKpi').innerHTML, '');
  });
}
check('investor: recovers after invalid input with a fractional positive price', () => {
  investor.set({ siCity: 'Santos', siPrice: '1200000.50' });
  investor.context.calcInvest();
  assert.match(investor.nodes.get('simKpi').innerHTML, /R\$ 1\.200\.001/);
  assert.equal(investor.nodes.get('simKpi').textContent, '');
  assert.equal(investor.networkCalls(), 0);
});
// Exercise the inline onsubmit itself, with the HTML entity decoding a browser
// performs. No analytics scripts or network APIs are invoked by this fixture.
const seasonHTML = fs.readFileSync(path.join(__dirname, '..', 'ferramentas-gratuitas/imobiliarias/analise-retorno-temporada-litoral.html'), 'utf8');
const seasonCode = seasonHTML.match(/\bonsubmit="([^"]+)"/)[1]
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const seasonScript = new vm.Script(`(function(event) { ${seasonCode} })`);
const seasonFields = { diaria: { value: '' }, dias: { value: '' }, taxa: { value: '' } };
const seasonResult = { style: {}, textContent: '' };
const seasonContext = vm.createContext({
  document: {
    getElementById(id) { return seasonFields[id]; },
    querySelector(selector) { assert.equal(selector, '.result'); return seasonResult; },
  },
});
const seasonHandler = seasonScript.runInContext(seasonContext);
function calculateSeason(values) {
  for (const [id, value] of Object.entries(values)) seasonFields[id].value = String(value);
  let prevented = false;
  seasonHandler({ preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(seasonResult.style.display, 'block');
  return seasonResult.textContent;
}
const seasonValid = { diaria: 800, dias: 45, taxa: 70 };
check('season: 70% occupation means gross revenue of R$ 25,200, without costs', () => {
  const result = calculateSeason(seasonValid);
  assert.match(result, /Faturamento bruto estimado: R\$ 25\.200,00/);
  assert.match(result, /Custos não incluídos; este valor não é lucro nem ROI/);
  assert.match(seasonHTML, /não desconta custos/);
});
check('season: fractional daily price and occupation are preserved', () => {
  assert.match(calculateSeason({ diaria: 100.5, dias: 3, taxa: 25.5 }), /R\$ 76,88/);
});
for (const [field, values] of Object.entries({
  diaria: ['', ' ', 0, -1, 'abc', 'Infinity', '1e308'],
  dias: ['', -1, 366, 0.5, 'NaN', 'Infinity'],
  taxa: ['', -1, 100.1, 'NaN', 'Infinity'],
})) {
  for (const value of values) {
    check(`season: rejects invalid ${field}=${JSON.stringify(value)}`, () => {
      assert.match(calculateSeason({ ...seasonValid, [field]: value }), /Informe diária positiva/);
      assert.doesNotMatch(seasonResult.textContent, /Faturamento bruto estimado/);
    });
  }
}
check('season: zero available days or occupation correctly gives zero revenue', () => {
  assert.match(calculateSeason({ ...seasonValid, dias: 0 }), /R\$ 0,00/);
  assert.match(calculateSeason({ ...seasonValid, taxa: 0 }), /R\$ 0,00/);
});
check('season: maximum days and full occupation are accepted', () => {
  assert.match(calculateSeason({ diaria: 100, dias: 365, taxa: 100 }), /R\$ 36\.500,00/);
});
check('season: computed value beyond safe precision is rejected', () => {
  assert.match(calculateSeason({ diaria: Number.MAX_SAFE_INTEGER, dias: 365, taxa: 100 }), /limite de precisão/);
});
console.log(`${passed} service IA and season checks passed without external sending.`);
