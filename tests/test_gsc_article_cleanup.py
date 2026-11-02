"""Focused regressions for four Search Console opportunity articles.

These tests check markup/content hygiene, not rankings, legal accuracy or CWV.
"""
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'predicao-mercado-imoveis-litoral-2026.html',
    'quanto-custa-morar-em-bertioga-2026.html',
    'itbi-registro-imoveis-santos-guaruja-bertioga-2026.html',
    'melhor-epoca-para-visitar-riviera-de-sao-lourenco-2026.html',
)


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ArticleCleanupTests(unittest.TestCase):
    def read(self, name):
        return (ROOT / 'blog' / name).read_text(encoding='utf-8')

    def test_canonicals_metadata_and_schemas_are_unambiguous(self):
        for name in FILES:
            with self.subTest(page=name):
                text = self.read(name)
                tags = Tags(text).tags
                self.assertEqual(1, sum(t == 'h1' for t, _ in tags))
                canonical = [a['href'] for t, a in tags if t == 'link' and a.get('rel') == 'canonical']
                self.assertEqual(['https://praia.digital/blog/' + name], canonical)
                keys = Counter(a.get('name') or a.get('property') for t, a in tags if t == 'meta')
                for key in ('description', 'og:title', 'og:description', 'og:image', 'twitter:title', 'twitter:description', 'twitter:image'):
                    self.assertEqual(1, keys[key], key)
                schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S)]
                articles = [x for x in schemas if x.get('@type') in ('Article', 'BlogPosting')]
                self.assertEqual(1, len(articles))
                self.assertEqual('2026-11-02', articles[0]['dateModified'])
                description = next(a['content'] for t, a in tags if t == 'meta' and a.get('name') == 'description')
                self.assertEqual(description, articles[0]['description'])
                self.assertNotRegex(text, r'</p\s*\n')
                self.assertNotRegex(text, r'(?m)^>\s*$', 'orphan tag delimiter')
                self.assertNotIn('document.write', text)

    def test_bertioga_has_budget_guidance_not_draft_or_unsupported_prices(self):
        text = self.read(FILES[1])
        for scaffold in ('CTA sugerido', 'Imagens sugeridas', 'ALT sugerido', 'Schema markup sugerido', 'Links internos recomendados', 'Guaraú'):
            self.assertNotIn(scaffold, text)
        self.assertNotIn('R$', text)
        self.assertNotRegex(text, r'<li>\s*</li>')
        self.assertIn('/imoveis.html?cidade=Bertioga', text)
        self.assertIn('Orçamento mensal: o que anotar', text)
        schemas = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', text, re.S)]
        faq = next(x for x in schemas if x.get('@type') == 'FAQPage')
        for question in faq['mainEntity']:
            self.assertIn('<p>' + question['acceptedAnswer']['text'] + '</p>', text)

    def test_riviera_related_links_resolve_to_actual_pages(self):
        text = self.read(FILES[3])
        self.assertNotIn('href="blog/', text)
        for slug in ('como-chegar-na-riviera-de-sao-lourenco-rotas-dicas-2026.html', 'guia-completo-praias-de-bertioga-2026.html', 'guia-de-servicos-e-conveniencia-riviera-de-sao-lourenco-2026.html'):
            href = '/blog/' + slug
            self.assertIn('href="' + href + '"', text)
            self.assertTrue((ROOT / href.lstrip('/')).is_file())
        self.assertIn('não substituem a previsão do tempo', text)

    def test_tax_page_does_not_fabricate_freshness_or_rate_rules(self):
        text = self.read(FILES[2])
        self.assertIn('Revisão editorial em <time datetime="2026-11-02">02/11/2026</time>', text)
        self.assertNotIn('prevalecendo o maior', text)
        self.assertNotIn('~R$ 3.000', text)
        self.assertIn('não apresenta alíquotas verificadas', text)
        self.assertIn('href="/apps/custo-de-compra/"', text)

    def test_market_page_has_main_target_and_valid_contact_link(self):
        text = self.read(FILES[0])
        tags = Tags(text).tags
        self.assertEqual(1, sum(t == 'main' and a.get('id') == 'main' for t, a in tags))
        self.assertEqual(1, text.count('</main>'))
        self.assertIn('não uma previsão validada', text)
        self.assertIn('utm_campaign=geral&amp;text=', text)
        self.assertNotIn('"text=Quero', text)


if __name__ == '__main__':
    unittest.main()
