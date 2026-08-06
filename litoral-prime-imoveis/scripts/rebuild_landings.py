import json
from pathlib import Path
from datetime import date
import random

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
imoveis_dir = base / 'imoveis'
imoveis_dir.mkdir(parents=True, exist_ok=True)

properties_path = base / 'imoveis' / 'properties.json'
properties = json.loads(properties_path.read_text(encoding='utf-8'))

# CSS style block reused
STYLE = '''<style>
  body{font-family:'Segoe UI',system-ui,sans-serif;background:#0b1220;color:#e8ecf1;margin:0;padding:0}
  .wrap{max-width:960px;margin:0 auto;padding:28px 22px}
  header nav a{color:#cfe3ff;text-decoration:none;margin-right:14px;font-weight:500}
  h1{font-size:1.8rem;margin:0 0 .5rem}
  .lead{opacity:.85;line-height:1.6;margin-bottom:1rem}
  .card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px 20px;margin-top:14px}
  .cta{background:#00B4D8;color:#fff;padding:.7rem 1.2rem;border-radius:999px;font-weight:700;text-decoration:none;display:inline-block;margin-top:.6rem;margin-right:10px}
  .price{font-size:1.6rem;font-weight:800;color:#90E0EF;margin-top:8px}
  footer{margin-top:22px;opacity:.6;font-size:12px}
  img{width:100%;border-radius:16px;margin-top:14px}
</style>'''

for p in properties:
    slug = p['slug']
    file_path = imoveis_dir / f"{slug}.html"
    existing = file_path.read_text(encoding='utf-8') if file_path.exists() else ''
    if 'Propriedade ' in existing or '<!-- generated -->' not in existing:
        # Skip regeneration if page already looks generated; only extend missing files
        pass
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['title']} — Litoral Prime Imóveis</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="https://praia.digital/litoral-prime-imoveis/imoveis/{slug}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{p['title']} — Litoral Prime Imóveis">
  <meta property="og:description" content="{p['description']}">
  <meta property="og:image" content="{p['image']}">
  <meta property="og:url" content="https://praia.digital/litoral-prime-imoveis/imoveis/{slug}.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://wa.me">
  <link rel="stylesheet" href="../css/style.css">
  {STYLE}
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "RealEstateListing",
    "name": "{p['title']}",
    "description": "{p['description']}",
    "image": "{p['image']}",
    "url": "https://praia.digital/litoral-prime-imoveis/imoveis/{slug}.html",
    "offers": {{"@type": "Offer", "price": "{p['price'].replace('R$ ','').replace('.','')}", "priceCurrency": "BRL"}},
    "area": "{p['area']}",
    "bedrooms": "{p['bedrooms']}",
    "address": {{"@type": "PostalAddress", "addressLocality": "{p['city']}", "addressRegion": "SP", "addressCountry": "BR"}},
    "provider": {{"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}}
  }}
  </script>
</head>
<body>
  <div class="wrap">
    <header>
      <nav aria-label="Navegação principal">
        <a href="../index.html">Início</a>
        <a href="../imoveis.html">Imóveis</a>
        <a href="../servicos.html">Serviços</a>
        <a href="https://wa.me/5511954346288?text=Olá! Quero falar sobre: {p['title']}" class="cta" target="_blank" rel="noopener">WhatsApp</a>
      </nav>
    </header>

    <main id="main">
      <h1>{p['title']}</h1>
      <img src="{p['image']}" alt="{p['title']}" loading="lazy">
      <p class="lead">{p['description']}</p>

      <div class="card">
        <p><strong>Tipo:</strong> {p['type']}</p>
        <p><strong>Cidade:</strong> {p['city']}</p>
        <p><strong>Bairro:</strong> {p['bairro']}</p>
        <p><strong>Área:</strong> {p['area']}</p>
        <p><strong>Quartos:</strong> {p['bedrooms']}</p>
        <p class="price">{p['price']}</p>
        <p><strong>Destaques:</strong> {', '.join(p['tags'])}</p>
        <a class="cta" href="https://wa.me/5511954346288?text=Olá! Tenho interesse em: {p['title']}. Quero mais detalhes." target="_blank" rel="noopener">Conversar no WhatsApp</a>
      </div>
    </main>

    <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
  </div>
</body>
</html>
'''
    file_path.write_text(html, encoding='utf-8')

print('Landing pages regeneradas:', len(properties))
