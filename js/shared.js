// Shared navigation/footer injector for Praia Digital static site
(function () {
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html?v=2';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html?v=2';
  window.__pdShared = window.__pdShared || [];

  function inject(marker, url) {
    if (!marker || marker.getAttribute('data-partial') === 'done') return;
    marker.setAttribute('data-partial', 'done');
    window.__pdShared.push(['inject-start', url]);
    fetch(url, { credentials: 'omit', cache: 'no-store' }).then(function (r) {
      window.__pdShared.push(['inject-fetch', url, r.status]);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }).then(function (html) {
      window.__pdShared.push(['inject-html', url, html.length]);
      var tmp = document.createElement('div');
      tmp.innerHTML = html;
      var node = tmp.querySelector('header') || tmp.querySelector('nav');
      var footer = tmp.querySelector('footer');
      if (node && marker.parentNode) {
        marker.parentNode.replaceChild(node, marker);
        window.__pdShared.push(['inject-nav-ok', url]);
        // Remove header/nav inline legado (duplicado) após injetar o menu compartilhado
        var legacy = document.querySelectorAll('header.pd-nav, body > header, body > nav:not(.pd-nav)');
        for (var i = 0; i < legacy.length; i++) {
          if (legacy[i] !== node && legacy[i].parentNode) {
            legacy[i].parentNode.removeChild(legacy[i]);
            window.__pdShared.push(['inline-nav-removed']);
          }
        }
      } else {
        window.__pdShared.push(['inject-nav-miss', url]);
      }
      if (footer && document.body) {
        document.body.appendChild(footer);
        window.__pdShared.push(['inject-footer-ok', url]);
      }
    }).catch(function (err) {
      window.__pdShared.push(['inject-error', url, err && err.message]);
    });
  }

  function removeMarker(marker, reason) {
    window.__pdShared.push(['inject-skip', reason]);
    if (marker && marker.parentNode) marker.parentNode.removeChild(marker);
  }

  function boot() {
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    window.__pdShared.push(['boot', !!(navMarker || footerMarker), !!(navMarker), !!(footerMarker)]);

    // FIX duplicate header: se a página tem um <header>/<nav> inline legado
    // (ex.: index.html), ele será removido APÓS a injeção do menu compartilhado
    // (evita ficar sem navegação se o fetch falhar).
    if (navMarker) {
      inject(navMarker, NAV_URL);
    }

    // Same guard for the footer: never append a second footer.
    var hasInlineFooter = !!document.querySelector('footer');
    if (footerMarker) {
      if (hasInlineFooter) removeMarker(footerMarker, 'inline-footer-present');
      else inject(footerMarker, FOOTER_URL);
    }

    setTimeout(function () {
      window.__pdShared.push(['boot-delay', !!document.querySelector('.pd-nav'), !!document.querySelector('footer')]);
    }, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  // retry after load if needed
  window.addEventListener('load', function () {
    setTimeout(boot, 0);
  });
})();
