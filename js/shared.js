// Shared navigation/footer injector for Praia Digital static site
(function() {
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html?v=2';
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
      if (node && marker.parentNode) {
        marker.parentNode.replaceChild(node, marker);
        window.__pdShared.push(['inject-nav-ok', url]);
      } else {
        window.__pdShared.push(['inject-nav-miss', url]);
      }
      if (footer && document.body) {
        document.body.appendChild(footer);
        window.__pdShared.push(['inject-footer-ok', url]);
      }
    }).catch(function(err) {
      window.__pdShared.push(['inject-error', url, err && err.message]);
    });
  }


  // Enhance an existing static header: add a working mobile toggle if missing
  function enhanceStaticNav() {
    var header = document.querySelector('header.pd-nav');
    if (!header || header.querySelector('.pd-nav-toggle')) return;
    var menu = header.querySelector('.pd-nav-menu');
    if (!menu) return;
    if (!menu.id) menu.id = 'pd-main-menu';
    var btn = document.createElement('button');
    btn.className = 'pd-nav-toggle';
    btn.type = 'button';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', menu.id);
    btn.setAttribute('aria-label', 'Abrir menu');
    btn.textContent = '☰ Menu';
    btn.addEventListener('click', function() {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });
    header.insertBefore(btn, menu);
    // safety CSS so the mobile menu hides until toggled
    var st = document.createElement('style');
    st.textContent = '@media (max-width:980px){header.pd-nav .pd-nav-toggle{display:inline-flex}header.pd-nav .pd-nav-menu{display:none;width:100%}header.pd-nav .pd-nav-menu.open{display:flex;flex-direction:column;align-items:stretch}}';
    document.head.appendChild(st);
  }
  function boot() {
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    if (document.querySelector('header.pd-nav') || document.querySelector('nav.pd-nav')) navMarker = null;
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    if (document.querySelector('footer')) footerMarker = null;
    window.__pdShared.push(['boot', !!(navMarker || footerMarker), !!(navMarker), !!(footerMarker)]);
    enhanceStaticNav();
    if (navMarker) inject(navMarker, NAV_URL);
    if (footerMarker) inject(footerMarker, FOOTER_URL);
    setTimeout(function() {
      window.__pdShared.push(['boot-delay', !!document.querySelector('.pd-nav'), !!document.querySelector('footer')]);
    }, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
  // retry after load if needed
  window.addEventListener('load', function() {
    setTimeout(boot, 0);
  });
})();
