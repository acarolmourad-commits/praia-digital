"""Offline regressions: no real HTTP, issue writes, or repository scans."""
from contextlib import redirect_stdout
import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
SPEC = importlib.util.spec_from_file_location('inspector', ROOT / 'scripts/site_inspector.py')
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)
MONDAY = datetime.date(2026, 11, 16)


class InspectorTests(unittest.TestCase):
    def setUp(self):
        # An incomplete mock must fail the test instead of making a real request.
        for target in ('socket.getaddrinfo', 'socket.socket.connect', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError('Unexpected network access'))
            guard.start()
            self.addCleanup(guard.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def test_import_has_no_scanning_or_publication_side_effect(self):
        module = importlib.util.module_from_spec(SPEC)
        with patch.object(Path, 'rglob', side_effect=AssertionError('Import must be inert')):
            SPEC.loader.exec_module(module)

    def test_html_parser_reads_attribute_variants_but_not_script_strings(self):
        html = '''<A HREF = '/a?x=1&amp;y=2'>a</A><img src=photo.jpg>
        <video poster="cover.jpg"></video><form action='/send'></form>
        <button formaction="/other"></button><blockquote cite="/source"></blockquote>
        <script>const example = '<a href="/not-a-real-link">';</script>
        <!-- <a href='/comment'> -->'''
        links = inspector.References(html).links
        self.assertEqual(len(links), 2)
        self.assertIn('/a?x=1&y=2', links)
        self.assertIn('photo.jpg', links)

    def test_local_paths_queries_encoding_and_same_domain_urls(self):
        self.write('blog/ação.html', 'ok')
        self.write('apps/demo/index.html', 'ok')
        for url in ('../blog/a%C3%A7%C3%A3o.html?x=1#intro',
                    'https://praia.digital/blog/a%C3%A7%C3%A3o.html#intro',
                    '//praia.digital/blog/a%C3%A7%C3%A3o.html',
                    '//www.praia.digital/blog/a%C3%A7%C3%A3o.html'):
            kind, target = inspector.reference(url, 'cidades/itanhaem.html')
            self.assertEqual(kind, 'internal')
            self.assertTrue(inspector.local_exists(target, self.root))
        self.assertTrue(inspector.local_exists('/apps/demo/', self.root))
        self.assertTrue(inspector.local_exists('/blog/ação', self.root))
        self.assertFalse(inspector.local_exists('/blog/', self.root))
        self.assertFalse(inspector.local_exists('/missing.html', self.root))

    def test_path_traversal_and_symlinks_do_not_escape_checkout(self):
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / 'secret.html'
            outside.write_text('outside')
            (self.root / 'alias.html').symlink_to(outside)
            self.assertFalse(inspector.local_exists('/alias.html', self.root))
            self.assertFalse(inspector.local_exists('/../' + outside.as_posix(), self.root))
            self.assertFalse(inspector.local_exists('/bad\x00', self.root))

    def test_base_tag_and_protocol_relative_urls(self):
        page = inspector.References('<base href="/apps/demo/"><a href="guide.html">x</a>')
        self.assertEqual(inspector.reference('guide.html', 'index.html', page.base),
                         ('internal', '/apps/demo/guide.html'))
        self.assertEqual(inspector.reference('//EXAMPLE.org/a#one', 'index.html'),
                         ('external', 'https://example.org/a'))

    def test_external_unicode_spaces_and_default_ports_are_normalized(self):
        kind, url = inspector.reference('https://EXAMPLE.org:443/ação aqui?q=São Paulo#top', 'index.html')
        self.assertEqual(kind, 'external')
        self.assertEqual(url, 'https://example.org/a%C3%A7%C3%A3o%20aqui?q=S%C3%A3o%20Paulo')
        self.assertEqual(inspector.reference('https://user:pass@example.org/', 'index.html')[0], 'ignored')
        self.assertEqual(inspector.reference('https://[broken', 'index.html')[0], 'ignored')

    def test_scan_accounts_for_duplicates_skips_and_real_missing_files(self):
        self.write('index.html', '''<a HREF = '/missing.html'>Missing</a><a href='/missing.html'>Again</a>
        <a href="https://example.org/a#one">one</a><a href="https://example.org/a#two">two</a>
        <form action="https://example.org/submit"></form><a href="#top">top</a>
        <a href="mailto:a@example.org">mail</a><a href="${dynamic}">template</a>''')
        self.write('social/unused.html', '<a href="/skip">x</a>')
        counts, ignored, broken, _, errors, urls = inspector.scan(self.root)
        self.assertEqual(counts['pages_scanned'], 1)
        self.assertEqual(counts['references_extracted'], 6)
        self.assertEqual(counts['internal_checked'], 2)
        self.assertEqual(counts['external_references'], 2)
        self.assertEqual(sum(ignored.values()), 2)
        self.assertEqual(broken, [{'page': 'index.html', 'link': '/missing.html'}])
        self.assertEqual(list(urls), ['https://example.org/a'])
        self.assertEqual(errors, [])

    def test_sample_is_unique_bounded_and_rotates_over_all_candidates(self):
        urls = [f'https://example.org/{i:03}' for i in range(165)]
        batches = [inspector.weekly_sample(urls + urls, MONDAY + datetime.timedelta(weeks=i))
                   for i in range(3)]
        self.assertEqual(set().union(*map(set, batches)), set(urls))
        self.assertTrue(all(len(batch) <= 80 for batch in batches))
        self.assertEqual(sum(map(len, batches)), 165)
        self.assertEqual(inspector.weekly_sample(urls, MONDAY),
                         inspector.weekly_sample(list(reversed(urls)), MONDAY))
        self.assertEqual(inspector.weekly_sample([], MONDAY), [])

    def test_status_categories_do_not_mislabel_access_blocks_as_broken(self):
        for status, expected in {200: 'ok', 204: 'ok', 301: 'redirect', 404: 'broken',
                                 410: 'broken', 401: 'access_blocked', 403: 'access_blocked',
                                 429: 'rate_limited', 408: 'transient_http', 503: 'transient_http',
                                 400: 'review'}.items():
            self.assertEqual(inspector.classify_status(status), expected)
        self.assertEqual(inspector.classify_status(200, True), 'redirect')
        self.assertEqual(inspector.classify_status(404, True), 'broken')

    def response(self, status=200, url='https://example.org/a'):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = status
        response.geturl.return_value = url
        return response

    def test_head_fallback_is_read_only_and_closes_response_without_reading(self):
        response = self.response()
        opener = MagicMock()
        opener.open.side_effect = [HTTPError('https://example.org/a', 405, 'Not allowed', {}, None), response]
        with patch.object(inspector, 'public_url'), patch.object(inspector.urllib.request, 'build_opener', return_value=opener):
            result = inspector.check_external('https://example.org/a')
        self.assertEqual(result['category'], 'ok')
        self.assertEqual(result['method'], 'GET')
        self.assertEqual([call.args[0].get_method() for call in opener.open.call_args_list], ['HEAD', 'GET'])
        for call in opener.open.call_args_list:
            self.assertEqual(call.kwargs['timeout'], 12)
            self.assertIsNone(call.args[0].data)
            self.assertFalse(call.args[0].has_header('Authorization'))
        response.read.assert_not_called()
        response.__exit__.assert_called_once()

    def test_http_errors_redirects_and_network_failures_are_recorded(self):
        for failure, expected in [(HTTPError('https://example.org/a', 404, 'Missing', {}, None), 'broken'),
                                  (HTTPError('https://example.org/a', 429, 'Limited', {}, None), 'rate_limited'),
                                  (URLError('timeout'), 'network_error')]:
            opener = MagicMock()
            opener.open.side_effect = failure
            with patch.object(inspector, 'public_url'), patch.object(inspector.urllib.request, 'build_opener', return_value=opener):
                self.assertEqual(inspector.check_external('https://example.org/a')['category'], expected)
        opener = MagicMock()
        opener.open.return_value = self.response(url='https://example.org/new')
        with patch.object(inspector, 'public_url'), patch.object(inspector.urllib.request, 'build_opener', return_value=opener):
            result = inspector.check_external('https://example.org/a')
        self.assertEqual(result['category'], 'redirect')
        self.assertEqual(result['final_url'], 'https://example.org/new')

    def test_private_targets_and_redirects_are_not_requested(self):
        with patch.object(inspector.socket, 'getaddrinfo', return_value=[(2, 1, 6, '', ('127.0.0.1', 443))]):
            with self.assertRaises(ValueError):
                inspector.public_url('https://example.org/')
            self.assertEqual(inspector.check_external('https://example.org/')['category'], 'not_checked')
            with self.assertRaises(ValueError):
                inspector.PublicRedirects().redirect_request(Request('https://example.org/'), None, 302,
                                                            'Found', {}, 'http://127.0.0.1/')
        for url in ('file:///etc/passwd', 'https://user:pass@example.org/', 'http://example.org:8080/'):
            with self.assertRaises(ValueError):
                inspector.public_url(url)

    def test_external_report_has_explicit_partial_and_disabled_coverage(self):
        urls = {f'https://example.org/{i}': {'page': 'index.html', 'attribute': 'href'} for i in range(85)}
        with patch.object(inspector, 'check_external') as check:
            report = inspector.external_report(urls, False, MONDAY)
            check.assert_not_called()
        self.assertEqual(report['status'], 'not_run')
        self.assertEqual(report['pending'], 85)
        with patch.object(inspector, 'check_external', side_effect=lambda u: {'url': u, 'category': 'transient'}):
            report = inspector.external_report(urls, True, MONDAY)
        self.assertEqual(report['http_responses'], 0)
        self.assertGreater(report['selected'], 0)
        self.assertEqual(report['selected_without_response'], report['selected'])
        self.assertEqual(report['selected'] + report['pending'], 85)

    def test_artifact_keeps_full_list_of_missing_internal_references(self):
        links = [f'/missing-{i}' for i in range(inspector.DETAIL_LIMIT + 1)]
        self.write('index.html', ''.join(f'<a href="{link}">page</a>' for link in links))
        with redirect_stdout(io.StringIO()):
            inspector.main(['--root', str(self.root), '--no-publish'])
        report = json.loads((self.root / 'site_inspection_report.json').read_text())
        self.assertCountEqual([r['link'] for r in report['broken_links']], links)
        self.assertEqual(report['totals']['broken'], len(report['broken_links']))

    def test_main_writes_report_without_publishing_and_marks_empty_coverage_failed(self):
        self.write('index.html', '<a href="/missing">x</a><a href="https://example.org/a">external</a>')
        with patch.object(inspector, 'publish_issue') as publish, patch.dict(os.environ, {}, clear=True), redirect_stdout(io.StringIO()):
            self.assertEqual(inspector.main(['--root', str(self.root), '--no-publish']), 0)
            publish.assert_not_called()
        report = json.loads((self.root / 'site_inspection_report.json').read_text())
        self.assertTrue(report['coverage_ok'])
        self.assertEqual(report['totals']['broken'], 1)
        self.assertEqual(report['external']['status'], 'not_run')
        self.assertEqual(report['external_links'], ['https://example.org/a'])
        self.assertFalse(report['coverage']['external_http_checked'])
        self.assertEqual(report['status'], 'needs_review')
        self.write('index.html', '<p>No links were extracted</p>')
        with patch.object(inspector, 'publish_issue') as publish, patch.dict(os.environ, {}, clear=True), redirect_stdout(io.StringIO()):
            self.assertEqual(inspector.main(['--root', str(self.root)]), 1)
            publish.assert_not_called()

    def test_external_findings_cannot_open_internal_issue(self):
        self.write('index.html', '<a href="https://example.org/a">external</a>')
        with patch.object(inspector, 'check_external', return_value={'url': 'https://example.org/a', 'status': 404, 'category': 'broken'}), patch.dict(os.environ, {'GITHUB_TOKEN': 'test-only'}, clear=True), redirect_stdout(io.StringIO()):
            # urlopen is guarded: any attempt to open/update an issue fails this test.
            self.assertEqual(inspector.main(['--root', str(self.root), '--external']), 0)
        report = json.loads((self.root / 'site_inspection_report.json').read_text())
        self.assertEqual(report['external']['categories'], {'broken': 1})
        body = inspector.issue_body(MONDAY, 1, [], [])
        self.assertNotIn('https://example.org/a', body)
        self.assertIn('sem presumir erro', body)
        self.assertIn('nao autoriza reescrever artigos', body)

    def test_workflow_preserves_21_slots_and_isolates_prs_from_inspection(self):
        workflow = (ROOT / '.github/workflows/site-inspector.yml').read_text()
        crons = re.findall(r"cron: '([^']+)'", workflow)
        slots = []
        for cron in crons:
            minute, hours, _, _, days = cron.split()
            expanded = range(7) if days == '*' else ([0, 2, 3, 4, 5, 6] if days == '0,2-6' else [int(days)])
            slots.extend((day, int(hour), int(minute)) for day in expanded for hour in hours.split(','))
        self.assertEqual(len(slots), 21)
        self.assertEqual(set(slots), {(d, h, 0) for d in range(7) for h in (11, 17, 23)})
        self.assertIn("github.event_name != 'pull_request'", workflow)
        self.assertIn("github.event.schedule == '0 11 * * 1'", workflow)
        self.assertEqual(workflow.count('issues: write'), 1)
        self.assertIn('retention-days: 30', workflow)
        self.assertIn('needs: test', workflow)
        self.assertIn('test_link_inventory.py', workflow)
        self.assertIn('inputs.check_external', workflow)
        self.assertIn('args+=(--no-publish)', workflow)


if __name__ == '__main__':
    unittest.main()
