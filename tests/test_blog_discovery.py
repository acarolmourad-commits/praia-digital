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
