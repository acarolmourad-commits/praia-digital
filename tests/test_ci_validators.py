import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

validator = load('render_validator', 'scripts/validate_render_deploy.py')
nav = load('navigation_builder', 'scripts/build-navigation.py')

class ValidatorTests(unittest.TestCase):
    def test_pr_mode_is_validation_only(self):
        env = {'GITHUB_ACTIONS': 'true', 'GITHUB_EVENT_NAME': 'pull_request',
               'GITHUB_BASE_REF': 'main', 'GITHUB_REF': 'refs/pull/35/merge'}
        self.assertTrue(validator.branch_context_valid('HEAD', 'pr', env))
        self.assertFalse(validator.branch_context_valid('HEAD', 'deployment', env))
        for key, value in [('GITHUB_BASE_REF', 'develop'), ('GITHUB_REF', 'refs/heads/main'),
                           ('GITHUB_ACTIONS', 'false'), ('GITHUB_EVENT_NAME', 'push')]:
            self.assertFalse(validator.branch_context_valid('HEAD', 'pr', dict(env, **{key: value})))

    def test_deployment_requires_main(self):
        self.assertTrue(validator.branch_context_valid('main', 'deployment', {}))
        self.assertFalse(validator.branch_context_valid('feature', 'deployment', {}))
        for event in ['push', 'workflow_dispatch']:
            env = {'GITHUB_ACTIONS': 'true', 'GITHUB_EVENT_NAME': event, 'GITHUB_REF': 'refs/heads/main'}
            self.assertTrue(validator.branch_context_valid('HEAD', 'deployment', env))
            env['GITHUB_REF'] = 'refs/heads/feature'
            self.assertFalse(validator.branch_context_valid('HEAD', 'deployment', env))

    def test_repairs_only_known_empty_headings(self):
        for path, title in nav.IA_HEADINGS.items():
            source = '<h1></h1><form id="tool"><input></form>'
            fixed = nav.repair_heading(path, source)
            self.assertEqual(fixed, '<h1>' + title + '</h1><form id="tool"><input></form>')
            self.assertEqual(nav.repair_heading(path, fixed), fixed)
            self.assertEqual(nav.repair_heading(path, '<h1>Custom title</h1>'), '<h1>Custom title</h1>')
        self.assertEqual(nav.repair_heading('other.html', '<h1></h1>'), '<h1></h1>')

    def test_audit_allows_self_canonical_but_rejects_wrong_page(self):
        workflow = (ROOT / '.github/workflows/seo-page-audit.yml').read_text()
        script = textwrap.dedent(workflow.split("python3 - << 'EOF'\n", 1)[1].split('          EOF', 1)[0])
        target = 'guias/marketing-imobiliario-corretores-litoral.html'
        html = '<html><head><link rel="canonical" href="https://praia.digital/' + target + '"></head><body><h1>Guia</h1></body></html>'
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'guias').mkdir()
            (root / target).write_text(html)
            good = subprocess.run([sys.executable, '-'], input=script, text=True, cwd=root, capture_output=True)
            self.assertEqual(good.returncode, 0, good.stdout + good.stderr)
            (root / 'wrong.html').write_text(html)
            bad = subprocess.run([sys.executable, '-'], input=script, text=True, cwd=root, capture_output=True)
            self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)
            self.assertIn('ERROR wrong.html', bad.stdout)

if __name__ == '__main__':
    unittest.main()
