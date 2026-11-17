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

    def test_registry_and_generated_navigation_are_current(self):
        self.assertEqual(builder.build(check=True),[])

if __name__ == '__main__': unittest.main()
