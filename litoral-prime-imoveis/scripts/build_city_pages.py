import json
from pathlib import Path

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))
today = '2026-08-06'

cities = {}
for p in properties:
    city = p['city']
    if city not in cities:
        cities[city] = []
    cities[city].append(p)

for city, city_props in cities.items():
    top = sorted(city_props, key=lambda x: x['score'], reverse=True)[:5]
    top_links = '\n'.join([f'      <article class="servico-card">\n        <h3>🏠 {p["title"]}</h3>\n        <p>{p["price"]} · {p["area"]} · {p["bedrooms"]} quartos</p>\n        <p>{", ".join(p["tags"])}</p>\n        <a class="btn-whatsapp" href="https://wa.me/5511954346288?text=Olá! Tenho interesse no imóvel: {p["title"]} — {p["city"]}. Pode me enviar mais detalhes?" target="_blank" rel="noopener">Conversar no WhatsApp</a>\n        <a class="btn-secondary" href="/imoveis/{p["slug"]}.html" target="_blank" rel="noopener">Ver detalhes</a>\n      </article>' for p in top])
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Imóveis em {city} — Litoral Prime Imóveis</title>
  <meta name="description" content="Encontre imóveis em {city} no litoral de SP. Apartamentos, casas e coberturas com atendimento pelo WhatsApp.">
  <link rel="canonical" href="https://praia.digital/litoral-prime-imoveis/cidades/{city.lower()}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Imóveis em {city} — Litoral Prime Imóveis">
  <meta property="og:description" content="Oportunidades exclusivas em {city}. Atendimento humano pelo WhatsApp.">
  <meta property="og:url" content="https://praia.digital/litoral-prime-imoveis/cidades/{city.lower()}.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://wa.me">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Litoral Prime Imóveis",
    "description": "Imóveis em {city}: apartamentos, casas e coberturas no litoral de SP.",
    "telephone": "+5511954346288",
    "areaServed": ["{city}"],
    "address": {{"@type": "PostalAddress", "addressLocality": "{city}", "addressRegion": "SP", "addressCountry": "BR"}}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Imóveis em {city}",
    "url": "https://praia.digital/litoral-prime-imoveis/cidades/{city.lower()}.html",
    "itemListElement": [
      {', '.join([f'{{"@type": "ListItem", "position": {i+1}, "url": "https://praia.digital/imoveis/{p["slug"]}.html", "name": "{p["title"]}"}}' for i, p in enumerate(top)])}
    ]
  }}
  </script>
</head>
<body>
  <header>
    <nav aria-label="Navegação principal">
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">Imóveis em {city}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../index.html">Início</a></li>
        <li><a href="../servicos.html">Serviços</a></li>
        <li><a href="../imoveis.html">Imóveis</a></li>
        <li><a href="https://wa.me/5511954346288?text=Olá! Tenho interesse em imóveis em {city}." class="btn-whatsapp" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <h1>Imóveis em {city}</h1>
      <p class="subtitle">Oportunidades exclusivas em {city}, com atendimento humano pelo WhatsApp.</p>
      <div class="search-bar">
        <a class="cta" href="https://wa.me/5511954346288?text=Olá! Quero ver imóveis em {city}." target="_blank" rel="noopener">Ver opções no WhatsApp</a>
        <a class="cta" style="background:#fff;color:#0b1220;margin-left:10px" href="../encontrar-imovel.html">Buscar imóveis</a>
      </div>
    </section>

    <section class="servicos-section">
      <h2>Destaques em {city}</h2>
      <div class="servicos-grid">
        {top_links}
      </div>
    </section>
  </main>

  <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
</body>
</html>
'''
    path = base / 'cidades' / f'{city.lower()}.html'
    path.write_text(html, encoding='utf-8')

print('Páginas de cidade atualizadas:', len(cities))
