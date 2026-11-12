// Regression: links below the old inline script must be searchable after parsing.
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../js/blog-search.js'), 'utf8');

function element() {
  return { children: [], hidden: false, value: '', textContent: '', events: {},
    appendChild(child) { this.children.push(child); },
    addEventListener(name, callback) { this.events[name] = callback; },
    focus() { this.focused = true; } };
}
function anchor(href, text, title) {
  return { getAttribute() { return href; }, textContent: text,
    closest() { return title ? { querySelector() { return { textContent: title }; } } : null; } };
}
function fixture(readyState = 'loading') {
  const ids = Object.fromEntries(['pdBlogList', 'pdBlogSearch', 'pdBlogCount', 'pdBlogClear', 'pdBlogEmpty'].map(id => [id, element()]));
  const anchors = [anchor('/blog/airbnb.html', 'Airbnb'), anchor('/servicos.html', 'Serviços')];
  const document = { readyState, baseURI: 'https://praia.digital/blog/index.html', events: {},
    getElementById(id) { return ids[id]; }, createElement: element,
    querySelectorAll() { return anchors; },
    addEventListener(name, callback) { this.events[name] = callback; } };
  vm.runInNewContext(source, { document, window: { location: { origin: 'https://praia.digital' } }, URL });
  return { ids, anchors, document,
    visible() { return ids.pdBlogList.children.filter(x => !x.hidden).map(x => x.children[0].textContent); },
    search(query) { ids.pdBlogSearch.value = query; ids.pdBlogSearch.events.input(); } };
}
test('waits for late links, normalizes accents and matches multiple words', () => {
  const f = fixture();
  assert.equal(f.ids.pdBlogList.children.length, 0);
  f.anchors.push(anchor('sao-vicente-financiamento.html', 'São Vicente — financiamento'));
  f.document.events.DOMContentLoaded();
  f.search('  VICENTE   sao ');
  assert.deepEqual(f.visible(), ['São Vicente — financiamento']);
});
test('canonicalizes duplicate relative links and excludes external and commercial links', () => {
  const f = fixture();
  f.anchors.push(anchor('airbnb.html', 'Duplicate'), anchor('https://example.com/blog/a.html', 'External'));
  f.document.events.DOMContentLoaded();
  assert.deepEqual(f.visible(), ['Airbnb']);
});
test('indexes root-level editorial guides and descriptive card titles', () => {
  const f = fixture();
  f.anchors.push(anchor('/dados-ocupacao-temporada-litoral-sp-2026.html', 'Dados de ocupação'));
  f.anchors.push(anchor('/guias/litoral-norte-imoveis.html', 'Abrir guia', 'Litoral Norte'));
  f.document.events.DOMContentLoaded();
  f.search('ocupacao'); assert.deepEqual(f.visible(), ['Dados de ocupação']);
  f.search('norte'); assert.deepEqual(f.visible(), ['Litoral Norte']);
});
test('shows no results, treats input as text and clear restores results and focus', () => {
  const f = fixture('complete');
  f.search('<img src=x onerror=alert(1)>');
  assert.equal(f.ids.pdBlogEmpty.hidden, false);
  assert.match(f.ids.pdBlogCount.textContent, /0 guias encontrados/);
  assert.equal(f.ids.pdBlogList.children.length, 1);
  f.ids.pdBlogClear.events.click();
  assert.deepEqual(f.visible(), ['Airbnb']);
  assert.equal(f.ids.pdBlogEmpty.hidden, true);
  assert.equal(f.ids.pdBlogSearch.focused, true);
});
