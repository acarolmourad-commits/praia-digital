from pathlib import Path
import re

REPO = Path('.').resolve()
SITEMAP = REPO / 'sitemap.xml'

# Landing pages that should be in sitemap
landings = [
    'apartamento-duplex-santos',
    'apartamento-1-quartos-mongagua',
    'apartamento-2-quartos-santos',
    'apartamento-garden-santos',
    'studio-investimento-praia-grande',
    'casa-condominio-fechado-santos',
    'apartamento-frente-mar-guaruja',
    'sobrado-guaruja',
    'apartamento-cobertura-sao-vicente',
    'casa-ita-encontro-aguas',
    'apartamento-mobiliado-mongagua',
    'terreno-bertioga',
]

text = SITEMAP.read_text(encoding='utf-8', errors='ignore')
existing = set(re.findall(r'<loc>([^<]+)</loc>', text))
added = 0
for slug in landings:
    url = f'https://praia.digital/imoveis/{slug}.html'
    if url not in existing:
        block = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03T22:15:04+00:00</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
        text = text.replace('</urlset>', block + '</urlset>', 1)
        added += 1

SITEMAP.write_text(text, encoding='utf-8')
print('SITEMAP_LANDINGS_ADDED', added)
