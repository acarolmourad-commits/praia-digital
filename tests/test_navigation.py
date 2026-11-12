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
    def test_leading_skip_link_precedes_navigation(self):
        skip = '<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>'
        text = '<html><head></head><body>' + skip + '<meta name="pd-shared-nav"><main id="conteudo">Guide</main></body></html>'
        result, ok = nav.transform(text, HEADER)
        self.assertTrue(ok)
        self.assertLess(result.index(skip), result.index('<header'))
        again, _ = nav.transform(result, HEADER)
        self.assertEqual(again.count(skip), 1)
        self.assertLess(again.index(skip), again.index('<header'))
        self.assertEqual(again, result)

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
        self.assertEqual(result.count('/js/pd-navigation.js?v=4'), 1)
        self.assertEqual(result.count('/assets/css/pd-navigation.css?v=4'), 1)

    def test_missing_legacy_skip_target_preserves_heading(self):
        heading = '<h1 id="guia">Guia <em>do litoral</em></h1>'
        skip = '<a class="skip-link" href="#main" style="position:absolute;left:-9999px">Pular conteúdo</a>'
        text = '<html><head></head><body>' + skip + heading + '<p>Original</p></body></html>'
        result, _ = nav.transform(text, HEADER)
        target = '<span id="main" class="pd-skip-target" tabindex="-1"></span>'
        self.assertIn(target + heading, result)
        self.assertIn('class="skip-link pd-skip-link"', result)
        self.assertIn('style="position:absolute;left:-9999px"', result)
        self.assertLess(result.index('href="#main"'), result.index('<header'))
        self.assertEqual(nav.transform(result, HEADER)[0], result)

    def test_existing_skip_target_is_not_duplicated_or_rewritten(self):
        for target in ['<main id="main"><h1>Guide</h1></main>',
                       '<h1 id="main" tabindex="-1">Guide</h1>',
                       '<a name="main"></a><h1>Guide</h1>']:
            text = '<html><head></head><body><a href="#main" class="skip-link">Skip</a>' + target + '</body></html>'
            result, _ = nav.transform(text, HEADER)
            self.assertIn(target, result)
            self.assertNotIn('pd-skip-target', result)
            self.assertEqual(nav.transform(result, HEADER)[0], result)

    def test_duplicate_and_pre_body_skip_links_become_one(self):
        first = '<a href="#main" class="skip-link">Pular para o conteúdo</a>'
        text = '<html><head></head>' + first + '<body>' + first + '<article><h1>Guide</h1></article></body></html>'
        result, _ = nav.transform(text, HEADER)
        self.assertEqual(result.count('href="#main"'), 1)
        self.assertEqual(result.count('id="main"'), 1)
        self.assertLess(result.index('<body>'), result.index('href="#main"'))
        self.assertLess(result.index('href="#main"'), result.index('<header'))
        self.assertEqual(nav.transform(result, HEADER)[0], result)

    def test_article_without_heading_gets_target_and_regular_links_stay_intact(self):
        text = '<html><head></head><body><a class="skip-link" href="#main">Skip</a><article>Original</article><a href="#main">Back to content</a></body></html>'
        result, _ = nav.transform(text, HEADER)
        self.assertIn('tabindex="-1"></span><article>Original</article>', result)
        self.assertIn('<a href="#main">Back to content</a>', result)

    def test_no_skip_link_does_not_add_target(self):
        text = '<html><head></head><body><a href="#main">Related section</a><h1 id="guide">Guide</h1></body></html>'
        result, _ = nav.transform(text, HEADER)
        self.assertNotIn('pd-skip-target', result)
        self.assertNotIn('pd-skip-link', result)

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
        self.assertEqual(HEADER.count('<a '), 28)

if __name__ == '__main__':
    unittest.main()
