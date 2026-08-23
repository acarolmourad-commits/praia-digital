/* ============================================================
   Praia Digital — Push Notifications + Share Widgets
   ============================================================ */
window.PD_ENGAGEMENT = window.PD_ENGAGEMENT || {};

PD_ENGAGEMENT.initPush = function ({ serviceWorkerPath = '/sw.js', promptDelayMs = 3000 } = {}) {
  if (!('serviceWorker' in navigator)) return;

  navigator.serviceWorker.register(serviceWorkerPath, { scope: '/' }).catch(() => {});

  setTimeout(() => {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'granted') return;
    if (Notification.permission === 'denied') return;

    const prompt = document.createElement('div');
    prompt.className = 'pd-push-prompt';
    prompt.setAttribute('data-pd-push', '');
    prompt.innerHTML = `
      <div class="pd-push-prompt__inner">
        <p class="pd-push-prompt__title">Receba alertas de oportunidades no litoral</p>
        <p class="pd-push-prompt__text">Notificações somente quando houver conteúdo novo ou queda de estoque.</p>
        <div class="pd-push-prompt__actions">
          <button class="pd-push-prompt__button" data-action="allow">Permitir</button>
          <button class="pd-push-prompt__button pd-push-prompt__button--secondary" data-action="later">Agora não</button>
        </div>
      </div>
    `;
    document.body.appendChild(prompt);

    prompt.querySelector('[data-action="allow"]').addEventListener('click', async () => {
      const perm = await Notification.requestPermission();
      prompt.classList.add('is-closed');
    });
    prompt.querySelector('[data-action="later"]').addEventListener('click', () => {
      prompt.classList.add('is-closed');
    });
  }, promptDelayMs);
};

PD_ENGAGEMENT.initGPTTelemetry = function () {
  if (!window.googletag) return;
  googletag.pubads().addEventListener('slotRenderEnded', (event) => {
    if (!window.gtag) return;
    try {
      gtag('event', 'ad_render', {
        adUnitPath: event.slot.getAdUnitPath(),
        adWidth: event.size?.[0] || null,
        adHeight: event.size?.[1] || null,
        isEmpty: event.isEmpty,
        sourceAgnosticCreativeId: event.sourceAgnosticCreativeId || null
      });
    } catch (e) { /* no-op */ }
  });
};

PD_ENGAGEMENT.initShare = function () {
  const urls = [
    'https://wa.me/?text=' + encodeURIComponent(location.href),
    'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(location.href),
    'https://twitter.com/intent/tweet?url=' + encodeURIComponent(location.href)
  ];
  const labels = ['WhatsApp', 'Facebook', 'Twitter'];
  const container = document.createElement('div');
  container.className = 'pd-share';
  container.setAttribute('data-pd-share', '');
  container.innerHTML = '<p class="pd-share__title">Compartilhar</p>';
  const row = document.createElement('div');
  row.className = 'pd-share__row';
  for (let i = 0; i < urls.length; i++) {
    const a = document.createElement('a');
    a.href = urls[i];
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = labels[i];
    row.appendChild(a);
  }
  container.appendChild(row);
  document.body.appendChild(container);
};

PD_ENGAGEMENT.initStickyOffset = function ({ offsetPx = 60 } = {}) {
  const sticky = document.querySelector('.pd-sticky-ad');
  const whatsapp = document.querySelector('.pd-whatsapp-float');
  if (!sticky || !whatsapp) return;

  const apply = () => {
    const hidden = sticky.classList.contains('is-closed') || getComputedStyle(sticky).display === 'none';
    if (!hidden) {
      whatsapp.style.bottom = `calc(16px + ${offsetPx}px)`;
      document.body.classList.add('has-sticky-ad');
    } else {
      whatsapp.style.bottom = '';
      document.body.classList.remove('has-sticky-ad');
    }
  };

  apply();
  const observer = new MutationObserver(apply);
  observer.observe(sticky, { attributes: true, attributeFilter: ['class', 'style'] });
  window.addEventListener('resize', apply);
};
