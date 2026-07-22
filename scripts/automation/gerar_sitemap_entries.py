#!/usr/bin/env python3
"""
gerar_sitemap_entries.py
Gera entradas XML para novas páginas e adiciona ao sitemap.xml.
Uso: python scripts/automation/gerar_sitemap_entries.py
"""
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
SITEMAP = BASE / 'sitemap.xml'
TODAY = date.today().isoformat()

pages = [
    'automacao-imobiliarias.html',
    'captacao-imoveis-litoral.html',
    'solucao-proptech-unificada.html',
    'descricao-imoveis-ia.html',
    'seo-local-imobiliarias.html',
    'avaliacao-preco-imoveis.html',
    'consultoria-transformacao-digital-imobiliarias.html',
    'planos-proptech-2026.html',
]

entries = []
for page in pages:
    entries.append(f'''  <url>
    <loc>https://acarolmourad-commits.github.io/praia-digital/{page}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>''')

text = SITEMAP.read_text(encoding='utf-8')
needle = '  </urlset>\n'
insert = '\n'.join(entries) + '\n</urlset>\n'
if '<urlset>' in text and '</urlset>' in text:
    text = text.replace('</urlset>\n', insert, 1)
    SITEMAP.write_text(text, encoding='utf-8')
    print('sitemap updated with', len(pages), 'pages')
else:
    print('sitemap structure not found')
