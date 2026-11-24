import hashlib
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/app-interactions.json'
REGISTRY = json.loads((ROOT / 'data/app-network.json').read_text(encoding='utf-8'))
SLUGS = [app['slug'] for group in REGISTRY for app in group['apps']]
PAGES = ['index.html', 'apps/index.html', *(f'apps/{slug}/index.html' for slug in SLUGS)]


class Interactions(HTMLParser):
    """Keep ordered script tags, inline code digests and form controls visible in diffs."""

    def __init__(self, source):
        super().__init__()
        self.scripts = []
        self.controls = []
        self.inline = None
        self.heading_id = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.heading_id = dict(attrs).get('id')
        if tag in {'input', 'select', 'textarea', 'button'}:
            self.controls.append(self.get_starttag_text())
        if tag == 'script' and dict(attrs).get('type', '').lower() != 'application/ld+json':
            self.scripts.append(self.get_starttag_text())
            self.inline = []

    def handle_data(self, data):
        if self.inline is not None:
            self.inline.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.inline is not None:
            body = ''.join(self.inline)
            if body.strip():
                digest = hashlib.sha256(body.encode('utf-8')).hexdigest()
                self.scripts[-1] += ' sha256:' + digest
            self.inline = None


class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.labels=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='label' and 'for' in a:self.labels.append(a['for'])
        if tag=='h1':self.h1+=1
class NetworkTests(unittest.TestCase):
    def test_structure_and_targets(self):
        for path in PAGES:
            with self.subTest(path=path):
                text=(ROOT/path).read_text();page=Page(text)
                self.assertEqual(page.h1,1);self.assertEqual(len(page.ids),len(set(page.ids)))
                self.assertTrue(set(page.labels)<=set(page.ids));self.assertNotIn('//',page.links)
                self.assertIn('/css/app-network.css',text)
                if path.startswith('apps/'):
                    self.assertIn('pd-network-title',page.ids)
                    for slug in SLUGS:
                        if path!='apps/'+slug+'/index.html':self.assertIn('/apps/'+slug+'/',page.links)
    def test_interactions_match_reviewed_pages(self):
        expected = json.loads(FIXTURE.read_text(encoding='utf-8'))
        self.assertEqual(set(expected), set(PAGES))
        for path in PAGES:
            page = Interactions((ROOT / path).read_text(encoding='utf-8'))
            with self.subTest(page=path, element='heading'):
                self.assertEqual(page.heading_id, expected[path]['heading_id'])
            with self.subTest(page=path, element='scripts'):
                self.assertEqual(page.scripts, expected[path]['scripts'])
            with self.subTest(page=path, element='controls'):
                self.assertEqual(page.controls, expected[path]['controls'])

    def test_home_has_single_journeys_section(self):
        text=(ROOT/'index.html').read_text();page=Page(text)
        self.assertEqual(page.ids.count('jornadas-apps'),1)
        for slug in SLUGS:self.assertIn('/apps/'+slug+'/',page.links)
if __name__=='__main__':unittest.main()
