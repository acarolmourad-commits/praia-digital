/* Progressive enhancement: the HTML is the published catalog and works without JS. */
(() => {
  const tools = document.getElementById('guide-tools');
  if (!tools) return;
  const search = document.getElementById('guide-search');
  const city = document.getElementById('guide-city');
  const cards = [...document.querySelectorAll('.city-card')];
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const result = document.getElementById('guide-results');
  const empty = document.getElementById('guide-empty');
  function filter() {
    const terms = normalize(search.value).split(/\s+/).filter(Boolean);
    let guides = 0, articles = 0, cities = 0;
    for (const card of cards) {
      const inCity = !city.value || city.value === card.id;
      const matches = text => inCity && terms.every(term => normalize(`${card.dataset.city} ${text}`).includes(term));
      let count = 0, related = 0;
      card.querySelectorAll('.neighborhood-links li').forEach(item => {
        item.hidden = !matches(`${item.textContent} guia de bairro`);
        if (!item.hidden) count++;
      });
      card.querySelectorAll('.related-entry').forEach(item => {
        item.hidden = !matches(`${item.textContent} ${item.dataset.keywords || ''}`);
        if (!item.hidden) related++;
      });
      card.hidden = count + related === 0;
      card.querySelector('details').hidden = count === 0;
      card.querySelector('.city-count').textContent = `${count} de ${card.querySelectorAll('.neighborhood-links li').length} guias`;
      if (terms.length || city.value) card.querySelector('details').open = true;
      guides += count; articles += related; if (!card.hidden) cities++;
    }
    result.textContent = `${guides} guias de bairro e ${articles} matérias relacionadas em ${cities} cidades.`;
    empty.hidden = guides + articles > 0;
  }
  tools.hidden = false;
  search.addEventListener('input', filter);
  city.addEventListener('change', filter);
  document.getElementById('guide-clear').addEventListener('click', () => {
    search.value = ''; city.value = ''; filter(); search.focus();
  });
  document.getElementById('guide-expand').addEventListener('click', () => cards.filter(c => !c.hidden).forEach(c => c.querySelector('details').open = true));
  document.getElementById('guide-collapse').addEventListener('click', () => cards.filter(c => !c.hidden).forEach(c => c.querySelector('details').open = false));
  function revealCity() {
    const id = location.hash.slice(1);
    const card = cards.find(c => c.id === id);
    if (!card) return;
    search.value = ''; city.value = ''; filter(); card.querySelector('details').open = true;
    card.scrollIntoView({block: 'start'});
  }
  document.querySelector('.city-nav').addEventListener('click', event => {
    const link = event.target.closest('a');
    if (link) { search.value = ''; city.value = ''; filter(); const card = cards.find(c => `#${c.id}` === link.getAttribute('href')); if (card) card.querySelector('details').open = true; }
  });
  window.addEventListener('hashchange', revealCity);
  filter(); revealCity();
})();
