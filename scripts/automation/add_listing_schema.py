#!/usr/bin/env python3
"""
add_listing_schema.py
Adiciona RealEstateListing + BreadcrumbList JSON-LD nas páginas de imoveis/.
"""
from pathlib import Path
import re, json

BASE = Path(__file__).resolve().parents[2]
IMOVEIS = BASE / 'imoveis'

CITY_SLUG_TO_NAME = {
    'santos': 'Santos',
    'guaruja': 'Guarujá',
    'praia-grande': 'Praia Grande',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
    'bertioga': 'Bertioga',
}

def extract_city_from_slug(slug: str):
    name = slug.replace('.html', '')
    # try direct match
    for k, v in CITY_SLUG_TO_NAME.items():
        if k in name.lower():
            return v
    return 'Litoral de SP'

def extract_title(text: str, fallback: str):
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    return fallback

def extract_meta_description(text: str):
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    return ''

def extract_price(text: str):
    m = re.search(r'R\$\s*([\d\.]+)', text)
    if m:
        return m.group(1).replace('.', '')
    return 'Consulte'

def extract_image(text: str, path: Path):
    m = re.search(r'<img[^>]+src=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        src = m.group(1).strip()
        if src.startswith('http'):
            return src
        # make absolute-ish
        return 'https://acarolmourad.github.io/praia-digital/' + str(path.relative_to(BASE)).replace('\\', '/')
    return 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/default-home.jpg'

def make_breadcrumb(name: str, url: str):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/index.html'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Imóveis', 'item': 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/imoveis.html'},
            {'@type': 'ListItem', 'position': 3, 'name': name, 'item': url},
        ],
    }

def make_listing(name: str, description: str, url: str, image: str, price: str, city: str):
    return {
        '@context': 'https://schema.org',
        '@type': 'RealEstateListing',
        'name': name,
        'description': description,
        'url': url,
        'image': image,
        'offers': {
            '@type': 'Offer',
            'price': price,
            'priceCurrency': 'BRL',
            'availability': 'https://schema.org/InStock',
        },
        'provider': {
            '@type': 'RealEstateAgent',
            'name': 'Litoral Prime Imóveis',
            'telephone': '+5511954346288',
            'areaServed': ['Santos', 'Guarujá', 'Praia Grande', 'Bertioga', 'Itanhaém', 'Mongaguá', 'São Vicente', 'Peruíbe'],
        },
    }

updated = 0
skipped = 0
errors = 0
for path in sorted(IMOVEIS.glob('*.html')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue

    # skip if already has RealEstateListing
    if 'RealEstateListing' in text:
        skipped += 1
        continue

    title = extract_title(text, path.stem)
    description = extract_meta_description(text) or title
    price = extract_price(text)
    image = extract_image(text, path)
    city = extract_city_from_slug(path.name)
    rel_path = str(path.relative_to(BASE)).replace('\\', '/')
    url = 'https://acarolmourad.github.io/praia-digital/' + rel_path

    bc = make_breadcrumb(title, url)
    rl = make_listing(title, description, url, image, price, city)

    bc_json = json.dumps(bc, ensure_ascii=False, indent=2)
    rl_json = json.dumps(rl, ensure_ascii=False, indent=2)
    injection = f'<script type="application/ld+json">\n{bc_json}\n</script>\n<script type="application/ld+json">\n{rl_json}\n</script>\n'

    if '</main>' in text:
        text = text.replace('</main>', injection + '</main>', 1)
    elif '</body>' in text:
        text = text.replace('</body>', injection + '</body>', 1)
    else:
        text += '\n' + injection

    try:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(BASE))
        updated += 1
    except Exception as e:
        print('write error', path.relative_to(BASE), e)
        errors += 1

print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
