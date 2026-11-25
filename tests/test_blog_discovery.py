"""Protect the edited discovery paths, metadata and existing diagnostic URL."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
GUIDES = [
    'blog/diagnostico-anuncio-temporada-litoral-2026.html',
    'blog/sincronizar-calendario-airbnb-booking-ical.html',
    'blog/briefing-criacao-anuncio-airbnb-booking.html',
]
PROFESSIONAL_GUIDES = [
    'blog/google-sheets-gestao-imoveis-litoral.html',
    'blog/mensuracao-attribution-marketing-imobiliario-local-litoral-2026.html',
    'blog/como-gerar-avaliacoes-google-imobiliarias-litoral-2026.html',
]
PAGES = ['blog/index.html', 'anfitrioes/index.html', *GUIDES, *PROFESSIONAL_GUIDES]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class BlogDiscoveryTests(unittest.TestCase):
    def test_historical_blog_links_open_the_published_guides(self):
        guides = {
            'guia-pet-friendly-riviera-de-sao-lourenco-bertioga-2026.html': 'guia-pet-friendly-riviera-sao-lourenco-bertioga-2026.html',
            'guia-gastronomia-japonesa-delivery-riviera-bertioga-2026.html': 'guia-sushi-gastronomia-japonesa-delivery-riviera-bertioga-2026.html',
            'gastronomia-e-restaurantes-na-riviera-de-sao-lourenco-2026.html': 'onde-comer-na-riviera-de-sao-lourenco-restaurantes-2026.html',
        }
        for old, current in guides.items():
            with self.subTest(old=old):
                tags = Page((ROOT / 'blog/blog' / old).read_text()).tags
                path = '/blog/' + current
                canonical = 'https://praia.digital' + path
                self.assertIn(('link', {'rel': 'canonical', 'href': canonical}), tags)
                self.assertIn(('meta', {'http-equiv': 'refresh', 'content': '0; url=' + canonical}), tags)
                self.assertIn(('meta', {'name': 'robots', 'content': 'noindex, follow'}), tags)
                self.assertIn(('a', {'href': path}), tags)
                self.assertIn(('link', {'rel': 'canonical', 'href': canonical}),
                              Page((ROOT / 'blog' / current).read_text()).tags)

    def test_historical_stylesheets_load_the_shared_design(self):
        paths = ['assets/css/style.css', 'assets/css/main.css', 'styles.css',
                 'css/main.css', 'primeiro-imovel-litoral-sp-2026/css/style.css']
        self.assertTrue((ROOT / 'css/style.css').is_file())
        for path in paths:
            with self.subTest(path=path):
                self.assertIn('@import url("/css/style.css")', (ROOT / path).read_text())

    def test_riviera_cross_links_use_published_paths(self):
        recommendations = [
            ('guia-equipamentos-praia-premium-acessorios-luxo-riviera-2026', 'guia-pet-friendly-riviera-sao-lourenco-bertioga-2026'),
            ('guia-adega-bar-em-casa-vinhos-mixologia-riviera-2026', 'guia-sushi-gastronomia-japonesa-delivery-riviera-bertioga-2026'),
            ('guia-sushi-gastronomia-japonesa-delivery-riviera-bertioga-2026', 'onde-comer-na-riviera-de-sao-lourenco-restaurantes-2026'),
        ]
        for source, destination in recommendations:
            with self.subTest(source=source):
                links = [attrs.get('href', '') for tag, attrs in Page((ROOT / 'blog' / f'{source}.html').read_text()).tags if tag == 'a']
                target = f'/blog/{destination}.html'
                self.assertIn(target, links)
                self.assertTrue((ROOT / target.lstrip('/')).is_file())
                self.assertFalse(any(link.startswith('blog/') for link in links))

    def test_links_assets_and_fragments_resolve(self):
        for file in PAGES:
            for tag, attrs in Page((ROOT / file).read_text()).tags:
                value = attrs.get('href') if tag in ('a', 'link') else attrs.get('src') if tag in ('script', 'img') else None
                if not value:
                    continue
                url = urlsplit(value)
                if url.netloc not in ('', 'praia.digital') or url.scheme not in ('', 'http', 'https'):
                    continue
                target = (ROOT / unquote(url.path).lstrip('/') if url.path.startswith('/') or url.netloc
                          else ROOT / file if not url.path else ROOT / file / '..' / unquote(url.path))
                target = target.resolve()
                if target.is_dir():
                    target /= 'index.html'
                self.assertTrue(target.is_file(), f'{file}: {value}')
                if url.fragment:
                    ids = {a.get('id') for _, a in Page(target.read_text()).tags}
                    self.assertIn(unquote(url.fragment), ids, f'{file}: {value}')

    def test_schema_is_valid_and_page_type_matches(self):
        for file in ['blog/index.html', *GUIDES, *PROFESSIONAL_GUIDES]:
            text = (ROOT / file).read_text()
            schemas = [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
            self.assertEqual(len(schemas), 1, file)
            self.assertEqual(schemas[0]['@type'], 'CollectionPage' if file == 'blog/index.html' else 'BlogPosting')
            tags = Page(text).tags
            for tag in ('h1', 'main', 'title'):
                self.assertEqual(sum(t == tag for t, _ in tags), 1, file)
            for name in ('description', 'robots'):
                self.assertEqual(sum(t == 'meta' and a.get('name') == name for t, a in tags), 1, file)
            self.assertEqual(schemas[0]['url'], 'https://praia.digital/' + file)

    def test_discovery_and_sitemap_keep_each_guide(self):
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
        for file in GUIDES:
            self.assertEqual(urls.count('https://praia.digital/' + file), 1)
            for hub in PAGES[:2]:
                self.assertIn(f'href="/{file}"', (ROOT / hub).read_text())
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', (ROOT / GUIDES[0]).read_text(), re.S)[1])
        self.assertEqual(schema['datePublished'], '2026-08-16')

    def test_professional_guides_keep_existing_urls_and_discovery(self):
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ns)]
        blog = (ROOT / 'blog/index.html').read_text()
        for file in PROFESSIONAL_GUIDES:
            self.assertEqual(urls.count('https://praia.digital/' + file), 1)
            self.assertIn(f'href="/{file}"', blog)
            tags = Page((ROOT / file).read_text()).tags
            self.assertIn(('link', {'rel': 'canonical', 'href': 'https://praia.digital/' + file}), tags)
            self.assertTrue(any(t == 'a' and a.get('href') == '/servicos/ia-para-imobiliarias.html'
                                for t, a in tags), file)

    def test_search_loads_after_parsing_and_has_accessible_fallback(self):
        text = (ROOT / 'blog/index.html').read_text()
        tags = Page(text).tags
        scripts = [a for t, a in tags if t == 'script' and a.get('src') == '/js/blog-search.js']
        self.assertEqual(len(scripts), 1)
        self.assertIn('defer', scripts[0])
        self.assertIn('<label for="pdBlogSearch">', text)
        self.assertIn('role="status"', text)
        self.assertIn('Todos os guias selecionados continuam disponíveis', text)
        self.assertNotIn('aid=XXXXXX', text)


if __name__ == '__main__':
    unittest.main()
