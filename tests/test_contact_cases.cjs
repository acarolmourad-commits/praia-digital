// Offline regression checks: no external forms, WhatsApp or payments are submitted.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'interesse.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].at(-1)[1];
const productHtml = html.match(/<select id="produto"[^>]*>([\s\S]*?)<\/select>/)[1];
const options = [...productHtml.matchAll(/<option value="([^"]*)">([^<]*)<\/option>/g)].map(m => ({ value: m[1], textContent: m[2] }));
function setup(search) {
  const elements = {};
  for (const id of ['nome', 'tel', 'cidade', 'produto', 'pagto', 'mensagem', 'contexto-produto', 'pagamento-opcional']) elements[id] = { value: '', hidden: false, disabled: false, textContent: '', listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; } };
  elements.produto.options = options;
  const window = { listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; } };
  const location = { search };
  vm.runInNewContext(script, { document: { getElementById: id => elements[id] }, window, location, URLSearchParams });
  return { elements, window, location };
}
for (const value of ['', 'avaliacao', 'comprar', 'investir', 'outro']) {
  const { elements } = setup('?produto=' + value);
  assert.equal(elements.produto.value, value);
  assert.equal(elements['pagamento-opcional'].hidden, true);
  assert.equal(elements.pagto.disabled, true);
}
for (const value of ['airbnb-booking', 'pricelabs', 'anunciar', 'temporada', 'planos', 'automacao']) {
  const { elements } = setup('?produto=' + value);
  assert.equal(elements.produto.value, value);
  assert.equal(elements['pagamento-opcional'].hidden, false);
  assert.equal(elements.pagto.disabled, false);
  elements.pagto.value = 'Pix';
  elements.produto.value = 'avaliacao';
  elements.produto.listeners.change();
  assert.equal(elements.pagto.value, '');
  assert.equal(elements['pagamento-opcional'].hidden, true);
}
const invalid = setup('?produto=%3Cscript%3E');
assert.equal(invalid.elements.produto.value, '');
assert(!invalid.elements['contexto-produto'].textContent.includes('<script>'));
const history = setup('?produto=pricelabs');
history.location.search = '?produto=airbnb-booking';
history.window.listeners.popstate();
assert.equal(history.elements.produto.value, 'airbnb-booking');
history.location.search = '';
history.window.listeners.popstate();
assert.equal(history.elements.produto.value, '');
assert.equal(history.elements['pagamento-opcional'].hidden, true);
assert(!/<select id="pagto"[^>]*\brequired\b/.test(html));
for (const id of ['nome', 'tel', 'cidade', 'produto', 'pagto', 'mensagem']) assert(html.includes(`for="${id}"`));
assert(!html.includes('href="//"'));
assert(html.includes('Esta consulta não gera cobrança nem contratação'));
const cases = fs.readFileSync(path.join(root, 'cases.html'), 'utf8');
assert(cases.includes('<title>Exemplos ilustrativos de aplicação'));
assert(cases.includes('<h1>Exemplos ilustrativos de aplicação'));
assert(!/métricas verificáveis|Ver como|Quero um resultado assim|Piloto sem custo inicial|Cases e resultados/.test(cases));
assert.equal((cases.match(/<div class="metric">Hipótese:/g) || []).length, 4);
assert(cases.includes('<main class="container" id="main">'));
assert(!cases.includes('SearchAction'));
console.log('Contact/cases: contextual choices, optional payment, reset/history, labels and illustrative copy passed. No submissions.');
