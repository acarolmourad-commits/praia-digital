# Local state locking is currently Windows-only; no POSIX guarantee is claimed.
import sys
import unittest
if sys.platform != 'win32':
    raise unittest.SkipTest('Hermes local-state protocol requires Windows')

import json
import multiprocessing as mp
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_hermes_state_safety as support
from state_recovery import Recovery
import state_recovery as recovery_module
import state_store as store
import delivery_journal as journal


def later_worker(root, expected):
    try:
        with journal.run_guard(root, expected):
            journal.send_once(root, 'second-lead', 'D0', 'recipient', 'message',
                              lambda *_: ('unknown', 0), lambda *_: None, expected)
    except journal.ReconciliationRequired:
        pass


class ResumeTests(unittest.TestCase):
    setUp = support.StateTests.setUp
    stop_children = support.StateTests.stop_children
    spawn = support.StateTests.spawn
    completed_attempt = support.StateTests.completed_attempt

    def recovery(self, guarded=False):
        if guarded:
            ready, release = mp.Event(), mp.Event()
            p = mp.Process(target=support.child_guarded,
                           args=(self.state, self.identity, ready, release, self.root / 'calls.txt'))
            self.children.append(p)
            p.start()
            self.assertTrue(ready.wait(5))
            p.terminate()
            p.join(5)
        else:
            p = self.completed_attempt()
        verifier = support.SyntheticVerifier([p], self.resource)
        item = Recovery(self.state, self.identity, verifier)
        approval, report = item.prepare()
        return item, approval, verifier

    def test_reproduced_first_fsync_failure_can_resume_and_ack_idempotently(self):
        item, approval, verifier = self.recovery()
        with patch.object(recovery_module.os, 'fsync', side_effect=OSError('synthetic disk full')):
            with self.assertRaises(OSError):
                item.approve(approval)
        partial = next(self.state.glob('*.partial'))
        preserved = partial.read_bytes()
        audit = item.approve(approval)
        data = json.loads(audit.read_text())
        self.assertEqual(data['phase'], 'COMPLETE')
        self.assertEqual(partial.read_bytes(), preserved)
        self.assertTrue(data['prior_partials'][0]['valid_payload'])
        stable = audit.read_bytes()
        verifier.handles = []
        verifier.remote = 'UNKNOWN'
        self.assertEqual(item.approve(approval), audit)
        self.assertEqual(audit.read_bytes(), stable)
        self.assertTrue(journal.blocked(self.state, 'lead', 'D0'))

    def test_truncated_partial_is_preserved_but_never_authorizes_recovery(self):
        item, approval, verifier = self.recovery()
        partial = self.state / ('.recovery-' + approval + '-broken.partial')
        partial.write_bytes(b'{"schema":3,')
        verifier.remote = 'UNKNOWN'
        with self.assertRaises(journal.ReconciliationRequired):
            item.approve(approval)
        verifier.remote = 'DELIVERED'
        data = json.loads(item.approve(approval).read_text())
        self.assertEqual(partial.read_bytes(), b'{"schema":3,')
        self.assertFalse(data['prior_partials'][0]['valid_payload'])

    def test_failure_after_archive_resumes_without_old_process_handles(self):
        item, approval, verifier = self.recovery(guarded=True)
        original = recovery_module.os.fsync
        calls = 0
        def fail_second(fd):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('synthetic final audit failure')
            return original(fd)
        with patch.object(recovery_module.os, 'fsync', side_effect=fail_second):
            with self.assertRaises(OSError):
                item.approve(approval)
        audit = self.state / ('recovery-' + approval + '.json')
        self.assertEqual(json.loads(audit.read_text())['phase'], 'PREPARED')
        self.assertFalse((self.state / 'run.pending.json').exists())
        self.assertEqual(len(list(self.state.glob('run-*.archived.json'))), 1)
        with self.assertRaises(store.StateRefused):
            with journal.run_guard(self.state, self.identity):
                self.fail('incomplete recovery must block new writers')
        with self.assertRaises(store.StateRefused):
            journal.send_once(self.state, 'unrelated', 'D0', 'recipient', 'msg',
                              lambda *_: self.fail('transport forbidden'), lambda *_: 'receipt', self.identity)
        verifier.handles = []
        item.approve(approval)
        self.assertEqual(json.loads(audit.read_text())['phase'], 'COMPLETE')
        self.assertEqual(len(list(self.state.glob('run-*.archived.json'))), 1)

    def test_replace_failure_preserves_partial_and_is_retryable(self):
        item, approval, _ = self.recovery()
        with patch.object(recovery_module.os, 'replace', side_effect=OSError('synthetic replace failure')):
            with self.assertRaises(OSError):
                item.approve(approval)
        self.assertEqual(len(list(self.state.glob('*.partial'))), 1)
        self.assertEqual(json.loads(item.approve(approval).read_text())['phase'], 'COMPLETE')

    def test_run_archive_failure_is_retryable(self):
        item, approval, _ = self.recovery(guarded=True)
        with patch.object(item, 'archive_run', side_effect=OSError('synthetic rename failure')):
            with self.assertRaises(OSError):
                item.approve(approval)
        self.assertTrue((self.state / 'run.pending.json').exists())
        item.approve(approval)
        self.assertFalse((self.state / 'run.pending.json').exists())

    def test_future_recovery_uses_only_new_owner_and_old_resend_stays_blocked(self):
        item, approval, _ = self.recovery()
        item.approve(approval)
        p = mp.Process(target=later_worker, args=(self.state, self.identity))
        self.children.append(p)
        p.start()
        p.join(5)
        self.assertEqual(p.exitcode, 0)
        new = Recovery(self.state, self.identity, support.SyntheticVerifier([p], self.resource))
        second, report = new.prepare()
        self.assertEqual(report['processes'], [p.pid])
        self.assertEqual(len(report['attempts']), 1)
        self.assertEqual(report['attempts'][0]['file'], journal.attempt_path(self.state, 'second-lead', 'D0').name)
        marker = (self.state / 'run.pending.json').read_bytes()
        item.approve(approval)  # Idempotent old acknowledgement MUST NOT touch newer run.
        self.assertEqual((self.state / 'run.pending.json').read_bytes(), marker)
        new.approve(second)
        self.assertEqual(len(list(self.state.glob('recovery-*.json'))), 2)
        self.assertTrue(journal.blocked(self.state, 'lead', 'D2'))
        self.assertTrue(journal.blocked(self.state, 'second-lead', 'D2'))

    def test_corrupt_completed_audit_is_not_ignored(self):
        item, approval, _ = self.recovery()
        audit = item.approve(approval)
        audit.write_text('{"schema":3')
        with self.assertRaises(journal.ReconciliationRequired):
            item.prepare()

    def test_missing_attempt_after_completion_cannot_enable_resend(self):
        item, approval, _ = self.recovery()
        item.approve(approval)
        next(self.state.glob('*.attempt.json')).unlink()  # Synthetic fault, never production cleanup.
        with self.assertRaises(store.StateRefused):
            journal.send_once(self.state, 'lead', 'D0', 'recipient', 'msg',
                              lambda *_: self.fail('resent'), lambda *_: 'receipt', self.identity)
        with self.assertRaises(store.StateRefused):
            with journal.run_guard(self.state, self.identity):
                pass

    def test_changed_attempt_after_completion_refuses_future_recovery(self):
        item, approval, _ = self.recovery()
        item.approve(approval)
        attempt = next(self.state.glob('*.attempt.json'))
        attempt.write_bytes(attempt.read_bytes() + b' ')
        with self.assertRaises(journal.ReconciliationRequired):
            item.prepare()


if __name__ == '__main__':
    mp.freeze_support()
    unittest.main(verbosity=2)
