import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('nav_build', ROOT / 'scripts/build-navigation.py')
nav = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nav)
HEADER = (ROOT / 'partials/header.html').read_text(encoding='utf-8')

class NavigationTests(unittest.TestCase):
    def test_replaces_menu_preserves_content(self):
        content = '<main><h1>Imóveis — Bertioga</h1><form id="lead"><input></form></main><script>window.listings=[];</script>'
        text = '<html><head><title>Teste</title></head><body><meta name="pd-shared-nav"><header class="pd"><a class="logo" href="//">Praia</a></header>' + content + '</body></html>'
        result, ok = nav.transform(text, HEADER)
        self.assertTrue(ok)
        self.assertIn(content, result)
        self.assertEqual(result.count('data-pd-navigation="3"'), 1)
        self.assertNotIn('pd-shared-nav', result)
        self.assertNotIn('href="//"', result)

    def test_idempotent(self):
        text = '<html><head></head><body><header><nav>old</nav></header><main>original</main></body></html>'
        result, _ = nav.transform(text, HEADER)
        self.assertEqual(nav.transform(result, HEADER)[0], result)
        self.assertEqual(result.count('/js/pd-navigation.js?v=3'), 1)
        self.assertEqual(result.count('/assets/css/pd-navigation.css?v=3'), 1)

    def test_keeps_editorial_header(self):
        content = '<header><h1>Guia da cidade</h1></header><article><header><h2>Bairro</h2></header></article>'
        text = '<html><head></head><body>' + content + '</body></html>'
        self.assertIn(content, nav.transform(text, HEADER)[0])

    def test_skips_redirect_and_fragment(self):
        for text in ['<header>fragment</header>', '<html><head><meta http-equiv="refresh" content="0;url=/"></head><body>redirect</body></html>']:
            self.assertEqual(nav.transform(text, HEADER), (text, False))

    def test_excluded_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'partials').mkdir()
            (root / 'partials/header.html').write_text(HEADER)
            (root / 'admin').mkdir()
            text = '<html><head></head><body>private</body></html>'
            (root / 'admin/index.html').write_text(text)
            (root / 'index.html').write_text(text)
            report = nav.build(root)
            self.assertEqual(report['included'], ['index.html'])
            self.assertEqual((root / 'admin/index.html').read_text(), text)

    def test_homepage_groups_and_cta(self):
        for label in ['Comprar', 'Investir', 'Meu Imóvel', 'Profissionais', 'Inteligência']:
            self.assertIn('>' + label + '</button>', HEADER)
        self.assertIn('href="/interesse.html">Falar com especialista', HEADER)
        self.assertEqual(HEADER.count('class="pd-site-group"'), 5)
        self.assertEqual(HEADER.count('<a '), 26)

if __name__ == '__main__':
    unittest.main()
