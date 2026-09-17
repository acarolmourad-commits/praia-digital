// Praia Digital — Shared Header/Footer Injector v2.0
// Single-source navigation injection with no boot duplication
(function() {
  'use strict';

  var HEADER_URL = 'https://praia.digital/partials/header.html?v=2.0';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html?v=2.0';
  var injected = false;

  window.__pdShared = window.__pdShared || [];

  function inject(marker, url, injectFn) {
    if (!marker) return;
    if (marker.getAttribute('data-partial') === 'done') return;
    marker.setAttribute('data-partial', 'done');
    window.__pdShared.push(['inject-start', url]);
    fetch(url, { credentials: 'omit', cache: 'no-store' })
      .then(function(r) {
        window.__pdShared.push(['inject-fetch', url, r.status]);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.text();
      })
      .then(function(html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        injectFn(tmp);
      })
      .catch(function(err) {
        window.__pdShared.push(['inject-error', url, err && err.message]);
      });
  }

  function boot() {
    if (injected) return; // hard guard — run ONCE
    injected = true;
    injectAppsSection();

    var navMarker  = document.querySelector('meta[name="pd-shared-nav"]');
    var footMarker = document.querySelector('meta[name="pd-shared-footer"]');
    window.__pdShared.push(['boot', !!(navMarker || footMarker), !!(navMarker), !!(footMarker)]);

    if (navMarker) {
      inject(navMarker, HEADER_URL, function(tmp) {
        var header = tmp.querySelector('header');
        if (header && navMarker.parentNode) {
          navMarker.parentNode.replaceChild(header, navMarker);
          window.__pdShared.push(['inject-header-ok']);
          initDropdowns();
          // Remove headers/nav inline legados (ex.: index.html) para evitar menu duplicado.
          // Só roda DEPOIS da injeção bem-sucedida, para nunca deixar a página sem navegação.
          var legacy = document.querySelectorAll('header.pd-nav, body > header:not(.pd-header), body > nav.pd-nav');
          for (var i = 0; i < legacy.length; i++) {
            if (legacy[i] !== header && legacy[i].parentNode) {
              legacy[i].parentNode.removeChild(legacy[i]);
              window.__pdShared.push(['legacy-nav-removed']);
            }
          }
        } else {
          window.__pdShared.push(['inject-header-miss']);
        }
      });
    }
    if (footMarker) {
      inject(footMarker, FOOTER_URL, function(tmp) {
        var footer = tmp.querySelector('footer');
        if (footer && footMarker.parentNode) {
          footMarker.parentNode.replaceChild(footer, footMarker);
          window.__pdShared.push(['inject-footer-ok']);
        }
      });
    }
  }

  // Dropdown interaction: hover on desktop, click on mobile/tablet
  function initDropdowns() {
    var groups = document.querySelectorAll('.pd-nav-group[data-dropdown]');
    groups.forEach(function(group) {
      var label  = group.querySelector('.pd-nav-label');
      var submenu = group.querySelector('.pd-nav-submenu');
      if (!label || !submenu) return;

      // Desktop: hover
      group.addEventListener('mouseenter', function() {
        if (window.innerWidth > 768) {
          submenu.classList.add('open');
          label.setAttribute('aria-expanded', 'true');
        }
      });
      group.addEventListener('mouseleave', function() {
        if (window.innerWidth > 768) {
          submenu.classList.remove('open');
          label.setAttribute('aria-expanded', 'false');
        }
      });

      // Mobile: click toggle
      label.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          var isOpen = submenu.classList.toggle('open');
          label.setAttribute('aria-expanded', isOpen);
        }
      });
    });

    // Mobile menu toggle (hamburger)
    var toggle = document.querySelector('.pd-nav-toggle');
    var menu   = document.querySelector('.pd-nav-menu');
    if (toggle && menu) {
      // Use onclick already set inline; also ensure aria-expanded sync
      menu.addEventListener('transitionend', function() {
        // optional: close submenus when menu collapses
      });
    }

    // Close mobile menu / dropdowns when clicking outside
    document.addEventListener('click', function(e) {
      if (window.innerWidth > 768) return;
      var isMenuClick = e.target.closest('.pd-nav-menu');
      if (!isMenuClick && menu && menu.classList.contains('open')) {
        menu.classList.remove('open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }


  // Homepage: inject Apps section (from partials/apps-section.html) after #ferramentas
  function injectAppsSection() {
    var path = window.location.pathname;
    var isHome = path === '/' || path === '/index.html' || path === '';
    if (!isHome) return;
    if (document.getElementById('apps')) return;
    var anchor = document.getElementById('ferramentas') || document.querySelector('footer');
    if (!anchor) return;
    fetch('https://praia.digital/partials/apps-section.html?v=1.0', { credentials: 'omit', cache: 'no-store' })
      .then(function(r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .then(function(html) {
        var tmp = document.createElement('div');
        tmp.innerHTML = html;
        var section = tmp.querySelector('section');
        if (!section) return;
        if (anchor.nextSibling) {
          anchor.parentNode.insertBefore(section, anchor.nextSibling);
        } else {
          anchor.parentNode.appendChild(section);
        }
        window.__pdShared.push(['inject-apps-ok']);
      })
      .catch(function(err) {
        window.__pdShared.push(['inject-apps-error', err && err.message]);
      });
  }

  // Boot once
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
