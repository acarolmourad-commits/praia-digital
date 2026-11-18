"""Inspect generator templates without executing outbound or reading trackers."""
import ast
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_sitemap_targets import IndexingDirectives, indexing_exclusions

GENERATORS = {
    'gerar_dashboard_email.py': 'dashboard-email-proprietarios.html',
    'gerar_dashboard_outbound.py': 'dashboard-outbound-proprietarios.html',
    'executar_outbound.py': 'dashboard-outbound-proprietarios.html',
    'gerar_dashboard_whatsapp.py': 'dashboard-whatsapp-proprietarios.html',
    'gerar_prova_entrega.py': 'prova-entrega-outbound.html',
    'gerar_relatorio_executivo.py': 'relatorio-executivo-outbound.html',
}

class SalesGeneratorIndexing(unittest.TestCase):
    def test_all_generator_heads_preserve_reviewed_indexing(self):
        for script, page in GENERATORS.items():
            with self.subTest(script=script):
                tree = ast.parse((ROOT/'scripts'/script).read_text())
                templates = [n for n in ast.walk(tree) if isinstance(n, ast.JoinedStr)
                             and any(isinstance(v, ast.Constant) and isinstance(v.value, str)
                                     and '<head>' in v.value for v in n.values)]
                self.assertEqual(1, len(templates))
                template = ''.join(v.value if isinstance(v, ast.Constant) else 'TEST'
                                   for v in templates[0].values)
                parser = IndexingDirectives()
                parser.feed(template)
                self.assertEqual(['https://praia.digital/docs/sales/' + page], parser.canonicals)
                self.assertTrue(any('noindex' in reason for reason in parser.reasons))

    def test_report_pages_are_not_sitemap_candidates(self):
        for page in set(GENERATORS.values()):
            with self.subTest(page=page):
                self.assertIn('noindex', indexing_exclusions(ROOT/'docs/sales'/page))

if __name__ == '__main__':
    unittest.main()
