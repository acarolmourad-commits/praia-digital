"""Regression tests for listing metadata, without touching the published pages."""
import contextlib
import importlib.util
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('listing_schema', ROOT / 'scripts/automation/add_listing_schema.py')
listing = importlib.util.module_from_spec(spec)
# Import must not rewrite files or print a batch execution report.
with patch.object(Path, 'write_text', side_effect=AssertionError('import wrote a file')):
    with contextlib.redirect_stdout(io.StringIO()) as import_output:
        spec.loader.exec_module(listing)


class ListingSchemaTests(unittest.TestCase):
    def test_import_is_side_effect_free(self):
        self.assertEqual(import_output.getvalue(), '')

    def test_brazilian_prices_preserve_cents(self):
        for text, expected in [('R$ 1.234.567,89', '1234567.89'),
                               ('R$ 1234,56', '1234.56'),
                               ('R$ 950.000', '950000'), ('R$&nbsp;900,50', '900.50'),
                               ('R$ 0,00', '0.00')]:
            with self.subTest(text=text):
                self.assertEqual(listing.extract_price(text), expected)

    def test_unknown_and_malformed_prices_are_not_invented(self):
        for text in ['Sob consulta', 'R$ 1.23,45', 'R$ 123,4', 'R$ 1,234', 'R$ -100']:
            with self.subTest(text=text):
                self.assertEqual(listing.extract_price(text), '')

    def test_relative_and_absolute_images(self):
        page = ROOT / 'imoveis/casa.html'
        for src, expected in [('../img/casa.jpg', 'https://praia.digital/img/casa.jpg'),
                              ('fotos/casa.jpg', 'https://praia.digital/imoveis/fotos/casa.jpg'),
                              ('/img/casa.jpg', 'https://praia.digital/img/casa.jpg'),
                              ('//cdn.example.com/casa.jpg', 'https://cdn.example.com/casa.jpg'),
                              ('https://cdn.example.com/casa.jpg?a=1&amp;b=2', 'https://cdn.example.com/casa.jpg?a=1&b=2')]:
            with self.subTest(src=src):
                self.assertEqual(listing.extract_image(f'<img src="{src}">', page), expected)

    def test_absent_or_unsupported_images_do_not_create_broken_defaults(self):
        page = ROOT / 'imoveis/casa.html'
        for html in ['', '<img src="">', '<img data-src="/not-loaded.jpg">', '<img src="data:image/png;base64,abc">', '<img src="javascript:alert(1)">']:
            self.assertEqual(listing.extract_image(html, page), '')

    def test_unquoted_src_is_supported(self):
        self.assertEqual(listing.extract_image('<IMG SRC=/img/casa.jpg>', ROOT / 'imoveis/casa.html'),
                         'https://praia.digital/img/casa.jpg')

    def test_malformed_image_does_not_abort_the_batch(self):
        self.assertEqual(listing.extract_image('<img src="http://[broken"><img src="/img/casa.jpg">', ROOT / 'imoveis/casa.html'),
                         'https://praia.digital/img/casa.jpg')

    def test_offer_only_contains_a_numeric_price(self):
        for price in ['', 'Consulte', '1.000,00', 'NaN', True, {'@type': 'AggregateOffer'}]:
            schema = listing.make_listing('Casa', 'Descrição', 'https://praia.digital/imoveis/casa.html', '', price, 'Santos')
            self.assertNotIn('price', schema['offers'])
            self.assertNotIn('priceCurrency', schema['offers'])
            self.assertNotIn('image', schema)
        schema = listing.make_listing('Casa', 'Descrição', 'https://praia.digital/imoveis/casa.html', '', '1234.56', 'Santos')
        self.assertEqual(schema['offers']['price'], '1234.56')
        self.assertEqual(schema['offers']['priceCurrency'], 'BRL')

    def test_generation_uses_production_domain_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            listings = root / 'imoveis'
            listings.mkdir()
            page = listings / 'casa-santos.html'
            page.write_text('<title>Casa</title><meta name="description" content="&lt;/script&gt;"><main><p>R$ 1.234,56</p><img src="../img/casa.jpg"></main>', encoding='utf-8')
            with patch.object(listing, 'BASE', root), patch.object(listing, 'IMOVEIS', listings), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(listing.main(), 0)
                first = page.read_text(encoding='utf-8')
                self.assertEqual(listing.main(), 0)
                self.assertEqual(page.read_text(encoding='utf-8'), first)
            schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', first, re.S).group(1))
            self.assertEqual(schema['url'], 'https://praia.digital/imoveis/casa-santos.html')
            self.assertEqual(schema['image'], 'https://praia.digital/img/casa.jpg')
            self.assertEqual(schema['offers']['price'], '1234.56')

    def test_embedded_json_cannot_close_its_script_element(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            listings = root / 'imoveis'
            listings.mkdir()
            page = listings / 'casa.html'
            page.write_text('<main><img src="/img/&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;.jpg"></main>')
            with patch.object(listing, 'BASE', root), patch.object(listing, 'IMOVEIS', listings), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(listing.main(), 0)
            html = page.read_text()
            self.assertEqual(html.count('</script>'), 1)
            schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S).group(1))
            self.assertIn('</script>', schema['image'])


if __name__ == '__main__':
    unittest.main()
