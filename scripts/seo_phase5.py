#!/usr/bin/env python3
# Fix (2026-09-25): padroniza bairros/index.html e blog/index.html
# Idempotente: so aplica se os marcadores ainda nao existirem.
import re

# --- bairros/index.html: CSS 404 + sem header/footer padrao ---
p = 'bairros/index.html'
b = open(p, encoding='utf-8', errors='replace').read()
orig = b
b = b.replace('href="/assets/css/style.css"', 'href="/css/style.css?v=3"')
if 'pd-shared-nav' not in b:
    b = b.replace('<body>', '<body>\n<meta name="pd-shared-nav">', 1)
if 'pd-shared-footer' not in b:
    b = b.replace('</body>', '<meta name="pd-shared-footer">\n<script src="https://praia.digital/js/shared.js?v=2.0"></script>\n</body>', 1)
if b != orig:
    open(p, 'w', encoding='utf-8').write(b)
    print('bairros/index.html corrigido')
else:
    print('bairros/index.html ja ok')

# --- blog/index.html: header legado aninhado + listagem dinamica ---
p = 'blog/index.html'
g = open(p, encoding='utf-8', errors='replace').read()
orig = g
# 1) remover header inline legado, manter so o marcador
new = re.sub(r'<header>\s*<meta name="pd-shared-nav">.*?</nav>\s*', '<meta name="pd-shared-nav">\n', g, flags=re.S)
if new == g:
    new = re.sub(r'<header>.*?</header>', '<meta name="pd-shared-nav">', g, flags=re.S, count=1)
g = new
if '</header>' in g and '<header' not in g:
    g = g.replace('</header>', '', 1)

# 2) secao de guias + listagem dinamica (uma vez)
if 'pdBlogList' not in g:
    section = '''
    <h2 style="margin-top:2rem">📚 Guias completos</h2>
    <div class="grid">
      <article class="card"><h2>Temporada & Airbnb</h2><p>Tudo sobre aluguel de temporada, Airbnb e Booking no litoral.</p><div class="actions"><a class="btn" href="/guias/aluguel-temporada-airbnb-litoral-sp.html">Abrir guia</a></div></article>
      <article class="card"><h2>Baixada Santista</h2><p>Santos, Guarujá, Praia Grande, Bertioga e litoral sul.</p><div class="actions"><a class="btn" href="/guias/baixada-santista-imoveis.html">Abrir guia</a></div></article>
      <article class="card"><h2>Litoral Norte</h2><p>Ubatuba, Caraguatatuba, São Sebastião e Ilhabela.</p><div class="actions"><a class="btn" href="/guias/litoral-norte-imoveis.html">Abrir guia</a></div></article>
      <article class="card"><h2>Investimento</h2><p>ROI, rentabilidade e valorização por cidade.</p><div class="actions"><a class="btn" href="/guias/investir-imoveis-litoral-paulista.html">Abrir guia</a></div></article>
      <article class="card"><h2>Financiamento & Consórcio</h2><p>FGTS, Caixa, aprovação e consórcio sem juros.</p><div class="actions"><a class="btn" href="/guias/financiamento-consorcio-imovel-litoral.html">Abrir guia</a></div></article>
      <article class="card"><h2>Comprar Imóvel</h2><p>Passo a passo completo e seguro.</p><div class="actions"><a class="btn" href="/guias/comprar-imovel-litoral.html">Abrir guia</a></div></article>
      <article class="card"><h2>Impostos & Custos</h2><p>ITBI, IPTU, ganho de capital, aforamento.</p><div class="actions"><a class="btn" href="/guias/impostos-custos-imovel-litoral.html">Abrir guia</a></div></article>
      <article class="card"><h2>Marketing Imobiliário</h2><p>Para corretores e imobiliárias do litoral.</p><div class="actions"><a class="btn" href="/guias/marketing-imobiliario-corretores-litoral.html">Abrir guia</a></div></article>
    </div>

    <h2 style="margin-top:2.5rem">🗂️ Todos os artigos</h2>
    <input id="pdBlogSearch" type="search" placeholder="Buscar artigo... (ex.: airbnb, santos, financiamento)" style="width:100%;padding:.8rem 1rem;border:2px solid #e0e0e0;border-radius:12px;font-size:1rem;margin-bottom:1rem">
    <p id="pdBlogCount" style="font-size:.85rem;color:#6b7280">Carregando artigos...</p>
    <ul id="pdBlogList" style="list-style:none;padding:0;margin:0;display:grid;gap:.4rem"></ul>
'''
    g = g.replace('<div class="adsense-block"', section + '\n<div class="adsense-block"', 1)
    script = '''
<script>
(function(){
  var ul = document.getElementById('pdBlogList');
  if (!ul) return;
  fetch('/sitemap.xml').then(function(r){return r.text()}).then(function(t){
    var urls = (t.match(/<loc>https:\\/\\/praia\\.digital\\/blog\\/[^<]+<\\/loc>/g) || [])
      .map(function(s){ return s.replace('<loc>','').replace('</loc>',''); })
      .filter(function(u){ return !/\\/blog\\/(index\\.html|bairros\\/|imoveis\\/prop-)/.test(u); });
    urls.sort();
    document.getElementById('pdBlogCount').textContent = urls.length + ' artigos publicados';
    function title(u){
      return decodeURIComponent(u.split('/blog/')[1]).replace('.html','').replace(/-/g,' ');
    }
    function render(list){
      ul.innerHTML = list.slice(0,300).map(function(u){
        return '<li style="background:#fff;border:1px solid #E5E7EB;border-radius:10px;padding:.6rem .9rem"><a style="color:#0077B6;text-decoration:none;font-weight:600" href="'+u+'">'+title(u)+'</a></li>';
      }).join('') + (list.length>300 ? '<li style="color:#6b7280;font-size:.85rem;padding:.4rem">+ '+(list.length-300)+' artigos — refine a busca acima</li>' : '');
    }
    render(urls);
    document.getElementById('pdBlogSearch').addEventListener('input', function(e){
      var q = e.target.value.toLowerCase();
      render(urls.filter(function(u){ return title(u).toLowerCase().indexOf(q) !== -1; }));
    });
  }).catch(function(){
    document.getElementById('pdBlogCount').textContent = 'Não foi possível carregar a lista de artigos.';
  });
})();
</script>
'''
    g = g.replace('</body>', script + '\n</body>', 1)
if g != orig:
    open(p, 'w', encoding='utf-8').write(g)
    print('blog/index.html corrigido')
else:
    print('blog/index.html ja ok')
