"""Regression coverage for decisions lost by legacy generation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from preserve_reviewed_indexing import preserve
from validate_sitemap_targets import IndexingDirectives

class ReviewedGeneration(unittest.TestCase):
    def test_only_recorded_demonstration_is_labelled_and_values_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'data').mkdir()
            rel = 'litoral-prime-imoveis/imoveis/example.html'
            canonical = 'https://praia.digital/' + rel
            intent = {'canonicals': {rel: canonical}, 'noindex': {rel: 'reviewed'}, 'evidence': {'generated_listings': {'slugs': ['example']}}}
            (root / 'data/indexing-intent-20261111.json').write_text(json.dumps(intent))
            original = '<html><head><link rel="canonical" href="https://praia.digital/imoveis/example.html"></head><body><main id="main"><p>R$ 7343, 59m², 1 quarto</p></main></body></html>'
            result = preserve(original, root / rel, root)
            parser = IndexingDirectives(); parser.feed(result)
            self.assertEqual([canonical], parser.canonicals)
            self.assertIn('noindex', parser.reasons)
            self.assertIn('Registro demonstrativo.', result)
            self.assertIn('<p>R$ 7343, 59m², 1 quarto</p>', result)
            self.assertEqual(result, preserve(result, root / rel, root))
            self.assertEqual(original, preserve(original, root / 'imoveis/real.html', root))

    def test_exact_empty_draft_is_excluded_but_developed_article_is_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / 'data').mkdir()
            (root / 'data/indexing-intent-20261111.json').write_text(json.dumps({'canonicals': {}, 'noindex': {}, 'evidence': {'generated_listings': {'slugs': []}}}))
            original = '<head></head><article><h2>Pontos principais</h2><ul><li>Estratégias práticas</li><li>Dicas profissionais</li><li>Ferramentas recomendadas</li></ul></article>'
            self.assertIn('noindex', preserve(original, root / 'blog/draft.html', root))
            developed = original.replace('</article>', '<p>' + 'Conteúdo desenvolvido. ' * 20 + '</p></article>')
            self.assertEqual(developed, preserve(developed, root / 'blog/guide.html', root))

    def test_sitemap_omits_retired_templates_and_preserves_public_pages(self):
        from gerar_sitemaps import discover_pages
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root / 'data').mkdir(); (root / 'imoveis').mkdir()
            (root / 'data/retired-listings.json').write_text(json.dumps({'slugs': ['retired']}))
            for rel in ['imoveis/retired.html', 'imoveis/real.html', 'template-email-confirmacao-parceria-pos-formulario.html']:
                (root / rel).write_text('<title>Page</title>')
            pages, _ = discover_pages(root)
            self.assertEqual(['imoveis/real.html'], pages)

    def test_legacy_academy_sales_pages_expose_their_existing_canonical(self):
        root = Path(__file__).resolve().parents[1]
        for page in (root / 'academy/cursos').glob('*/vendas.html'):
            parser = IndexingDirectives(); parser.feed(page.read_text(encoding='utf-8'))
            self.assertEqual(1, len(parser.canonicals), str(page))
