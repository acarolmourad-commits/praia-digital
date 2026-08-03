from pathlib import Path
import csv

REPO = Path('.').resolve()
OUT_DIR = REPO / 'imoveis'
OUT_DIR.mkdir(exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{title}} | Litoral Prime Imóveis</title>
  <meta name="description" content="{{description}}">
  <meta name="keywords" content="{{title}}, imóveis litoral paulista, Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe">
  <link rel="canonical" href="https://praia.digital/imoveis/{{slug}}.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{title}} | Litoral Prime Imóveis">
  <meta property="og:description" content="{{description}}">
  <meta property="og:image" content="https://praia.digital/img/default-home.jpg">
  <meta property="og:url" content="https://praia.digital/imoveis/{{slug}}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{title}} | Litoral Prime Imóveis">
  <meta name="twitter:description" content="{{description}}">
  <meta name="twitter:image" content="https://praia.digital/img/default-home.jpg">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "RealEstateListing",
    "name": "{{title}}",
    "description": "{{description}}",
    "url": "https://praia.digital/imoveis/{{slug}}.html",
    "provider": {"@type": "Organization", "name": "Litoral Prime Imóveis", "url": "https://praia.digital/"}
  }
  </script>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header>
    <nav aria-label="Navegação principal">
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">{{city}}</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../index.html">Início</a></li>
        <li><a href="../servicos.html">Serviços</a></li>
        <li><a href="index.html">Imóveis</a></li>
      </ul>
    </nav>
  </header>
  <main id="main">
    <section class="hero">
      <picture>
        <source srcset="{{image}}.webp" type="image/webp">
        <img src="{{image}}" alt="{{title}}" loading="lazy" width="800" height="600" decoding="async">
      </picture>
      <h1>{{title}}</h1>
      <p class="subtitle">{{description}}</p>
      <a class="btn-whatsapp" href="{{whatsapp_link}}" target="_blank" rel="noopener">Tenho interesse neste imóvel</a>
    </section>
    <section class="servicos-section">
      <h2>Informações</h2>
      <div class="servicos-grid">
        <article class="servico-card">
          <h3>🏷️ Tipo</h3>
          <p>{{type}}</p>
        </article>
        <article class="servico-card">
          <h3>💰 Preço</h3>
          <p>{{price}}</p>
        </article>
        <article class="servico-card">
          <h3>🛏️ Quartos</h3>
          <p>{{bedrooms}}</p>
        </article>
        <article class="servico-card">
          <h3>📐 Área</h3>
          <p>{{area}}</p>
        </article>
      </div>
    </section>
    <section class="servicos-section">
      <h2>Destaques</h2>
      <div class="servicos-grid">
        {{tags}}
      </div>
    </section>
    <section class="servicos-section">
      <h2>Imóveis relacionados</h2>
      <div class="servicos-grid">
        {{related}}
      </div>
    </section>
  </main>
</body>
</html>"""

csv_path = REPO / 'imoveis' / 'landings.csv'
if not csv_path.exists():
    raise SystemExit('landings.csv not found at imoveis/landings.csv')

created = []
skipped = []
with csv_path.open('r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row.get('slug', '').strip()
        title = row.get('title', '').strip()
        description = row.get('description', '').strip()
        city = row.get('city', '').strip()
        type_ = row.get('type', '').strip()
        price = row.get('price', '').strip()
        bedrooms = row.get('bedrooms', '').strip()
        area = row.get('area', '').strip()
        image = row.get('image', '').strip()
        tags = row.get('tags', '').strip()
        related = row.get('related', '').strip()
        whatsapp_link = row.get('whatsapp_link', '').strip()
        if not slug or not title:
            skipped.append(slug or '<empty>')
            continue
        html = TEMPLATE
        html = html.replace('{{slug}}', slug)
        html = html.replace('{{title}}', title)
        html = html.replace('{{description}}', description)
        html = html.replace('{{city}}', city)
        html = html.replace('{{type}}', type_)
        html = html.replace('{{price}}', price)
        html = html.replace('{{bedrooms}}', bedrooms)
        html = html.replace('{{area}}', area)
        html = html.replace('{{image}}', image)
        html = html.replace('{{tags}}', tags)
        html = html.replace('{{related}}', related)
        html = html.replace('{{whatsapp_link}}', whatsapp_link)
        out = OUT_DIR / f"{slug}.html"
        if out.exists():
            skipped.append(slug)
            continue
        out.write_text(html, encoding='utf-8')
        created.append(str(out))

print('LANDINGS_CREATED', len(created))
for p in created:
    print('-', Path(p).name)
print('LANDINGS_SKIPPED', len(skipped))
if skipped:
    for s in skipped[:20]:
        print('  ', s)
