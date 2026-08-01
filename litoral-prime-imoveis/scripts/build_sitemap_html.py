from pathlib import Path
import re
from datetime import datetime, timezone

REPO = Path('.').resolve()
SITEMAP_XML = REPO / 'sitemap.xml'
SITEMAP_HTML = REPO / 'sitemap.html'

BASE_URL = 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/'

if not SITEMAP_XML.exists():
    raise SystemExit('sitemap.xml not found')

text = SITEMAP_XML.read_text(encoding='utf-8', errors='ignore')
urls = re.findall(r'<loc>(.*?)</loc>', text)

categories = {
    'Principais': [],
    'Imóveis': [],
    'Serviços': [],
    'Serviços por cidade': [],
    'Cidades': [],
    'Documentos e operação': [],
    'Guias': [],
    'Outros': [],
}

for url in urls:
    if not url.startswith(BASE_URL):
        continue
    rel = url[len(BASE_URL):]
    if rel in {'index.html', 'imoveis.html', 'servicos.html', 'encontrar-imovel.html'}:
        categories['Principais'].append((rel.replace('.html', '').replace('-', ' ').title(), url))
    elif rel.startswith('imoveis/'):
        name = rel.replace('imoveis/', '').replace('.html', '').replace('-', ' ').title()
        categories['Imóveis'].append((name, url))
    elif rel.startswith('servicos/cidade-servico/'):
        name = rel.replace('servicos/cidade-servico/', '').replace('.html', '').replace('-', ' ').title()
        categories['Serviços por cidade'].append((name, url))
    elif rel.startswith('servicos/'):
        name = rel.replace('servicos/', '').replace('.html', '').replace('-', ' ').title()
        categories['Serviços'].append((name, url))
    elif rel.startswith('cidades/'):
        name = rel.replace('cidades/', '').replace('.html', '').replace('-', ' ').title()
        categories['Cidades'].append((name, url))
    elif rel.startswith('docs/') or rel.startswith('outreach/'):
        name = rel.replace('.html', '').replace('-', ' ').title()
        categories['Documentos e operação'].append((name, url))
    elif rel.startswith('guia-') or rel.startswith('blog/'):
        name = rel.replace('.html', '').replace('-', ' ').title()
        categories['Guias'].append((name, url))
    else:
        categories['Outros'].append((rel.replace('.html', '').replace('-', ' ').title(), url))

# Sort each category
for k in categories:
    categories[k].sort(key=lambda x: x[0].lower())

# Build HTML
sections = []
for title, items in categories.items():
    if not items:
        continue
    # Limit large categories to first 50 for readability
    if len(items) > 50:
        display = items[:50]
        more = len(items) - 50
        cards = '\n'.join([f'        <a class="servico-card" href="{url}">{name}</a>' for name, url in display])
        cards += f'\n        <p class="subtitle">... e mais {more} páginas. Veja o <a href="sitemap.xml">sitemap XML</a> para a lista completa.</p>'
    else:
        cards = '\n'.join([f'        <a class="servico-card" href="{url}">{name}</a>' for name, url in items])
    sections.append(f'''    <section class="servicos-section">
      <h2>{title} ({len(items)})</h2>
      <div class="servicos-grid">
{cards}
      </div>
    </section>
''')

now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mapa do site — Litoral Prime Imóveis</title>
  <link rel="stylesheet" href="../css/style.css">
  <meta name="description" content="Mapa do site da Litoral Prime Imóveis: {len(urls)} páginas indexadas.">
  <link rel="canonical" href="{BASE_URL}sitemap.html">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Mapa do site — Litoral Prime Imóveis">
  <meta property="og:description" content="Mapa do site da Litoral Prime Imóveis: {len(urls)} páginas indexadas.">
  <meta property="og:url" content="{BASE_URL}sitemap.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Mapa do site — Litoral Prime Imóveis">
  <meta name="twitter:description" content="Mapa do site da Litoral Prime Imóveis: {len(urls)} páginas indexadas.">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Mapa do site — Litoral Prime Imóveis",
    "description": "Mapa do site da Litoral Prime Imóveis: {len(urls)} páginas indexadas.",
    "url": "{BASE_URL}sitemap.html",
    "isPartOf": {{"@type": "WebSite", "name": "Litoral Prime Imóveis", "url": "{BASE_URL}"}}
  }}
  </script>
</head>
<body>
  <header>
    <nav>
      <div class="logo">
        <h1>🏖️ Litoral Prime Imóveis</h1>
        <p class="tagline">Mapa do site</p>
      </div>
      <ul class="nav-menu">
        <li><a href="../index.html">Início</a></li>
        <li><a href="imoveis.html">Imóveis</a></li>
        <li><a href="servicos.html">Serviços</a></li>
        <li><a href="https://wa.me/5511954346288" class="btn-whatsapp">WhatsApp</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Mapa do site</h1>
      <p class="subtitle">Todas as páginas da Litoral Prime Imóveis em um só lugar. ({len(urls)} páginas)</p>
    </section>
{''.join(sections)}  </main>

  <footer>
    <p>© 2026 Litoral Prime Imóveis. Todos os direitos reservados. | Criado pela Praia Digital</p>
    <p><a href="sitemap.xml">Sitemap XML</a></p>
  </footer>
  <a class="whatsapp-fab" href="https://wa.me/5511954346288" target="_blank" rel="noopener" aria-label="WhatsApp">W</a>
</body>
</html>'''

SITEMAP_HTML.write_text(html, encoding='utf-8')
print('SITEMAP_HTML_GENERATED', len(urls))
