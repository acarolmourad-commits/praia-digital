# Local state locking is currently Windows-only; no POSIX guarantee is claimed.
import sys
import unittest
if sys.platform != 'win32':
    raise unittest.SkipTest('Hermes local-state protocol requires Windows')

import hashlib
import importlib.util
import json
import multiprocessing as mp
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'scripts'))
import state_store as store
import delivery_journal as journal
from state_recovery import Recovery


def child_send(root, expected, stage, ready, release, log):
    def network_forbidden(*a, **kw):
        raise AssertionError('Network forbidden')
    socket.socket = network_forbidden
    def transport(*args):
        with open(log, 'a') as stream:
            stream.write(stage + '\n')
        ready.set()
        release.wait(5)
        raise TimeoutError('Synthetic unknown outcome')
    try:
        journal.send_once(root, 'lead', stage, 'recipient', 'message', transport, lambda *_: None, expected)
    except (journal.ReconciliationRequired, store.StateRefused):
        pass


def child_guarded(root, expected, ready, release, log):
    with journal.run_guard(root, expected):
        child_send(root, expected, 'D0', ready, release, log)


class SyntheticVerifier:
    """Test-only authoritative destination and supervisor, never production proof."""
    def __init__(self, handles, resource):
        self.handles = handles
        self.resource = resource
        self.complete = True
        self.remote = 'DELIVERED'
        self.wrong_account = False
        self.local_ok = True
        self.publication = 'RECONCILED'

    def process_handles(self):
        return self.handles

    def tree_is_complete(self):
        return self.complete

    def observe(self, identity, record):
        return {'account': 'wrong' if self.wrong_account else identity['account'],
                'attempt_id': record['attempt_id'], 'recipient_hash': record['recipient_hash'],
                'message_hash': record['message_hash'], 'evidence_id': 'synthetic-event-1',
                'outcome': self.remote, 'receipt_id': 'synthetic-receipt'}

    def local_reconciled(self, resource, record, evidence):
        return self.local_ok and resource.read_text() == 'reconciled'

    def resource_snapshot(self, resource):
        return {'sha256': hashlib.sha256(resource.read_bytes()).hexdigest(),
                'publication': self.publication}


class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='state-v2-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.resource = self.root / 'synthetic.csv'
        self.resource.write_text('reconciled')
        self.state = self.root / 'private'
        self.identity = store.identity('synthetic', 'account-A', 'dataset-A', self.resource)
        store.initialize(self.state, self.identity)
        self.children = []
        self.addCleanup(self.stop_children)

    def stop_children(self):
        for p in self.children:
            if p.is_alive():
                p.terminate()
            p.join(5)

    def spawn(self, stage='D0'):
        ready, release = mp.Event(), mp.Event()
        p = mp.Process(target=child_send, args=(self.state, self.identity, stage, ready, release, self.root / 'calls.txt'))
        self.children.append(p)
        p.start()
        self.assertTrue(ready.wait(5))
        return p, release

    def completed_attempt(self):
        p, release = self.spawn()
        release.set()
        p.join(5)
        self.assertEqual(p.exitcode, 0)
        return p

    def test_missing_or_uninitialized_state_never_sends(self):
        for root in (self.root / 'typo', self.root / 'empty'):
            if root.name == 'empty':
                root.mkdir()
            calls = []
            with self.assertRaises((store.StateRefused, FileNotFoundError)):
                journal.send_once(root, 'lead', 'D0', 'recipient', 'msg', lambda *_: calls.append(1), lambda *_: 'receipt', self.identity)
            self.assertEqual(calls, [])
        self.assertFalse((self.root / 'typo').exists())

    def test_account_dataset_and_resource_mismatch_refused(self):
        other = self.root / 'other.csv'
        other.write_text('reconciled')
        identities = [store.identity('synthetic', 'account-B', 'dataset-A', self.resource),
                      store.identity('synthetic', 'account-A', 'dataset-B', self.resource),
                      store.identity('synthetic', 'account-A', 'dataset-A', other)]
        for value in identities:
            with self.assertRaises(store.StateRefused):
                store.validate(self.state, value)

    def test_copied_state_and_reinitialization_refused(self):
        copied = self.root / 'copied'
        shutil.copytree(self.state, copied)
        with self.assertRaises(store.StateRefused):
            store.validate(copied, self.identity)
        with self.assertRaises(store.StateRefused):
            store.initialize(self.state, self.identity)

    def test_directory_replacement_same_path_detected(self):
        old = self.root / 'old-state'
        self.state.rename(old)
        shutil.copytree(old, self.state)
        with self.assertRaises(store.StateRefused):
            store.validate(self.state, self.identity)

    def test_hardlinked_metadata_refused(self):
        os.link(self.state / 'identity.json', self.root / 'manifest-link')
        with self.assertRaises(store.StateRefused):
            store.validate(self.state, self.identity)

    def test_different_stages_real_processes_never_both_send(self):
        first, release = self.spawn('D0')
        ready2, release2 = mp.Event(), mp.Event()
        release2.set()
        second = mp.Process(target=child_send, args=(self.state, self.identity, 'D2', ready2, release2, self.root / 'calls.txt'))
        self.children.append(second)
        second.start()
        second.join(5)
        self.assertFalse(ready2.is_set())
        self.assertEqual(second.exitcode, 0)
        release.set()
        first.join(5)
        with self.assertRaises(journal.ReconciliationRequired):
            journal.send_once(self.state, 'lead', 'D2', 'recipient', 'msg', lambda *_: self.fail('resent'), lambda *_: 'receipt', self.identity)
        self.assertEqual((self.root / 'calls.txt').read_text().splitlines(), ['D0'])

    def test_abrupt_death_releases_os_lock_but_intent_blocks(self):
        p, _ = self.spawn()
        p.terminate()
        p.join(5)
        with self.assertRaises(journal.ReconciliationRequired):
            journal.send_once(self.state, 'lead', 'D2', 'recipient', 'msg', lambda *_: self.fail('resent'), lambda *_: 'receipt', self.identity)
        self.assertTrue((self.state / 'delivery.lock').exists())

    def test_run_marker_ownership_change_is_not_deleted(self):
        with self.assertRaises(journal.ReconciliationRequired):
            with journal.run_guard(self.state, self.identity):
                (self.state / 'run.pending.json').write_text('{"other":"owner"}')
        self.assertTrue((self.state / 'run.pending.json').exists())

    def test_recovery_requires_complete_dead_tree_and_bound_remote_proof(self):
        p, release = self.spawn()
        verifier = SyntheticVerifier([p], self.resource)
        recovery = Recovery(self.state, self.identity, verifier)
        with self.assertRaises(store.StateRefused):
            recovery.prepare()  # transport lock is still held
        release.set()
        p.join(5)
        for field, value in [('complete', False), ('wrong_account', True), ('remote', 'UNKNOWN'),
                             ('local_ok', False), ('publication', 'UNKNOWN')]:
            old = getattr(verifier, field)
            setattr(verifier, field, value)
            with self.assertRaises(journal.ReconciliationRequired):
                recovery.prepare()
            setattr(verifier, field, old)
        verifier.handles = []
        with self.assertRaises(journal.ReconciliationRequired):
            recovery.prepare()

    def test_recovery_requires_approval_and_preserves_attempt_no_retry(self):
        p = self.completed_attempt()
        recovery = Recovery(self.state, self.identity, SyntheticVerifier([p], self.resource))
        attempt = next(self.state.glob('*.attempt.json'))
        before = attempt.read_bytes()
        approval, report = recovery.prepare()
        with self.assertRaises(journal.ReconciliationRequired):
            recovery.approve('')
        audit = recovery.approve(approval)
        self.assertTrue(audit.exists())
        self.assertEqual(attempt.read_bytes(), before)
        self.assertTrue(journal.blocked(self.state, 'lead', 'D0'))
        self.assertTrue((self.state / 'delivery.lock').exists())

    def test_recovery_rechecks_changed_evidence(self):
        p = self.completed_attempt()
        verifier = SyntheticVerifier([p], self.resource)
        recovery = Recovery(self.state, self.identity, verifier)
        approval, _ = recovery.prepare()
        verifier.remote = 'NOT_DELIVERED'
        with self.assertRaises(journal.ReconciliationRequired):
            recovery.approve(approval)
        self.assertEqual(list(self.state.glob('recovery-*.json')), [])

    def test_recovery_audit_persistence_failure_preserves_attempt(self):
        p = self.completed_attempt()
        recovery = Recovery(self.state, self.identity, SyntheticVerifier([p], self.resource))
        approval, _ = recovery.prepare()
        with patch('state_recovery.os.fsync', side_effect=OSError('synthetic disk full')):
            with self.assertRaises(OSError):
                recovery.approve(approval)
        self.assertTrue(journal.blocked(self.state, 'lead', 'D0'))

    def test_recovery_archives_interrupted_run_only_after_proof(self):
        ready, release = mp.Event(), mp.Event()
        p = mp.Process(target=child_guarded, args=(self.state, self.identity, ready, release, self.root / 'calls.txt'))
        self.children.append(p)
        p.start()
        self.assertTrue(ready.wait(5))
        p.terminate()
        p.join(5)
        marker = self.state / 'run.pending.json'
        before = marker.read_bytes()
        recovery = Recovery(self.state, self.identity, SyntheticVerifier([p], self.resource))
        approval, _ = recovery.prepare()
        recovery.approve(approval)
        self.assertFalse(marker.exists())
        self.assertEqual(next(self.state.glob('run-*.archived.json')).read_bytes(), before)
        self.assertTrue(journal.blocked(self.state, 'lead', 'D2'))
        with journal.run_guard(self.state, self.identity):
            pass  # Other reconciled work can run; this lead is still blocked.


if __name__ == '__main__':
    mp.freeze_support()
    unittest.main(verbosity=2)
