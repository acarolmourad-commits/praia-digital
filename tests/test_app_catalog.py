"""Public discovery paths must remain connected after the Pages navigation build."""
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

catalog = module('catalog', 'scripts/build_app_catalog.py')
nav = module('nav', 'scripts/build-navigation.py')

class CatalogTest(unittest.TestCase):
    def test_catalog_and_home_reach_every_app(self):
        for file in ['index.html', 'apps/index.html']:
            text = (ROOT / file).read_text()
            for app in catalog.APPS:
                self.assertIn('href="/apps/' + app[0] + '/"', text, file)
                self.assertTrue((ROOT / 'apps' / app[0] / 'index.html').is_file())

    def test_every_app_reaches_every_other_app(self):
        for current in catalog.APPS:
            text = (ROOT / 'apps' / current[0] / 'index.html').read_text()
            footer = re.search(r'<section class="pd-network".*?</section>', text, re.S).group()
            self.assertEqual(text.count('id="pd-network-title"'), 1)
            for target in catalog.APPS:
                if current != target:
                    self.assertIn('href="/apps/' + target[0] + '/"', footer)

    def test_navigation_build_preserves_catalog_journey(self):
        text = (ROOT / 'apps/index.html').read_text()
        built, changed = nav.transform(text, (ROOT / 'partials/header.html').read_text())
        self.assertTrue(changed)
        self.assertEqual(len(re.findall(r'<h1\b', built)), 1)
        self.assertIn('class="pd-catalog-hero"', built)
        self.assertIn('Encontrar minha ferramenta', built)
        self.assertEqual(built.count('class="pd-catalog-card"'), 16)

if __name__ == '__main__':
    unittest.main()
