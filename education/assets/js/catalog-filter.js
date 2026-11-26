(() => {
  'use strict';
  const input = document.getElementById('kit-search');
  const clear = document.getElementById('catalog-clear');
  const count = document.getElementById('kit-count');
  const empty = document.getElementById('empty');
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  // Index the editorial content once, before copy-status messages are inserted.
  const offers = [...document.querySelectorAll('[data-kit], [data-bundle]')].map(card => ({
    card, text: normalize(card.textContent), bundle: card.hasAttribute('data-bundle')
  }));
  function filter() {
    const terms = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    let kits = 0, bundles = 0;
    for (const offer of offers) {
      offer.card.hidden = !terms.every(term => offer.text.includes(term));
      if (!offer.card.hidden) offer.bundle ? bundles++ : kits++;
    }
    count.textContent = `Resultados: ${kits} ${kits === 1 ? 'kit' : 'kits'} e ${bundles} ${bundles === 1 ? 'trilha' : 'trilhas'}.`;
    empty.hidden = kits + bundles > 0;
    clear.hidden = input.value.length === 0;
  }
  input.addEventListener('input', filter);
  clear.addEventListener('click', () => {
    input.value = '';
    filter();
    input.focus();
  });
  filter();
})();
