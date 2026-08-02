(function(){
  const target = document.getElementById('last-properties') || document.getElementById('lp-last-properties');
  if (!target) return;
  const base = target.dataset.base || '';
  const citySlug = target.dataset.city || '';
  function load(url){
    return fetch(url, {cache:'no-store'}).then(r => r.ok ? r.json() : Promise.reject('fail'));
  }
  load((base ? base + '/' : '') + 'imoveis/properties-index.json')
    .then(data => render(Array.isArray(data) ? data : []))
    .catch(() => load((base ? base + '/' : '') + 'imoveis/properties.json')
      .then(data => Array.isArray(data) ? render(data.slice(-8).reverse()) : Promise.reject('fail'))
      .catch(() => { target.innerHTML = '<p style="padding:8px;color:#64748b">Sem imóveis no momento.</p>'; }));
  function render(items){
    if (!Array.isArray(items)) return;
    let out = items;
    if (citySlug) {
      const norm = (s='') => s.toLowerCase().replace(/[áà]/g,'a').replace(/[éê]/g,'e').replace(/[í]/g,'i').replace(/[óôõ]/g,'o').replace(/[úü]/g,'u').replace(/\s+/g,'-').trim();
      out = items.filter(x => norm(x.city||'') === citySlug || norm(x.title||'') === citySlug);
    }
    if (!out.length) {
      target.innerHTML = '<p style="padding:8px;color:#64748b">Sem imóveis no momento.</p>';
      return;
    }
    target.innerHTML = out.slice(0,8).map(item => {
      const title = item.title || '';
      const slug = item.slug || '';
      const city = item.city || '';
      const price = item.price || '';
      const img = item.image || '';
      const score = item.score ? `<span style="display:inline-block;margin-top:4px;padding:2px 8px;border-radius:999px;background:#0f172a;color:#fff;font-size:12px">${item.score}/100</span>` : '';
      return `<a href="imoveis/${slug}.html" style="display:flex;gap:8px;text-decoration:none;color:#0f172a;padding:8px;border-radius:10px;background:#f8fafc;margin-bottom:6px">
        <div style="flex:1;min-width:0">
          <div style="font-weight:600;font-size:13px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${title}</div>
          <div style="color:#64748b;font-size:12px;margin-top:2px">${city} • ${price}</div>
          ${score}
        </div>
        ${img ? `<img src="${img}" alt="" style="width:56px;height:56px;object-fit:cover;border-radius:8px">` : ''}
      </a>`;
    }).join('');
  }
})();
