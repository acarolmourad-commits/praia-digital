(function () {
  'use strict';
  function normalize(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[-_/]+/g, ' ');
  }
  function search(items, query, category) {
    const terms = normalize(query).trim().split(/\s+/).filter(Boolean);
    return items.filter(item => (!category || item.category === category) && terms.every(term =>
      normalize(item.title + ' ' + item.url + ' ' + item.category).includes(term)))
      .map(item => ({item, score: terms.reduce((score, term) => score + (normalize(item.title).includes(term) ? 1 : 0), 0)}))
      .sort((a, b) => b.score - a.score).map(result => result.item);
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {normalize, search};
  if (typeof document === 'undefined') return;
  const form = document.getElementById('content-search');
  if (!form) return;
  const query = document.getElementById('content-query');
  const category = document.getElementById('content-category');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  const list = document.getElementById('results-list');
  const more = document.getElementById('load-more');
  const clear = document.getElementById('content-clear');
  let catalog, pending, matched = [], shown = 0, request = 0;
  function load() {
    if (catalog) return Promise.resolve(catalog);
    if (!pending) pending = fetch('/data/content-search.json').then(response => {
      if (!response.ok) throw new Error('catalog');
      return response.json();
    }).then(items => {
      if (!Array.isArray(items) || !items.every(item => typeof item.title === 'string' && typeof item.category === 'string' &&
          typeof item.url === 'string' && item.url.startsWith('/') && !item.url.startsWith('//'))) throw new Error('catalog');
      catalog = items; return items;
    }).catch(error => { pending = null; throw error; });
    return pending;
  }
  function append() {
    const batch = matched.slice(shown, shown + 30);
    const firstNew = list.children.length;
    batch.forEach(item => {
      const li = document.createElement('li'), a = document.createElement('a'), label = document.createElement('span');
      a.href = item.url; a.textContent = item.title; label.textContent = item.category;
      li.append(a, label); list.append(li);
    });
    shown += batch.length; more.hidden = shown >= matched.length;
    status.textContent = matched.length ? `${matched.length.toLocaleString('pt-BR')} ${matched.length === 1 ? 'resultado' : 'resultados'}. Mostrando ${shown.toLocaleString('pt-BR')}.` :
      'Nenhum resultado. Tente menos palavras, outra cidade ou selecione todos os tipos.';
    return firstNew;
  }
  async function run(updateURL, focus) {
    const ticket = ++request;
    const q = query.value.trim().slice(0, 200), c = category.value;
    clear.hidden = false;
    if (updateURL) {
      const url = new URL(location.href); url.search = '';
      if (q) url.searchParams.set('q', q);
      if (c) url.searchParams.set('categoria', c);
      history.pushState({}, '', url);
    }
    status.textContent = 'Carregando a busca…';
    try {
      const items = await load();
      if (ticket !== request) return;
      matched = search(items, q, c); shown = 0; list.replaceChildren(); results.hidden = false;
      append();
      if (focus) document.getElementById('results-heading').focus();
    } catch (_) {
      if (ticket !== request) return;
      results.hidden = true;
      status.textContent = 'Não foi possível carregar a busca. Tente Buscar novamente ou use o diretório de A a Z abaixo.';
    }
  }
  function restore() {
    const params = new URLSearchParams(location.search);
    query.value = (params.get('q') || '').slice(0, 200);
    category.value = params.get('categoria') || '';
    if (category.selectedIndex < 0) category.value = '';
    if (query.value || category.value) run(false, false);
    else { ++request; results.hidden = true; clear.hidden = true; status.textContent = 'Explore o diretório abaixo ou busque em todas as páginas.'; }
  }
  form.addEventListener('submit', event => {event.preventDefault(); run(true, true);});
  category.addEventListener('change', () => run(true, false));
  clear.addEventListener('click', () => {query.value = ''; category.value = ''; run(true, false); query.focus();});
  more.addEventListener('click', () => {const first = append(); list.children[first]?.querySelector('a').focus();});
  window.addEventListener('popstate', restore);
  restore();
})();
