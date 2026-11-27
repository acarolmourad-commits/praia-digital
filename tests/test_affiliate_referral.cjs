const {strict: assert} = require('node:assert');
const {readFileSync} = require('node:fs');
const {test} = require('node:test');
const vm = require('node:vm');

const html = readFileSync(require.resolve('../afiliados/index.html'), 'utf8');
const source = readFileSync(require.resolve('../js/affiliate-referral.js'), 'utf8');
const formMarkup = html.match(/<form id="property-referral"[\s\S]*?<\/form>/)[0];

class Field {
  listeners = {};
  value = '';
  textContent = '';
  href = '';
  custom = '';
  focused = false;
  addEventListener(type, handler) { this.listeners[type] = handler; }
  setCustomValidity(text) { this.custom = text; }
  focus() { this.focused = true; }
  removeAttribute(name) { delete this[name]; }
}
function setup({runScript = true} = {}) {
  const ids = ['fields', 'channel', 'contact', 'contact-label', 'city', 'type', 'summary',
               'preview', 'draft', 'body', 'status'];
  const elements = Object.fromEntries(ids.map(id => ['referral-' + id, new Field()]));
  const form = elements['property-referral'] = new Field();
  const el = id => elements['referral-' + id];
  const attempts = [];
  el('fields').disabled = true;
  el('preview').hidden = true;
  el('channel').value = 'email';
  el('contact').type = 'email';
  form.reportValidity = () => {
    const contact = el('contact');
    return !['contact', 'city', 'summary'].some(id => el(id).custom) && Boolean(el('type').value) &&
      (contact.type !== 'email' || /^\S+@\S+\.\S+$/.test(contact.value.trim()));
  };
  if (runScript) vm.runInNewContext(source, {
    document: {getElementById: id => elements[id]},
    window: {open() { attempts.push('window.open'); }, location: {assign() { attempts.push('navigate'); }}},
    fetch() { attempts.push('fetch'); },
    navigator: {sendBeacon() { attempts.push('beacon'); }},
  });
  return {el, form, attempts};
}
function valid({el}) {
  el('contact').value = 'teste+afiliado@example.invalid';
  el('city').value = '  São Sebastião ';
  el('type').value = 'Casa';
  el('summary').value = 'Venda & reforma?\nCom dois quartos.';
}
function prepare({form}) {
  let prevented = false;
  form.listeners.submit({preventDefault: () => { prevented = true; }});
  assert.equal(prevented, true);
}

test('only intended fields, native label/tab order, accessible status and a blocked/no-JS fallback', () => {
  const fallback = html.match(/<p id="referral-fallback">.*?<\/p>/)[0];
  const ctx = setup({runScript: false});
  assert.equal(ctx.el('fields').disabled, true);
  assert.match(formMarkup, /<fieldset [^>]*\bdisabled>/);
  assert.match(formMarkup, /aria-describedby="referral-instructions referral-minimum"/);
  assert.doesNotMatch(formMarkup, /\b(?:name|action|target)=|afiliado_pix|proprietario_|condom[ií]nio|endereco|bairro|valor/iu);
  const controls = [...formMarkup.matchAll(/<(?:select|input|textarea) id="([^"]+)"/g)].map(x => x[1]);
  assert.deepEqual(controls, ['referral-channel', 'referral-contact', 'referral-city', 'referral-type', 'referral-summary']);
  for (const id of controls) assert.match(formMarkup, new RegExp('label for="' + id + '"'));
  assert.equal([...formMarkup.matchAll(/>Preparar rascunho de e-mail</g)].length, 1);
  assert.match(html, /id="referral-status" role="status"/);
  assert.match(html, /id="referral-preview" hidden/);
  assert.match(html, /id="referral-body"[^>]*readonly/);
  assert.match(fallback, /não abrir|não estiver disponível/);
  assert.match(fallback, /comercial@praia\.digital/);
  assert.match(fallback, /Indicação de imóvel - Afiliado/);
  assert.match(fallback, /precisa de conexão para enviá-la/);
  assert.match(html, /<a href="\/meu-imovel\.html">Central do proprietário/);
  assert.match(html, /https:\/\/praia\.digital\/politica-de-privacidade\.html/);
  assert.match(html, /Não inclua CPF, chave Pix, dados bancários ou de pagamento/);
});

test('keyboard-submit handler builds a safe local mailto, focuses the native draft link, and never opens or sends it', () => {
  const ctx = setup();
  valid(ctx);
  assert.equal(ctx.el('fields').disabled, false);
  prepare(ctx);
  assert.equal(ctx.el('preview').hidden, false);
  assert.equal(ctx.el('draft').focused, true);
  const uri = new URL(ctx.el('draft').href);
  assert.equal(uri.protocol, 'mailto:');
  assert.equal(uri.pathname, 'comercial@praia.digital');
  assert.deepEqual([...uri.searchParams.keys()], ['subject', 'body']);
  assert.equal(uri.searchParams.get('subject'), 'Indicação de imóvel - Afiliado');
  assert.equal(uri.searchParams.get('body'), ctx.el('body').value);
  assert.equal(uri.searchParams.get('body'),
    'Contato para retorno (E-mail): teste+afiliado@example.invalid\r\nCidade: São Sebastião\r\nTipo de imóvel: Casa\r\nResumo: Venda & reforma? Com dois quartos.');
  assert.deepEqual(ctx.attempts, []);
  assert.match(ctx.el('status').textContent, /não enviou/);
  assert.doesNotMatch(source, /\.click\(|fetch\(|sendBeacon\(|localStorage|sessionStorage/);
});

test('a blocked mailto has a readable copy and no false success; subsequent edits invalidate the old draft', () => {
  const ctx = setup();
  valid(ctx);
  prepare(ctx);
  assert.match(ctx.el('body').value, /exemplo|example\.invalid/);
  assert.equal(ctx.el('preview').hidden, false);
  assert.deepEqual(ctx.attempts, []);
  ctx.el('summary').value = 'Novo resumo.';
  ctx.form.listeners.input();
  assert.equal(ctx.el('preview').hidden, true);
  assert.equal(ctx.el('draft').href, undefined);
  assert.equal(ctx.el('body').value, '');
  prepare(ctx);
  assert.match(ctx.el('body').value, /Novo resumo/);
});

test('changing to WhatsApp clears the old e-mail; invalid phone and whitespace cannot prepare a draft', () => {
  const ctx = setup();
  valid(ctx);
  ctx.el('channel').value = 'whatsapp';
  ctx.el('channel').listeners.change();
  assert.equal(ctx.el('contact').type, 'tel');
  assert.equal(ctx.el('contact').autocomplete, 'tel');
  assert.equal(ctx.el('contact-label').textContent, 'Seu WhatsApp');
  assert.equal(ctx.el('contact').value, '');
  ctx.el('contact').value = 'não é telefone';
  prepare(ctx);
  assert.equal(ctx.el('preview').hidden, true);
  assert.match(ctx.el('contact').custom, /DDD/);
  ctx.el('contact').value = '+55 (11) 00000-0000';
  ctx.el('summary').value = '   ';
  prepare(ctx);
  assert.equal(ctx.el('preview').hidden, true);
  assert.match(ctx.el('summary').custom, /resumo/);
  ctx.el('summary').value = 'Casa para temporada.';
  prepare(ctx);
  assert.match(ctx.el('body').value, /^Contato para retorno \(WhatsApp\): \+55 \(11\) 00000-0000/);
  assert.doesNotMatch(ctx.el('body').value, /example\.invalid/);
  assert.deepEqual(ctx.attempts, []);
});
