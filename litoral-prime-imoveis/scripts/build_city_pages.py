import json
from pathlib import Path
from urllib.parse import quote

base = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(base.parent / 'scripts'))
from preserve_reviewed_indexing import preserve
properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))
today = '2026-08-06'

cities = {}
for p in properties:
    city = p['city']
    if city not in cities:
        cities[city] = []
    cities[city].append(p)

for city in cities:
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Imóveis em {city} — Litoral Prime Imóveis</title>
  <meta name="description" content="Encontre imóveis em {city} no litoral de SP. Apartamentos, casas e coberturas com atendimento por e-mail.">
  <link rel="canonical" href="https://praia.digital/litoral-prime-imoveis/cidades/{city.lower()}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Imóveis em {city} — Litoral Prime Imóveis">
  <meta property="og:description" content="Catálogo de imóveis em {city}. Atendimento humano por e-mail.">
  <meta property="og:url" content="https://praia.digital/litoral-prime-imoveis/cidades/{city.lower()}.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Litoral Prime Imóveis",
    "description": "Imóveis em {city}: apartamentos, casas e coberturas no litoral de SP.",
    "email": "comercial@praia.digital",
    "areaServed": ["{city}"],
    "address": {{"@type": "PostalAddress", "addressLocality": "{city}", "addressRegion": "SP", "addressCountry": "BR"}}
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
        <li><a href="mailto:comercial@praia.digital" class="btn-whatsapp" target="_blank" rel="noopener">Contato por e-mail</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <h1>Imóveis em {city}</h1>
      <p class="subtitle">Consulte as fichas do catálogo para planejar sua busca em {city}.</p>
      <div class="search-bar">
        <a class="cta" href="mailto:comercial@praia.digital" target="_blank" rel="noopener">Consultar por e-mail</a>
        <a class="cta" style="background:#fff;color:#0b1220;margin-left:10px" href="../encontrar-imovel.html">Buscar imóveis</a>
      </div>
    </section>

    <section class="servicos-section">
      <h2>Consultar imóveis em {city}</h2>
      <p>Confira no catálogo as fichas disponíveis para a cidade. Você pode ajustar os filtros ou consultar outras localidades.</p>
      <p><a class="btn-secondary" href="/imoveis.html?cidade={quote(city, safe='')}">Abrir o catálogo de {city}</a></p>
    </section>
  </main>

  <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
</body>
</html>
'''
    path = base / 'cidades' / f'{city.lower()}.html'
    path.write_text(preserve(html, path), encoding='utf-8')

print('Páginas de cidade atualizadas:', len(cities))
