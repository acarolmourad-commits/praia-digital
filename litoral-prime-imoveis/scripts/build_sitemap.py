import json
from pathlib import Path
from datetime import date

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
properties = json.loads((base / 'imoveis' / 'properties.json').read_text(encoding='utf-8'))
today = date.today().isoformat()

urls = []
# Existing high-value URLs
existing = [
  'https://praia.digital/litoral-prime-imoveis/encontrar-imovel.html',
  'https://praia.digital/litoral-prime-imoveis/imoveis.html',
  'https://praia.digital/litoral-prime-imoveis/index.html',
  'https://praia.digital/litoral-prime-imoveis/servicos.html',
  'https://praia.digital/litoral-prime-imoveis/sitemap.html',
  'https://praia.digital/litoral-prime-imoveis/guia-como-comprar-imovel-litoral.html',
  'https://praia.digital/litoral-prime-imoveis/guia-como-comprar-imovel-temporada-litoral.html',
  'https://praia.digital/litoral-prime-imoveis/guia-investidor-imovel-litoral.html',
  'https://praia.digital/litoral-prime-imoveis/docs/briefing-diario.html',
  'https://praia.digital/litoral-prime-imoveis/docs/duvidas-frequentes.html',
  'https://praia.digital/litoral-prime-imoveis/docs/guia-rapido.html',
  'https://praia.digital/litoral-prime-imoveis/docs/relatorio-diario-litoral-prime.html'
]
for u in existing:
    urls.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.9</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

# Cidades
for city in ['bertioga','guaruja','itanhaem','mongagua','peruibe','praia-grande','santos','sao-vicente']:
    urls.append(f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/cidades/{city}.html</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')
    urls.append(f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/cidades/{city}-imoveis-venda.html</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

# Property landing pages
for p in properties:
    urls.append(f'  <url>\n    <loc>https://praia.digital/imoveis/{p["slug"]}.html</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

# Outreach
for name in ['checklist-compartilhamento.html','desempenho.html','despacho.html','materiais.html','posts-redes-sociais.html','posts-redes-sociais-servicos.html','tracker.html','tracker-offline.html']:
    urls.append(f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/outreach/{name}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.6</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

# Leads
for p in properties[:8]:
    urls.append(f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/leads/{p["slug"]}.html</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

# Servicos cidade-servico
for city in ['bertioga','guaruja','itanhaem','mongagua','peruibe','praia-grande','santos','sao-vicente']:
    for s in ['automacao','avaliacao','captacao','consultoria','descricao-ia','venda-imovel']:
        urls.append(f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/servicos/cidade-servico/{city}-{s}.html</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n  <changefreq>weekly</changefreq>\n  </url>\n')

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '</urlset>\n'
(base / 'sitemap.xml').write_text(xml, encoding='utf-8')
print('sitemap.xml atualizado com', len(urls), 'URLs.')
