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

# Regional hubs
hubs = [
    'litoral-norte.html',
    'litoral-sul.html',
]

# Event pages
eventos = [
    'eventos-litoral-paulista-2026-2027/reveillon-santos.html',
    'eventos-litoral-paulista-2026-2027/carnaval-santos.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-santos.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-santos.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-santos.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-santos.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-santos.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-santos.html',
    'eventos-litoral-paulista-2026-2027/reveillon-guaruja.html',
    'eventos-litoral-paulista-2026-2027/carnaval-guaruja.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-guaruja.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-guaruja.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-guaruja.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-guaruja.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-guaruja.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-guaruja.html',
    'eventos-litoral-paulista-2026-2027/reveillon-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/carnaval-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-praia-grande.html',
    'eventos-litoral-paulista-2026-2027/reveillon-bertioga.html',
    'eventos-litoral-paulista-2026-2027/carnaval-bertioga.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-bertioga.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-bertioga.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-bertioga.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-bertioga.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-bertioga.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-bertioga.html',
    'eventos-litoral-paulista-2026-2027/reveillon-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/carnaval-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-itanhaem.html',
    'eventos-litoral-paulista-2026-2027/reveillon-mongagua.html',
    'eventos-litoral-paulista-2026-2027/carnaval-mongagua.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-mongagua.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-mongagua.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-mongagua.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-mongagua.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-mongagua.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-mongagua.html',
    'eventos-litoral-paulista-2026-2027/reveillon-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/carnaval-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-sao-vicente.html',
    'eventos-litoral-paulista-2026-2027/reveillon-peruibe.html',
    'eventos-litoral-paulista-2026-2027/carnaval-peruibe.html',
    'eventos-litoral-paulista-2026-2027/festivais-verao-peruibe.html',
    'eventos-litoral-paulista-2026-2027/temporada-alta-peruibe.html',
    'eventos-litoral-paulista-2026-2027/feriados-prolongados-peruibe.html',
    'eventos-litoral-paulista-2026-2027/eventos-culturais-peruibe.html',
    'eventos-litoral-paulista-2026-2027/festas-tradicionais-peruibe.html',
    'eventos-litoral-paulista-2026-2027/agenda-eventos-peruibe.html',
]

# Persona pages
personas = [
    'personas/investidor.html',
    'personas/familia.html',
    'personas/temporada.html',
    'personas/primeiro-imovel.html',
]

# Core pages
core = [
    'contato.html',
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

for hub in hubs:
    url = f'https://praia.digital/{hub}'
    if url not in existing:
        block = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03T22:15:04+00:00</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
        text = text.replace('</urlset>', block + '</urlset>', 1)
        added += 1

for persona in personas:
    url = f'https://praia.digital/{persona}'
    if url not in existing:
        block = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03T22:15:04+00:00</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
        text = text.replace('</urlset>', block + '</urlset>', 1)
        added += 1

for ev in eventos:
    url = f'https://praia.digital/{ev}'
    if url not in existing:
        block = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03T22:15:04+00:00</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
        text = text.replace('</urlset>', block + '</urlset>', 1)
        added += 1

for c in core:
    url = f'https://praia.digital/{c}'
    if url not in existing:
        block = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03T22:15:04+00:00</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>\n'
        text = text.replace('</urlset>', block + '</urlset>', 1)
        added += 1

SITEMAP.write_text(text, encoding='utf-8')
print('SITEMAP_LANDINGS_ADDED', added)
