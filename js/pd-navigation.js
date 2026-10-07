// Accessible homepage-style navigation. No listing or form side effects.
(function () {
  'use strict';
  function init(header) {
    if (header.dataset.pdNavReady) return;
    header.dataset.pdNavReady = 'true';
    var toggle = header.querySelector('.pd-site-toggle');
    var menu = header.querySelector('.pd-site-menu');
    var groups = header.querySelectorAll('.pd-site-group');
    if (!toggle || !menu) return;
    function setGroup(group, open) {
      group.classList.toggle('is-open', open);
      group.querySelector('button').setAttribute('aria-expanded', String(open));
    }
    function closeGroups() { groups.forEach(function (g) { setGroup(g, false); }); }
    function setMenu(open) {
      header.classList.toggle('is-menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fechar menu de navegação' : 'Abrir menu de navegação');
      if (!open) closeGroups();
    }
    toggle.addEventListener('click', function () { setMenu(!header.classList.contains('is-menu-open')); });
    groups.forEach(function (group) {
      var button = group.querySelector('button');
      button.addEventListener('click', function () {
        var open = !group.classList.contains('is-open');
        closeGroups(); setGroup(group, open);
      });
      group.addEventListener('mouseenter', function () {
        if (window.innerWidth > 1080) setGroup(group, true);
      });
      group.addEventListener('mouseleave', function () {
        if (window.innerWidth > 1080 && !group.contains(document.activeElement)) setGroup(group, false);
      });
      group.addEventListener('focusin', function () {
        if (window.innerWidth > 1080) setGroup(group, true);
      });
      group.addEventListener('focusout', function (event) {
        if (!group.contains(event.relatedTarget)) setGroup(group, false);
      });
    });
    document.addEventListener('click', function (event) {
      if (!header.contains(event.target)) { setMenu(false); closeGroups(); }
    });
    header.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') return;
      var group = event.target.closest('.pd-site-group');
      if (group && group.classList.contains('is-open')) {
        group.querySelector('button').focus(); setGroup(group, false);
      } else { setMenu(false); toggle.focus(); }
    });
    menu.addEventListener('click', function (event) { if (event.target.closest('a')) setMenu(false); });
    window.addEventListener('resize', function () { setMenu(false); });
  }
  function boot() { document.querySelectorAll('.pd-site-header').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
