#!/usr/bin/env python3
"""
add_institutional_sitemap.py
Garante que as páginas institucionais e principais estejam no sitemap.xml.
Idempotente: não duplica URLs já presentes.
Uso: python scripts/automation/add_institutional_sitemap.py
"""
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
SITEMAP = BASE / 'sitemap.xml'
TODAY = date.today().isoformat()

# (página, prioridade, changefreq)
pages = [
    ('index.html', '1.0', 'weekly'),
    ('servicos.html', '0.8', 'monthly'),
    ('cases.html', '0.7', 'monthly'),
    ('planos-assinatura.html', '0.7', 'monthly'),
    ('faq.html', '0.6', 'monthly'),
    ('contato.html', '0.6', 'monthly'),
    ('sobre.html', '0.5', 'monthly'),
    ('quem-somos.html', '0.5', 'monthly'),
    ('fale-conosco.html', '0.5', 'monthly'),
    ('politica-de-privacidade.html', '0.3', 'yearly'),
    ('termos-de-uso.html', '0.3', 'yearly'),
]

text = SITEMAP.read_text(encoding='utf-8')
entries = []
for page, priority, freq in pages:
    loc = f'https://praia.digital/{page}'
    if loc in text:
        continue
    entries.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>''')

if not entries:
    print('sitemap já contém todas as páginas institucionais')
else:
    insert = '\n'.join(entries) + '\n</urlset>'
    if '</urlset>' in text:
        text = text.replace('</urlset>', insert, 1)
        SITEMAP.write_text(text, encoding='utf-8')
        print(f'sitemap atualizado com {len(entries)} páginas institucionais')
    else:
        raise SystemExit('sitemap.xml: estrutura </urlset> não encontrada')
