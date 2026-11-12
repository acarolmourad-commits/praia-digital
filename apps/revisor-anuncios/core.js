(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PraiaConsistency = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const MODES = Object.freeze({ venda: 'Venda', mensal: 'Locação mensal', temporada: 'Temporada · por diária' });
  const FIELDS = Object.freeze([
    { key: 'mode', label: 'Modalidade' },
    { key: 'area', label: 'Área informada', unit: 'm²' },
    { key: 'rooms', label: 'Quartos' },
    { key: 'parking', label: 'Vagas' },
    { key: 'price', label: 'Preço pedido' }
  ]);
  const decimal = new Intl.NumberFormat('pt-BR', { maximumFractionDigits: 2 });
  const money = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

  function parseNumber(raw, key) {
    const value = String(raw ?? '').trim();
    if (!value) return { value: null };
    const integer = key === 'rooms' || key === 'parking';
    const pattern = integer ? /^\d+$/ : /^(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d{1,2})?$/;
    if (!pattern.test(value)) return { error: integer ? 'Informe um inteiro igual ou maior que zero.' : 'Use formato brasileiro, como 1.234,56, sem símbolos.' };
    const clean = value.replace(/\./g, '').replace(',', '.');
    const n = Number(clean);
    if (!Number.isFinite(n) || n > 1000000000000 || !Number.isSafeInteger(Math.round(n * 100))) return { error: 'O número excede o limite aceito de 1 trilhão.' };
    if ((!integer && n <= 0) || (integer && n < 0)) return { error: integer ? 'Informe zero ou um número positivo.' : 'Informe um valor maior que zero ou deixe em branco.' };
    return { value: n };
  }

  function normalize(record, label) {
    const values = { mode: null, area: null, rooms: null, parking: null, price: null };
    const errors = [];
    const mode = String(record.mode ?? '').trim();
    if (mode && !Object.hasOwn(MODES, mode)) errors.push({ record: label, field: 'mode', message: 'Selecione uma modalidade válida.' });
    else values.mode = mode || null;
    for (const { key } of FIELDS.filter(f => f.key !== 'mode')) {
      const parsed = parseNumber(record[key], key);
      if (parsed.error) errors.push({ record: label, field: key, message: parsed.error });
      else values[key] = parsed.value;
    }
    return { values, errors };
  }

  function display(key, value, mode) {
    if (value === null) return 'Não informado';
    if (key === 'mode') return MODES[value];
    if (key === 'price') {
      const suffix = mode === 'mensal' ? '/mês' : mode === 'temporada' ? '/diária' : '';
      return `${money.format(value)}${suffix}`;
    }
    return `${decimal.format(value)}${key === 'area' ? ' m²' : ''}`;
  }

  function review(reference, versions, confirmed) {
    const ref = normalize(reference, 'Ficha de referência');
    const normalized = versions.map((v, i) => ({ ...normalize(v, `Versão ${i + 1}`), name: String(v.name || `Versão ${i + 1}`).trim().slice(0, 120) || `Versão ${i + 1}` }));
    const errors = [...ref.errors, ...normalized.flatMap(v => v.errors)];
    if (!confirmed) errors.unshift({ record: 'Ficha de referência', field: 'confirmed', message: 'Confirme que a ficha foi conferida antes de comparar.' });
    if (errors.length) return { ok: false, errors };

    const rows = normalized.flatMap((v, i) => FIELDS.map(({ key, label }) => {
      const expected = ref.values[key];
      const actual = v.values[key];
      let status, detail;
      if (expected === null) {
        status = 'reference_missing'; detail = 'Falta informação na referência. Confirme antes de concluir.';
      } else if (actual === null) {
        status = 'missing'; detail = 'O campo não foi informado nesta versão.';
      } else if (key === 'price' && (!ref.values.mode || !v.values.mode || ref.values.mode !== v.values.mode)) {
        status = 'incomparable'; detail = 'Preços só são comparados quando a modalidade e a periodicidade são iguais e informadas.';
      } else if (expected === actual) {
        status = 'match'; detail = 'Coincide com a referência informada.';
      } else {
        status = 'different'; detail = 'Há diferença entre os valores informados. Verifique a fonte e a versão correta.';
      }
      return { version: i, name: v.name, key, label, status, detail, reference: display(key, expected, ref.values.mode), value: display(key, actual, v.values.mode) };
    }));
    return { ok: true, rows, counts: {
      different: rows.filter(r => r.status === 'different').length,
      pending: rows.filter(r => ['reference_missing', 'missing', 'incomparable'].includes(r.status)).length,
      matching: rows.filter(r => r.status === 'match').length
    } };
  }
  return { MODES, FIELDS, parseNumber, normalize, display, review };
});
