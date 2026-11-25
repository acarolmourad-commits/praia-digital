const assert = require('node:assert/strict');
const {test} = require('node:test');
const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const vm = require('node:vm');

test('a migrated form prepares exactly one email with the reviewed fields', () => {
  const source = readFileSync(join(__dirname, '../js/contact-email-form.js'), 'utf8');
  const navigations = [], listeners = [];
  const action = 'mailto:comercial@praia.digital?subject=Interesse%20em%20Bertioga';
  const field = (name, value, type = 'text') => ({name, value, type, tagName: 'INPUT'});
  const form = {
    dataset: {},
    elements: [field('name', 'Ana & João'), field('city', 'Bertioga'), field('token', 'private', 'password'),
      {...field('desmarcado', 'não enviar', 'checkbox'), checked: false}],
    getAttribute: () => action,
    querySelector: () => null,
    addEventListener: (event, fn, capture) => {assert.equal(event, 'submit'); assert.equal(capture, true); listeners.push(fn);},
    append() {},
  };
  const ctx = vm.createContext({
    URL, document: {querySelectorAll: () => [form], getElementById: () => null, createElement: () => ({append() {}})},
    window: {location: {set href(url) {navigations.push(new URL(url));}}},
  });
  vm.runInContext(source, ctx);
  vm.runInContext(source, ctx);
  assert.equal(listeners.length, 1);
  assert.equal(navigations.length, 0);
  listeners[0]({preventDefault() {}, stopImmediatePropagation() {}});
  assert.equal(navigations.length, 1);
  const [draft] = navigations;
  assert.equal(draft.protocol, 'mailto:');
  assert.equal(draft.pathname, 'comercial@praia.digital');
  assert.equal(draft.searchParams.get('subject'), 'Interesse em Bertioga');
  assert.equal(draft.searchParams.get('body'), 'Nome: Ana & João\r\nCidade: Bertioga');
});
