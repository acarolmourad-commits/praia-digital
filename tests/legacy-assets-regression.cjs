const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const files = {
  planning: 'assets/predicao-vendidos-litoral.html',
  priority: 'assets/priorizacao-leads-ia.html',
  visit: 'assets/servico-assistente-virtual-compradores-litoral.html',
};
let checks = 0;
function test(name, fn) { fn(); checks++; }
function inlineScripts(html) {
  return [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
    .filter(match => !/\bsrc\s*=|ld\+json/i.test(match[1]))
    .map(match => match[2]);
}
function setup(file, functionName) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const elements = new Map();
  for (const match of html.matchAll(/\bid="([^"]+)"/g)) {
    elements.set(match[1], { value: '', innerHTML: '', textContent: '', style: {} });
  }
  const context = {
    document: { getElementById: id => elements.get(id) },
    fetch() { throw new Error('Unexpected network request'); },
    localStorage: { setItem() { throw new Error('Unexpected persisted contact'); } },
  };
  context.window = context;
  vm.createContext(context);
  for (const script of inlineScripts(html)) vm.runInContext(script, context);
  return {
    html,
    el: id => elements.get(id),
    run(values) {
      for (const [id, value] of Object.entries(values)) {
        assert(elements.has(id), `Missing field ${id}`);
        elements.get(id).value = value;
      }
      elements.get('resultado').innerHTML = '';
      elements.get('resultado').textContent = '';
      context[functionName]();
      assert.equal(elements.get('resultado').style.display, 'block');
      return elements.get('resultado');
    },
  };
}

test('all three pages have valid inline JavaScript', () => {
  for (const file of Object.values(files)) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    for (const script of inlineScripts(html)) new vm.Script(script, { filename: file });
  }
});

const planning = setup(files.planning, 'predizer');
test('planning keeps entered details and does not manufacture a prediction', () => {
  const result = planning.run({ cidade: 'Praia Grande', mes: 'Janeiro', ticket: '450000' });
  assert.match(result.innerHTML, /Praia Grande/);
  assert.match(result.innerHTML, /Janeiro/);
  assert.match(result.innerHTML, /450\.000,00/);
  assert.match(result.innerHTML, /Não é uma previsão/);
  assert.doesNotMatch(result.innerHTML, /\d+(?:[.,]\d+)?%|\d+ dias|Lead time/);
});
test('planning supports every listed city and month without fictional defaults', () => {
  for (const cidade of ['Santos', 'Guarujá', 'Praia Grande', 'São Vicente', 'Bertioga', 'Itanhaém', 'Peruíbe', 'Mongaguá']) {
    assert.match(planning.run({ cidade, mes: 'Dezembro', ticket: '100' }).innerHTML, /Cenário informado/);
  }
});
test('planning rejects empty, zero, negative, malformed and non-finite values', () => {
  for (const ticket of ['', '0', '-1', '450000garbage', 'Infinity', '1e309']) {
    assert.match(planning.run({ cidade: 'Santos', mes: 'Janeiro', ticket }).textContent, /maior que zero/);
  }
});
test('planning rejects invalid selections without rendering supplied markup', () => {
  for (const fields of [{ cidade: '<img src=x>', mes: 'Janeiro' }, { cidade: 'Santos', mes: 'Outro' }]) {
    const result = planning.run({ ...fields, ticket: '100' });
    assert.match(result.textContent, /Selecione/);
    assert.equal(result.innerHTML, '');
  }
});

const priority = setup(files.priority, 'priorizar');
test('priority applies disclosed rules and produces a bounded illustrative score', () => {
  const result = priority.run({ origem: 'Indicação', tempo: '15', interacoes: '3' });
  assert.match(result.innerHTML, /81\/100/);
  assert.match(result.innerHTML, /Alta/);
  assert.match(result.innerHTML, /sem validação estatística/);
  assert.match(result.innerHTML, /Nenhum contato é salvo ou enviado/);
  assert.match(priority.run({ origem: 'Website', tempo: '60', interacoes: '1000' }).innerHTML, /100\/100/);
});
test('zero response time and zero interactions are valid', () => {
  assert.match(priority.run({ origem: 'Website', tempo: '0', interacoes: '0' }).innerHTML, /30\/100/);
});
test('priority rejects empty, negative, fractional interactions and invalid numbers', () => {
  for (const fields of [
    { tempo: '', interacoes: '3' }, { tempo: '-1', interacoes: '3' },
    { tempo: 'Infinity', interacoes: '3' }, { tempo: '15oops', interacoes: '3' },
    { tempo: '15', interacoes: '' }, { tempo: '15', interacoes: '-1' },
    { tempo: '15', interacoes: '1.5' }, { tempo: '15', interacoes: '1e309' },
  ]) {
    assert.match(priority.run({ origem: 'Website', ...fields }).textContent, /número inteiro/);
  }
});
test('priority validates origins and has no duplicate submission integration', () => {
  assert.match(priority.run({ origem: '<script>', tempo: '15', interacoes: '3' }).textContent, /Selecione a origem/);
  assert.doesNotMatch(priority.html, /integrated-form|\/api\/v1\/lead\/capture|fetch\(/);
});

const visit = setup(files.visit, 'sugerir');
test('visit guide reflects valid selected criteria without invented neighborhood matches', () => {
  const result = visit.run({ cidade: 'São Vicente', objetivo: 'Comprar', perfil: 'Família' });
  assert.match(result.innerHTML, /São Vicente/);
  assert.match(result.innerHTML, /documentação/);
  assert.match(result.innerHTML, /rotina da família/);
  assert.match(result.innerHTML, /Não consulta imóveis disponíveis/);
});
test('seasonal rental and remote work get the applicable general checklist', () => {
  const result = visit.run({ cidade: 'Praia Grande', objetivo: 'Alugar temporada', perfil: 'Trabalho remoto' });
  assert.match(result.innerHTML, /condições de cancelamento/);
  assert.match(result.innerHTML, /internet/);
});
test('investment guide asks for evidence rather than predicting returns', () => {
  const result = visit.run({ cidade: 'Bertioga', objetivo: 'Investir', perfil: 'Casal' });
  assert.match(result.innerHTML, /registros que sustentem/);
  assert.doesNotMatch(result.innerHTML, /\d+%/);
});
test('visit guide rejects missing or unexpected selections without injecting HTML', () => {
  for (const fields of [{ cidade: '' }, { objetivo: '' }, { perfil: '' }, { cidade: '<img src=x>' }, { perfil: 'Outro' }]) {
    const result = visit.run({ cidade: 'Santos', objetivo: 'Comprar', perfil: 'Casal', ...fields });
    assert.match(result.textContent, /Selecione cidade/);
    assert.equal(result.innerHTML, '');
  }
});

console.log(JSON.stringify({ checks, passed: checks }));
