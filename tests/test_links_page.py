"""Regression checks for the links page; no network or deployment."""
import importlib.util
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.nodes = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

class LinksTests(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / 'links/index.html').read_text(encoding='utf-8')
        self.nodes = Page(self.text).nodes
    def test_single_navigation_and_heading(self):
        self.assertEqual(sum(tag == 'header' for tag, _ in self.nodes), 1)
        self.assertEqual(sum(tag == 'h1' for tag, _ in self.nodes), 1)
        self.assertEqual(sum(tag == 'nav' and a.get('aria-label') == 'Navegação principal' for tag, a in self.nodes), 1)
        self.assertNotIn('js/shared.js', self.text)
    def test_canonical(self):
        canonical = [a['href'] for tag, a in self.nodes if tag == 'link' and a.get('rel') == 'canonical']
        self.assertEqual(canonical, ['https://praia.digital/links/index.html'])
    def test_card_targets(self):
        targets = [a['href'] for tag, a in self.nodes if tag == 'a' and a.get('class') == 'link-card']
        self.assertEqual(len(targets), 8)
        for target in ['/apps/', '/apps/simulador-roi-temporada/index.html', '/apps/temporada-ou-anual/index.html', '/corretores/cadastrar-imovel.html', '/interesse.html']:
            self.assertIn(target, targets)
        self.assertIn('CRECI válido', self.text)
    def test_amazon_transparency(self):
        amazon = [a for tag, a in self.nodes if tag == 'a' and 'amazon.' in a.get('href', '')]
        self.assertEqual(len(amazon), 4)
        for a in amazon:
            url = urlparse(a['href'])
            self.assertEqual(url.netloc, 'www.amazon.com.br')
            self.assertNotIn('tag', parse_qs(url.query))
            self.assertTrue({'sponsored', 'noopener', 'noreferrer'} <= set(a['rel'].split()))
        self.assertIn('não contêm código de afiliado', self.text)
        for unsupported in ['★★★★★', '★★★★☆', 'Mais Vendido', 'Entrega Rápida', 'Compra Segura']:
            self.assertNotIn(unsupported, self.text)
    def test_unique_ids_and_accessibility(self):
        ids = [a['id'] for _, a in self.nodes if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        for _, a in self.nodes:
            for attr in ['aria-controls', 'aria-labelledby']:
                if attr in a:
                    for value in a[attr].split():
                        self.assertIn(value, ids)
            if a.get('href', '').startswith('#'):
                self.assertIn(a['href'][1:], ids)
    def test_sitemap(self):
        xml = ET.parse(ROOT / 'sitemap-links.xml')
        locs = [x.text for x in xml.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(locs, ['https://praia.digital/links/index.html'])
    def test_navigation_build_is_idempotent(self):
        spec = importlib.util.spec_from_file_location('pd_links_build', ROOT / 'scripts/build-navigation.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        header = (ROOT / 'partials/header.html').read_text(encoding='utf-8')
        built, included = module.transform(self.text, header)
        self.assertTrue(included)
        self.assertEqual(built.count('data-pd-navigation="3"'), 1)
        self.assertEqual(len(re.findall(r'<header\b', built)), 1)
        self.assertEqual(module.transform(built, header)[0], built)
        self.assertEqual(re.findall(r'<h1\b[^>]*>.*?</h1>', built), re.findall(r'<h1\b[^>]*>.*?</h1>', self.text))

if __name__ == '__main__':
    unittest.main()
