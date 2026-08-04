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
    # matrix expansion
    'apartamento-1-quartos-santos',
    'studio-santos',
    'casa-condominio-santos',
    'cobertura-santos',
    'casa-terrea-santos',
    'frente-mar-santos',
    'apartamento-1-quartos-guaruja',
    'apartamento-2-quartos-guaruja',
    'studio-guaruja',
    'casa-condominio-guaruja',
    'cobertura-guaruja',
    'casa-terrea-guaruja',
    'frente-mar-guaruja',
    'apartamento-1-quartos-praia-grande',
    'apartamento-2-quartos-praia-grande',
    'studio-praia-grande',
    'casa-condominio-praia-grande',
    'cobertura-praia-grande',
    'casa-terrea-praia-grande',
    'frente-mar-praia-grande',
    'apartamento-1-quartos-bertioga',
    'apartamento-2-quartos-bertioga',
    'studio-bertioga',
    'casa-condominio-bertioga',
    'cobertura-bertioga',
    'casa-terrea-bertioga',
    'frente-mar-bertioga',
    'apartamento-1-quartos-itanhaem',
    'apartamento-2-quartos-itanhaem',
    'studio-itanhaem',
    'casa-condominio-itanhaem',
    'cobertura-itanhaem',
    'casa-terrea-itanhaem',
    'frente-mar-itanhaem',
    'apartamento-2-quartos-mongagua',
    'studio-mongagua',
    'casa-condominio-mongagua',
    'cobertura-mongagua',
    'casa-terrea-mongagua',
    'frente-mar-mongagua',
    'apartamento-1-quartos-sao-vicente',
    'apartamento-2-quartos-sao-vicente',
    'studio-sao-vicente',
    'casa-condominio-sao-vicente',
    'cobertura-sao-vicente',
    'casa-terrea-sao-vicente',
    'frente-mar-sao-vicente',
    'apartamento-1-quartos-peruibe',
    'apartamento-2-quartos-peruibe',
    'studio-peruibe',
    'casa-condominio-peruibe',
    'cobertura-peruibe',
    'casa-terrea-peruibe',
    'frente-mar-peruibe',
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
