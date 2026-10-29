/* Shared, deterministic query parsing. No network or generated listings. */
(function (root) {
  'use strict';
  const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const cities = ['São Sebastião','Caraguatatuba','Praia Grande','São Vicente','Bertioga','Guarujá','Santos','Mongaguá','Itanhaém','Peruíbe','Ubatuba','Ilhabela'];
  function money(value) {
    let s = normalize(value).replace(/r\$\s*/g, '').trim();
    const match = s.match(/^([\d.,]+)\s*(milhoes|milhao|mil|mi)?$/);
    if (!match) return null;
    let amount = match[1];
    if (amount.includes(',')) amount = amount.replace(/\./g, '').replace(',', '.');
    else if (/^\d{1,3}(\.\d{3})+$/.test(amount)) amount = amount.replace(/\./g, '');
    let n = Number(amount) * (match[2] === 'mil' ? 1000 : match[2] ? 1000000 : 1);
    return Number.isFinite(n) && n > 0 ? Math.round(n * 100) / 100 : null;
  }
  function parse(query) {
    let rest = normalize(query);
    const result = { cidade:'', quartos:'', preco_max:'', tipo:'', finalidade:'', perfil:'', terms:[] };
    for (const city of cities) {
      const re = new RegExp('\\b' + normalize(city) + '\\b', 'g');
      if (re.test(rest)) { result.cidade = city; rest = rest.replace(re, ' '); break; }
    }
    if (/\briviera(?: de sao lourenco)?\b/.test(rest)) {
      result.cidade = 'Bertioga'; rest = rest.replace(/\briviera(?: de sao lourenco)?\b/g, ' riviera ');
    }
    rest = rest.replace(/\b(\d{1,2})\s*(?:quartos?|dormitorios?|dorms?|suites?)\b/g, (_, n) => { result.quartos=String(Number(n)); return ' '; });
    rest = rest.replace(/(?:ate\s*(?:r\$\s*)?|r\$\s*)([\d.,]+\s*(?:milhoes|milhao|mil|mi)?)/g, (_, n) => { result.preco_max=money(n) || ''; return ' '; });
    for (const [re, type] of [[/\b(?:apartamentos?|aptos?|apes?)\b/g,'apartamento'],[/\bcasas?\b/g,'casa'],[/\bcoberturas?\b/g,'cobertura'],[/\bterrenos?\b/g,'terreno'],[/\bstudios?\b/g,'studio']]) {
      if(re.test(rest)) { result.tipo=type; rest=rest.replace(re,' '); break; }
    }
    rest = rest.replace(/\b(?:comprar|compra|venda)\b/g, () => { result.finalidade='Venda'; return ' '; });
    rest = rest.replace(/\b(?:alugar|aluguel|locacao)\b/g, () => { result.finalidade='Aluguel'; return ' '; });
    rest = rest.replace(/\btemporada\b/g, () => { result.perfil='temporada'; return ' '; });
    rest = rest.replace(/\binvest\w*\b/g, () => { result.perfil='investimento'; return ' '; });
    const stop = new Set('a o as os um uma uns umas de do da dos das em no na nos nas e com para por ate perto potencial litoral praia paulista quero procuro buscar encontrar imovel imoveis minimo minima pelo menos'.split(' '));
    result.terms=rest.split(/[^a-z0-9]+/).filter(t=>t&&!stop.has(t));
    return result;
  }
  function fromParams(params) {
    const q=params.get('q') || '';
    const state={q,...parse(q)};
    for(const key of ['cidade','quartos','preco_max','tipo','finalidade','perfil']) if(params.has(key)) state[key]=params.get(key);
    for(const key of ['quartos','preco_max']) if(state[key] && (!Number.isFinite(Number(state[key])) || Number(state[key])<0)) state[key]='';
    return state;
  }
  function matches(p, state) {
    const text=normalize([p.title,p.city,p.type,p.description,...(p.tags||[])].join(' '));
    if(state.cidade && normalize(p.city)!==normalize(state.cidade)) return false;
    if(state.finalidade && normalize(p.type)!==normalize(state.finalidade)) return false;
    if(state.tipo && !normalize(p.title).split(/[^a-z0-9]+/).some(word=>word.startsWith(normalize(state.tipo)))) return false;
    if(state.quartos && Number(p.bedrooms)<Number(state.quartos)) return false;
    const price=money(String(p.price).replace(/\/(?:mes|mês|dia).*$/i,''));
    if(state.preco_max && (price===null || price>Number(state.preco_max))) return false;
    if(state.perfil==='temporada' && !/temporada/.test(text)) return false;
    return state.terms.every(term=>text.includes(term));
  }
  const api={normalize,money,parse,fromParams,matches,cities};
  if(typeof module==='object'&&module.exports) module.exports=api;
  else root.PDPropertySearch=api;
})(typeof window==='undefined'?globalThis:window);
