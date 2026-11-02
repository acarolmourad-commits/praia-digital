import copy
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / file)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
builder = load('bulletin', 'gerar_boletim_diario.py')
queue = load('queue', 'prepare_bulletin_candidates.py')

class BulletinTests(unittest.TestCase):
    def setUp(self):
        self.edition = json.loads((ROOT / 'data/boletim/edicoes/2026-11-02.json').read_text())
    def test_verified_metadata(self):
        builder.validate(self.edition)
        for item in self.edition['items']:
            self.assertLessEqual(item['published_at'], item['checked_at'][:10])
    def test_reject_unreviewed_and_invalid_dates(self):
        for mutate in [lambda e:e.update(status='draft'),lambda e:e['items'][0].update(status='pending'),lambda e:e['items'][0].update(source_url='javascript:alert(1)'),lambda e:e['items'][0].update(published_at='2099-01-01'),lambda e:e['items'][0].update(checked_at='2099-01-01T00:00:00Z')]:
            e=copy.deepcopy(self.edition);mutate(e)
            with self.assertRaises(ValueError): builder.validate(e)
    def test_no_duplicate_or_missing_sources(self):
        e=copy.deepcopy(self.edition);e['items'].append(e['items'][0])
        with self.assertRaises(ValueError):builder.validate(e)
        e=copy.deepcopy(self.edition);del e['items'][0]['source_name']
        with self.assertRaises(ValueError):builder.validate(e)
    def test_reject_future_review(self):
        from datetime import datetime, timezone
        with self.assertRaises(ValueError):
            builder.validate(self.edition, as_of=datetime(2026, 11, 1, tzinfo=timezone.utc))
    def test_html_escaping(self):
        e=copy.deepcopy(self.edition);e['items'][0]['title']='<script>alert(1)</script>'
        html=builder.render_edition(ROOT,e,'/test.html')
        self.assertIn('&lt;script&gt;',html);self.assertNotIn('<script>alert(1)</script>',html)
    def test_reproducible_and_no_fake_clock(self):
        out=ROOT/'docs/inteligencia'
        files=list(out.glob('*.html'))+[out/'feed.xml', ROOT/'sitemap-boletim.xml']
        before={p:p.read_bytes() for p in files};builder.build(ROOT)
        for p,data in before.items():self.assertEqual(p.read_bytes(),data,str(p))
        self.assertNotIn('new Date', (ROOT/'js/boletim.js').read_text())
    def test_current_page_integrity(self):
        html=(ROOT/'docs/inteligencia/boletim-diario.html').read_text()
        for phrase in ['Yield ~','Score 99','Sem dados inventados','158.2%']:
            self.assertNotIn(phrase,html)
        for phrase in ['rel="canonical"','application/ld+json','última revisão'.lower(),'feed.xml']:
            self.assertIn(phrase,html.lower())
        latest=json.loads(sorted((ROOT/'data/boletim/edicoes').glob('*.json'))[-1].read_text())
        self.assertEqual(html.count('class="bulletin-card news-item"'),len(latest['items']))
    def test_rss_has_permanent_dates(self):
        root=ET.parse(ROOT/'docs/inteligencia/feed.xml').getroot()
        self.assertEqual(root.tag,'rss');items=root.findall('./channel/item');self.assertTrue(items)
        self.assertEqual(len({i.findtext('guid') for i in items}),len(items))
        for item in items:self.assertIn('boletim-2026-',item.findtext('link'))
    def test_supplementary_sitemap(self):
        validator=load('sitemap_gate','validate_sitemap_targets.py')
        self.assertEqual(validator.validate_sitemap(ROOT/'sitemap-boletim.xml',ROOT),[])
        self.assertIn('Sitemap: https://praia.digital/sitemap-boletim.xml',(ROOT/'robots.txt').read_text())
        ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls=ET.parse(ROOT/'sitemap-boletim.xml').findall('s:url',ns)
        self.assertEqual(len(urls),len(list((ROOT/'data/boletim/edicoes').glob('*.json'))))
        for url in urls:
            self.assertTrue(url.findtext('s:loc',namespaces=ns).startswith('https://praia.digital/docs/inteligencia/boletim-'))
            builder.stamp(url.findtext('s:lastmod',namespaces=ns))
    def test_newsletter_cannot_claim_signup(self):
        html=(ROOT/'newsletter/assinatura.html').read_text()
        self.assertNotIn('subscribeForm',html);self.assertNotIn('Confira sua caixa de entrada',html)
        self.assertNotIn('<form',html);self.assertIn('não está ativa',html)
        self.assertNotIn('Cadastro simulado',(ROOT/'assets/js/cta-newsletter.js').read_text())
    def test_missing_feed_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=queue.prepare(Path(tmp));self.assertEqual(result['status'],'source_state_missing');self.assertEqual(result['candidates'],[])
    def test_queue_never_promotes_detection_date(self):
        result=queue.prepare(ROOT)
        for item in result['candidates']:
            self.assertIsNone(item['published_at']);self.assertEqual(item['status'],'needs_editorial_review')
    def test_internal_links_exist(self):
        import re
        for p in [ROOT/'docs/inteligencia/boletim-diario.html',ROOT/'newsletter/assinatura.html']:
            for link in re.findall(r'(?:href|src)="(/[^"]*)"',p.read_text()):
                target=ROOT/link.split('?')[0].lstrip('/')
                self.assertTrue(target.exists(),f'{p}: {link}')

if __name__=='__main__':unittest.main()
