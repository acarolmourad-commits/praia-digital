"""Sitemap generation uses page indexing intent and is safe to import."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "scripts.gerar_sitemaps", ROOT / "scripts/gerar_sitemaps.py"
)
generator = importlib.util.module_from_spec(SPEC)
with patch('builtins.open', side_effect=AssertionError('import opened a file')):
    with patch('os.walk', side_effect=AssertionError('import scanned the site')):
        with contextlib.redirect_stdout(io.StringIO()) as import_output:
            SPEC.loader.exec_module(generator)


class SitemapGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def page(self, name, text='<title>Public page</title>'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def test_import_has_no_generation_side_effects(self):
        self.assertEqual('', import_output.getvalue())

    def test_explicit_directives_excluded_from_both_sitemaps(self):
        self.page('index.html')
        self.page('blog/public.html', '<meta name="robots" content="index, follow">')
        self.page('apps/public/index.html')
        for prefix in ['blog', 'apps']:
            self.page(prefix + '/private.html', '<meta name="robots" content="noindex, follow">')
            self.page(prefix + '/google.html', '<META CONTENT="NONE" NAME="Googlebot">')
            self.page(prefix + '/redirect.html', '<meta content="0; url=/" http-equiv="REFRESH">')
        pages, apps = generator.discover_pages(self.root)
        self.assertEqual(['blog/public.html', 'index.html'], sorted(pages))
        self.assertEqual(['apps/public/index.html'], sorted(apps))
        self.assertFalse((self.root / 'sitemap.xml').exists())

    def test_existing_directory_filename_and_hidden_exclusions_preserved(self):
        excluded = [
            'docs/public.html', 'assets/public.html', 'backup/page.html',
            'backups/page.html', 'outreach/page.html', 'partials/page.html',
            'dashboards/page.html', 'api/page.html', 'backend/page.html',
            'automation/page.html', 'academy/uploads/page.html',
            'node_modules/page.html', '.private/page.html', '404.html',
            'obrigado-contato.html', 'apps/.private/page.html',
        ]
        for name in excluded:
            self.page(name)
        self.page('academy/public.html')
        self.page('apps/visible/index.html')
        self.page('blog/not-html.txt')
        pages, apps = generator.discover_pages(self.root)
        self.assertEqual(['academy/public.html'], pages)
        self.assertEqual(['apps/visible/index.html'], apps)

    def test_main_writes_only_fixture_sitemaps_with_encoded_sorted_urls(self):
        self.page('index.html')
        self.page('blog/avaliação.html')
        self.page('blog/draft.html', '<meta name="robots" content="noindex">')
        self.page('apps/public/index.html')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, generator.main(self.root))
        def urls(name):
            return [el.text for el in ET.parse(self.root / name).findall('.//{*}loc')]
        self.assertEqual([
            'https://praia.digital/blog/avalia%C3%A7%C3%A3o.html',
            'https://praia.digital/index.html',
        ], urls('sitemap.xml'))
        self.assertEqual(['https://praia.digital/apps/public/index.html'], urls('sitemap-apps.xml'))
        self.assertIn('noindex', (self.root / 'blog/draft.html').read_text())


if __name__ == '__main__':
    unittest.main()
