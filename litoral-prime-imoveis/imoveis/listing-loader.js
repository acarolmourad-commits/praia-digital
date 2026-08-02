(function(){
  const container = document.querySelector('.imoveis-grid[data-props]');
  if (!container) return;
  const props = JSON.parse(container.getAttribute('data-props') || '[]');
  const base = container.getAttribute('data-base') || 'imoveis';
  const paths = [
    '../imoveis/properties-index.json',
    '../imoveis/properties.json'
  ];
  Promise.all(paths.map(url => fetch(url, {cache:'no-store'}).then(r => r.ok ? r.json() : Promise.reject('fail')).catch(() => null)))
    .then(arrays => {
      const data = arrays.find(a => Array.isArray(a)) || [];
      const map = {};
      for (const item of data) {
        const title = item.title || '';
        const slug = item.slug || '';
        const city = item.city || '';
        const price = item.price || '';
        const img = item.image || '';
        const score = item.score || '';
        map[title] = {title, slug, city, price, img, score};
      }
      const items = props.map(p => map[p]).filter(Boolean);
      if (!items.length) {
        container.innerHTML = '<p>Nenhuma oferta encontrada.</p>';
        return;
      }
      container.innerHTML = items.map(it => {
        const scoreHtml = it.score ? `<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:#0f172a;color:#fff;font-size:12px;margin-left:8px">${it.score}/100</span>` : '';
        const imgHtml = it.img ? `<img src="${it.img}" alt="" style="width:56px;height:56px;object-fit:cover;border-radius:8px">` : '';
        return `<a class="servico-card" href="../${base}/${it.slug}.html" style="display:flex;gap:10px;text-decoration:none;color:#0f172a">
          ${imgHtml}
          <div style="flex:1;min-width:0">
            <h3 style="margin:0 0 4px;font-size:15px;line-height:1.3;font-weight:600">${it.title}</h3>
            <div style="color:#64748b;font-size:13px">${it.city} • ${it.price}</div>
            ${scoreHtml}
          </div>
        </a>`;
      }).join('');
    })
    .catch(() => {
      container.innerHTML = '<p>Não foi possível carregar as ofertas agora.</p>';
    });
})();
