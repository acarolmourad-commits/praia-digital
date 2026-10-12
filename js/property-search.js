/* Shared, side-effect-free search contract. Prices are BRL estimates, not availability promises. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.PDPropertySearch = api;
})(typeof globalThis === 'object' ? globalThis : this, function () {
  'use strict';
  const keys = ['q', 'cidade', 'quartos', 'preco_max', 'tipo', 'perfil', 'finalidade'];
  const cities = ['sao sebastiao', 'caraguatatuba', 'praia grande', 'sao vicente', 'bertioga', 'guaruja', 'santos', 'mongagua', 'itanhaem', 'peruibe', 'ubatuba', 'ilhabela', 'riviera'];
  const norm = value => String(value == null ? '' : value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  function amount(raw, unit) {
    let s = String(raw);
    if (/^\d{1,3}(?:\.\d{3})+(?:,\d{1,2})?$/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
    else if (/^\d+(?:,\d{1,2})?$/.test(s)) s = s.replace(',', '.');
    else if (!/^\d+(?:\.\d{1,2})?$/.test(s)) return null;
    const value = Number(s) * (unit === 'mil' ? 1000 : unit ? 1000000 : 1);
    return Number.isFinite(value) && value >= 0 && value <= 1e10 ? Math.round(value * 100) / 100 : null;
  }
  function parse(query) {
    const f = { q: String(query || '').slice(0, 2000) }, n = norm(f.q);
    const city = cities.find(c => new RegExp('(?:^|\\W)' + c + '(?:$|\\W)').test(n));
    if (city) f.cidade = city;
    let m = n.match(/\b(\d{1,2})\s*(?:quartos?|dormitorios?)\b/);
    if (m && Number(m[1]) > 0) f.quartos = Number(m[1]);
    m = n.match(/(?:r\$\s*|\b(?:ate|no maximo|maximo de|orcamento(?: de)?)\s*)(\d[\d.,]*)(?:\s*(milhoes|milhao|mil|mi)\b)?/);
    if (m) { const v = amount(m[1], m[2]); if (v !== null) f.preco_max = v; }
    if (/\b(?:apartamento|apto)\b/.test(n)) f.tipo = 'apartamento';
    else for (const t of ['casa', 'studio', 'cobertura', 'sobrado']) if (new RegExp('\\b' + t + '\\b').test(n)) { f.tipo = t; break; }
    if (/\b(?:aluguel|alugar|locacao|locar)\b/.test(n)) f.finalidade = 'aluguel';
    else if (/\b(?:comprar|compra|venda)\b/.test(n)) f.finalidade = 'venda';
    if (/\btemporada\b/.test(n)) f.perfil = 'temporada';
    else if (/\binvest\w*\b/.test(n)) f.perfil = 'investimento';
    return f;
  }
  function read(search) {
    const p = new URLSearchParams(search), f = parse(p.get('q') || '');
    f.invalid = [];
    for (const key of keys.slice(1)) {
      if (!p.has(key)) continue;
      const raw = p.get(key).trim();
      if (!raw) { delete f[key]; continue; }
      let value = norm(raw), valid = true;
      if (key === 'quartos') { valid = /^\d{1,2}$/.test(raw) && Number(raw) > 0; value = Number(raw); }
      if (key === 'preco_max') { valid = /^\d+(?:\.\d{1,2})?$/.test(raw) && Number.isFinite(Number(raw)) && Number(raw) <= 1e10; value = Number(raw); }
      if (key === 'cidade') valid = value.length <= 100;
      if (key === 'tipo') valid = ['casa', 'apartamento', 'studio', 'cobertura', 'sobrado'].includes(value);
      if (key === 'perfil') valid = ['temporada', 'investimento'].includes(value);
      if (key === 'finalidade') valid = ['venda', 'aluguel', 'lancamento'].includes(value);
      if (valid) f[key] = value; else { delete f[key]; f.invalid.push(key); }
    }
    return f;
  }
  function params(f) {
    const p = new URLSearchParams();
    for (const key of keys) if (f[key] !== undefined && f[key] !== '') p.set(key, String(f[key]));
    return p;
  }
  function matches(p, f) {
    if (f.invalid && f.invalid.length) return false;
    const title = norm(p.title), city = norm(p.city), text = norm([p.title, p.city, p.type, p.description, ...(p.tags || [])].join(' '));
    if (f.cidade && !(f.cidade === 'riviera' ? (city === 'bertioga' && text.includes('riviera')) : city === norm(f.cidade))) return false;
    if (f.tipo && !(f.tipo === 'apartamento' ? /\b(?:apartamento|apto)\b/.test(title) : new RegExp('\\b' + f.tipo + '\\b').test(title))) return false;
    if (f.finalidade && norm(p.type) !== norm(f.finalidade)) return false;
    if (f.quartos && (!/^\d+$/.test(String(p.bedrooms)) || Number(p.bedrooms) < f.quartos)) return false;
    if (f.preco_max !== undefined) {
      const match = String(p.price || '').match(/(?:R\$\s*)?(\d[\d.,]*)/), price = match ? amount(match[1]) : null;
      if (price === null || price > f.preco_max) return false;
    }
    if (f.perfil && !new RegExp('\\b' + f.perfil + '\\b').test(text)) return false;
    const structured = keys.slice(1).some(k => f[k] !== undefined);
    return structured || !f.q || text.includes(norm(f.q));
  }
  return Object.freeze({ norm, amount, parse, read, params, matches });
});
