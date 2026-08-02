(function(){
  const el = document.getElementById('score-local');
  if (!el) return;
  const slug = location.pathname.split('/').pop().replace(/\.html$/,'');
  if (!slug) return;
  const bases = ['imoveis/properties-index.json','imoveis/properties.json'];
  Promise.all(bases.map(url => fetch(url, {cache:'no-store'}).then(r => r.ok ? r.json() : Promise.reject('fail')).catch(() => null)))
    .then(arrays => {
      const data = arrays.find(a => Array.isArray(a)) || [];
      const item = data.find(x => x.slug === slug);
      if (!item) return;
      const score = item.score ? `<span style="display:inline-block;padding:2px 10px;border-radius:999px;background:#0f172a;color:#fff;font-size:12px;margin-left:10px">${item.score}/100</span>` : '';
      el.innerHTML = `Relevância: ${score ? score : 'N/A'}`;
    })
    .catch(() => {});
})();
