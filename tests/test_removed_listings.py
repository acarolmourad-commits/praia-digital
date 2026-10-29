"""Owner-withdrawn listings must not remain advertised or regenerate."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'peruibe-centro-venda'
DATASETS = [
    'imoveis/properties.json',
    'litoral-prime-imoveis/imoveis/properties.json',
    'litoral-prime-imoveis/litoral-prime-imoveis/imoveis/properties.json',
]


class RemovedListingTests(unittest.TestCase):
    def test_removed_page_copies_do_not_exist(self):
        for directory in ['imoveis', 'litoral-prime-imoveis/imoveis']:
            self.assertFalse((ROOT / directory / (SLUG + '.html')).exists())

    def test_active_datasets_preserve_other_peruibe_listings(self):
        for name in DATASETS:
            with self.subTest(name=name):
                records = json.loads((ROOT / name).read_text())
                slugs = [item['slug'] for item in records]
                self.assertNotIn(SLUG, slugs)
                self.assertIn('peruibe-vila-sao-paulo-aluguel', slugs)
                self.assertIn('peruibe-rio-preto-venda', slugs)

    def test_no_active_card_feed_or_sitemap_reference(self):
        for name in ['litoral-prime-imoveis/js/main.js',
                     'litoral-prime-imoveis/cidades/peruibe.html',
                     'feed.xml', 'sitemap.xml', 'sitemap-apps.xml']:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertNotIn(SLUG, text)
                self.assertNotIn('photo-1503600000000', text)
        for name in ['feed.xml', 'sitemap.xml', 'sitemap-apps.xml']:
            ET.parse(ROOT / name)

    def test_portfolio_regeneration_does_not_resurrect_listing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            js = root / 'litoral-prime-imoveis/js/main.js'
            js.parent.mkdir(parents=True)
            js.write_text('  const properties = [];\n  function escapeHtml(text) { return text; }')
            subprocess.run([sys.executable, str(ROOT / 'litoral-prime-imoveis/scripts/expand_portfolio.py')],
                           cwd=root, check=True, capture_output=True, text=True)
            records = json.loads((root / 'litoral-prime-imoveis/imoveis/properties.json').read_text())
            self.assertEqual(len(records), 39)
            self.assertNotIn(SLUG, [item['slug'] for item in records])
            self.assertNotIn(SLUG, js.read_text())
            by_id = {item['id']: item for item in records}
            self.assertNotIn(36, by_id)
            self.assertEqual(by_id[35]['slug'], 'sao vicente-sao-vicente-aluguel')
            self.assertEqual(by_id[37]['slug'], 'peruibe-vila-sao-paulo-aluguel')
            self.assertIn('photo-1503500000000', by_id[35]['image'])
            self.assertIn('photo-1503700000000', by_id[37]['image'])


if __name__ == '__main__':
    unittest.main()
