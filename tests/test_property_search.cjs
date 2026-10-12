'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const api = require('../js/property-search.js');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const fixtures = [
  { title: 'Apartamento teste', city: 'Bertioga', type: 'Venda', price: 'R$ 700.000', bedrooms: '2', tags: ['Investimento'] },
  { title: 'Casa teste', city: 'Guarujá', type: 'Aluguel', price: 'R$ 4.500/mês', bedrooms: '4', description: 'Ideal para temporada', tags: [] }
];
for (const [q, value] of [
  ['apartamento de 2 quartos em Bertioga', undefined], ['casa de 3 quartos', undefined],
  ['apartamento até 1 milhão em Santos', 1000000], ['apartamento de 2 quartos até R$ 700 mil em Bertioga', 700000],
  ['casa até R$ 1.250.000', 1250000], ['até 1,5 milhão', 1500000], ['até 1.5 mi', 1500000],
  ['até 2 milhões', 2000000], ['até 700 mil', 700000], ['R$ 4500', 4500], ['R$ 1.250.000,50', 1250000.5],
  ['2 quartos e 105 m²', undefined], ['R$ 1.2.3', undefined]
]) test('price: ' + q, () => assert.equal(api.parse(q).preco_max, value));
for (const [q, city] of [['SÃO VICENTE', 'sao vicente'], ['Guarujá', 'guaruja'], ['em Praia Grande', 'praia grande'], ['santosdumont', undefined]])
  test('city: ' + q, () => assert.equal(api.parse(q).cidade, city));
test('bedrooms and category are separate from transaction', () => {
  const f = api.parse('comprar apartamento de 2 quartos até R$ 700 mil em Bertioga');
  assert.equal(f.quartos, 2); assert.equal(f.tipo, 'apartamento'); assert.equal(f.finalidade, 'venda');
  assert.equal(api.matches(fixtures[0], f), true); assert.equal(api.matches(fixtures[1], f), false);
});
test('monthly price and literal seasonal metadata', () => assert.equal(api.matches(fixtures[1], api.parse('alugar casa de 4 quartos até R$ 4500 em Guarujá para temporada')), true));
test('literal investment metadata is not an ROI guarantee', () => {
  assert.equal(api.matches(fixtures[0], { perfil: 'investimento' }), true);
  assert.equal(api.matches(fixtures[1], { perfil: 'investimento' }), false);
});
test('missing price and bedrooms do not satisfy numeric filters', () => {
  assert.equal(api.matches({ title: 'Casa', tags: [] }, { preco_max: 700000 }), false);
  assert.equal(api.matches({ title: 'Casa', tags: [] }, { quartos: 2 }), false);
});
test('price ceiling is inclusive and bedrooms are minimum', () => {
  assert.equal(api.matches(fixtures[0], { preco_max: 700000, quartos: 1 }), true);
  assert.equal(api.matches(fixtures[0], { preco_max: 699999 }), false);
  assert.equal(api.matches(fixtures[0], { quartos: 3 }), false);
});
test('URL explicit filters override inferred q', () => {
  const f = api.read('?q=casa%20de%203%20quartos&quartos=2&tipo=apartamento');
  assert.equal(f.quartos, 2); assert.equal(f.tipo, 'apartamento');
});
for (const input of ['preco_max=-1', 'preco_max=Infinity', 'preco_max=12abc', 'quartos=0', 'quartos=2.5', 'tipo=venda', 'perfil=garantido'])
  test('invalid URL fails closed: ' + input, () => { const f = api.read('?' + input); assert.equal(f.invalid.length, 1); assert.equal(api.matches(fixtures[0], f), false); });
test('empty explicit filters remove inference', () => assert.equal(api.read('?q=casa&tipo=').tipo, undefined));
test('transport round trip preserves q and all structured fields', () => {
  const f = api.parse('apartamento de 2 quartos até R$ 700 mil em Bertioga investimento');
  const round = api.read('?' + api.params(f)); for (const k of Object.keys(f)) assert.equal(round[k], f[k]);
});
test('free text search remains supported', () => { assert.equal(api.matches(fixtures[0], { q: 'teste' }), true); assert.equal(api.matches(fixtures[0], { q: 'inexistente' }), false); });
function element() {
  return { value: '', textContent: '', innerHTML: '', style: {}, children: [], options: [], handlers: {},
    setAttribute() {}, appendChild(child) { this.children.push(child); if (child.value !== undefined) this.options.push(child); },
    addEventListener(name, fn) { this.handlers[name] = fn; }, parentNode: { insertBefore() {} } };
}
function inline(file, marker) {
  const blocks = [...read(file).matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  const found = blocks.filter(s => s.includes(marker)); assert.equal(found.length, 1); return found[0];
}
test('home submits explicit encoded URL and prevents default GET', () => {
  const form = element(), q = element(); q.value = 'apartamento de 2 quartos até R$ 700 mil em Bertioga'; let target, prevented = false;
  vm.runInNewContext(inline('index.html', "getElementById('smartsearch')"), {
    PDPropertySearch: api, document: { getElementById: id => id === 'q' ? q : form }, window: { location: { assign: value => target = value } }
  });
  form.handlers.submit({ preventDefault() { prevented = true; } });
  assert.equal(prevented, true); const f = api.read(new URL(target, 'https://example.invalid').search);
  assert.equal(f.preco_max, 700000); assert.equal(f.quartos, 2);
});
test('landing displays untrusted q as text and preserves link filters', () => {
  const box = element(), search = '?q=%3Cimg%20onerror%3Dx%3E&quartos=2&preco_max=700000';
  vm.runInNewContext(inline('encontrar-imovel.html', 'PDPropertySearch.read'), {
    PDPropertySearch: api, window: { location: { search } }, document: { getElementById: () => box, createElement: element }
  });
  assert.equal(box.innerHTML, ''); assert.ok(box.textContent.includes('<img onerror=x>'));
  assert.equal(api.read(new URL(box.children[0].href, 'https://example.invalid').search).quartos, 2);
});
test('invalid landing filters do not create a broadened catalog link', () => {
  const box = element(); vm.runInNewContext(inline('encontrar-imovel.html', 'PDPropertySearch.read'), {
    PDPropertySearch: api, window: { location: { search: '?preco_max=-1' } }, document: { getElementById: () => box, createElement: element }
  }); assert.equal(box.children.length, 0); assert.ok(box.textContent.includes('inválidos'));
});
function catalog(search, preloaded = true) {
  const grid = element(), status = element(), controls = { 'lista-imoveis': grid, 'pd-search-status': status, 'busca': element() };
  const handlers = {}, head = element();
  const context = { window: { location: { search } }, document: { head, getElementById: id => controls[id] || null, createElement: element, addEventListener: (k, fn) => handlers[k] = fn } };
  if (preloaded) context.window.PDPropertySearch = api;
  vm.runInNewContext(read('js/main.js'), context); handlers.DOMContentLoaded(); return { grid, status, controls, head, context };
}
test('catalog applies incoming structured URL on first render', () => {
  const c = catalog('?cidade=bertioga&tipo=casa&quartos=2&preco_max=700000');
  assert.ok(c.grid.innerHTML.includes('Casa em condomínio fechado - Bertioga')); assert.ok(!c.grid.innerHTML.includes('Apartamento vista mar - Santos'));
});
test('catalog explicit URL does not get overridden by original q', () => {
  const c = catalog('?q=casa%20em%20Bertioga&cidade=santos&tipo=apartamento');
  assert.ok(c.grid.innerHTML.includes('Apartamento vista mar - Santos')); assert.ok(!c.grid.innerHTML.includes('Casa em condomínio fechado - Bertioga'));
});
test('catalog empty and invalid states are visible', () => {
  assert.ok(catalog('?preco_max=1').status.textContent.includes('Nenhum imóvel'));
  assert.ok(catalog('?quartos=-2').status.textContent.includes('inválidos'));
});
test('legacy pages load shared module before rendering; failure is visible', () => {
  const c = catalog('?cidade=santos', false); assert.equal(c.head.children.length, 1); const script = c.head.children[0];
  assert.equal(script.src, '/js/property-search.js'); c.context.window.PDPropertySearch = api; script.onload(); assert.ok(c.grid.innerHTML.includes('Santos'));
  const failed = catalog('?cidade=santos', false); failed.head.children[0].onerror(); assert.equal(failed.grid.innerHTML, ''); assert.ok(failed.status.textContent.includes('indisponível'));
});
test('UI text, module references and read-only workflow boundaries', () => {
  for (const f of ['index.html', 'encontrar-imovel.html']) assert.ok(read(f).includes('<script src="/js/property-search.js"></script>'));
  assert.ok(read('index.html').includes('Exemplos ilustrativos de aplicação; não representam resultados comprovados de clientes.'));
  const workflow = read('.github/workflows/property-search-tests.yml');
  assert.ok(workflow.includes('contents: read')); assert.ok(workflow.includes('persist-credentials: false'));
  assert.ok(!/workflow_dispatch|\bpush:|secrets\.|pages:|id-token:|upload-artifact|deploy-pages/.test(workflow));
});
