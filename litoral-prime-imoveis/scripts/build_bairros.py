import json
from pathlib import Path
from datetime import date

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))
today = date.today().isoformat()

by_city = {}
for p in properties:
    by_city.setdefault(p['city'], []).append(p)

bairros_dir = base / 'bairros'
bairros_dir.mkdir(parents=True, exist_ok=True)

for city, items in by_city.items():
    city_lower = city.lower()
    # City hub
    hub_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bairros em {city} — Litoral Prime Imóveis</title>
  <meta name="description" content="Conteúdo por bairro em {city}: imóveis, destaques e atendimento pelo WhatsApp.">
  <link rel="canonical" href="https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/index.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Bairros em {city} — Litoral Prime Imóveis">
  <meta property="og:description" content="Destaques por bairro em {city}. Atendimento humano pelo WhatsApp.">
  <meta property="og:url" content="https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/index.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://wa.me">
  <link rel="stylesheet" href="../../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ItemList",
    "name": "Bairros em {city}",
    "url": "https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/index.html",
    "itemListElement": [
      {', '.join([f'{{"@type": "ListItem", "position": {i+1}, "url": "https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/{city_lower}-{x["bairro"].lower().replace(" ", "-")}.html", "name": "{x["bairro"]}"}}' for i, x in enumerate(items)])}
    ]
  }}
  </script>
</head>
<body>
  <header>
    <nav aria-label="Navegação principal">
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">Bairros em {city}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../../index.html">Início</a></li>
        <li><a href="../../servicos.html">Serviços</a></li>
        <li><a href="../../imoveis.html">Imóveis</a></li>
        <li><a href="https://wa.me/5511954346288?text=Olá! Quero ver imóveis em {city}." class="btn-whatsapp" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <h1>Bairros em {city}</h1>
      <p class="subtitle">Conteúdo local, imóveis e atendimento no WhatsApp.</p>
    </section>

    <section class="servicos-section">
      <h2>Destaques por bairro</h2>
      <div class="servicos-grid">
        {''.join([f'<article class="servico-card"><h3>🏠 {x["bairro"]}</h3><p>{x["type"]}: {x["price"]} · {x["area"]} · {x["bedrooms"]} quartos</p><a class="btn-secondary" href="{city_lower}-{x["bairro"].lower().replace(" ", "-")}.html">Ver bairro</a></article>' for x in items])}
      </div>
    </section>
  </main>

  <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
</body>
</html>
'''
    (bairros_dir / city_lower).mkdir(parents=True, exist_ok=True)
    (bairros_dir / city_lower / 'index.html').write_text(hub_html, encoding='utf-8')

    # Bairro pages
    for item in items:
        bairro_slug = item['bairro'].lower().replace(' ', '-')
        top = sorted(items, key=lambda x: x['score'], reverse=True)[:3]
        top_links = '\n'.join([f'      <article class="servico-card">\n        <h3>🏠 {p["title"]}</h3>\n        <p>{p["price"]} · {p["area"]} · {p["bedrooms"]} quartos</p>\n        <p>{", ".join(p["tags"])}</p>\n        <a class="btn-whatsapp" href="https://wa.me/5511954346288?text=Olá! Tenho interesse no imóvel: {p["title"]} — {p["city"]}. Pode me enviar mais detalhes?" target="_blank" rel="noopener">Conversar no WhatsApp</a>\n        <a class="btn-secondary" href="/imoveis/{p["slug"]}.html" target="_blank" rel="noopener">Ver detalhes</a>\n      </article>' for p in top])
        
        html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{item["bairro"]} — Imóveis em {city} | Litoral Prime Imóveis</title>
  <meta name="description" content="Imóveis em {item["bairro"]}, {city}. Oportunidades exclusivas no litoral de SP.">
  <link rel="canonical" href="https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/{city_lower}-{bairro_slug}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{item["bairro"]} — Imóveis em {city} | Litoral Prime Imóveis">
  <meta property="og:description" content="Oportunidades exclusivas em {item["bairro"]}, {city}.">
  <meta property="og:url" content="https://praia.digital/litoral-prime-imoveis/bairros/{city_lower}/{city_lower}-{bairro_slug}.html">
  <meta property="og:site_name" content="Litoral Prime Imóveis">
  <meta name="theme-color" content="#0ea5e9">
  <link rel="preconnect" href="https://praia.digital">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preconnect" href="https://wa.me">
  <link rel="stylesheet" href="../../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Litoral Prime Imóveis",
    "description": "Imóveis em {item["bairro"]}, {city}.",
    "telephone": "+5511954346288",
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
        <p class="tagline">{item["bairro"]}, {city}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../../index.html">Início</a></li>
        <li><a href="../../servicos.html">Serviços</a></li>
        <li><a href="../../imoveis.html">Imóveis</a></li>
        <li><a href="../index.html">Bairros</a></li>
        <li><a href="https://wa.me/5511954346288?text=Olá! Tenho interesse em {item["bairro"]}, {city}." class="btn-whatsapp" target="_blank" rel="noopener">WhatsApp</a></li>
      </ul>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <h1>{item["bairro"]}</h1>
      <p class="subtitle">Imóveis e destaques em {item["bairro"]}, {city}.</p>
    </section>

    <section class="servicos-section">
      <h2>Oportunidades em {item["bairro"]}</h2>
      <div class="servicos-grid">
        {top_links}
      </div>
    </section>
  </main>

  <footer>Litoral Prime Imóveis — imóveis no litoral de São Paulo.</footer>
</body>
</html>
'''
        (bairros_dir / city_lower / f'{city_lower}-{bairro_slug}.html').write_text(html, encoding='utf-8')

print('Páginas de bairro criadas para', len(by_city), 'cidades.')
