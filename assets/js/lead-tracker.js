/* Praia Digital — Lead Tracker
   Padroniza eventos GA4 para CTAs de captação e enriquecimento de parâmetros UTM.
*/
window.PD_LEAD_TRACKER = window.PD_LEAD_TRACKER || {};
PD_LEAD_TRACKER.init = function () {
  document.addEventListener('click', function (e) {
    var target = e.target.closest('a[data-event], button[data-event]');
    if (!target) return;
    var eventName = target.getAttribute('data-event') || 'lead_click';
    var category = target.getAttribute('data-event-category') || 'cta';
    var label = target.getAttribute('data-event-label') || target.textContent.trim().slice(0, 40);
    var href = target.getAttribute('href') || '';
    var params = {
      event_category: category,
      event_label: label,
      page_path: location.pathname,
      destination_url: href,
      link_text: label
    };
    try { if (window.gtag) gtag('event', eventName, params); } catch (err) { /* no-op */ }
  });
};
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function () { PD_LEAD_TRACKER.init(); });
} else {
  PD_LEAD_TRACKER.init();
}
