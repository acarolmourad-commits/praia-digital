const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { parseNumber, review } = require('../apps/revisor-anuncios/core.js');
const base = () => ({ mode: 'venda', area: '70,53', rooms: '2', parking: '1', price: '600.000,00' });

test('formato brasileiro aceita centavos e distingue campo vazio de zero', () => {
  assert.equal(parseNumber('1.234.567,89', 'price').value, 1234567.89);
  assert.equal(parseNumber('70,53', 'area').value, 70.53);
  assert.equal(parseNumber('', 'parking').value, null);
  assert.equal(parseNumber('0', 'parking').value, 0);
  assert.equal(parseNumber('0', 'rooms').value, 0);
  assert.ok(parseNumber('0', 'area').error);
  assert.ok(parseNumber('0', 'price').error);
});

test('rejeita negativos, fracionários de contagem, agrupamentos inválidos e precisão excessiva', () => {
  for (const value of ['-1', '2,5', '1.000']) assert.ok(parseNumber(value, 'rooms').error, value);
  for (const value of ['R$ 500', '1.23.456', '500.50', '1e6', '12,345', 'NaN', 'Infinity', '1.000.000.000.000,01', '999999999999999999999']) assert.ok(parseNumber(value, 'price').error, value);
});

test('não compara uma referência sem confirmação e não ignora dados inválidos', () => {
  assert.equal(review(base(), [base(), base()], false).ok, false);
  const result = review(base(), [{ ...base(), area: '-10' }, { ...base(), mode: 'aluguel' }], true);
  assert.equal(result.ok, false);
  assert.equal(result.errors.length, 2);
});

test('encontra coincidências mesmo com formatos numéricos equivalentes', () => {
  const result = review(base(), [{ ...base(), price: '600000', area: '70,53' }, base()], true);
  assert.equal(result.ok, true);
  assert.deepEqual(result.counts, { different: 0, pending: 0, matching: 10 });
});

test('diferenças reais de quartos e preço geram apenas os alertas correspondentes', () => {
  const result = review(base(), [{ ...base(), rooms: '3', price: '595.000' }, base()], true);
  assert.deepEqual(result.rows.filter(r => r.status === 'different').map(r => r.key), ['rooms', 'price']);
  assert.equal(result.counts.different, 2);
});

test('não trata preço de modalidades diferentes como divergência numérica', () => {
  const result = review(base(), [{ ...base(), mode: 'mensal', price: '3.200' }, { ...base(), mode: 'temporada', price: '650' }], true);
  assert.equal(result.rows.filter(r => r.key === 'price' && r.status === 'incomparable').length, 2);
  assert.equal(result.rows.filter(r => r.key === 'mode' && r.status === 'different').length, 2);
  assert.equal(result.rows.find(r => r.version === 0 && r.key === 'price').value.endsWith('/mês'), true);
});

test('preço exige modalidade nas duas fichas mesmo quando o número é idêntico', () => {
  const result = review({ ...base(), mode: '' }, [base(), base()], true);
  assert.equal(result.rows.filter(r => r.key === 'price' && r.status === 'incomparable').length, 2);
  assert.equal(result.rows.filter(r => r.key === 'mode' && r.status === 'reference_missing').length, 2);
});

test('referência incompleta e ausência de dados preservam pendências em vez de assumir zero', () => {
  const result = review({ ...base(), area: '' }, [{ ...base(), parking: '' }, { ...base(), parking: '0' }], true);
  assert.equal(result.rows.filter(r => r.key === 'area' && r.status === 'reference_missing').length, 2);
  assert.equal(result.rows.find(r => r.version === 0 && r.key === 'parking').status, 'missing');
  assert.equal(result.rows.find(r => r.version === 1 && r.key === 'parking').status, 'different');
});

test('nomes de versões são dados de texto, limitados sem interpretação de HTML', () => {
  const result = review(base(), [{ ...base(), name: '<img src=x onerror=alert(1)>' }, { ...base(), name: 'x'.repeat(200) }], true);
  assert.equal(result.rows[0].name, '<img src=x onerror=alert(1)>');
  assert.equal(result.rows[5].name.length, 120);
});

// Minimal DOM fixture built from the shipped markup, used to exercise the real
// bootstrap without relying on a browser or duplicating the comparison logic.
function loadPage({ failCreate = false, coreAvailable = true, failListenerAt = '', confirm = () => false, navigator = {}, downloadFailure = false } = {}) {
  const html = fs.readFileSync(path.join(__dirname, '../apps/revisor-anuncios/index.html'), 'utf8');
  const code = fs.readFileSync(path.join(__dirname, '../apps/revisor-anuncios/app.js'), 'utf8');
  const ids = new Map();
  const nodes = [];
  const unlocks = [];
  const downloads = [], revoked = [], timers = [];
  class Element {
    constructor(tag, attrs = {}) {
      this.tagName = tag;
      this.attrs = attrs;
      this.children = [];
      this.listeners = {};
      this._disabled = Object.hasOwn(attrs, 'disabled');
      this.hidden = Object.hasOwn(attrs, 'hidden');
      this.value = attrs.value || '';
      this.checked = false;
      this.type = attrs.type;
      this.name = attrs.name;
      this.id = attrs.id;
      nodes.push(this);
    }
    set id(value) { this._id = value; if (value) ids.set(value, this); }
    get id() { return this._id; }
    set disabled(value) {
      if (value === false && this._disabled) {
        unlocks.push({ id: this.id, submitHandlers: (ids.get('review-form')?.listeners.submit || []).length,
          exampleReady: !!ids.get('example')?.listeners.click?.length,
          copyReady: !!ids.get('copy')?.listeners.click?.length,
          printReady: !!ids.get('print')?.listeners.click?.length, downloadReady: !!ids.get('download-report')?.listeners.click?.length });
      }
      this._disabled = value;
    }
    get disabled() { return this._disabled; }
    append(...items) { for (const item of items) { item.parent = this; this.children.push(item); } }
    before(node) { node.parent = this.parent; this.parent.children.splice(this.parent.children.indexOf(this), 0, node); }
    click() { if (this.tagName === 'a') downloads.push({ name: this.download, href: this.href }); }
    replaceChildren(...items) { this.children = []; this.append(...items); }
    addEventListener(type, handler) {
      if (this.id === failListenerAt) throw new Error('simulated late initialization failure');
      (this.listeners[type] ||= []).push(handler);
    }
    setAttribute(name, value) { this.attrs[name] = value; }
    removeAttribute(name) { delete this.attrs[name]; }
    focus() {}
    reset() { for (const n of nodes) { n.value = ''; n.checked = false; } }
  }
  const root = new Element('root');
  const stack = [root];
  const voids = new Set(['meta', 'link', 'input', 'br', 'img', 'hr']);
  for (const token of html.matchAll(/<\/?([a-z][a-z0-9-]*)([^>]*)>/gi)) {
    const tag = token[1].toLowerCase();
    if (token[0].startsWith('</')) {
      const i = stack.map(e => e.tagName).lastIndexOf(tag);
      if (i > 0) stack.length = i;
      continue;
    }
    const attrs = {};
    for (const attr of token[2].matchAll(/([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
      attrs[attr[1]] = attr[2] ?? attr[3] ?? attr[4] ?? '';
    }
    const node = new Element(tag, attrs);
    stack.at(-1).append(node);
    if (!voids.has(tag)) stack.push(node);
  }
  function disabled(node) {
    if (node.disabled) return true;
    for (let p = node.parent; p; p = p.parent) if (p.tagName === 'fieldset' && p.disabled) return true;
    return false;
  }
  const document = {
    getElementById: id => ids.get(id),
    createElement: tag => { if (failCreate) throw new Error('simulated initialization failure'); return new Element(tag); },
    querySelectorAll: () => nodes.filter(n => Object.hasOwn(n.attrs, 'aria-invalid'))
  };
  function submit() {
    const event = { defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
    for (const handler of ids.get('review-form').listeners.submit || []) handler(event);
    return event;
  }
  const blobs = [];
  return { ids, nodes, unlocks, disabled, submit, downloads, blobs, revoked, timers,
    init() { vm.runInNewContext(code, { document, window: { confirm, PraiaConsistency: coreAvailable ? require('../apps/revisor-anuncios/core.js') : undefined }, navigator, Blob, URL: {createObjectURL(blob) { if (downloadFailure) throw new Error('Download unavailable'); blobs.push(blob); return 'blob:test-' + blobs.length; }, revokeObjectURL(url) { revoked.push(url); }}, setTimeout(fn, ms) { timers.push({fn, ms}); } }); } };
}

test('sem JavaScript, campos e ações permanecem inertes e não há campo nomeado para GET', () => {
  const page = loadPage();
  const property = page.ids.get('property');
  const submit = page.nodes.find(n => n.tagName === 'button' && n.type === 'submit');
  assert.ok(page.disabled(property), 'identificação não pode ser preenchida antes do bootstrap');
  assert.ok(page.disabled(submit), 'o submit nativo deve começar desabilitado');
  assert.ok(page.disabled(page.ids.get('confirmed')));
  for (const id of ['example', 'copy', 'print', 'clear']) assert.ok(page.disabled(page.ids.get(id)), id);
  assert.equal(page.nodes.filter(n => ['input', 'select', 'textarea'].includes(n.tagName) && n.name).length, 0);
});

test('inicialização completa habilita controles só depois dos handlers e cancela submissão nativa', () => {
  const page = loadPage();
  page.init();
  assert.equal(page.unlocks.length, 5);
  for (const state of page.unlocks) {
    assert.ok(state.submitHandlers >= 1, state.id);
    assert.ok(state.exampleReady && state.copyReady && state.printReady && state.downloadReady, state.id);
  }
  assert.equal(page.disabled(page.ids.get('property')), false);
  assert.equal(page.disabled(page.ids.get('ref-price')), false);
  assert.equal(page.nodes.filter(n => ['input', 'select'].includes(n.tagName) && n.name).length, 0);
  assert.ok(page.submit().defaultPrevented, 'mesmo uma ficha vazia nunca navega por GET');
  assert.equal(page.ids.get('errors').hidden, false, 'a validação real deve orientar a confirmação');
});

test('falha parcial ou ausência do núcleo mantém os controles bloqueados e guarda preventDefault', () => {
  for (const options of [{ failCreate: true }, { coreAvailable: false }, { failListenerAt: 'copy' }]) {
    const page = loadPage(options);
    assert.throws(() => page.init());
    assert.equal(page.unlocks.length, 0);
    assert.ok(page.disabled(page.ids.get('property')));
    assert.ok(page.disabled(page.nodes.find(n => n.tagName === 'button' && n.type === 'submit')));
    assert.ok(page.submit().defaultPrevented);
  }
});


test('limpeza e exemplo preservam dados quando a pessoa cancela', () => {
  const page = loadPage(); page.init();
  page.ids.get('ref-price').value = '900.000,00';
  for (const id of ['clear', 'example']) {
    page.ids.get(id).listeners.click[0]();
    assert.equal(page.ids.get('ref-price').value, '900.000,00');
  }
});
test('limpeza e exemplo funcionam após confirmação explícita', () => {
  const page = loadPage({ confirm: () => true }); page.init();
  page.ids.get('ref-price').value = '900.000,00';
  page.ids.get('example').listeners.click[0]();
  assert.equal(page.ids.get('ref-price').value, '600.000,00');
  page.ids.get('clear').listeners.click[0]();
  assert.equal(page.ids.get('ref-price').value, '');
  assert.equal(page.ids.get('report').hidden, true);
});

test('alterar qualquer dado de referência exige nova confirmação antes de comparar', () => {
  const changes = { mode: 'mensal', area: '80', rooms: '3', parking: '2', price: '700.000,00' };
  for (const type of ['input', 'change']) {
    for (const [key, value] of Object.entries(changes)) {
      const page = loadPage(); page.init();
      page.ids.get('example').listeners.click[0](); page.submit();
      const target = page.ids.get(`ref-${key}`); target.value = value;
      page.ids.get('review-form').listeners[type][0]({ target });
      assert.equal(page.ids.get('confirmed').checked, false, `${type}: ${key}`);
      assert.equal(page.ids.get('report').hidden, true);
      assert.equal(page.ids.get('report-text').value, '');
      assert.match(page.ids.get('live-status').textContent, /confirme a ficha novamente/);
      page.submit();
      assert.equal(page.ids.get('errors').hidden, false);
      assert.equal(page.ids.get('confirmed').attrs['aria-invalid'], 'true');
      assert.equal(page.ids.get('report').hidden, true);
      assert.equal(target.value, value, 'a nova conferência não apaga o dado alterado');
      page.ids.get('confirmed').checked = true; page.submit();
      assert.equal(page.ids.get('errors').hidden, true);
      assert.equal(page.ids.get('report').hidden, false);
    }
  }
});

test('editar identificação ou anúncios preserva a confirmação da ficha e invalida só o relatório', () => {
  for (const id of ['property', 'v1-name', 'v1-price', 'v2-mode']) {
    const page = loadPage(); page.init();
    page.ids.get('example').listeners.click[0](); page.submit();
    const target = page.ids.get(id);
    target.value = id === 'v1-price' ? '550.000,00' : id === 'v2-mode' ? 'venda' : 'Versão revisada';
    page.ids.get('review-form').listeners.input[0]({ target });
    assert.equal(page.ids.get('confirmed').checked, true, id);
    assert.equal(page.ids.get('report').hidden, true);
    page.submit();
    assert.equal(page.ids.get('report').hidden, false);
  }
});

test('resposta atrasada de cópia não confirma relatório alterado nem reabre texto limpo', async () => {
  let resolve, reject, calls = 0;
  const page = loadPage({confirm:()=>true,navigator:{clipboard:{writeText:()=>{calls++;return new Promise((yes,no)=>{resolve=yes;reject=no;});}}}});
  page.init(); page.ids.get('example').listeners.click[0](); page.submit();
  const copy=page.ids.get('copy'), status=page.ids.get('copy-status');
  const pending=copy.listeners.click[0]();assert.equal(copy.disabled,true);
  await copy.listeners.click[0]();assert.equal(calls,1,'cliques repetidos não iniciam outra cópia');
  page.ids.get('review-form').listeners.input[0]();resolve();await pending;
  assert.equal(status.textContent,'');assert.equal(copy.disabled,false);
  page.submit();const failed=copy.listeners.click[0]();page.ids.get('clear').listeners.click[0]();reject(new Error('denied'));await failed;
  assert.equal(status.textContent,'');assert.equal(page.ids.get('report-text').value,'');
  page.ids.get('example').listeners.click[0]();page.submit();const success=copy.listeners.click[0]();resolve();await success;
  assert.equal(status.textContent,'Relatório copiado.');assert.equal(copy.disabled,false);
});


test('TXT guarda a comparação vigente e não exporta relatório invalidado ou limpo', async () => {
  const page = loadPage({confirm:()=>true}); page.init();
  const download = () => page.ids.get('download-report').listeners.click[0]();
  download(); assert.equal(page.downloads.length, 0);
  page.ids.get('example').listeners.click[0](); page.submit(); download();
  assert.equal(page.downloads[0].name, 'revisor-anuncios-exemplo-ficticio.txt');
  assert.equal(page.blobs[0].type, 'text/plain;charset=utf-8');
  assert.equal(await page.blobs[0].text(), page.ids.get('report-text').value + '\n');
  assert.match(await page.blobs[0].text(), /DEMONSTRAÇÃO COM DADOS FICTÍCIOS/);
  assert.match(await page.blobs[0].text(), /Coincidência não comprova/);
  assert.equal(page.revoked.length, 0);
  page.timers[0].fn(); assert.equal(page.revoked[0], page.downloads[0].href);
  const target = page.ids.get('v1-price'); target.value = '590.000,00';
  page.ids.get('review-form').listeners.input[0]({target}); download();
  assert.equal(page.downloads.length, 1);
  page.submit(); download();
  assert.match(await page.blobs[1].text(), /590.000,00/);
  assert.doesNotMatch(await page.blobs[1].text(), /595.000,00/);
  page.ids.get('clear').listeners.click[0](); download();
  assert.equal(page.downloads.length, 2);
  page.ids.get('confirmed').checked = true; page.submit(); download();
  assert.equal(page.downloads[2].name, 'revisor-anuncios.txt');
  assert.doesNotMatch(await page.blobs[2].text(), /FICTÍCIOS|590.000,00/);
  assert.match(await page.blobs[2].text(), /Não informado/);
});

test('falha de download orienta alternativas sem anunciar arquivo baixado', () => {
  const page = loadPage({downloadFailure:true}); page.init();
  page.ids.get('example').listeners.click[0](); page.submit();
  page.ids.get('download-report').listeners.click[0]();
  assert.equal(page.downloads.length, 0);
  assert.match(page.ids.get('copy-status').textContent, /Não foi possível iniciar o download/);
  assert.match(page.ids.get('copy-status').textContent, /Copiar relatório/);
});
