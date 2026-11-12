"""Protect canonical destinations, intentional exclusions and factual article cleanup."""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_sitemap_targets import (
    IndexingDirectives, canonical_sitemap_path, is_placeholder_article,
    validate_indexing_intent,
)
SPEC = importlib.util.spec_from_file_location('reviewed_sitemap_generator', ROOT/'scripts/gerar_sitemaps.py')
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class ReviewedIndexing(unittest.TestCase):
    def test_reviewed_pages_and_all_sitemaps_agree(self):
        self.assertEqual([], validate_indexing_intent(ROOT))

    def test_regenerated_draft_or_conflicting_canonical_cannot_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'data').mkdir()
            (root/'blog').mkdir()
            page = root/'blog/draft.html'
            expected = 'https://praia.digital/blog/draft.html'
            intent = {'canonicals': {'blog/draft.html': expected}, 'noindex': {'blog/draft.html': 'draft'}}
            (root/'data/indexing-intent-20261111.json').write_text(json.dumps(intent))
            page.write_text(f'<link rel="canonical" href="{expected}"><meta name="robots" content="noindex,follow">')
            self.assertEqual([], validate_indexing_intent(root))
            page.write_text(f'<link rel="canonical" href="{expected}">')
            self.assertTrue(any('noindex regression' in x for x in validate_indexing_intent(root)))
            page.write_text(f'<link rel="canonical" href="{expected}"><link rel="canonical" href="https://praia.digital/">')
            self.assertTrue(any('canonical regression' in x for x in validate_indexing_intent(root)))

    def test_exact_empty_template_is_not_a_word_count_filter(self):
        shell = '<article><h2>Pontos principais</h2><ul><li>Estratégias práticas</li><li>Dicas profissionais</li><li>Ferramentas recomendadas</li></ul></article>'
        self.assertTrue(is_placeholder_article(shell))
        self.assertFalse(is_placeholder_article(shell.replace('</article>', '<p>'+'Conteúdo desenvolvido. '*20+'</p></article>')))
        self.assertFalse(is_placeholder_article('<article><p>Uma resposta curta e completa.</p></article>'))

    def test_generator_uses_real_same_file_urls_and_omits_aliases(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'apps/tool').mkdir(parents=True)
            page = root/'apps/tool/index.html'
            page.write_text('<link rel="canonical" href="https://praia.digital/apps/tool/">')
            self.assertEqual('apps/tool/', canonical_sitemap_path(page, root))
            alias = root/'copy.html'
            alias.write_text('<link rel="canonical" href="https://praia.digital/apps/tool/">')
            self.assertIsNone(canonical_sitemap_path(alias, root))
            alias.write_text('<link rel="canonical" href="https://praia.digital/missing.html">')
            self.assertIsNone(canonical_sitemap_path(alias, root))

    def test_generator_keeps_known_lastmod_and_does_not_invent_new_dates(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'sitemap.xml'
            path.write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://praia.digital/known.html</loc><lastmod>2026-09-24</lastmod></url></urlset>')
            generator.write(str(path), ['known.html', 'new.html'])
            entries = {x.find('{*}loc').text: x for x in ET.parse(path).findall('{*}url')}
            self.assertEqual('2026-09-24', entries['https://praia.digital/known.html'].find('{*}lastmod').text)
            self.assertIsNone(entries['https://praia.digital/new.html'].find('{*}lastmod'))

    def test_generated_listing_data_preserved_but_not_promoted_as_confirmed_offers(self):
        intent = json.loads((ROOT/'data/indexing-intent-20261111.json').read_text())
        records = json.loads((ROOT/'litoral-prime-imoveis/imoveis/properties.json').read_text())
        self.assertEqual(20, len(records))
        self.assertEqual({x['slug'] for x in records}, set(intent['evidence']['generated_listings']['slugs']))
        for record in records:
            rel = 'litoral-prime-imoveis/imoveis/'+record['slug']+'.html'
            self.assertIn(rel, intent['noindex'])
            self.assertIn('Registro demonstrativo', (ROOT/rel).read_text())
        for rel in ['casa-condominio-fechado-bertioga.html', 'imoveis/casas-lancamento-sao-lourenco.html',
                    'imoveis/apartamento-bertioga-70m2.html', 'imoveis/casa-jardim-indaia-180m2.html',
                    'imoveis/apartamento-indaia-bertioga-84m2.html']:
            self.assertNotIn(rel, intent['noindex'])

    def test_revised_financial_articles_use_official_sources_and_valid_page_identity(self):
        pages = ['iptu-taxas-municipais-litoral-sp-2026.html',
                 'portabilidade-financiamento-fgts-litoral-2026.html',
                 'reformas-inteligentes-litoral-2026.html',
                 'primeiro-imovel-litoral-sp-2026/financiamento-vs-consorcio-primeiro-imovel-litoral-2026.html']
        for rel in pages:
            text = (ROOT/rel).read_text()
            parser = IndexingDirectives()
            parser.feed(text)
            self.assertEqual(['https://praia.digital/'+rel], parser.canonicals)
            self.assertNotIn('noindex', parser.reasons)
            self.assertIn('Fontes oficiais consultadas', text)
            self.assertNotIn('5511999999999', text)
            self.assertNotRegex(text, r'IPCA \+ [0-9]')
            self.assertNotIn('ROI 18-35%', text)
            for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S):
                data = json.loads(raw)
                self.assertEqual('https://praia.digital/'+rel, data['mainEntityOfPage'])


if __name__ == '__main__':
    unittest.main()
