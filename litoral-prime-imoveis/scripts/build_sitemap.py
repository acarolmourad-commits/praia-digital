import re
from pathlib import Path
from datetime import date

base = Path('C:/Users/Carolina/praia-digital/litoral-prime-imoveis')
SITEMAP = base / 'sitemap.xml'
INDEXABLE_EXTENSIONS = {'.html', '.htm'}

EXCLUDE_PATTERNS = [
    r'^backup(/|$)',
    r'/backup/',
    r'^\.',
    r'(^|/)(__pycache__|node_modules|dist|build|tmp)(/|$)',
]

SKIP_TOKENS = ['backup', 'draft', 'template', 'internal', 'temp-', '404.html']


def should_exclude(path: str) -> bool:
    if not any(path.lower().endswith(ext) for ext in INDEXABLE_EXTENSIONS):
        return True
    if any(token in path.lower() for token in SKIP_TOKENS):
        return True
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def collect_urls() -> list:
    urls = []
    today = date.today().isoformat()

    # Páginas públicas principais
    public = [
        'encontrar-imovel.html',
        'imoveis.html',
        'index.html',
        'servicos.html',
        'sitemap.html',
        'guia-como-comprar-imovel-litoral.html',
        'guia-como-comprar-imovel-temporada-litoral.html',
        'guia-investidor-imovel-litoral.html',
    ]
    for name in public:
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/{name}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.9</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    # Cidades
    for city in ['bertioga', 'guaruja', 'itanhaem', 'mongagua', 'peruibe', 'praia-grande', 'santos', 'sao-vicente']:
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/cidades/{city}.html</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/cidades/{city}-imoveis-venda.html</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    # Páginas públicas de docs mantidas; internas/backups são filtradas pelo should_exclude
    for p in (base / 'docs').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(base).as_posix()
        if should_exclude(rel):
            continue
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/{rel}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    # Bairros públicos
    for p in (base / 'bairros').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(base).as_posix()
        if should_exclude(rel):
            continue
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/{rel}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.8</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    # Conteúdo público operacional: outreach e servicos/cidade-servico
    for p in (base / 'outreach').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(base).as_posix()
        if should_exclude(rel):
            continue
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/{rel}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.6</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    for p in (base / 'servicos').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(base).as_posix()
        if should_exclude(rel):
            continue
        urls.append(
            f'  <url>\n    <loc>https://praia.digital/litoral-prime-imoveis/{rel}</loc>\n'
            f'    <lastmod>{today}</lastmod>\n    <priority>0.7</priority>\n'
            f'  <changefreq>weekly</changefreq>\n  </url>\n'
        )

    return urls


xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(collect_urls()) + '</urlset>\n'
SITEMAP.write_text(xml, encoding='utf-8')
print('sitemap.xml atualizado com', xml.count('<url>'), 'URLs.')
