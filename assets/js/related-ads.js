/* ============================================================
   Praia Digital — Related Content + Native Ad
   ============================================================ */
window.PD_RELATED = window.PD_RELATED || {};

PD_RELATED.inject = function ({ category, fallbackSlugs = [] } = {}) {
  const container = document.querySelector('.related');
  if (!container) return null;

  const allArticles = Array.from(document.querySelectorAll('article a, .card a'));
  // best-effort related: prefer same category via href match, else fallback
  let related = [];
  const hrefs = new Set();
  for (const a of allArticles) {
    const href = (a.getAttribute('href') || '').trim();
    if (!href || href.startsWith('http')) continue;
    if (hrefs.has(href)) continue;
    hrefs.add(href);
    related.push({ href, title: a.textContent.trim() });
    if (related.length >= 2) break;
  }

  for (const slug of fallbackSlugs) {
    if (related.length >= 2) break;
    const href = 'blog/' + slug;
    if (!hrefs.has(href)) {
      hrefs.add(href);
      related.push({ href, title: slug.replace(/-/g, ' ').replace('.html', '') });
    }
  }

  if (!related.length) return null;

  const nativeCard = document.createElement('a');
  nativeCard.className = 'pd-related__card pd-related__native';
  nativeCard.href = '/bairros/';
  nativeCard.target = '_blank';
  nativeCard.rel = 'noopener';
  nativeCard.innerHTML = `<h3>Encontre o imóvel ideal no litoral</h3><p>Explore oportunidades por bairro, cidade e perfil de investimento.</p>`;

  const grid = document.createElement('div');
  grid.className = 'pd-related__grid';

  const title = document.createElement('div');
  title.className = 'pd-related__title';
  title.textContent = 'Leia também';

  const wrapper = document.createElement('div');
  wrapper.className = 'pd-related';
  wrapper.appendChild(title);
  wrapper.appendChild(grid);

  for (const item of related) {
    const card = document.createElement('a');
    card.className = 'pd-related__card';
    card.href = item.href;
    card.target = '_self';
    card.innerHTML = `<h3>${item.title}</h3><p>Artigo relacionado</p>`;
    grid.appendChild(card);
  }

  grid.appendChild(nativeCard);

  container.parentNode.insertBefore(wrapper, container);

  return wrapper;
};
