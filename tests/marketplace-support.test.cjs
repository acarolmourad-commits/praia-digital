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
const changedTopics = [1, 2, 4, 8, 9, 11, 12];

test('all FAQ questions are indexed, with exact visible/schema text for the revised answers', () => {
  assert.equal(rows.length, 13);
  assert.deepEqual(faq.mainEntity.map(entry => entry.name), rows.map(row => row.title));
  for (const i of changedTopics) {
    assert.equal(faq.mainEntity[i].acceptedAnswer.text, plain(rows[i].answer), rows[i].title);
  }
  assert.doesNotMatch(html, /28\.061\.00|9404\.9000|\b5102\b|Taxas 2026:|margem real|nunca cancele|não cancele/i);
  assert.match(rows[9].answer, /mesmo quando a operação não está sujeita à substituição tributária/);
  assert.match(rows[11].answer, /cabe ao comprador escolher/);
  assert.match(rows[8].answer, /estimar sua margem/);
});

test('FAQ filter retains matching, opening and resetting the revised rows', () => {
  const input = { value: '' };
  const categories = Array.from({ length: 5 }, () => ({ style: {} }));
  const items = rows.map(({ terms, title, answer }) => ({
    hidden: false,
    open: false,
    getAttribute(name) { assert.equal(name, 'data-t'); return terms; },
    textContent: title + ' ' + plain(answer),
  }));
  for (const row of items) {
    row.classList = { toggle(name, hidden) { assert.equal(name, 'hidden'); row.hidden = Boolean(hidden); } };
  }
  const document = {
    getElementById(id) { assert.equal(id, 'q'); return input; },
    querySelectorAll(selector) {
      if (selector === '#lista details') return items;
      assert.equal(selector, '#lista .cat');
      return categories;
    },
  };
  const context = vm.createContext({ document });
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1], context);
  const handler = html.match(/id="q"[^>]*oninput="([^"]+)"/)[1];
  function query(value, expected) {
    input.value = value;
    items.forEach(item => { item.open = false; });
    vm.runInContext(handler, context);
    assert.deepEqual(items.flatMap((item, i) => item.hidden ? [] : [i]), expected);
    assert.deepEqual(items.flatMap((item, i) => item.open ? [i] : []), value ? expected : []);
    assert.ok(categories.every(category => category.style.display === (value ? 'none' : '')));
  }
  query('CEST', [9]);
  query('estoque', [2, 11]);
  query('cancelamento', [2, 11]);
  query('reembolso', [11]);
  query('comissao', [8]);
  query('sem correspondência', []);
  query('', rows.map((_, i) => i));
});

test('canonical, official sources and seller journey point to the intended destinations', () => {
  assert.match(html, /rel="canonical" href="https:\/\/praia\.digital\/suporte-marketplaces\.html"/);
  const hrefs = markup => [...markup.matchAll(/href="([^"]+)"/g)].map(match => match[1]);
  assert.deepEqual(hrefs(html.match(/<footer[\s\S]*?<\/footer>/)[0]), [
    '/apps/guia-de-uso.html#vender', '/contato.html',
  ]);
  assert.match(read('apps/guia-de-uso.html'), /id="vender"/);
  assert.match(read('apps/calculadora-precificacao-shopee/index.html'), /rel="canonical" href="https:\/\/praia\.digital\/apps\/calculadora-precificacao-shopee\/"/);
  assert.deepEqual(hrefs(rows[8].answer), [
    'https://seller.shopee.com.br/edu/home', '/apps/calculadora-precificacao-shopee/',
  ]);
  assert.deepEqual(hrefs(rows[9].answer).map(url => new URL(url).hostname), [
    'www.gov.br', 'www.confaz.fazenda.gov.br', 'www.confaz.fazenda.gov.br',
  ]);
  assert.deepEqual(hrefs(rows[11].answer), [
    'https://help.shopee.com.br/portal/4/article/76351',
    'https://planalto.gov.br/ccivil_03/leis/l8078compilado.htm',
  ]);
});
