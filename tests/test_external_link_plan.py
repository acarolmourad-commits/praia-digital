"""Offline planning and HTTP classification regressions; sockets are guarded."""
from contextlib import redirect_stdout
import datetime
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import external_link_plan as planner
import site_inspector as inspector

NOW = datetime.datetime(2026, 11, 17, 12, tzinfo=datetime.timezone.utc)


class PlannerTests(unittest.TestCase):
    def setUp(self):
        for target in ('socket.getaddrinfo', 'socket.socket.connect', 'urllib.request.urlopen'):
            guard = patch(target, side_effect=AssertionError('Unexpected network access'))
            guard.start()
            self.addCleanup(guard.stop)
        self.history = {'version': 1, 'urls': {}, 'hosts': {}}

    def candidates(self, hosts=10, count=40):
        return {f'https://h{h}.example/{n:03}': {'page': 'blog/example.html'}
                for h in range(hosts) for n in range(count)}

    def test_plan_is_deterministic_capped_and_has_no_duplicate(self):
        urls = self.candidates()
        first = planner.plan_external(urls, self.history, NOW)
        second = planner.plan_external(dict(reversed(list(urls.items()))), self.history, NOW)
        self.assertEqual(first, second)
        selected = [r['url'] for r in first['results']]
        self.assertEqual(len(selected), 80)
        self.assertEqual(len(set(selected)), 80)
        self.assertLessEqual(max(first['host_counts'].values()), 20)
        self.assertFalse(first['network_performed'])

    def test_priority_has_reserved_capacity_and_breadth_is_preserved(self):
        urls = self.candidates()
        urls.update({f'https://risk{h}.example/{n:03}': {'page': 'compras/index.html'}
                     for h in range(4) for n in range(10)})
        plan = planner.plan_external(urls, self.history, NOW)
        self.assertEqual(sum(r['lane'] == 'risk' for r in plan['results']), 20)
        self.assertEqual(sum(r['lane'] == 'breadth' for r in plan['results']), 60)

    def test_priority_cannot_starve_unseen_urls_on_the_same_host(self):
        urls = {f'https://same.example/risk{n}': {'page': 'index.html'} for n in range(60)}
        for url in urls:
            self.history['urls'][url] = {'last_attempt': NOW.timestamp() - 86400, 'category': 'ok'}
        urls['https://same.example/ordinary'] = {'page': 'blog/article.html'}
        plan = planner.plan_external(urls, self.history, NOW)
        self.assertIn('https://same.example/ordinary', {r['url'] for r in plan['results']})
        self.assertEqual(sum(r['lane'] == 'risk' for r in plan['results']), 5)

    def test_single_host_is_underfilled_without_claiming_error_or_coverage(self):
        plan = planner.plan_external(self.candidates(1, 200), self.history, NOW)
        self.assertEqual(plan['selected'], 20)
        self.assertEqual(plan['eligible_not_selected'], 180)
        self.assertEqual(plan['deferred'], {})

    def test_inventory_growth_does_not_skip_unseen_urls(self):
        urls = self.candidates(3, 2)
        first = planner.plan_external(urls, self.history, NOW, limit=3, priority_slots=0)
        for result in first['results']:
            self.history['urls'][result['url']] = {'last_attempt': NOW.timestamp(), 'category': 'ok'}
        urls['https://a-new.example/new'] = {'page': 'index.html'}
        second = planner.plan_external(urls, self.history, NOW + datetime.timedelta(hours=6), limit=4)
        self.assertEqual(len({r['url'] for r in first['results']} & {r['url'] for r in second['results']}), 0)
        self.assertIn('https://a-new.example/new', {r['url'] for r in second['results']})

    def test_stable_inventory_gets_full_attempt_coverage_in_three_batches(self):
        urls = self.candidates(5, 33)
        seen = set()
        for slot in range(3):
            now = NOW + datetime.timedelta(hours=6 * slot)
            plan = planner.plan_external(urls, self.history, now, priority_slots=0)
            for row in plan['results']:
                seen.add(row['url'])
                self.history['urls'][row['url']] = {'last_attempt': now.timestamp(), 'category': 'network_error'}
        self.assertEqual(seen, set(urls))

    def test_retry_after_and_host_cooldown_are_not_bypassed(self):
        urls = self.candidates(2, 2)
        target = 'https://h1.example/000'
        self.history['urls'][target] = {'last_attempt': NOW.timestamp() - 48 * 3600,
                                       'category': 'rate_limited',
                                       'retry_after_until': NOW.timestamp() + 72 * 3600}
        self.history['hosts']['h0.example'] = NOW.timestamp() + 3600
        result = planner.plan_external(urls, self.history, NOW)
        self.assertEqual(result['selected'], 1)
        self.assertEqual(result['deferred'], {'host_cooldown': 2, 'not_due': 1})
        self.assertEqual(self.history['urls'][target]['category'], 'rate_limited')

    def test_access_blocks_are_delayed_and_network_failures_have_no_response(self):
        entry = {'last_attempt': NOW.timestamp(), 'category': 'access_blocked'}
        self.assertEqual(planner.due_at(entry, 3), NOW.timestamp() + 7 * 86400)
        entry['category'] = 'network_error'
        self.assertEqual(planner.due_at(entry, 3), NOW.timestamp() + 6 * 3600)
        self.assertNotIn('last_http_response', entry)

    def test_invalid_history_fails_instead_of_resetting_cooldowns(self):
        for history in ({}, {'version': 2}, {'version': 1, 'urls': [], 'hosts': {}},
                        {'version': 1, 'urls': {'x': {'last_attempt': float('nan')}}, 'hosts': {}},
                        {'version': 1, 'urls': {'x': {'last_http_response': 1}}, 'hosts': {}},
                        {'version': 1, 'urls': {}, 'hosts': {'x': -1}}):
            with self.subTest(history=history), self.assertRaises(ValueError):
                planner.plan_external({}, history, NOW)

    def test_invalid_limits_fail(self):
        for kwargs in ({'limit': 81}, {'limit': 0}, {'per_host': 21},
                       {'priority_slots': -1}, {'limit': True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                planner.plan_external({}, self.history, NOW, **kwargs)

    def test_priority_uses_commercial_source_even_if_archive_seen_first(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'backup').mkdir()
            (root / 'backup/old.html').write_text('<a href="https://example.org/">x</a>')
            (root / 'index.html').write_text('<a href="https://example.org/">x</a>')
            urls = inspector.scan(root)[-1]
            meta = urls['https://example.org/']
            self.assertEqual(meta['priority'], 3)
            self.assertEqual(meta['priority_page'], 'index.html')
            self.assertEqual(meta['references'], 2)
            self.assertEqual(planner.page_priority('backup/apps/a.html'), 0)

    def test_cli_plan_does_not_perform_http_or_publish_issues(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'index.html').write_text('<a href="https://example.org/a?tag=unchanged">x</a>')
            with (patch.object(inspector, 'external_report', side_effect=AssertionError('HTTP mode')),
                 patch.object(inspector, 'publish_issue', side_effect=AssertionError('Issue write')),
                 redirect_stdout(io.StringIO())):
                result = inspector.main(['--root', folder, '--plan-external'])
            self.assertEqual(result, 0)
            plan = json.loads((root / 'external_inspection_plan.json').read_text())
            self.assertEqual(plan['results'][0]['url'], 'https://example.org/a?tag=unchanged')
            self.assertFalse(plan['network_performed'])
            self.assertFalse((root / 'site_inspection_report.json').exists())

    def test_cli_modes_are_mutually_exclusive(self):
        with patch('sys.stderr', io.StringIO()), self.assertRaises(SystemExit) as error:
            inspector.main(['--external', '--plan-external'])
        self.assertEqual(error.exception.code, 2)

    def test_rate_limit_records_retry_header_without_automatic_retry(self):
        opener = MagicMock()
        opener.open.side_effect = HTTPError('https://example.org/', 429, 'Limited', {'Retry-After': '3600'}, None)
        with patch.object(inspector, 'public_url'), patch.object(inspector.urllib.request, 'build_opener', return_value=opener):
            result = inspector.check_external('https://example.org/')
        self.assertEqual(result['category'], 'rate_limited')
        self.assertEqual(result['retry_after'], '3600')
        self.assertEqual(opener.open.call_count, 1)

    def test_wrapped_dns_failure_is_not_an_http_error(self):
        opener = MagicMock()
        opener.open.side_effect = URLError(socket.gaierror(-2, 'test-only DNS failure'))
        with patch.object(inspector, 'public_url'), patch.object(inspector.urllib.request, 'build_opener', return_value=opener):
            result = inspector.check_external('https://example.org/')
        self.assertEqual(result['category'], 'network_error')
        self.assertEqual(result['reason'], 'gaierror')
        self.assertNotIn('status', result)

    def test_redirect_keeps_head_instead_of_implicitly_becoming_get(self):
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code), patch.object(inspector, 'public_url'):
                request = inspector.PublicRedirects().redirect_request(
                    Request('https://example.org/', method='HEAD'), None, code,
                    'Moved', {}, 'https://other.example/')
            self.assertEqual(request.get_method(), 'HEAD')


if __name__ == '__main__':
    unittest.main()
