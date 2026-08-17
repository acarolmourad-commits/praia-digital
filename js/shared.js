// Shared navigation/footer injector for Praia Digital static site
(function() {
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html';

  function inject(marker, url) {
    if (!marker || marker.getAttribute('data-partial') === 'done') return;
    marker.setAttribute('data-partial', 'done');
    fetch(url, { credentials: 'omit' }).then(function(r) { return r.text(); }).then(function(html) {
      var tmp = document.createElement('div');
      tmp.innerHTML = html;
      var node = tmp.querySelector('header') || tmp.querySelector('nav');
      var footer = tmp.querySelector('footer');
      if (node && marker.parentNode) {
        marker.parentNode.replaceChild(node, marker);
      }
      if (footer && document.body) {
        document.body.appendChild(footer);
      }
    }).catch(function() {});
  }

  function boot() {
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    if (navMarker) inject(navMarker, NAV_URL);
    if (footerMarker) inject(footerMarker, FOOTER_URL);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
