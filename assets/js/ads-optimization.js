/* ============================================================
   Praia Digital — Ad Injection + GPT Lazy Load
   ============================================================ */

/**
 * Initialize GPT with lazy loading tuned for viewability
 * without harming scroll experience.
 */
window.PD_ADS = window.PD_ADS || {};

PD_ADS.initGPT = function (adUnitPath, targeting) {
  if (!window.googletag) return null;

  const slot = googletag.defineSlot(adUnitPath, targeting.sizes || [[300,250],[336,280],[320,100]], targeting.div)
    .addService(googletag.pubads());

  if (targeting.keyValues) {
    googletag.pubads().setTargeting(targeting.key);
    Object.entries(targeting.keyValues).forEach(([k, v]) => slot.setTargeting(k, v));
  }

  googletag.pubads().enableLazyLoad({
    fetchMarginPercent: 600,   // preload when within 6x viewport
    renderMarginPercent: 200,  // render when within 2x viewport
    mobileScaling: 2.0         // more preload on mobile to avoid blank spaces
  });

  return slot;
};

/**
 * Inject an in-article ad every N paragraphs.
 * Uses a placeholder container with CLS-safe CSS class.
 */
PD_ADS.injectInArticle = function ({
  articleSelector = 'article',
  paragraphSelector = 'p',
  every = 4,
  slotFactory
} = {}) {
  const article = document.querySelector(articleSelector);
  if (!article) return [];

  const paragraphs = Array.from(article.querySelectorAll(paragraphSelector));
  const inserted = [];
  let offset = 0;

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

/**
 * Inject an in-feed ad every N items in card/list feeds.
 */
PD_ADS.injectInFeed = function ({
  listSelector = '.grid',
  itemSelector = '.card, article, li',
  every = 5,
  slotFactory
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

/**
 * Example bootstrap for pages that use GPT:
 * - loads GPT async
 * - enables lazy load
 * - boots DAI on article/feed routes
 */
PD_ADS.boot = function ({ adUnitPath = '/1234/example', targeting = {} } = {}) {
  if (!window.googletag) {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://securepubads.g.doubleclick.net/tag/js/gpt.js';
    document.head.appendChild(s);
  }

  const init = () => {
    googletag.cmd.push(() => {
      PD_ADS.initGPT(adUnitPath, targeting);
      googletag.pubads().enableSingleRequest();
      googletag.enableServices();

      PD_ADS.injectInArticle({ every: 4 });
      PD_ADS.injectInFeed({ every: 5 });
    });
  };

  if (window.googletag && googletag.apiReady) init();
  else window.googletag = window.googletag || { cmd: [] };
  window.googletag.cmd.push(init);
};
