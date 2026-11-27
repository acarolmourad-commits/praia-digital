# Local state locking is currently Windows-only; no POSIX guarantee is claimed.
import sys
import unittest
if sys.platform != 'win32':
    raise unittest.SkipTest('Hermes local-state protocol requires Windows')

import contextlib
import builtins
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import socket
import subprocess
import types
import tempfile
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parent
CANDIDATE = LAB.parent
import sys
sys.path[:0] = [str(CANDIDATE / 'scripts'), str(CANDIDATE / 'scripts/automation')]

def load(rel):
    spec = importlib.util.spec_from_file_location('candidate_' + Path(rel).stem, CANDIDATE / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.blockers = [patch('socket.socket', side_effect=AssertionError('network forbidden')),
                         patch('subprocess.Popen', side_effect=AssertionError('process forbidden')),
                         patch('os.system', side_effect=AssertionError('shell forbidden'))]
        for blocker in self.blockers:
            blocker.start()
        self.addCleanup(self.temp.cleanup)
        for blocker in self.blockers:
            self.addCleanup(blocker.stop)

    def runner(self):
        m = load('scripts/automation/run_vendas_do_dia.py')
        first, second, notify = [self.root / n for n in ('first.py', 'second.py', 'notify.py')]
        for p in (first, second, notify): p.write_text('# synthetic', encoding='utf-8')
        m.SCRIPTS, m.NOTIFY_SCRIPT = [first, second], notify
        m.BASE = self.root
        return m

    def test_runner_stops_on_failure_without_notification(self):
        m = self.runner()
        with patch.object(m.subprocess, 'run', side_effect=subprocess.CalledProcessError(7, ['synthetic'])) as run:
            with self.assertRaises(subprocess.CalledProcessError): m.main()
        self.assertEqual(run.call_count, 1)
        self.assertTrue(run.call_args.kwargs['check'])

    def test_runner_missing_script_fails(self):
        m = self.runner()
        m.SCRIPTS = [self.root / 'missing.py']
        with self.assertRaises(FileNotFoundError): m.main()

    def test_runner_success_order(self):
        m = self.runner()
        with patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as run:
            m.main()
        self.assertEqual([Path(c.args[0][1]).name for c in run.call_args_list], ['first.py', 'second.py', 'notify.py'])

    def outbound(self, conflict='', dirty='', failure=False):
        m = load('scripts/executar_outbound.py')
        m.REPO = str(self.root)
        def git(cmd, **kwargs):
            self.assertEqual(cmd[:3], ['git', '-C', str(self.root)])
            self.assertTrue(kwargs['check'])
            tail = cmd[3:]
            if failure: raise subprocess.CalledProcessError(128, cmd)
            if tail[0] == 'diff': out = conflict
            elif tail[0] == 'rev-parse': out = str(self.root / '.git' / tail[-1])
            elif tail[0] == 'status': out = dirty
            else: self.fail('Unexpected Git write: ' + str(tail))
            return subprocess.CompletedProcess(cmd, 0, stdout=out)
        return m, git

    def check_blocked(self, **kwargs):
        m, git = self.outbound(**kwargs)
        with patch.object(m.subprocess, 'run', side_effect=git), patch.object(m, 'run') as generate, patch('sys.argv', ['script', '--push']):
            with self.assertRaises((RuntimeError, subprocess.CalledProcessError)): m.main()
        generate.assert_not_called()

    def test_outbound_conflict_before_generation(self): self.check_blocked(conflict='synthetic.html')
    def test_outbound_dirty_before_generation(self): self.check_blocked(dirty=' M pending.txt')
    def test_outbound_git_error_before_generation(self): self.check_blocked(failure=True)

    def test_outbound_pending_git_operation_preserved(self):
        marker = self.root / '.git' / 'MERGE_HEAD'
        marker.parent.mkdir()
        marker.write_text('synthetic', encoding='utf-8')
        self.check_blocked()
        self.assertEqual(marker.read_text(), 'synthetic')

    def test_outbound_clean_preflight(self):
        m, git = self.outbound()
        with patch.object(m.subprocess, 'run', side_effect=git): m.preflight(True)

    def followup(self, status='PROSPECTAR', extra=None):
        m = load('scripts/follow_up_automacao.py')
        m.BASE = self.root
        m.LEADS_PATH = self.root / 'leads.csv'
        m.LOTE_PATH_TMPL = self.root / 'lote_{today}.md'
        row = {'lead_id': '1', 'nome_empresa': 'Empresa Ficticia', 'city': 'Bertioga',
               'status': status, 'canal_contato': 'Instagram', 'score': '10'}
        row.update(extra or {})
        with m.LEADS_PATH.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(row))
            writer.writeheader(); writer.writerow(row)
        m.KNOWN_PSIDS = {1: 'SYNTHETIC_ONLY'}
        import uuid
        state = self.root / ('state-' + uuid.uuid4().hex)
        from state_store import initialize, identity
        initialize(state, identity('composio', 'synthetic-account', 'synthetic-data', m.LEADS_PATH))
        m.test_manual_args = ['--state-dir', str(state), '--account-id', 'synthetic-account', '--dataset-id', 'synthetic-data']
        m.test_send_args = ['--send', *m.test_manual_args]
        return m

    def read_row(self, m):
        with m.LEADS_PATH.open(encoding='utf-8') as f: return next(csv.DictReader(f))

    def test_followup_dry_run_no_writes_or_send(self):
        m = self.followup()
        before = m.LEADS_PATH.read_bytes()
        snapshot = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(m, 'send_instagram_dm', side_effect=AssertionError('send forbidden')):
            self.assertEqual(m.main(['--dry-run', '--send']), 0)
        self.assertEqual(m.LEADS_PATH.read_bytes(), before)
        self.assertEqual({str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}, snapshot)

    def test_followup_manual_not_marked_sent(self):
        m = self.followup()
        with patch.object(m, 'send_instagram_dm', side_effect=AssertionError('send forbidden')):
            self.assertEqual(m.main(m.test_manual_args), 0)
        self.assertEqual(self.read_row(m)['status'], 'PROSPECTAR')
        self.assertIn('PREPARADO_D0', next(self.root.glob('lote_*.md')).read_text(encoding='utf-8'))

    def test_followup_failure_not_marked_sent_and_returns_error(self):
        for response in [('provider failed', 1), ('no receipt', 0), ('{"successful":false,"data":{"message_id":"fake"}}', 0)]:
            m = self.followup()
            with patch.object(m, 'send_instagram_dm', return_value=response):
                self.assertEqual(m.main(m.test_send_args), 1)
            self.assertEqual(self.read_row(m)['status'], 'PROSPECTAR')
            report = json.loads(next(self.root.glob('relatorio_*.json')).read_text(encoding='utf-8'))
            self.assertEqual(report['metrics']['instagram_sent'], 0)

    def test_followup_receipt_marks_d0_with_date(self):
        m = self.followup()
        with patch.object(m, 'send_instagram_dm', return_value=('{"successful":true,"data":{"message_id":"synthetic-receipt"}}', 0)):
            self.assertEqual(m.main(m.test_send_args), 0)
        row = self.read_row(m)
        self.assertEqual(row['status'], 'ENVIADO_D0')
        self.assertEqual(row['d0_enviado_em'], m.TODAY_STR)

    def test_followup_failed_d2_preserves_prior_date_and_status(self):
        m = self.followup('ENVIADO_D0', {'d0_enviado_em': '2000-01-01'})
        with patch.object(m, 'send_instagram_dm', return_value=('failed', 1)):
            self.assertEqual(m.main(m.test_send_args), 1)
        row = self.read_row(m)
        self.assertEqual(row['status'], 'ENVIADO_D0')
        self.assertEqual(row['d0_enviado_em'], '2000-01-01')
        self.assertFalse(row.get('d2_enviado_em'))

    def test_followup_rejects_unconfirmed_or_malformed_receipts(self):
        m = self.followup()
        for payload in [ {'message_id': 'x'}, {'data': {'message_id': 'x'}},
                         {'successful': 'true', 'data': {'message_id': 'x'}},
                         {'successful': True, 'data': {'message_id': True}},
                         {'successful': True, 'data': {'message_id': '  '}},
                         {'successful': True, 'data': {'message_id': 'x', 'error': 'failed'}},
                         {'successful': True, 'data': []} ]:
            with self.subTest(payload=payload):
                self.assertFalse(m.delivery_confirmed(json.dumps(payload), 0))

    def test_all_outbound_generators_stay_in_copy(self):
        scripts = self.root / 'scripts'
        scripts.mkdir()
        for p in (CANDIDATE / 'scripts').glob('*.py'):
            shutil.copyfile(p, scripts / p.name)
        sales = self.root / 'docs/sales'
        lots = sales / 'csv-lotes-email'
        lots.mkdir(parents=True)
        (sales / 'METAS_OUTBOUND.json').write_text(json.dumps({'metas': {'respondeu': 1, 'fechou': 1, 'receita_estimada': 1}}), encoding='utf-8')
        for channel, field, datefield in [('whatsapp', 'Telefone', 'Data_Msg1'), ('email', 'Email', 'Data_Email1')]:
            with (lots / f'lote-{channel}-proprietarios-1-2000-01-01.csv').open('w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=['Nome', field, 'Cidade', datefield, 'Status'], delimiter=';')
                w.writeheader(); w.writerow({'Nome': 'Contato Ficticio', field: 'ficticio@example.invalid', 'Cidade': 'Bertioga', datefield: '2000-01-01', 'Status': 'pendente'})
        original_open, original_io_open = builtins.open, io.open
        writes = []
        def guarded(opener):
            def call(file, mode='r', *args, **kwargs):
                if any(c in mode for c in 'wax+'):
                    path = Path(file).resolve()
                    self.assertTrue(path.is_relative_to(self.root), 'Write escaped isolated fixture: ' + str(path))
                    writes.append(path)
                return opener(file, mode, *args, **kwargs)
            return call
        children = []
        def dispatch(cmd, **kwargs):
            if cmd[0] == 'git':
                self.assertEqual(cmd[1:3], ['-C', str(self.root)])
                if cmd[3] == 'diff': value = ''
                elif cmd[3] == 'rev-parse': value = str(self.root / '.git' / cmd[-1])
                else: self.fail('Git write or network operation forbidden: ' + repr(cmd))
                return subprocess.CompletedProcess(cmd, 0, stdout=value)
            self.assertEqual(cmd[0], 'python')
            script = Path(cmd[1]).resolve()
            self.assertEqual(script.parent, scripts)
            children.append(script.name)
            runpy.run_path(str(script), run_name='__main__')
            return subprocess.CompletedProcess(cmd, 0)
        with patch('subprocess.run', side_effect=dispatch), patch('builtins.open', side_effect=guarded(original_open)), patch('io.open', side_effect=guarded(original_io_open)), patch('sys.argv', ['outbound']):
            runpy.run_path(str(scripts / 'executar_outbound.py'), run_name='__main__')
        self.assertEqual(len(children), 8)
        self.assertTrue(writes)
        self.assertTrue((sales / 'dashboard-outbound-proprietarios.html').is_file())
        for channel in ('whatsapp', 'email'):
            with (lots / f'tracker-{channel}-proprietarios.csv').open(encoding='utf-8-sig') as f:
                self.assertEqual(len(list(csv.DictReader(f, delimiter=';'))), 1)

    def test_complete_sales_runner_in_isolated_fixture(self):
        scripts = self.root / 'scripts/automation'
        scripts.mkdir(parents=True)
        for p in (CANDIDATE / 'scripts/automation').glob('*.py'):
            shutil.copyfile(p, scripts / p.name)
        lots = self.root / 'docs/sales/csv-lotes-b2b'
        lots.mkdir(parents=True)
        fields = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta',
                  'Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']
        services = ['automacao', 'automacao-pronto-envio', 'captacao', 'proptech-unificada',
                    'descricao', 'seo-local', 'consultoria', 'avaliacao', 'prospeccao', 'consultoria_proptech']
        for service in services:
            with (lots / f'lote-b2b-{service}-2026-07-22.csv').open('w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fields, delimiter=';')
                w.writeheader()
                w.writerow(dict.fromkeys(fields, '') | {'Lote':service, 'Nome':'Contato Sintetico',
                    'Telefone':'11999990000', 'Cidade':'Bertioga', 'Data_Msg1':'2026-07-22',
                    'Status':'pendente_msg1', 'Email':'fixture@example.invalid', 'Imobiliaria':'Empresa Ficticia'})
        original_open, original_io_open = builtins.open, io.open
        writes, children = [], []
        def guarded(opener):
            def call(file, mode='r', *args, **kwargs):
                path = Path(file).resolve()
                if any(c in mode for c in 'wax+'):
                    self.assertTrue(path.is_relative_to(self.root), 'Write outside fixture: ' + str(path))
                    writes.append(path)
                elif path.suffix.lower() in {'.csv', '.json', '.env', '.html'}:
                    self.assertTrue(path.is_relative_to(self.root), 'Data read outside fixture: ' + str(path))
                    self.assertNotEqual(path.name, '.env', 'Credential file must not be opened in fixture')
                return opener(file, mode, *args, **kwargs)
            return call
        def dispatch(cmd, **kwargs):
            script = Path(cmd[1]).resolve()
            self.assertEqual(script.parent, scripts)
            self.assertTrue(kwargs['check'])
            children.append(script.name)
            runpy.run_path(str(script), run_name='__main__')
            return subprocess.CompletedProcess(cmd, 0)
        blocked_requests = types.ModuleType('requests')
        blocked_requests.post = unittest.mock.Mock(side_effect=AssertionError('External notification forbidden'))
        with patch.dict('sys.modules', {'requests': blocked_requests}), patch('subprocess.run', side_effect=dispatch), patch('builtins.open', side_effect=guarded(original_open)), patch('io.open', side_effect=guarded(original_io_open)):
            runpy.run_path(str(scripts / 'run_vendas_do_dia.py'), run_name='__main__')
        self.assertEqual(len(children), 26)
        self.assertEqual(children[-1], 'notificar_vendas_b2b.py')
        blocked_requests.post.assert_not_called()
        self.assertGreater(len(writes), 20)
        self.assertFalse((self.root / '.env').exists())
        for service in ('automacao', 'captacao', 'avaliacao', 'descricao', 'seo-local', 'consultoria'):
            self.assertTrue((lots / f'tracker-{service}-2026-07-22.csv').exists(), service)

    def test_editorial_isolated_cwd_and_synthetic_articles(self):
        (self.root / 'blog').mkdir()
        for name, title in [('a', 'Teste editorial Bertioga'), ('b', 'Teste editorial Santos')]:
            (self.root / 'blog' / (name + '.html')).write_text('<html><title>' + title + '</title><h1>' + title + '</h1><p>Conteudo ficticio para teste.</p></html>', encoding='utf-8')
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            runpy.run_path(str(CANDIDATE / 'docs/scripts/build_banco_editorial.py'), run_name='__main__')
        finally:
            os.chdir(previous)
        result = json.loads((self.root / 'docs/banco-editorial.json').read_text(encoding='utf-8'))
        self.assertEqual(result['meta']['total_articles'], 2)
        self.assertEqual({a['slug'] for a in result['articles']}, {'a', 'b'})
        generated = {str(p.relative_to(self.root)).replace('\\', '/') for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(generated, {'blog/a.html', 'blog/b.html', 'docs/banco-editorial.json'})

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
    report = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()):
        result = unittest.TextTestRunner(stream=report, verbosity=2).run(suite)
    print(report.getvalue())
    raise SystemExit(not result.wasSuccessful())
