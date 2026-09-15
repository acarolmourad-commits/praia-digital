// Shared navigation/footer injector for Praia Digital static site
(function() {
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html?v=3';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html?v=3';
  window.__pdShared = window.__pdShared || [];

  function inject(marker, url) {
    if (!marker || marker.getAttribute('data-partial') === 'done') return;
    marker.setAttribute('data-partial', 'done');
    window.__pdShared.push(['inject-start', url]);
    fetch(url, { credentials: 'omit', cache: 'no-store' }).then(function(r) {
      window.__pdShared.push(['inject-fetch', url, r.status]);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }).then(function(html) {
      window.__pdShared.push(['inject-html', url, html.length]);
      var tmp = document.createElement('div');
      tmp.innerHTML = html;
      var node = tmp.querySelector('header') || tmp.querySelector('nav');
      var footer = tmp.querySelector('footer');

      // Evita duplicar navegação: se a página já tem header/nav próprio, não injeta.
      var alreadyHasNav = document.querySelector('header, nav.pd-nav');
      if (node && marker.parentNode && !alreadyHasNav) {
        marker.parentNode.replaceChild(node, marker);
        window.__pdShared.push(['inject-nav-ok', url]);
      } else {
        if (marker.parentNode) marker.parentNode.removeChild(marker);
        window.__pdShared.push(['inject-nav-skip', url, !!alreadyHasNav]);
      }

      // Evita duplicar rodapé.
      var alreadyHasFooter = document.querySelector('footer');
      if (footer && document.body && !alreadyHasFooter) {
        document.body.appendChild(footer);
        window.__pdShared.push(['inject-footer-ok', url]);
      } else {
        window.__pdShared.push(['inject-footer-skip', url, !!alreadyHasFooter]);
      }
    }).catch(function(err) {
      window.__pdShared.push(['inject-error', url, err && err.message]);
    });
  }

  // Acessibilidade: aria-expanded + fecha menu com Esc ou clique fora
  function enhanceNavToggle() {
    var toggle = document.querySelector('.pd-nav-toggle');
    var menu = document.getElementById('pd-nav-menu');
    if (!toggle || !menu) return;
    toggle.addEventListener('click', function() {
      toggle.setAttribute('aria-expanded', menu.classList.contains('open') ? 'true' : 'false');
    });
    document.addEventListener('click', function(e) {
      if (menu.classList.contains('open') && !menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  function boot() {
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    window.__pdShared.push(['boot', !!(navMarker || footerMarker), !!(navMarker), !!(footerMarker)]);
    if (navMarker) inject(navMarker, NAV_URL);
    if (footerMarker) inject(footerMarker, FOOTER_URL);
    enhanceNavToggle();
    setTimeout(function() {
      window.__pdShared.push(['boot-delay', !!document.querySelector('.pd-nav'), !!document.querySelector('footer')]);
    }, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
