// Offline tests of the production legacy handler. No OS app or network is used.
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');
const dir = path.resolve(__dirname, '../litoral-prime-imoveis');
const script = readFileSync(path.join(dir, 'js/main.js'), 'utf8');

for (const file of ['index.html', 'imoveis.html']) {
  test(`${file}: informs and provides a manual contact without leaking form values`, () => {
    const html = readFileSync(path.join(dir, file), 'utf8');
    const form = html.match(/<form id="contato-form"[\s\S]*?<\/form>/)[0];
    assert(!/\bname\s*=/.test(form), 'native fallback has no named controls');
    assert(form.includes('Abrir rascunho de e-mail'));
    assert(form.includes('aria-describedby="aviso-contato-email"'));
    assert(html.includes('id="aviso-contato-email"'));
    assert(html.includes('href="mailto:comercial@praia.digital">comercial@praia.digital</a>'));
    assert(html.includes('src="js/main.js?v=20261120-contato"'));
  });
}

test('shared form handler: invalid input does not navigate; valid input opens only the email draft', () => {
  const routes = [], attempts = [], alerts = [];
  const fields = Object.fromEntries(['nome', 'email', 'telefone', 'interesse', 'mensagem'].map(id => [id, { value: '' }]));
  let submit;
  fields['contato-form'] = { addEventListener(event, callback) { assert.equal(event, 'submit'); submit = callback; } };
  vm.runInNewContext(script, {
    window: { location: { set href(value) { routes.push(value); } } },
    document: {
      getElementById: id => fields[id],
      addEventListener(event, initialise) { assert.equal(event, 'DOMContentLoaded'); initialise(); }
    },
    fetch(...args) { attempts.push(['fetch', ...args]); throw Error('network disabled'); },
    Image: class { set src(value) { attempts.push(['image', value]); } },
    XMLHttpRequest: class { constructor() { attempts.push(['xhr']); throw Error('network disabled'); } },
    navigator: { sendBeacon(...args) { attempts.push(['beacon', ...args]); return false; } },
    alert: value => alerts.push(value)
  });
  let prevented = 0;
  const event = { preventDefault() { prevented++; } };
  submit(event);
  assert.equal(alerts.length, 1);
  assert.deepEqual(routes, []);
  assert.deepEqual(attempts, []);
  for (const [key, value] of Object.entries({
    nome: 'Pessoa Sintética', email: 'visitante@example.invalid', telefone: '11900000000',
    interesse: 'comprar', mensagem: 'teste & revisão'
  })) fields[key].value = value;
  submit(event);
  assert.equal(prevented, 2);
  assert.equal(routes.length, 1);
  assert.deepEqual(attempts, []);
  const email = new URL(routes[0]);
  assert.equal(email.protocol, 'mailto:');
  assert.equal(email.pathname, 'comercial@praia.digital');
  assert.equal(email.searchParams.get('subject'), 'Contato Litoral Prime Imóveis');
  assert.match(email.searchParams.get('body'), /Pessoa Sintética.*visitante@example\.invalid.*11900000000.*comprar.*teste & revisão/s);
});
