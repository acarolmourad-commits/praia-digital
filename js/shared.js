// Shared navigation/footer injector for Praia Digital static site
(function() {
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html?v=3';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html?v=2';
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
      // Skip nav injection when the page already renders its own nav/header (avoids duplicated menus)
      var existingNav = document.querySelector('header.pd-nav, nav.pd-nav');
      if (node && marker.parentNode && !existingNav) {
        marker.parentNode.replaceChild(node, marker);
        window.__pdShared.push(['inject-nav-ok', url]);
      } else {
        window.__pdShared.push([existingNav ? 'inject-nav-skip-existing' : 'inject-nav-miss', url]);
      }
      // Skip footer injection when a footer is already present
      if (footer && document.body && !document.querySelector('footer')) {
        document.body.appendChild(footer);
        window.__pdShared.push(['inject-footer-ok', url]);
      }
    }).catch(function(err) {
      window.__pdShared.push(['inject-error', url, err && err.message]);
    });
  }

  // If the page has a hardcoded nav without a mobile toggle button, add one
  function ensureMobileToggle() {
    var menu = document.querySelector('.pd-nav-menu');
    if (!menu || document.querySelector('.pd-nav-toggle')) return;
    if (!menu.id) menu.id = 'pd-nav-menu';
    var btn = document.createElement('button');
    btn.className = 'pd-nav-toggle';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', menu.id);
    btn.setAttribute('aria-label', 'Abrir menu');
    btn.textContent = '☰ Menu';
    btn.addEventListener('click', function() {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.parentNode.insertBefore(btn, menu);
    window.__pdShared.push(['mobile-toggle-added']);
  }

  function boot() {
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    window.__pdShared.push(['boot', !!(navMarker || footerMarker), !!(navMarker), !!(footerMarker)]);
    if (navMarker) inject(navMarker, NAV_URL);
    if (footerMarker) inject(footerMarker, FOOTER_URL);
    ensureMobileToggle();
    setTimeout(function() {
      window.__pdShared.push(['boot-delay', !!document.querySelector('.pd-nav'), !!document.querySelector('footer')]);
    }, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  window.addEventListener('load', function() {
    setTimeout(boot, 0);
  });
})();
