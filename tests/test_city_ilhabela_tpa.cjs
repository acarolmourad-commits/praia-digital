const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const root = path.resolve(__dirname, '..');
const data = require('../data/city-guides.json');
const official = 'https://www.ilhabela.sp.gov.br/taxa-de-preservacao-ambiental/';
const readGuide = slug => fs.readFileSync(path.join(root, 'cidades', `${slug}.html`), 'utf8');

test('Ilhabela links to permanent municipal TPA guidance without dated information', () => {
  assert.deepEqual(data.cities.filter(city => city.visitAdvice?.source === official).map(city => city.slug), ['ilhabela']);
  const page = readGuide('ilhabela');
  const references = page.match(/<section id="fontes"[^>]*>(.*?)<\/section>/s)[1];
  const note = references.match(/<p class="src"><strong>Antes de ir de veículo:<\/strong>(.*?)<\/p>/s)[1];
  assert.match(note, /veículos sujeitos à cobrança/);
  assert.match(note, /por entrada em Ilhabela, não por dia/);
  assert.match(note, /Taxa de Preservação Ambiental \(TPA\)/);
  assert.ok(note.includes(`href="${official}"`));
  assert.doesNotMatch(note, /anistia|\bdezembro\b|R\$|ecoilhabela|emitidos/i);
  assert.equal(page.split(official).length - 1, 1);
  assert.ok(page.includes('href="https://praia.digital/cidades/ilhabela.html"'));
});
test('the official TPA link does not leak to other city guides or the index', () => {
  for (const slug of ['index', ...data.cities.map(city => city.slug).filter(slug => slug !== 'ilhabela')]) {
    assert.ok(!readGuide(slug).includes(official), slug);
  }
});
