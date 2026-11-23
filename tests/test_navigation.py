import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('nav_build', ROOT / 'scripts/build-navigation.py')
nav = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nav)
HEADER = (ROOT / 'partials/header.html').read_text(encoding='utf-8')

class NavigationTests(unittest.TestCase):
    def test_ia_contact_is_contextual_and_other_pages_unchanged(self):
        services = nav.header_for_page('servicos-ia.html', HEADER)
        self.assertIn('href="/solicitar-servico.html?servico=Projeto%20personalizado">Solicitar proposta', services)
        self.assertNotIn('href="/interesse.html"', services)
        request = nav.header_for_page('solicitar-servico.html', HEADER)
        self.assertIn('href="#brief-form">Preencher solicitação', request)
        for page in ['index.html', 'servicos.html', 'imoveis.html', 'ia/marketplaces/index.html']:
            self.assertEqual(nav.header_for_page(page, HEADER), HEADER)

    def test_saoc_header_uses_the_listing_email(self):
        path = 'imoveis/apartamento-vicente-carvalho-ii-saoc-45m2.html'
        listing = (ROOT / path).read_text(encoding='utf-8')
        contact = re.search(r'href="(mailto:[^"]+)">Consultar por e-mail</a>', listing)
        self.assertIsNotNone(contact)
        header = nav.header_for_page(path, HEADER)
        self.assertIn(f'href="{contact[1]}">E-mail da corretora</a>', header)
        self.assertNotIn('href="/interesse.html"', header)
        for other in ['imoveis.html', 'imoveis/sobrado-indaia-94m2.html']:
            self.assertEqual(nav.header_for_page(other, HEADER), HEADER)

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
        self.assertIn('href="/servicos-ia.html">Serviços de IA para empresas', HEADER)
        self.assertEqual(HEADER.count('class="pd-site-group"'), 5)
        self.assertEqual(HEADER.count('<a '), 29)

if __name__ == '__main__':
    unittest.main()
