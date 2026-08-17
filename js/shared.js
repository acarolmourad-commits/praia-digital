// Shared navigation/footer injector for Praia Digital static site
(function(){
  'use strict';
  var NAV_URL = 'https://praia.digital/partials/nav-render.html';
  var FOOTER_URL = 'https://praia.digital/partials/footer.html';

  function inject(el, url){
    if(!el) return;
    var marker = el.getAttribute('data-partial');
    if(marker === 'done') return;
    el.setAttribute('data-partial', 'done');
    fetch(url, {credentials:'omit'}).then(function(r){ return r.text(); }).then(function(html){
      var tmp = document.createElement('div');
      tmp.innerHTML = html;
      var nav = tmp.querySelector('nav');
      var header = tmp.querySelector('header');
      var footer = tmp.querySelector('footer');
      if(nav || header){
        var node = header || nav;
        el.parentNode.insertBefore(node, el);
      }
      if(footer){
        var body = document.body;
        body.appendChild(footer);
      }
    }).catch(function(){});
  }

  function boot(){
    var navMarker = document.querySelector('meta[name="pd-shared-nav"]');
    var footerMarker = document.querySelector('meta[name="pd-shared-footer"]');
    if(navMarker){
      inject(navMarker, NAV_URL);
    }
    if(footerMarker){
      inject(footerMarker, FOOTER_URL);
    }
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
