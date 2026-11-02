// Progressive enhancement only: every reviewed item remains readable without JavaScript.
(function () {
  'use strict';
  var filters = document.querySelector('.bulletin-filters');
  var items = Array.from(document.querySelectorAll('.news-item'));
  if (!filters || !items.length) return;
  filters.hidden = false;
  function apply() {
    var city = document.getElementById('filter-city').value;
    var category = document.getElementById('filter-category').value;
    var count = 0;
    items.forEach(function (item) {
      item.hidden = !!((city && item.dataset.city !== city) || (category && item.dataset.category !== category));
      if (!item.hidden) count += 1;
    });
    document.getElementById('filter-status').textContent = count + ' de ' + items.length + ' notícia(s) nesta edição';
    document.getElementById('filter-empty').hidden = count !== 0;
  }
  filters.addEventListener('change', apply);
  apply();
})();
