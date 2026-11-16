"""The city guides must preserve browsing context without changing catalog SEO."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.current = None
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current = [dict(attrs).get('href', ''), '']
            self.links.append(self.current)
    def handle_endtag(self, tag):
        if tag == 'a': self.current = None
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data

class CitySearchLinksTests(unittest.TestCase):
    def test_itanhaem_elevator_recommends_existing_seasonal_guide(self):
        target = '/blog/itanhaem-guia-locacao-temporada-imoveis-2026.html'
        links = Links((ROOT / 'cidades/itanhaem-elevador.html').read_text()).links
        seasonal = [url for url, text in links if 'Aluguel de temporada' in text]
        self.assertEqual([target], seasonal)
        article = ROOT / target.lstrip('/')
        self.assertTrue(article.is_file())
        self.assertIn('https://praia.digital' + target, article.read_text())

    def test_peruibe_family_recommends_existing_seasonal_guide(self):
        target = '/blog/peruibe-guia-locacao-temporada-imoveis-2026.html'
        # Sauna remains outside this change: its link is already covered by PR #143.
        pages = [
            'academia', 'comercial', 'compra-programada', 'elevador',
            'gestao-de-imovel', 'midia-profissional', 'pet-friendly',
            'propaganda-imobiliaria', 'residencial', 'sacada', 'seguranca',
            'varanda', 'venda-rapida',
        ]
        self.assertTrue((ROOT / target.lstrip('/')).is_file())
        for suffix in pages:
            with self.subTest(page=suffix):
                links = Links((ROOT / ('cidades/peruibe-' + suffix + '.html')).read_text()).links
                seasonal = [url for url, text in links if 'Aluguel de temporada' in text]
                self.assertEqual([target], seasonal)

    def test_no_invalid_protocol_relative_home(self):
        for slug in ['santos', 'praia-grande', 'guaruja', 'bertioga']:
            links = Links((ROOT / 'cidades' / (slug + '.html')).read_text()).links
            self.assertNotIn('//', [url for url, text in links], slug)

    def test_city_ctas_pass_supported_filter(self):
        for slug, city in [('santos', 'Santos'), ('praia-grande', 'Praia Grande'),
                           ('bertioga', 'Bertioga')]:
            links = Links((ROOT / 'cidades' / (slug + '.html')).read_text()).links
            ctas = [url for url, text in links if text == 'Ver imóveis em ' + city]
            self.assertEqual(2, len(ctas), slug)
            for url in ctas:
                parts = urlsplit(url)
                self.assertEqual('/imoveis.html', parts.path)
                self.assertEqual({'cidade': [city]}, parse_qs(parts.query))

    def test_bertioga_city_breadcrumb_is_hub_not_self(self):
        links = Links((ROOT / 'cidades/bertioga.html').read_text()).links
        self.assertTrue(all(url == '/cidades/' for url, text in links if text == 'Cidades'))

if __name__ == '__main__': unittest.main()
