(function(){
  const container = document.getElementById('related-properties');
  if (!container) return;
  const slug = (location.pathname.split('/').pop() || '').replace(/\.html$/,'');
  if (!slug) return;
  fetch('imoveis/properties-index.json', {cache:'no-store'})
    .then(r => r.ok ? r.json() : Promise.reject('fail'))
    .then(data => {
      if (!Array.isArray(data)) return;
      const current = data.find(x => x.slug === slug);
      if (!current) return;
      const city = current.city || '';
      const type = current.type || '';
      const related = data.filter(x => x.slug !== slug && x.city && x.type && (x.city === city || x.type === type)).slice(0,6);
      if (!related.length) {
        container.innerHTML = '<p>Nenhum imóvel relacionado no momento.</p>';
        return;
      }
      container.innerHTML = related.map(item => {
        const scoreHtml = item.score ? `<span style="display:inline-block;padding:2px 8px;border-radius:999px;background:#0f172a;color:#fff;font-size:12px;margin-left:8px">${item.score}/100</span>` : '';
        const imgHtml = item.image ? `<img src="${item.image}" alt="" style="width:56px;height:56px;object-fit:cover;border-radius:8px">` : '';
        return `<a onclick="window.LP_TRACK && window.LP_TRACK.track('related','')" class="servico-card" href="imoveis/${item.slug}.html" style="display:flex;gap:10px;text-decoration:none;color:#0f172a">
          ${imgHtml}
          <div style="flex:1;min-width:0">
            <h3 style="margin:0 0 4px;font-size:15px;line-height:1.3;font-weight:600">${item.title}</h3>
            <div style="color:#64748b;font-size:13px">${item.city} • ${item.price}</div>
            ${scoreHtml}
          </div>
        </a>`;
      }).join('');
    })
    .catch(() => {});
})();
