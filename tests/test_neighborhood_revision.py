"""Regression coverage for the reviewed neighborhood pages. No network or form submissions."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'data/neighborhood-editorial-review.json').read_text(encoding='utf-8'))


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.headings = []
        self.labels = []
        self.inputs = []
        self.canonicals = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if re.fullmatch(r'h[1-6]', tag):
            self.headings.append(int(tag[1]))
        if tag == 'label':
            self.labels.append(a.get('for'))
        if tag == 'input' and a.get('type') != 'hidden':
            self.inputs.append(a.get('id'))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href'))


class NeighborhoodRevisionTests(unittest.TestCase):
    def test_reviewed_pages_preserve_urls_and_metadata(self):
        self.assertEqual(len(MANIFEST['pages']), 8)
        for item in MANIFEST['pages']:
            with self.subTest(page=item['path']):
                text = (ROOT / item['path']).read_text(encoding='utf-8')
                page = Page(text)
                self.assertEqual(page.canonicals, [item['canonical']])
                self.assertEqual(page.headings.count(1), 1)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertIn('data-editorial-review="2026-11-04"', text)
                self.assertIn('id="fontes"', text)
                self.assertIn('Revisão editorial:', text)
                self.assertNotIn('Guia completo', text)
                self.assertNotIn('RealEstateListing', text)
                self.assertNotIn('"price": "0"', text)
                schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
                self.assertEqual(len(schemas), 1)
                data = json.loads(schemas[0])
                self.assertEqual(data['@type'], 'WebPage')
                self.assertEqual(data['url'], item['canonical'])
                self.assertEqual(data['dateModified'], MANIFEST['reviewedOn'])
                for source in item['sources']:
                    self.assertIn(source, page.links)

    def test_labels_headings_and_internal_links(self):
        for item in MANIFEST['pages']:
            with self.subTest(page=item['path']):
                path = ROOT / item['path']
                text = path.read_text(encoding='utf-8')
                page = Page(text)
                previous = 0
                for rank in page.headings:
                    self.assertLessEqual(rank, previous + 1)
                    previous = rank
                self.assertEqual(set(page.inputs), {'name', 'email', 'phone'})
                self.assertTrue(set(page.inputs).issubset(page.labels))
                self.assertIn('role="status" aria-live="polite"', text)
                for link in page.links:
                    url = urlsplit(link)
                    if url.scheme or url.netloc:
                        continue
                    target = ROOT / url.path.lstrip('/') if url.path else path
                    if target.is_dir():
                        target /= 'index.html'
                    self.assertTrue(target.is_file(), str(target))
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), Page(target.read_text(encoding='utf-8')).ids)

    def test_no_stale_promises_or_known_broken_service_link(self):
        for item in MANIFEST['pages']:
            text = (ROOT / item['path']).read_text(encoding='utf-8')
            for invalid in ['ano Em breve', 'gratuidade para pedestres está confirmada', 'DERSA',
                            'https://semil.sp.gov.br/dh/travessias', 'fim de 2026',
                            'Hard Rock Cafe', 'Réveillon Isla Parador']:
                self.assertNotIn(invalid, text, item['path'])

    def test_uncertain_names_and_alias_are_explicit(self):
        ilhabela = (ROOT / 'bairros/ilhabela/pernambuco.html').read_text(encoding='utf-8')
        self.assertIn('Rua Pernambuco no bairro Barra Velha', ilhabela)
        self.assertIn('não é prova da inexistência', ilhabela)
        bertioga = (ROOT / 'bairros/bertioga/praia-do-ribeira.html').read_text(encoding='utf-8')
        self.assertIn('Localização ainda não confirmada', bertioga)
        camburi = (ROOT / 'bairros/caraguatatuba/camburi.html').read_text(encoding='utf-8')
        self.assertIn('Balneário Camburi', camburi)
        self.assertIn('Mirante do Camaroeiro', camburi)
        theme = (ROOT / 'bairros/itanhaem/condominios.html').read_text(encoding='utf-8')
        self.assertIn('Guia temático', theme)

    def test_catalog_counts_pages_and_explains_types(self):
        text = (ROOT / 'bairros/index.html').read_text(encoding='utf-8')
        self.assertIn('123 páginas da coleção', text)
        self.assertIn('não um cadastro oficial', text)
        self.assertNotIn('123 guias de bairro', text)
        self.assertNotIn('os páginas', text)
        self.assertEqual(text.count('data-kind="tema"'), 7)
        self.assertEqual(text.count('data-kind="alias"'), 1)
        self.assertEqual(text.count('data-kind="referencia"'), 3)
        self.assertRegex(text, r'id="guide-empty"[^>]*hidden')
        js = (ROOT / 'js/neighborhood-guide.js').read_text(encoding='utf-8')
        self.assertIn('páginas da coleção', js)

    def test_hub_affiliate_cleanup(self):
        text = (ROOT / 'bairros/praia-grande/index.html').read_text(encoding='utf-8')
        self.assertEqual(text.count('Programa de Associados'), 1)
        for invalid in ['aid=XXXXXX', 'Placeholder: substituir', 'reservedo', 'booking-placeholder',
                        'checkin_year=2026']:
            self.assertNotIn(invalid, text)
        self.assertIn('id="booking-heading"', text)
        self.assertIn('rel="sponsored noopener"', text)
        self.assertTrue(text.rstrip().endswith('</html>'))

    def test_legacy_generators_preserve_reviewed_pages(self):
        for rel in ['scripts/gerar_bairros.py', 'scripts/enhance_neighborhood_pages.py']:
            text = (ROOT / rel).read_text(encoding='utf-8')
            self.assertIn('data-editorial-review=', text)


if __name__ == '__main__':
    unittest.main()
