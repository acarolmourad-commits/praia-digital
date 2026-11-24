/* Progressive enhancement: the complete directory remains usable without JS. */
(function () {
  'use strict';
  const form = document.getElementById('catalog-search-form');
  const catalog = document.getElementById('catalogo-apps');
  if (!form || !catalog) return;
  const query = document.getElementById('app-query');
  const goal = document.getElementById('app-goal');
  const clear = document.getElementById('app-clear');
  const status = document.getElementById('app-results');
  const empty = document.getElementById('app-empty');
  const printSelection = document.getElementById('app-print');
  const shareLink = document.getElementById('app-share-link');
  const copySelection = document.getElementById('app-copy');
  const copyStatus = document.getElementById('app-copy-status');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR').replace(/[^a-z0-9]+/g, ' ').trim();
  const groups = Array.from(catalog.querySelectorAll('.pd-catalog-group')).map(section => ({
    section,
    id: section.getAttribute('aria-labelledby'),
    cards: Array.from(section.querySelectorAll('a.card')).map(card => ({
      card,
      text: normalize(card.textContent + ' ' + card.getAttribute('href') + ' ' + section.querySelector('h2').textContent)
    }))
  }));
  const total = groups.reduce((sum, group) => sum + group.cards.length, 0);
  // Read only the catalog filters. Keep the canonical page and all app URLs unchanged.
  const params = new URLSearchParams(window.location.search);
  if (params.has('busca')) query.value = params.get('busca').slice(0, 100);
  if (params.has('objetivo')) {
    const requested = params.get('objetivo');
    goal.value = groups.some(group => group.id === requested) ? requested : '';
  }
  function selectionUrl() {
    const url = new URL('/apps/', window.location.origin);
    const term = query.value.trim().slice(0, 100);
    if (term) url.searchParams.set('busca', term);
    if (goal.value) url.searchParams.set('objetivo', goal.value);
    url.hash = 'buscar-apps';
    return url.href;
  }
  function filter() {
    const terms = normalize(query.value).split(' ').filter(Boolean);
    let count = 0;
    for (const group of groups) {
      let visible = 0;
      for (const item of group.cards) {
        const match = (!goal.value || group.id === goal.value) && terms.every(term => item.text.includes(term));
        item.card.hidden = !match;
        if (match) visible++;
      }
      group.section.hidden = visible === 0;
      count += visible;
    }
    status.textContent = count === 1 ? '1 de ' + total + ' aplicativos encontrado.' : count + ' de ' + total + ' aplicativos encontrados.';
    empty.hidden = count !== 0;
    if (printSelection) printSelection.disabled = count === 0;
    if (shareLink) shareLink.value = selectionUrl();
    if (copyStatus) copyStatus.textContent = '';
  }
  function reset() {
    query.value = '';
    goal.value = '';
    filter();
  }
  if (printSelection) printSelection.addEventListener('click', () => window.print());
  if (copySelection && shareLink && copyStatus) copySelection.addEventListener('click', async () => {
    const value = shareLink.value;
    try {
      await navigator.clipboard.writeText(value);
      if (shareLink.value === value) copyStatus.textContent = 'Link copiado. Cole na conversa ou guarde para depois.';
    } catch (_) {
      shareLink.focus();
      shareLink.select();
      copyStatus.textContent = 'Selecione e copie o endereço no campo Link desta seleção.';
    }
  });
  query.addEventListener('input', filter);
  goal.addEventListener('change', filter);
  form.addEventListener('submit', event => event.preventDefault());
  clear.addEventListener('click', () => { reset(); query.focus(); });
  const objectives = document.getElementById('objetivos-apps');
  let handledHash = window.location.hash;
  if (objectives) objectives.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#grupo-"]');
    if (link) {
      reset();
      handledHash = link.getAttribute('href');
    }
  });
  window.addEventListener('hashchange', () => {
    // The click already restored the target; do not erase a subsequent query.
    if (window.location.hash === handledHash) return;
    handledHash = window.location.hash;
    if (groups.some(group => '#' + group.id === window.location.hash)) reset();
  });
  // Browsers may restore form values when returning from an app.
  window.addEventListener('pageshow', filter);
  form.hidden = false;
  filter();
})();
