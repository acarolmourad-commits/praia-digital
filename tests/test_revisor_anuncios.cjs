const test = require('node:test');
const assert = require('node:assert/strict');
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
