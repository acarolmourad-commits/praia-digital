# Local state locking is currently Windows-only; no POSIX guarantee is claimed.
import sys
import unittest
if sys.platform != 'win32':
    raise unittest.SkipTest('Hermes local-state protocol requires Windows')

import contextlib
import csv
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

LAB = Path(__file__).resolve().parent
SCRIPTS = LAB.parent / 'scripts'
sys.path[:0] = [str(SCRIPTS), str(SCRIPTS / 'automation')]
import delivery_journal as journal
import state_store as store
import hashlib
import safe_publication as publication
import notification_delivery as notification


def load(relative):
    spec = importlib.util.spec_from_file_location('fixture_' + Path(relative).stem, SCRIPTS / relative)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='delivery-hardening-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'private-state'
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        for name in ('socket.socket', 'socket.create_connection', 'subprocess.Popen', 'os.system'):
            self.stack.enter_context(patch(name, side_effect=AssertionError('External effect forbidden')))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.m = load('follow_up_automacao.py')
        self.m.BASE = self.root
        self.m.LEADS_PATH = self.root / 'leads.csv'
        self.m.LOTE_PATH_TMPL = self.root / 'batch_{today}.md'
        self.m.KNOWN_PSIDS = {1: 'synthetic'}
        with self.m.LEADS_PATH.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, ['lead_id', 'nome_empresa', 'status', 'canal_contato'])
            writer.writeheader()
            writer.writerow({'lead_id': 1, 'nome_empresa': 'Synthetic', 'status': 'PROSPECTAR',
                             'canal_contato': 'Instagram'})
        self.expected = store.identity('composio', 'synthetic-account', 'synthetic-data', self.m.LEADS_PATH)
        store.initialize(self.state, self.expected)
        self.args = ['--send', '--state-dir', str(self.state), '--account-id', 'synthetic-account', '--dataset-id', 'synthetic-data']
        self.receipt = ('{"successful":true,"data":{"message_id":"synthetic"}}', 0)

    def notification_state(self, label='default'):
        path = self.root / ('notification-' + label)
        expected = store.identity('telegram', 'bot:123:chat:' + hashlib.sha256(b'fake').hexdigest(),
                                  'notifications', SCRIPTS.parent)
        if not path.exists():
            store.initialize(path, expected)
        return path

    def test_argv_json_preserves_adversarial_input_without_shell(self):
        recipient = "O'Brien;$(touch SENTINEL)&`echo bad`"
        text = "aspas ' \" \\ newline\n$(id) ; & %PATH% emoji 🏠"
        with patch.object(self.m.subprocess, 'run', return_value=types.SimpleNamespace(stdout='{}', returncode=0)) as run:
            self.m.send_instagram_dm(recipient, text, 'synthetic-account')
        argv = run.call_args.args[0]
        self.assertEqual(argv[:3], ['wsl', '--exec', 'composio'])
        self.assertNotIn('bash', argv)
        self.assertEqual(argv[argv.index('--account') + 1], 'synthetic-account')
        self.assertIs(run.call_args.kwargs['shell'], False)
        self.assertEqual(json.loads(argv[-1]), {'recipient_id': recipient, 'text': text, 'ig_user_id': 'me'})

    def test_timeout_blocks_retry_even_if_text_or_recipient_changes(self):
        with patch.object(self.m, 'send_instagram_dm', side_effect=subprocess.TimeoutExpired('synthetic', 30)) as send:
            self.assertEqual(self.m.main(self.args), 1)
            self.m.KNOWN_PSIDS[1] = 'changed'
            self.assertEqual(self.m.main(self.args), 1)
        self.assertEqual(send.call_count, 1)
        record = json.loads(next(self.state.glob('*.attempt.json')).read_text())
        self.assertEqual(record['status'], 'UNCERTAIN')
        self.assertIn('RECONCILIAR_ENVIO', self.m.LEADS_PATH.read_text())
        self.assertNotIn('ENVIADO_D0', self.m.LEADS_PATH.read_text())

    def test_unrecognised_receipt_blocks_next_attempt(self):
        with patch.object(self.m, 'send_instagram_dm', return_value=('not a verified receipt', 0)) as send:
            self.assertEqual(self.m.main(self.args), 1)
            self.assertEqual(self.m.main(self.args), 1)
        self.assertEqual(send.call_count, 1)

    def test_intent_persistence_failure_prevents_transport(self):
        transport = Mock()
        with patch.object(journal.os, 'fsync', side_effect=OSError('synthetic disk full')):
            with self.assertRaises(OSError):
                journal.send_once(self.state, '1', 'D0', 'synthetic', 'message', transport, lambda *_: 'receipt', self.expected)
        transport.assert_not_called()
        self.assertTrue(journal.blocked(self.state, '1', 'D0'))

    def test_receipt_persistence_failure_preserves_intent_and_blocks(self):
        transport = Mock(return_value=self.receipt)
        with patch.object(journal, 'replace_json', side_effect=OSError('synthetic disk full')):
            with self.assertRaises(OSError):
                journal.send_once(self.state, '1', 'D0', 'synthetic', 'message', transport, self.m.delivery_confirmed, self.expected)
        with self.assertRaises(journal.ReconciliationRequired):
            journal.send_once(self.state, '1', 'D0', 'synthetic', 'different', transport, self.m.delivery_confirmed, self.expected)
        self.assertEqual(transport.call_count, 1)

    def test_csv_replace_failure_preserves_original_and_stops_future_run(self):
        before = self.m.LEADS_PATH.read_bytes()
        original = journal.os.replace
        def replace(src, dest):
            if Path(dest) == self.m.LEADS_PATH:
                raise OSError('synthetic disk full')
            return original(src, dest)
        with patch.object(self.m, 'send_instagram_dm', return_value=self.receipt) as send:
            with patch.object(journal.os, 'replace', side_effect=replace):
                with self.assertRaises(OSError):
                    self.m.main(self.args)
            with self.assertRaises(journal.ReconciliationRequired):
                self.m.main(self.args)
        self.assertEqual(send.call_count, 1)
        self.assertEqual(self.m.LEADS_PATH.read_bytes(), before)
        self.assertTrue((self.state / 'run.pending.json').exists())

    def test_success_persisted_and_no_duplicate(self):
        with patch.object(self.m, 'send_instagram_dm', return_value=self.receipt) as send:
            self.assertEqual(self.m.main(self.args), 0)
            self.assertEqual(self.m.main(self.args), 0)
        self.assertEqual(send.call_count, 1)
        self.assertIn('ENVIADO_D0', self.m.LEADS_PATH.read_text())
        record = json.loads(next(self.state.glob('*.attempt.json')).read_text())
        self.assertEqual(record['status'], 'CSV_COMMITTED')

    def test_journal_finalize_failure_after_csv_still_blocks_whole_run(self):
        with patch.object(self.m, 'send_instagram_dm', return_value=self.receipt) as send:
            with patch.object(self.m, 'mark_csv_committed', side_effect=OSError('synthetic disk full')):
                with self.assertRaises(OSError):
                    self.m.main(self.args)
            with self.assertRaises(journal.ReconciliationRequired):
                self.m.main(self.args)
        self.assertEqual(send.call_count, 1)
        self.assertIn('ENVIADO_D0', self.m.LEADS_PATH.read_text())
        self.assertTrue((self.state / 'run.pending.json').exists())

    def test_adversarial_identifiers_cannot_escape_journal(self):
        path = journal.attempt_path(self.state, '../../outside', "D0/../../'$(id)")
        self.assertEqual(path.parent, self.state)
        self.assertEqual(len(path.name.split('.')[0]), 64)

    def test_pending_run_and_missing_private_state_fail_closed(self):
        with self.assertRaises(SystemExit):
            self.m.main(['--send'])
        with journal.run_guard(self.state, self.expected):
            with self.assertRaises(store.StateRefused):
                self.m.main(self.args)

    def test_notification_http_failure_is_sanitized_and_not_retried(self):
        response = Mock()
        response.raise_for_status.side_effect = RuntimeError('URL contains SYNTHETIC_SECRET')
        client = Mock(post=Mock(return_value=response))
        with patch.dict(os.environ, HERMES_NOTIFICATION_STATE_DIR=str(self.notification_state())):
            for _ in range(2):
                with self.assertRaises(journal.ReconciliationRequired) as caught:
                    notification.notify(client, '123:fake', 'fake', 'message', 'test', 'today')
                self.assertNotIn('SYNTHETIC_SECRET', str(caught.exception))
        self.assertEqual(client.post.call_count, 1)
        self.assertEqual(client.post.call_args.kwargs['timeout'], (5, 20))

    def test_notification_false_ok_or_timeout_never_claim_success(self):
        for index, response in enumerate([{'ok': False}, {'ok': True}, {'ok': True, 'result': {'message_id': True}}]):
            client = Mock()
            client.post.return_value.json.return_value = response
            with patch.dict(os.environ, HERMES_NOTIFICATION_STATE_DIR=str(self.notification_state(str(index)))):
                with self.assertRaises(journal.ReconciliationRequired):
                    notification.notify(client, '123:fake', 'fake', 'msg', 'test', 'today')
        client = Mock(post=Mock(side_effect=TimeoutError('synthetic timeout')))
        with patch.dict(os.environ, HERMES_NOTIFICATION_STATE_DIR=str(self.notification_state('timeout'))):
            with self.assertRaises(journal.ReconciliationRequired):
                notification.notify(client, '123:fake', 'fake', 'msg', 'test', 'today')

    def test_notification_confirmation_and_log_failure_propagation(self):
        client = Mock()
        client.post.return_value.json.return_value = {'ok': True, 'result': {'message_id': 1, 'from': {'id': 123}}}
        with patch.dict(os.environ, HERMES_NOTIFICATION_STATE_DIR=str(self.notification_state())):
            receipt = notification.notify(client, '123:fake', 'fake', 'msg', 'test', 'today')
            notification.complete_notification(receipt)
        self.assertEqual(json.loads(receipt[0].read_text())['status'], 'CSV_COMMITTED')
        with patch.dict(sys.modules, {'requests': client}):
            module = load('automation/notificar_automacao.py')
        module.BATCH_LOG = self.root / 'missing' / 'log.csv'
        with self.assertRaises(OSError):
            module.append_batch_log('synthetic')

    def test_notification_confirmed_but_audit_failed_is_not_resent(self):
        client = Mock()
        client.post.return_value.json.return_value = {'ok': True, 'result': {'message_id': 1, 'from': {'id': 123}}}
        with patch.dict(sys.modules, {'requests': client}):
            module = load('automation/notificar_automacao.py')
        module.TELEGRAM_BOT_TOKEN = '123:synthetic'
        module.TELEGRAM_CHAT_ID = 'fake'
        module.FILE = self.root / 'absent.csv'
        module.BATCH_LOG = self.root / 'absent-directory' / 'log.csv'
        with patch.dict(os.environ, HERMES_NOTIFICATION_STATE_DIR=str(self.notification_state())):
            with self.assertRaises(OSError):
                module.main()
            with self.assertRaises(journal.ReconciliationRequired):
                module.main()
        self.assertEqual(client.post.call_count, 1)



if __name__ == '__main__':
    unittest.main(verbosity=2)
