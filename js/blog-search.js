(function () {
  'use strict';

  function normalize(value) {
    return value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR');
  }

  function init() {
    var list = document.getElementById('pdBlogList');
    var search = document.getElementById('pdBlogSearch');
    var count = document.getElementById('pdBlogCount');
    var clear = document.getElementById('pdBlogClear');
    var empty = document.getElementById('pdBlogEmpty');
    if (!list || !search || !count || !clear || !empty) return;
    var seen = new Set();
    var items = [];

    document.querySelectorAll('main a.btn[href], main section[aria-labelledby] li a[href]').forEach(function (anchor) {
      var url = new URL(anchor.getAttribute('href'), document.baseURI);
      // Keep discovery focused on editorial destinations, not service CTAs.
      if (url.origin !== window.location.origin || !(/^\/(blog|guias|primeiro-imovel-litoral-sp-2026)\//.test(url.pathname) || /^\/[^/]+\.html$/.test(url.pathname)) || url.pathname === '/servicos.html') return;
      if (seen.has(url.pathname)) return;
      seen.add(url.pathname);
      var label = anchor.textContent.trim();
      var card = anchor.closest('article');
      var heading = card && (card.querySelector('h3') || (label === 'Abrir guia' && card.querySelector('h2')));
      // Introductory cards use action labels; prefer their descriptive title.
      if (heading) label = heading.textContent.trim();
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = url.pathname;
      a.textContent = label;
      li.appendChild(a);
      list.appendChild(li);
      items.push({ element: li, text: normalize(label + ' ' + decodeURI(url.pathname).replace(/[-/]/g, ' ')) });
    });

    function render() {
      var query = normalize(search.value.trim());
      var terms = query.split(/\s+/).filter(Boolean);
      var shown = 0;
      items.forEach(function (item) {
        item.element.hidden = !terms.every(function (term) { return item.text.indexOf(term) !== -1; });
        if (!item.element.hidden) shown++;
      });
      count.textContent = shown + (shown === 1 ? ' guia encontrado' : ' guias encontrados') + (query ? ' para “' + search.value.trim() + '”.' : ' nesta seleção.');
      empty.hidden = shown !== 0;
    }
    search.addEventListener('input', render);
    clear.addEventListener('click', function () {
      search.value = '';
      render();
      search.focus();
    });
    render();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
