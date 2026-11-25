const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const assert = require('node:assert/strict');

const root = process.env.LISTING_TEST_ROOT || path.resolve(__dirname, '..');
function listing(file, scriptMarker) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const listeners = new Map();
  const nodes = new Map();
  const node = id => {
    if (nodes.has(id)) return nodes.get(id);
    const tag = new RegExp('<[^>]+\\bid="' + id + '"[^>]*>').exec(html)?.[0];
    assert.ok(tag, 'missing element: ' + id);
    let display = '';
    const obj = {
      value: /\bvalue="([^"]*)"/.exec(tag)?.[1] || '',
      addEventListener(event, fn) { listeners.set(id + ':' + event, fn); },
      get textContent() { return display.replace(/<[^>]*>/g, ''); },
      set textContent(value) { display = String(value); },
      set innerHTML(value) { display = String(value); },
    };
    nodes.set(id, obj);
    return obj;
  };
  const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)];
  const script = scripts.find(item => item[1].includes(scriptMarker));
  assert.ok(script, 'missing inline calculator');
  const context = vm.createContext({ document: { getElementById: node } });
  vm.runInContext(script[1], context);
  function dispatch(id, event) { listeners.get(id + ':' + event)?.({ target: node(id) }); }
  return { html, node, context, dispatch };
}

test('condominium calculator: only an explicit zero is a zero cost', () => {
  const l = listing('casa-condominio-fechado-bertioga.html', 'function calcROI()');
  const raw = ids => ids.map(id => l.node(id).value);
  const result = () => l.node('roiResult').textContent;
  assert.deepEqual(raw(['propValue', 'adr', 'occupancy', 'nights', 'costs']), ['595000', '750', '55', '200', '38000']);
  l.context.calcROI();
  assert.match(result(), /44\.500.*7\.5%/);
  l.node('costs').value = '';
  l.dispatch('roiCalc', 'input');
  assert.match(result(), /Preencha todos/);
  assert.doesNotMatch(result(), /44\.500|7\.5%|13\.9%/);
  l.context.calcROI();
  assert.match(result(), /Preencha todos/);
  l.node('costs').value = '0';
  l.dispatch('roiCalc', 'input');
  l.context.calcROI();
  assert.match(result(), /Resultado após os custos informados: R\$ 82\.500.*13\.9%/);
  l.node('occupancy').value = '';
  l.context.calcROI();
  assert.match(result(), /Preencha todos/);
});

test('São Lourenço calculator clears stale values while editing and accepts explicit zero', () => {
  const l = listing('imoveis/casas-lancamento-sao-lourenco.html', "const ids=['investimento','diaria','ocupacao','custos']");
  const ids = ['noites', 'bruto', 'liquido', 'yield', 'payback'];
  const result = () => ids.map(id => l.node(id).textContent);
  assert.deepEqual(['investimento', 'diaria', 'ocupacao', 'custos'].map(id => l.node(id).value), ['2500000', '1800', '30', '30']);
  assert.match(result()[0], /^109,5 noites$/);
  assert.match(result()[2], /137\.970/);
  assert.match(result()[3], /5,5%/);
  l.node('custos').value = '';
  l.dispatch('custos', 'input');
  assert.match(result()[0], /Preencha todos/);
  assert.deepEqual(result().slice(1), ['—', '—', '—', '—']);
  l.dispatch('calcular', 'click');
  assert.deepEqual(result().slice(1), ['—', '—', '—', '—']);
  l.node('custos').value = '0';
  l.dispatch('custos', 'input');
  assert.match(result()[2], /197\.100/);
  assert.match(result()[3], /7,9%/);
  l.node('ocupacao').value = '';
  l.dispatch('ocupacao', 'input');
  assert.deepEqual(result().slice(1), ['—', '—', '—', '—']);
});
