#!/usr/bin/env python3
"""
add_listing_schema.py
Adiciona RealEstateListing JSON-LD nas páginas de imoveis/. (breadcrumb removido em 2026-09-27)
"""
from pathlib import Path
import re, json
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

BASE = Path(__file__).resolve().parents[2]
IMOVEIS = BASE / 'imoveis'
SITE_URL = 'https://praia.digital/'

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
    # Brazilian displayed prices use dots for thousands and commas for cents.
    # Reject incomplete/malformed amounts instead of publishing a partial price.
    m = re.search(r'R\$\s*((?:[0-9]{1,3}(?:\.[0-9]{3})+|[0-9]+)(?:,[0-9]{2})?)(?![0-9.,])', unescape(text))
    if m:
        return m.group(1).replace('.', '').replace(',', '.')
    return ''


class ImageSources(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.sources.append(dict(attrs).get('src') or '')


def extract_image(text: str, path: Path):
    page_url = urljoin(SITE_URL, path.relative_to(BASE).as_posix())
    parser = ImageSources()
    parser.feed(text)
    for src in parser.sources:
        src = src.strip()
        if not src:
            continue
        try:
            image_url = urljoin(page_url, src)
            parsed = urlsplit(image_url)
        except ValueError:
            continue
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            return image_url
    # An absent image is preferable to an invented URL returning 404.
    return ''


def make_listing(name: str, description: str, url: str, image: str, price: str, city: str):
    return {
        '@context': 'https://schema.org',
        '@type': 'RealEstateListing',
        'name': name,
        'description': description,
        'url': url,
        **({'image': image} if image else {}),
        'offers': {
            '@type': 'Offer',
            **({'price': price, 'priceCurrency': 'BRL'} if re.fullmatch(r'[0-9]+(?:\.[0-9]{1,2})?', str(price)) else {}),
            'availability': 'https://schema.org/InStock',
        },
        'provider': {
            '@type': 'RealEstateAgent',
            'name': 'Litoral Prime Imóveis',
            'telephone': '+5511954346288',
            'areaServed': ['Santos', 'Guarujá', 'Praia Grande', 'Bertioga', 'Itanhaém', 'Mongaguá', 'São Vicente', 'Peruíbe'],
        },
    }


def main():
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
        url = urljoin(SITE_URL, rel_path)

        rl = make_listing(title, description, url, image, price, city)

        rl_json = json.dumps(rl, ensure_ascii=False, indent=2).replace('<', r'\u003c')
        injection = f'<script type="application/ld+json">\n{rl_json}\n</script>\n'

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
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
