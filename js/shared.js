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
    