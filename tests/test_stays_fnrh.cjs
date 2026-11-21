// Offline: exercise the current inline copy handler without touching the system clipboard.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = readFileSync(path.resolve(__dirname, '../anfitrioes/central-stays.html'), 'utf8');
const arrival = 'Olá, [nome]! Para sua chegada em [data], o check-in começa às [horário]. Endereço: [endereço]. Acesso: [instruções seguras enviadas em canal apropriado]. Wi-Fi: [orientação]. Em caso de necessidade, entre em contato por [canal]. Boa estadia!';
const current = html.match(/<p id="msg-checkin">([^<]*)<\/p>/)[1];
const script = html.match(/<script>\s*(\(function\(\)\{[\s\S]*?\}\)\(\);)\s*<\/script>/)[1];
const faq = 'https://www.gov.br/turismo/pt-br/acesso-a-informacao/acoes-e-programas/programas-projetos-acoes-obras-e-atividades/ficha-nacional-de-registro-de-hospedes/faq';

test('only the adjacent operator note links to the official FAQ', () => {
  const card = html.match(/<h3>2\. Instruções de chegada<\/h3>([\s\S]*?)<\/article>/)[1];
  assert.equal(current, arrival);
  assert.match(card, /data-copy="msg-checkin"[^>]*>Copiar mensagem<\/button><\/div>\s*<p class="hint">/);
  assert.ok(card.includes('Para hotéis e pousadas que usam a FNRH Digital:'));
  assert.ok(card.includes('portal gratuito'));
  assert.ok(card.includes('href="' + faq + '"'));
  assert.ok(!card.includes('<input') && !card.includes('<form'));
});

function loadCopy(reject) {
  const writes = [];
  let selected;
  let runCopy;
  const target = { innerText: current };
  const status = {};
  const button = {
    dataset: { copy: 'msg-checkin' },
    addEventListener(_event, fn) { runCopy = fn; },
  };
  const defaultField = { value: '', addEventListener() {} };
  const document = {
    querySelectorAll: selector => selector === '.copy-btn' ? [button] : [],
    getElementById: id => ({ 'msg-checkin': target, 'copy-status': status })[id] ?? defaultField,
    createRange: () => ({ selectNodeContents: node => { selected = node; } }),
  };
  const navigator = { clipboard: { writeText: async value => {
    if (reject) throw new Error('clipboard unavailable');
    writes.push(value);
  } } };
  const window = { getSelection: () => ({ removeAllRanges() {}, addRange() {} }) };
  vm.runInNewContext(script, { document, navigator, window });
  return { writes, target, status, get selected() { return selected; }, run: runCopy };
}

test('clipboard receives only the unchanged arrival message', async () => {
  const context = loadCopy(false);
  await context.run();
  assert.deepEqual(context.writes, [arrival]);
  assert.match(context.status.textContent, /Mensagem copiada/);
});

test('manual fallback selects only the arrival message when clipboard is denied', async () => {
  const context = loadCopy(true);
  await context.run();
  assert.deepEqual(context.writes, []);
  assert.equal(context.selected, context.target);
  assert.equal(context.selected.innerText, arrival);
  assert.match(context.status.textContent, /copie o texto destacado manualmente/);
});
