/* ============================================================
   Praia Digital — Advanced Ad Monetization
   - First-party key-values
   - Smart attention-based refresh
   - Mobile sticky anchor
   ============================================================ */

window.PD_ADS = window.PD_ADS || {};

/* ============================================================
   1. Context detection for first-party targeting
   ============================================================ */
PD_ADS.detectPageContext = function () {
  const path = (location.pathname || '').toLowerCase();
  const segments = path.split('/').filter(Boolean);

  const bairros = [
    'santos','guaruja','sao-vicente','praia-grande','bertioga',
    'ubatuba','ilhabela','mongagua','itanhaem','peruibe','caraguatatuba'
  ];
  const categoria = segments.includes('education') ? 'educacional'
    : /relatorio|mercado|valorizacao|yield|roi/.test(path) ? 'relatorio'
    : segments.includes('bairros') ? 'listagem_bairros'
    : 'editorial';

  const bairro = bairros.find((b) => path.includes(b)) || 'geral';

  const dispositivo = /mobile|android|iphone|ipad|iemobile|blackberry|opera mini/i.test(navigator.userAgent) ? 'mobile' : 'desktop';

  return { bairro, categoria, dispositivo };
};

/* ============================================================
   2. GPT init with lazy load + key-values
   ============================================================ */
PD_ADS.initGPT = function (adUnitPath, targeting) {
  if (!window.googletag) return null;

  const slot = googletag
    .defineSlot(adUnitPath, targeting.sizes || [[300, 250], [336, 280], [320, 100]], targeting.div)
    .addService(googletag.pubads());

  const ctx = PD_ADS.detectPageContext();

  // page-level first-party targeting
  googletag.pubads().setTargeting('bairro', ctx.bairro);
  googletag.pubads().setTargeting('categoria', ctx.categoria);
  googletag.pubads().setTargeting('dispositivo', ctx.dispositivo);

  // slot-level overrides
  if (targeting.keyValues) {
    Object.entries(targeting.keyValues).forEach(([k, v]) => slot.setTargeting(k, v));
  }

  googletag.pubads().enableLazyLoad({
    fetchMarginPercent: 600,
    renderMarginPercent: 200,
    mobileScaling: 2.0,
  });

  return slot;
};

/* ============================================================
   3. DAI: in-article / in-feed
   ============================================================ */
PD_ADS.injectInArticle = function ({
  articleSelector = 'article',
  paragraphSelector = 'p',
  every = 4,
} = {}) {
  const article = document.querySelector(articleSelector);
  if (!article) return [];

  const paragraphs = Array.from(article.querySelectorAll(paragraphSelector));
  const inserted = [];

  for (let i = every; i < paragraphs.length; i += every) {
    const wrapper = document.createElement('div');
    wrapper.className = 'pd-ad pd-ad--in-article';
    wrapper.setAttribute('data-pd-ad', 'in-article');
    wrapper.innerHTML = '<div class="pd-ad__placeholder">Conteúdo patrocinado</div>';

    const target = paragraphs[i - 1];
    if (target && target.parentNode) {
      target.parentNode.insertBefore(wrapper, target.nextSibling);
      inserted.push(wrapper);
    }
  }

  return inserted;
};

PD_ADS.injectInFeed = function ({
  listSelector = '.grid',
  itemSelector = '.card, article, li',
  every = 5,
} = {}) {
  const list = document.querySelector(listSelector);
  if (!list) return [];

  const items = Array.from(list.querySelectorAll(itemSelector));
  const inserted = [];

  for (let i = every; i < items.length; i += every) {
    const wrapper = document.createElement('div');
    wrapper.className = 'pd-ad pd-ad--in-feed';
    wrapper.setAttribute('data-pd-ad', 'in-feed');
    wrapper.innerHTML = '<div class="pd-ad__placeholder">Anúncio</div>';

    const target = items[i - 1];
    if (target && target.parentNode) {
      target.parentNode.insertBefore(wrapper, target.nextSibling);
      inserted.push(wrapper);
    }
  }

  return inserted;
};

/* ============================================================
   4. Smart refresh: time-based + visibility/viewport gated
   ============================================================ */
PD_ADS.scheduleSmartRefresh = function ({ intervalMs = 30000, maxRefreshes = 3 } = {}) {
  if (!window.googletag || !window.googletag.pubads) return;

  let refreshCount = 0;
  let timer = null;

  const visibleSlots = () => {
    if (!window.googletag || !window.googletag.pubads) return [];
    const all = window.googletag.pubads().getSlots();
    return all.filter((slot) => {
      const el = document.getElementById(slot.getSlotElementId());
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      return rect.top < window.innerHeight && rect.bottom > 0;
    });
  };

  const tryRefresh = () => {
    if (document.hidden) return;
    if (refreshCount >= maxRefreshes) return;

    const slots = visibleSlots();
    if (!slots.length) return;

    window.googletag.pubads().refresh(slots);
    refreshCount += 1;
  };

  const start = () => {
    if (timer) return;
    timer = setInterval(tryRefresh, intervalMs);
  };

  const stop = () => {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  };

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop(); else start();
  });

  start();
};

/* ============================================================
   5. Mobile sticky anchor ad
   ============================================================ */
PD_ADS.initStickyAnchorMobile = function (adUnitPath, sizes = [[320, 50], [320, 100]]) {
  if (!window.googletag) return null;
  if (!/mobile|android|iphone|ipad|iemobile|blackberry|opera mini/i.test(navigator.userAgent)) return null;

  const container = document.createElement('div');
  container.className = 'pd-sticky-ad';
  container.setAttribute('data-pd-ad', 'sticky-anchor');
  container.innerHTML = `
    <div class="pd-sticky-ad__inner">
      <div id="pd-sticky-ad-slot" class="pd-ad pd-ad--sticky"></div>
      <button class="pd-sticky-ad__close" aria-label="Fechar anúncio">×</button>
    </div>
  `;
  document.body.appendChild(container);

  const slot = googletag
    .defineSlot(adUnitPath, sizes, 'pd-sticky-ad-slot')
    .addService(googletag.pubads());

  const ctx = PD_ADS.detectPageContext();
  googletag.pubads().setTargeting('bairro', ctx.bairro);
  googletag.pubads().setTargeting('categoria', ctx.categoria);
  googletag.pubads().setTargeting('dispositivo', 'mobile');

  googletag.pubads().enableLazyLoad({
    fetchMarginPercent: 400,
    renderMarginPercent: 150,
    mobileScaling: 2.0,
  });

  const closeBtn = container.querySelector('.pd-sticky-ad__close');
  closeBtn.addEventListener('click', () => {
    container.classList.add('is-closed');
  });

  return slot;
};

/* ============================================================
   6. Bootstrap
   ============================================================ */
PD_ADS.boot = function ({
  adUnitPath = '/1234/praia-digital',
  targeting = {},
  enableStickyMobile = true,
  refreshIntervalMs = 30000,
} = {}) {
  const loadGPT = () => {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://securepubads.g.doubleclick.net/tag/js/gpt.js';
    document.head.appendChild(s);
  };

  const init = () => {
    googletag.cmd.push(() => {
      PD_ADS.initGPT(adUnitPath, targeting);
      googletag.pubads().enableSingleRequest();
      googletag.enableServices();

      PD_ADS.injectInArticle({ every: 4 });
      PD_ADS.injectInFeed({ every: 5 });

      PD_ADS.scheduleSmartRefresh({ intervalMs: refreshIntervalMs, maxRefreshes: 3 });

      if (enableStickyMobile) {
        PD_ADS.initStickyAnchorMobile(adUnitPath);
      }
    });
  };

  if (window.googletag && window.googletag.apiReady) {
    init();
  } else {
    loadGPT();
    window.googletag = window.googletag || { cmd: [] };
    window.googletag.cmd.push(init);
  }
};
