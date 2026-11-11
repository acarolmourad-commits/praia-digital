import copy
import io
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import marketplaces_editorial as editorial
import sentinela_airbnb_booking as monitor


class EditorialTests(unittest.TestCase):
    def setUp(self):
        self.data = editorial.load_editorial()
        self.state = json.loads(Path(monitor.STATE).read_text())

    def validate_data(self, data):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'editorial.json'
            path.write_text(json.dumps(data))
            return editorial.load_editorial(path)

    def test_source_dates_and_coverage(self):
        self.assertEqual(len(self.data['articles']), 10)
        self.assertEqual(sum(a['platform'] == 'Booking.com' for a in self.data['articles']), 2)
        by_file = {a['file']: a for a in self.data['articles']}
        for old in self.state['articles']:
            # New detections after this edition can remain explicitly unreviewed.
            if old['date'][:10] <= '2026-11-10':
                self.assertIn(old['file'], by_file)
        self.assertEqual(by_file['novidades-20261021-194712-airbnb-resources.html']['source_published'], '2026-09-30')
        self.assertEqual(by_file['novidades-20261110-111146-airbnb-news.html']['source_published'], '2026-11-09')

    def test_reviewed_sitemap(self):
        import validate_sitemap_targets as validator
        self.assertEqual(validator.validate_sitemap(ROOT / 'sitemap-marketplaces.xml', ROOT), [])
        self.assertIn('Sitemap: https://praia.digital/sitemap-marketplaces.xml', (ROOT / 'robots.txt').read_text())
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = ET.parse(ROOT / 'sitemap-marketplaces.xml').findall('s:url', ns)
        expected = {'https://praia.digital/blog/' + a['file'] for a in self.data['articles']}
        expected.add('https://praia.digital/blog/novidades-airbnb-booking.html')
        self.assertEqual({u.findtext('s:loc', namespaces=ns) for u in urls}, expected)
        for url in urls:
            self.assertEqual(url.findtext('s:lastmod', namespaces=ns), self.data['reviewed_on'])

    def test_invalid_source_paths_dates_and_duplicates_rejected(self):
        mutations = [
            lambda d: d.update(reviewed_on='2099-01-01'),
            lambda d: d['articles'][0].update(file='../index.html'),
            lambda d: d['articles'][0].update(source_published='2099-01-01'),
            lambda d: d['articles'][0]['sources'][0].update(url='javascript:alert(1)'),
            lambda d: d['articles'][0]['sources'][0].update(url='https://news.airbnb.com.evil.example/test'),
            lambda d: d['articles'][0]['sources'][0].update(date='2099-01-01'),
            lambda d: d['articles'].append(d['articles'][0]),
            lambda d: d['articles'][0].update(related_file='missing.html'),
        ]
        for mutate in mutations:
            data = copy.deepcopy(self.data)
            mutate(data)
            with self.assertRaises(ValueError):
                self.validate_data(data)

    def test_reproducible_publication_preserves_review(self):
        with tempfile.TemporaryDirectory() as temp:
            editorial.render_publication(self.state, temp, self.data)
            before = {p.name: p.read_bytes() for p in Path(temp).glob('*.html')}
            editorial.render_publication(self.state, temp, self.data)
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(temp).glob('*.html')})
            for name, body in before.items():
                self.assertEqual(body, (ROOT / 'blog' / name).read_bytes(), name)

    def test_content_integrity_and_links(self):
        names = ['novidades-airbnb-booking.html'] + [a['file'] for a in self.data['articles']]
        for name in names:
            body = (ROOT / 'blog' / name).read_text()
            self.assertEqual(len(re.findall(r'<h1\b', body)), 1, name)
            self.assertIn('rel="canonical" href="https://praia.digital/blog/' + name + '"', body)
            self.assertNotIn('Pode afetar anuncio, preco, calendario', body)
            self.assertNotIn('em tempo real →', body)
            for url in re.findall(r'href="(/[^"]*)"', body):
                path = ROOT / url.split('?')[0].split('#')[0].lstrip('/')
                self.assertTrue(path.exists(), f'{name}: {url}')
        tools = (ROOT / 'blog/novidades-20261021-194712-airbnb-resources.html').read_text()
        for text in ['30/09/2026', '2026-10-21 19:47 UTC', 'LiDAR', 'PriceLabs', 'América Latina']:
            self.assertIn(text, tools)
        index = (ROOT / 'blog/novidades-airbnb-booking.html').read_text()
        self.assertIn('assinatura por e-mail ainda não ativa', index)
        self.assertIn('Pesquisa de tendências', index)
        if any(s.get('status') != 200 or s.get('unavailable') for s in self.state['sources'].values()):
            self.assertIn('Conteúdo não pôde ser validado', index)

    def test_source_coverage_handles_recovery_and_failure(self):
        sources = {'test': {'name': 'Booking', 'url': 'https://news.booking.com/', 'status': 200}}
        self.assertNotIn('Conteúdo não pôde ser validado', editorial.index_html([], self.data, sources))
        sources['test'].update(status=403, unavailable=True)
        self.assertIn('Conteúdo não pôde ser validado', editorial.index_html([], self.data, sources))

    def test_html_escaping(self):
        data = copy.deepcopy(self.data['articles'][0])
        data['title'] = '<script>alert(1)</script>'
        body = editorial.article_html(data, self.data['reviewed_on'])
        self.assertIn('&lt;script&gt;', body)
        self.assertNotIn('<script>alert(1)</script>', body)

    def test_unreviewed_links_are_not_promoted(self):
        source = monitor.SOURCES[1]
        body = monitor.article_html('Airbnb', 'Link detectado', '2026-11-11 10:00 UTC', [('https://news.airbnb.com/new-long-news-title', 'Título da fonte')], source, False, 'novidades-test.html')
        self.assertIn('Data original de publicação não confirmada', body)
        self.assertIn('sem revisão editorial', body)
        self.assertIn('href="https://praia.digital/blog/novidades-test.html"', body)

    def test_extract_official_absolute_relative_links_only(self):
        source = next(s for s in monitor.SOURCES if s['id'] == 'booking-news')
        body = '''<a href="https://news.booking.com/some-official-news-title/?utm=test">Título oficial da notícia</a>
        <a href="/another-official-news-title/">Outra notícia oficial</a>
        <a href="https://evil.example/another-official-news-title">Não oficial</a>
        <a href="javascript:alert(1)">Não seguro</a>'''
        result = monitor.extract_items(body, source)
        self.assertEqual(len(result), 2)
        self.assertIn('https://news.booking.com/some-official-news-title', result)

    def run_monitor(self, state, source, response):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            state_path = base / 'state.json'
            state_path.write_text(json.dumps(state))
            with patch.multiple(monitor, STATE=str(state_path), REPORT=str(base / 'report.md'), OUTDIR=str(base / 'blog'), SOURCES=[source]), patch.object(monitor, 'fetch', return_value=response), patch.object(sys, 'argv', ['sentinela']), patch.dict('os.environ', {'GITHUB_OUTPUT': ''}), redirect_stdout(io.StringIO()):
                monitor.main()
            return json.loads(state_path.read_text()), (base / 'report.md').read_text(), {p.name: p.read_text() for p in (base / 'blog').glob('*.html')}

    def test_hash_change_never_publishes_news(self):
        source = next(s for s in monitor.SOURCES if s['id'] == 'booking-join')
        state = {'sources': {source['id']: {'hash': 'old-hash'}}, 'articles': []}
        after, report, pages = self.run_monitor(state, source, (200, '<h1>Changed page</h1>'))
        self.assertEqual(after['articles'], [])
        self.assertIn('Nenhum post publicado', report)
        self.assertEqual(len(pages), 11)  # reviewed pages + index, no hash article

    def test_unavailable_source_retains_history(self):
        source = monitor.SOURCES[1]
        state = {'sources': {source['id']: {'seen': {'https://news.airbnb.com/existing-official-news': 'Existing'}, 'hash': 'old'}}, 'articles': []}
        after, report, pages = self.run_monitor(state, source, (403, 'ERROR forbidden'))
        self.assertEqual(after['sources'][source['id']]['seen'], state['sources'][source['id']]['seen'])
        self.assertTrue(after['sources'][source['id']]['unavailable'])
        self.assertIn('checked_at', after['sources'][source['id']])
        self.assertEqual(after['articles'], [])

    def test_new_detection_does_not_overwrite_editorial(self):
        source = monitor.SOURCES[1]
        state = {'sources': {source['id']: {'seen': {'https://news.airbnb.com/existing-official-news': 'Existing'}}}, 'articles': []}
        after, report, pages = self.run_monitor(state, source, (200, '<a href="/another-official-news-headline">New official headline</a>'))
        self.assertEqual(len(after['articles']), 1)
        self.assertIn('sem revisão editorial', pages[after['articles'][0]['file']])
        self.assertIn('LiDAR', pages['novidades-20261021-194712-airbnb-resources.html'])
        self.assertIn('Links detectados ainda sem revisão', pages['novidades-airbnb-booking.html'])

    def test_more_than_five_links_are_not_lost(self):
        source = monitor.SOURCES[1]
        state = {'sources': {source['id']: {'seen': {'https://news.airbnb.com/existing-official-news': 'Existing'}}}, 'articles': []}
        body = ''.join(f'<a href="/another-official-news-headline-{i}">New official headline {i}</a>' for i in range(8))
        after, report, pages = self.run_monitor(state, source, (200, body))
        published = pages[after['articles'][0]['file']]
        for i in range(8):
            self.assertIn(f'/another-official-news-headline-{i}', published)


if __name__ == '__main__':
    unittest.main()
