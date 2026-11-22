const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const read = name => readFileSync(path.join(root, name), 'utf8');
const html = read('suporte-marketplaces.html');
const plain = value => value.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
const rows = [...html.matchAll(/<details data-t="([^"]*)"><summary>(.*?)<\/summary>([\s\S]*?)<\/details>/g)]
  .map(([, terms, title, answer]) => ({ terms, title, answer }));
const faq = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);

test('all 13 FAQ answers have identical visible and structured text', () => {
  assert.equal(rows.length, 13);
  assert.deepEqual(faq.mainEntity.map(entry => entry.name), rows.map(row => row.title));
  for (const i of rows.keys()) {
    assert.equal(faq.mainEntity[i].acceptedAnswer.text, plain(rows[i].answer), rows[i].title);
  }
  assert.doesNotMatch(html, /28\.061\.00|9404\.9000|\b5102\b|Taxas 2026:|margem real|nunca cancele|não cancele/i);
  const fiscal = faq.mainEntity[9].acceptedAnswer.text;
  assert.match(fiscal, /anexos II a XXVI do Convênio ICMS 142\/18/);
  assert.match(fiscal, /mesmo quando a operação não está sujeita à substituição tributária/);
  const stock = faq.mainEntity[11].acceptedAnswer.text;
  assert.match(stock, /art\. 35.*cabe ao comprador escolher entre exigir a entrega nas condições anunciadas, aceitar um produto equivalente ou rescindir o contrato/);
  assert.match(stock, /restituição do valor pago, corrigido monetariamente, e eventuais perdas e danos/);
  assert.match(stock, /direito de arrependimento nas compras a distância.*art\. 49/);
  assert.match(rows[8].answer, /estimar sua margem/);
  assert.match(rows[0].answer, /Não compartilhe senhas nem códigos/);
  assert.match(rows[6].answer, /Ele não mede o lucro/);
  assert.match(rows[10].answer, /não garante o recebimento/);
  assert.doesNotMatch(html, /nunca é bloqueado|100×150|álcool isopropílico|R\$ 10 por campanha|9[–-]10|9,7|máx\. 20|print da tela|respondemos rápido/i);
});

test('FAQ search normalizes terms, announces counts and restores accordion state', () => {
  const listeners = {};
  let active;
  const input = {
    value: '',
    addEventListener(event, fn) { listeners[event] = fn; },
    focus() { active = input; },
  };
  const clear = { disabled: true, addEventListener(event, fn) { listeners[event] = fn; } };
  const status = { textContent: '' }, search = { hidden: true };
  const categories = Array.from({ length: 5 }, () => ({ hidden: false }));
  const items = rows.map(({ terms, title, answer }, i) => ({
    hidden: false,
    open: i === 0,
    getAttribute(name) { assert.equal(name, 'data-t'); return terms; },
    textContent: title + ' ' + plain(answer),
  }));
  const document = {
    getElementById(id) { return { 'faq-search': search, q: input, 'faq-clear': clear, 'faq-status': status }[id]; },
    querySelectorAll(selector) {
      if (selector === '#lista details') return items;
      assert.equal(selector, '#lista .cat');
      return categories;
    },
  };
  const context = vm.createContext({ document });
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
  assert.match(html, /<label for="q">Buscar nas perguntas frequentes<\/label>/);
  assert.match(html, /id="faq-status" role="status"/);
  assert.equal(search.hidden, false);
  assert.equal(clear.disabled, true);
  assert.equal(status.textContent, '13 perguntas disponíveis.');

  function query(value, expected, message) {
    input.value = value;
    listeners.input();
    assert.deepEqual(items.flatMap((item, i) => item.hidden ? [] : [i]), expected);
    assert.equal(status.textContent, message);
    assert.ok(categories.every(category => category.hidden === Boolean(value.trim())));
  }
  query('  CEST  ', [9], '1 pergunta encontrada.');
  assert.equal(items[9].open, true);
  items[9].open = false; // a keyboard or pointer action may close a match
  query('cest', [9], '1 pergunta encontrada.');
  assert.equal(items[9].open, false);
  query('documentacao', [2], '1 pergunta encontrada.');
  query('  prazo   estoque ', [2], '1 pergunta encontrada.');
  query('estoque prazo', [2], '1 pergunta encontrada.');
  query('estoque', [2, 11], '2 perguntas encontradas.');
  query('reembolso', [11], '1 pergunta encontrada.');
  query('comissão', [8], '1 pergunta encontrada.');
  query('comissao', [8], '1 pergunta encontrada.');
  query('código fiscal', [9], '1 pergunta encontrada.');
  query('codigo fiscal', [9], '1 pergunta encontrada.');
  query('zz sem resultado', [], 'Nenhuma pergunta encontrada. Tente outro termo ou limpe a busca.');
  assert.equal(clear.disabled, false);
  listeners.click();
  assert.equal(input.value, '');
  assert.equal(active, input);
  assert.equal(clear.disabled, true);
  assert.equal(status.textContent, '13 perguntas disponíveis.');
  assert(items.every(item => !item.hidden));
  assert.deepEqual(items.flatMap((item, i) => item.open ? [i] : []), [0]);
  items[0].open = false;
  items[4].open = true;
  query('  RESTITUICAO  ', [11], '1 pergunta encontrada.');
  query('restituição', [11], '1 pergunta encontrada.');
  query('', rows.map((_, i) => i), '13 perguntas disponíveis.');
  assert.deepEqual(items.flatMap((item, i) => item.open ? [i] : []), [4]);
  query('    ', rows.map((_, i) => i), '13 perguntas disponíveis.');
});

test('canonical, official sources and seller journey point to the intended destinations', () => {
  assert.match(html, /rel="canonical" href="https:\/\/praia\.digital\/suporte-marketplaces\.html"/);
  const hrefs = markup => [...markup.matchAll(/href="([^"]+)"/g)].map(match => match[1]);
  assert.deepEqual(hrefs(html.match(/<header[\s\S]*?<\/header>/)[0]), ['/']);
  assert.deepEqual(hrefs(html.match(/<footer[\s\S]*?<\/footer>/)[0]), [
    '/apps/guia-de-uso.html#vender', '/contato.html',
  ]);
  assert.match(read('apps/guia-de-uso.html'), /id="vender"/);
  assert.match(read('apps/calculadora-precificacao-shopee/index.html'), /rel="canonical" href="https:\/\/praia\.digital\/apps\/calculadora-precificacao-shopee\/"/);
  assert.deepEqual(hrefs(rows[0].answer), ['https://seller.shopee.com.br/']);
  for (const i of [5, 6]) assert.deepEqual(hrefs(rows[i].answer), ['https://ads.shopee.com.br/learn/faq/217/2233']);
  assert.deepEqual(hrefs(rows[10].answer), ['https://help.shopee.com.br/portal/4/article/77113']);
  const cta = html.match(/<div class="cta">([\s\S]*?)<\/div>/)[1];
  assert.match(cta, /sem incluir senhas, códigos de acesso ou dados de clientes/);
  assert.deepEqual(hrefs(cta), ['https://wa.me/5511954346288?text=Preciso%20de%20ajuda%20com%20minha%20loja']);
  assert.deepEqual(hrefs(rows[8].answer), [
    'https://seller.shopee.com.br/edu/home', '/apps/calculadora-precificacao-shopee/',
  ]);
  assert.deepEqual(hrefs(rows[9].answer).map(url => new URL(url).hostname), [
    'www.gov.br', 'www.confaz.fazenda.gov.br', 'www.confaz.fazenda.gov.br',
  ]);
  assert.deepEqual(hrefs(rows[11].answer), [
    'https://help.shopee.com.br/portal/4/article/76351',
    'https://www2.camara.leg.br/legin/fed/lei/1990/lei-8078-11-setembro-1990-365086-normaatualizada-pl.html',
  ]);
});
