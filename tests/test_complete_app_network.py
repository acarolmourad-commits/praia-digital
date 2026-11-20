import importlib.util
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('app_network', ROOT/'scripts/build_app_network.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a': self.links.append(values.get('href',''))
        if 'id' in values: self.ids.append(values['id'])

class CompleteAppNetworkTests(unittest.TestCase):
    def setUp(self):
        self.slugs = {p.parent.name for p in (ROOT/'apps').glob('*/index.html')}
    def test_pilot_and_pricing_guide_have_contextual_round_trip(self):
        guide = (ROOT/'apps/guia-de-uso.html').read_text(encoding='utf-8')
        pilot = (ROOT/'ia/marketplaces/piloto/index.html').read_text(encoding='utf-8')
        route = guide.split('id="vender"', 1)[1].split('</section>', 1)[0]
        self.assertIn('/ia/marketplaces/piloto/', Links(route).links)
        self.assertIn('Simulação com produtos fictícios', route)
        self.assertIn('sem conexão com lojas ou estoque real', route)
        self.assertIn('/apps/guia-de-uso.html#vender', Links(pilot).links)
        self.assertIn('não são transferidos', pilot)
        self.assertEqual(guide.count('type="checkbox"'), 12)
        self.assertEqual(len(self.slugs), 16)

    def test_each_app_reaches_every_other_app_without_javascript(self):
        for slug in self.slugs:
            page = Links((ROOT/'apps'/slug/'index.html').read_text(encoding='utf-8'))
            for other in self.slugs - {slug}:
                self.assertIn('/apps/'+other+'/', page.links, slug+' -> '+other)
            self.assertIn('/#rede-apps', page.links)
            self.assertIn('/apps/guia-de-uso.html', page.links)
            self.assertEqual(page.ids.count('pd-network-title'),1,slug)
            self.assertEqual(len(page.ids),len(set(page.ids)),slug)
    def test_home_and_catalog_promote_every_app_and_shortcuts_resolve(self):
        for path in ['index.html','apps/index.html']:
            page=Links((ROOT/path).read_text(encoding='utf-8'))
            for slug in self.slugs:self.assertIn('/apps/'+slug+'/',page.links,path)
            for href in page.links:
                if href.startswith('#'):self.assertIn(href[1:],page.ids,path+' '+href)
            self.assertEqual(len(page.ids),len(set(page.ids)),path)
    def test_guide_links_and_anchors_resolve(self):
        page = Links((ROOT/'apps/guia-de-uso.html').read_text(encoding='utf-8'))
        self.assertEqual(len(page.ids), len(set(page.ids)))
        for slug in self.slugs:
            self.assertIn('/apps/'+slug+'/', page.links)
        for href in page.links:
            if href.startswith('#'):
                self.assertIn(href[1:], page.ids)
            elif href.startswith('/'):
                dest = ROOT / href.split('#')[0].lstrip('/')
                self.assertTrue(dest.exists(), href)
        for source in ['index.html', 'apps/index.html']:
            self.assertIn('/apps/guia-de-uso.html', Links((ROOT/source).read_text(encoding='utf-8')).links)

    def test_legacy_explore_cards_link_to_contextual_praia_digital_resources(self):
        destinations = {
            'comparador-cidades': ('/guias/ficha-comparacao-bairros-litoral.html#ficha',),
            'valor-imovel': ('/apps/guia-de-uso.html#comprar',),
            'calculadora-consorcio': (
                '/apps/guia-de-uso.html#comprar',
                '/guias/usar-apps-com-evidencias.html#registro',
            ),
            'checklist-vistoria': ('/apps/guia-de-uso.html#revisao-anuncios',),
        }
        for slug, hrefs in destinations.items():
            with self.subTest(app=slug):
                html = (ROOT/'apps'/slug/'index.html').read_text(encoding='utf-8')
                heading = '🔗 Explore mais</h2>'
                self.assertEqual(html.count(heading), 1)
                card = html.split(heading, 1)[1].split('</div>', 1)[0]
                explore = Links(card)
                page = Links(html)
                self.assertFalse(any('github.io/asf-app' in href for href in page.links))
                for href in hrefs:
                    self.assertIn(href, explore.links)
                    self.assertEqual(page.links.count(href), 1, href)
                    path, anchor = href.split('#')
                    target = Links((ROOT/path.lstrip('/')).read_text(encoding='utf-8'))
                    self.assertEqual(target.ids.count(anchor), 1, href)

    def test_daily_rate_resource_connects_catalog_and_seasonal_tools(self):
        resource = '/ferramentas/calculadora-diaria-ideal-airbnb-2026.html'
        catalog = (ROOT/'apps/index.html').read_text(encoding='utf-8')
        primary, extras = catalog.split('aria-label="Outros recursos"', 1)
        self.assertNotIn(resource + '#form-calculo', Links(primary).links)
        self.assertIn(resource + '#form-calculo', Links(extras.split('</nav>', 1)[0]).links)
        self.assertEqual(len(self.slugs), 16)
        daily = (ROOT/resource.lstrip('/')).read_text(encoding='utf-8')
        self.assertEqual(Links(daily).ids.count('form-calculo'), 1)
        next_steps = daily.split('aria-labelledby="proximos-passos-temporada"', 1)[1].split('</nav>', 1)[0]
        self.assertEqual(Links(next_steps).links, [
            '/apps/simulador-roi-temporada/', '/apps/temporada-ou-anual/', '/apps/',
        ])
        self.assertIn('Os dados não passam automaticamente', next_steps)
        self.assertIn('scroll-margin-top:100px', daily.split('#form-calculo,', 1)[1].split('}', 1)[0])

    def test_registry_and_generated_navigation_are_current(self):
        self.assertEqual(builder.build(check=True),[])

if __name__ == '__main__': unittest.main()
