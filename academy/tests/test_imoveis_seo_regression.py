from __future__ import annotations

from pathlib import Path
import json
from html.parser import HTMLParser

from scripts.seo.seo_audit import _audit_html


IMOVEIS_DIR = Path(__file__).resolve().parent.parent.parent / 'imoveis'


def _read_sample(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def test_imoveis_pages_have_h1():
    missing = []
    for path in sorted(IMOVEIS_DIR.glob('*.html')):
        html = _read_sample(path)
        result = _audit_html(html)
        if result['h1_status'] != 'PASS':
            missing.append(path.name)
    assert not missing, f'{len(missing)} imoveis pages missing H1: {missing[:5]}'


def test_imoveis_pages_pass_seo_audit():
    fails = []
    retired = set(json.loads((IMOVEIS_DIR.parent / 'data/retired-listings.json').read_text(encoding='utf-8'))['slugs'])
    for path in sorted(IMOVEIS_DIR.glob('*.html')):
        html = _read_sample(path)
        if path.stem in retired:
            class MetaTags(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.meta = {}
                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag == 'meta':
                        self.meta[attrs.get('name')] = attrs.get('content', '')
            tags = MetaTags()
            tags.feed(html)
            assert tags.meta.get('pd-retired-listing') == 'true', path.name
            assert 'noindex' in tags.meta.get('robots', '').split(','), path.name
            assert 'RealEstateListing' not in html and 'wa.me' not in html, path.name
            continue
        result = _audit_html(html)
        if result['overall'] != 'PASS':
            fails.append((path.name, result['overall']))
    assert not fails, f'{len(fails)} imoveis pages failing SEO audit: {fails[:5]}'
