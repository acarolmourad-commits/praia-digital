'use strict';
const search = document.querySelector('#course-search');
if (search) {
  const cards = Array.from(document.querySelectorAll('[data-course]'));
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  search.addEventListener('input', () => {
    const query = normalize(search.value.trim());
    let count = 0;
    cards.forEach(card => { card.hidden = !normalize(card.textContent).includes(query); if (!card.hidden) count++; });
    document.querySelector('#result-count').textContent = `${count} opções encontradas`;
  });
}
