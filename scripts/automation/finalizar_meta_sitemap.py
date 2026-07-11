#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalizador automático de metadata e sitemap para Praia Digital.
Varre blog, imoveis, pages e gera/atualiza sitemap.xml simples.
"""

import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_SITEMAP = os.path.join(ROOT, 'sitemap.xml')
BASE_URL = 'https://acarolmourad-commits.github.io/praia-digital/'

INCLUDE_DIRS = ['blog', 'imoveis', 'docs', 'assets', 'landing-parcerias-anuncios.html', 'landing-parcerias-captura-praia-digital-2026.html', 'cases.html', 'index.html', 'lgpd-imobiliarias-litoral-2026.html', 'newsletter', 'checklist-investidor-imoveis-litoral.html']
HTML_EXT = '.html'


def collect_paths():
    paths = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'scripts', 'scripts/automation'}]
        for name in files:
            if not name.endswith(HTML_EXT):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith('scripts/') or rel.startswith('docs/startup-proptech/'):
                continue
            paths.append(rel.replace('\', '/'))
    return sorted(set(paths))


def build_sitemap(paths):
    today = datetime.now().strftime('%Y-%m-%d')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paths:
        lines.append(f'<url><loc>{BASE_URL}{p}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')
    lines.append('</urlset>')
    return '\n'.join(lines)


def main():
    paths = collect_paths()
    sitemap = build_sitemap(paths)
    with open(OUT_SITEMAP, 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f'Sitemap gerado: {OUT_SITEMAP}')
    print(f'URLs incluídas: {len(paths)}')


if __name__ == '__main__':
    main()
