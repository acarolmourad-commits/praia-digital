/**
 * Motor B — Instrumentação local do site (sem GA4 externo).
 *
 * Intercepta eventos relevantes e registra em localStorage.
 * Nenhum dado é enviado a servidores externos.
 * O Motor B consome estes eventos via leitura local.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'motor_b_events_v1';
  const MAX_EVENTS = 500;

  function nowIso() {
    return new Date().toISOString();
  }

  function readEvents() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }

  function writeEvents(events) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(events.slice(-MAX_EVENTS)));
    } catch (e) {
      // quota exceeded — do not block user flow
    }
  }

  function pushEvent(event) {
    const events = readEvents();
    events.push(Object.assign({ timestamp: nowIso() }, event));
    writeEvents(events);
  }

  // Páginas onde o Motor B deve escutar eventos
  const TARGET_PATHS = [
    '/anfitrioes/diagnosticos-anfitrioes.html',
    '/assets/cadastro-imovel-publico.html',
    '/assets/ferramenta-gerador-leads-litoral.html',
    '/assets/captacao-leads-imobiliaria-litoral-ia.html',
    '/blog/diagnostico-anuncio-temporada-litoral-2026.html',
  ];

  if (!TARGET_PATHS.some(p => location.pathname === p || location.pathname.endsWith(p))) {
    return; // fora das páginas-alvo
  }

  // Page view já conta como evento de entrada
  pushEvent({
    type: 'page_view',
    path: location.pathname,
    referrer: document.referrer || '',
  });

  // CTAs de WhatsApp
  document.addEventListener('click', function (e) {
    const target = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
    if (!target) return;
    pushEvent({
      type: 'whatsapp_click',
      path: location.pathname,
      href: target.getAttribute('href') || '',
    });
  });

  // Formulários relevantes
  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (!form || !form.id) return;
    const formId = form.id.toLowerCase();
    if (!/cadastro|diagnostico|imovel|lead|gerador/.test(formId)) return;

    const fields = {};
    try {
      Array.from(form.elements).forEach(function (el) {
        if (!el.name) return;
        fields[el.name] = (el.value || '').trim().slice(0, 200);
      });
    } catch (err) {
      fields['_error'] = 'unreadable_form';
    }

    pushEvent({
      type: 'form_submit',
      path: location.pathname,
      formId: form.id,
      fields: fields,
    });
  });

  // Botões com atributo data-motor-b-event
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-motor-b-event]');
    if (!btn) return;
    pushEvent({
      type: 'custom_click',
      path: location.pathname,
      eventName: btn.getAttribute('data-motor-b-event') || '',
      label: btn.textContent ? btn.textContent.trim().slice(0, 100) : '',
    });
  });
})();
