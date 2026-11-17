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
  }
  function reset() {
    query.value = '';
    goal.value = '';
    filter();
  }
  query.addEventListener('input', filter);
  goal.addEventListener('change', filter);
  form.addEventListener('submit', event => event.preventDefault());
  clear.addEventListener('click', () => { reset(); query.focus(); });
  const objectives = document.getElementById('objetivos-apps');
  if (objectives) objectives.addEventListener('click', event => {
    if (event.target.closest('a[href^="#grupo-"]')) reset();
  });
  window.addEventListener('hashchange', () => {
    if (groups.some(group => '#' + group.id === window.location.hash)) reset();
  });
  // Browsers may restore form values when returning from an app.
  window.addEventListener('pageshow', filter);
  form.hidden = false;
  filter();
})();
