// Progressive enhancement only: every reviewed item remains readable without JavaScript.
(function () {
  'use strict';
  var copy = document.getElementById('copy-rss');
  var address = document.getElementById('rss-address');
  if (copy && address) {
    copy.hidden = false;
    copy.addEventListener('click', async function () {
      var status = document.getElementById('copy-status');
      try {
        if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(address.value);
        status.textContent = 'Endereço copiado. Cole no seu leitor de RSS.';
      } catch (_) {
        address.focus();
        address.select();
        status.textContent = 'Selecione e copie o endereço acima para adicionar ao seu leitor de RSS.';
      }
    });
  }
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
  var reset = document.getElementById('filter-reset');
  if (reset) reset.addEventListener('click', function () {
    document.getElementById('filter-city').value = '';
    document.getElementById('filter-category').value = '';
    apply();
  });
  apply();
})();
