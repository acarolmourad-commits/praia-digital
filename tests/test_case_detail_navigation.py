import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DETAILS = {
    'case-imobiliaria-porto-da-lua-35-leads-2026.html':
        '/blog/seo-local-imobiliarias-conteudo-util.html',
    'case-reducao-tempo-resposta-costa-verde-2026.html':
        '/apps/oficina-ia-imobiliaria/#followup',
    'case-fechamento-centro-historico-2026.html':
        '/apps/guia-de-uso.html#comprar',
    'case-recomendacao-automatica-imoveis-2026.html': None,
    'case-roi-imobiliaria-litoral-2026.html': None,
}


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def links(self):
        return [attrs.get('href') for tag, attrs in self.tags if tag == 'a']


class CaseDetailNavigation(unittest.TestCase):
    def test_illustrative_pages_keep_article_organization_and_canonical(self):
        for filename in DETAILS:
            with self.subTest(filename=filename):
                html = (ROOT / 'cases' / filename).read_text(encoding='utf-8')
                page = Page(html)
                schemas = [
                    json.loads(raw) for raw in
                    re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                ]
                canonical = 'https://praia.digital/cases/' + filename
                self.assertEqual([schema['@type'] for schema in schemas], ['Article', 'Organization'])
                self.assertEqual(schemas[0]['url'], canonical)
                self.assertEqual([a['href'] for tag, a in page.tags
                                  if tag == 'link' and a.get('rel') == 'canonical'], [canonical])
                self.assertIn('não representa resultado de cliente real.', html)
                self.assertEqual(page.links().count('../contato.html'), 1)

    def test_contextual_links_resolve_without_replacing_contact(self):
        for filename, href in DETAILS.items():
            with self.subTest(filename=filename):
                html = (ROOT / 'cases' / filename).read_text(encoding='utf-8')
                article = html.split('<article>', 1)[1].split('</article>', 1)[0]
                self.assertEqual(Page(article).links(),
                                 [href, '../contato.html'] if href else ['../contato.html'])
                if href:
                    dest = urlsplit(href)
                    path = ROOT / dest.path.lstrip('/')
                    target = path / 'index.html' if dest.path.endswith('/') else path
                    self.assertTrue(target.is_file(), href)
                    ids = [attrs.get('id') for _, attrs in Page(target.read_text(encoding='utf-8')).tags]
                    if dest.fragment:
                        self.assertEqual(ids.count(dest.fragment), 1, href)


if __name__ == '__main__':
    unittest.main()
