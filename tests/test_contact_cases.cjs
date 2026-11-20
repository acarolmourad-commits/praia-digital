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
function networkProbe() {
  const requests = [];
  const handoffs = [];
  return {
    requests, handoffs,
    globals: {
      fetch(...args) { requests.push(['fetch', ...args]); throw Error('network disabled'); },
      XMLHttpRequest: class { constructor() { requests.push(['xhr']); throw Error('network disabled'); } },
      Image: class { set src(value) { requests.push(['image', value]); } },
      navigator: { sendBeacon(...args) { requests.push(['beacon', ...args]); return false; } }
    },
    location: { set href(value) { handoffs.push(value); } }
  };
}
function setup(search) {
  const elements = {};
  for (const id of ['nome', 'tel', 'cidade', 'produto', 'pagto', 'mensagem', 'contexto-produto', 'pagamento-opcional']) elements[id] = { value: '', hidden: false, disabled: false, textContent: '', listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; } };
  elements.produto.options = options;
  Object.defineProperty(elements.produto, 'selectedOptions', { get() { return options.filter(o => o.value === this.value); } });
  elements.f = { reportValidity: () => true };
  elements.nome.focus = () => {};
  const probe = networkProbe();
  const window = { location: probe.location, listeners: {}, addEventListener(event, fn) { this.listeners[event] = fn; } };
  const location = { search };
  const sandbox = { ...probe.globals, document: { getElementById: id => elements[id] }, window, location, URLSearchParams };
  vm.runInNewContext(script, sandbox);
  return { elements, window, location, probe, submit: sandbox.enviar };
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
// Exact production handlers with synthetic values and every transport mocked.
const interest = setup('?produto=pricelabs');
let prevented = false;
const event = { preventDefault() { prevented = true; } };
interest.elements.f.reportValidity = () => false;
interest.submit(event);
assert(prevented);
assert.deepEqual(interest.probe.handoffs, []);
interest.elements.f.reportValidity = () => true;
interest.submit(event); // blank trimmed name still blocks
assert.deepEqual(interest.probe.handoffs, []);
Object.assign(interest.elements.nome, { value: 'Pessoa Sintética' });
Object.assign(interest.elements.tel, { value: '11900000000' });
Object.assign(interest.elements.cidade, { value: 'Bertioga' });
Object.assign(interest.elements.mensagem, { value: 'Somente teste & revisão' });
Object.assign(interest.elements.pagto, { value: 'Pix' });
interest.submit(event);
assert.equal(interest.probe.handoffs.length, 1);
const wa = new URL(interest.probe.handoffs[0]);
assert.equal(wa.origin + wa.pathname, 'https://wa.me/5511954346288');
assert.match(wa.searchParams.get('text'), /Pessoa Sintética.*Cidade: Bertioga.*PriceLabs.*Pix.*teste & revisão.*11900000000/s);
assert.deepEqual(interest.probe.requests, []);

const catalog = fs.readFileSync(path.join(root, 'imoveis.html'), 'utf8');
for (const [page, id, notice] of [[html, 'f', 'aviso-whatsapp'], [catalog, 'contato-form', 'aviso-contato-email']]) {
  const [, markup] = page.split(`<form id="${id}"`);
  const form = markup.split("</form>", 1)[0];
  assert(!/\bname\s*=/.test(form), 'native form fallback must not serialize visitor input');
  assert(form.includes(`aria-describedby="${notice}"`));
  assert(page.includes(`id="${notice}"`));
  assert(page.includes('href="mailto:comercial@praia.digital">comercial@praia.digital</a>'));
}
const contact = networkProbe();
const fields = Object.fromEntries(['nome', 'email', 'telefone', 'interesse', 'mensagem'].map(id => [id, { value: '' }]));
fields['contato-form'] = { addEventListener(name, callback) { assert.equal(name, 'submit'); this.submit = callback; } };
const alerts = [];
const main = fs.readFileSync(path.join(root, 'js/main.js'), 'utf8');
vm.runInNewContext(main, {
  ...contact.globals, window: { location: contact.location },
  document: { getElementById: id => fields[id], addEventListener(name, callback) { assert.equal(name, 'DOMContentLoaded'); callback(); } },
  alert: message => alerts.push(message)
});
fields['contato-form'].submit(event);
assert.equal(alerts.length, 1);
assert.deepEqual(contact.handoffs, []);
for (const [key, value] of Object.entries({nome: 'Pessoa Sintética', email: 'visitante@example.invalid', telefone: '11900000000', interesse: 'comprar', mensagem: 'Uma revisão & nada enviado'})) fields[key].value = value;
fields['contato-form'].submit(event);
assert.equal(contact.handoffs.length, 1);
const email = new URL(contact.handoffs[0]);
assert.equal(email.protocol, 'mailto:');
assert.equal(email.pathname, 'comercial@praia.digital');
assert.equal(email.searchParams.get('subject'), 'Contato Litoral Prime Imóveis');
assert.match(email.searchParams.get('body'), /Pessoa Sintética.*visitante@example\.invalid.*11900000000.*comprar.*Uma revisão & nada enviado/s);
assert.deepEqual(contact.requests, []);
console.log('Synthetic contact submissions: invalid cases do not hand off; each valid case only opens the intended draft, with no background requests.');

const cases = fs.readFileSync(path.join(root, 'cases.html'), 'utf8');
assert(cases.includes('<title>Exemplos ilustrativos de aplicação'));
assert(cases.includes('<h1>Exemplos ilustrativos de aplicação'));
assert(!/métricas verificáveis|Ver como|Quero um resultado assim|Piloto sem custo inicial|Cases e resultados/.test(cases));
assert.equal((cases.match(/<div class="metric">Métrica a observar:/g) || []).length, 5);
assert(cases.includes('<main class="container" id="main">'));
assert(!cases.includes('SearchAction'));
console.log('Contact/cases: contextual choices, optional payment, reset/history, labels and illustrative copy passed. No submissions.');
