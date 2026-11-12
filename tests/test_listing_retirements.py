"""Owner-scoped retirement: remove only confirmed records, preserve the rest."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from enforce_listing_retirements import clean_html, clean_xml, enforce, retired_slugs, retired_url


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


class ListingRetirements(unittest.TestCase):
    def test_exact_scope_and_preserved_records(self):
        slugs = retired_slugs()
        self.assertEqual(len(slugs), 45)
        fixture = json.loads((ROOT / 'tests/fixtures/catalog-preservation.json').read_text(encoding='utf-8'))
        text = (ROOT / 'js/main.js').read_text(encoding='utf-8')
        records = json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);', text, re.S)[1])
        self.assertEqual([p['id'] for p in records], [17, 16, 15, 14, 13, 12, 11, 10, 9])
        # Keep the original preservation proof intact when adding a new listing.
        self.assertEqual(digest(records[4:]), fixture['real_catalog_sha256'])
        self.assertEqual(records[3]['slug'], 'apartamento-indaia-bertioga-84m2')
        for name in ['imoveis/properties.json', 'litoral-prime-imoveis/litoral-prime-imoveis/imoveis/properties.json']:
            self.assertEqual(json.loads((ROOT / name).read_text(encoding='utf-8')), [])
        remaining = json.loads((ROOT / 'litoral-prime-imoveis/imoveis/properties.json').read_text(encoding='utf-8'))
        self.assertEqual(len(remaining), 20)
        self.assertEqual(digest(remaining), fixture['other_twenty_sha256'])
        legacy = (ROOT / 'litoral-prime-imoveis/imoveis.html').read_text(encoding='utf-8')
        self.assertIn('sobrado-geminado-peruibe.html', legacy)
        self.assertIn('apartamento-alto-padrao-bertioga.html', legacy)

    def test_cards_schema_and_unrelated_content(self):
        slugs = retired_slugs()
        unknown = '<article class="property-card"><h3>Outro imóvel</h3><a href="imoveis/keep.html">Detalhes</a></article>'
        targeted = '<article class="property-card"><div><h3>Venda sintética</h3><a href="https://wa.me/1">Contato</a><a href="/imoveis/santos-vila-nova-venda.html">Detalhes</a></div></article>'
        schema = {'@type': 'ItemList', 'numberOfItems': 2, 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'url': '/imoveis/santos-vila-nova-venda.html'},
            {'@type': 'ListItem', 'position': 2, 'url': '/imoveis/keep.html'}]}
        document = '<main>'+targeted+unknown+'</main><script type="application/ld+json">'+json.dumps(schema)+'</script>'
        cleaned = clean_html(document, slugs)
        self.assertNotIn('Venda sintética', cleaned)
        self.assertNotIn('wa.me/1', cleaned)
        self.assertNotIn('santos-vila-nova-venda', cleaned)
        self.assertIn(unknown, cleaned)
        data = json.loads(re.search(r'<script.*?>(.*?)</script>', cleaned, re.S)[1])
        self.assertEqual(data['numberOfItems'], 1)
        self.assertEqual(data['itemListElement'][0]['position'], 1)
        self.assertEqual(clean_html(cleaned, slugs), cleaned)
        untouched = '<script type="application/ld+json">{"@type":"ItemList","itemListElement":[{"position":7,"url":"keep.html"}]}</script>'
        self.assertEqual(clean_html(untouched, slugs), untouched)

    def test_exact_urls_encoded_paths_and_external_links(self):
        slugs = retired_slugs()
        self.assertTrue(retired_url('/imoveis/santos-ponta-da-praia-lan%C3%A7amento.html?x=1', slugs))
        self.assertFalse(retired_url('/imoveis/apartamento-indaia-88m2.html', slugs))
        self.assertFalse(retired_url('/imoveis/santos-vila-nova-venda-novo.html', slugs))
        self.assertFalse(retired_url('https://example.com/santos-vila-nova-venda.html', slugs))

    def test_notice_feed_and_publication_idempotence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'imoveis').mkdir()
            page = root/'imoveis/casa-terrea-itanhaem.html'
            page.write_text('<h1>Casa à venda</h1><a href="https://wa.me/1">Comprar</a>', encoding='utf-8')
            (root/'feed.xml').write_text('<feed><entry><link href="https://praia.digital/imoveis/casa-terrea-itanhaem.html"/></entry><entry><link href="https://praia.digital/imoveis/keep.html"/></entry></feed>')
            changes = enforce(root, apply=True)
            self.assertEqual(set(changes), {'imoveis/casa-terrea-itanhaem.html', 'feed.xml'})
            notice = page.read_text(encoding='utf-8')
            self.assertIn('Anúncio retirado', notice)
            self.assertIn('noindex, follow', notice)
            self.assertNotIn('RealEstateListing', notice)
            self.assertNotIn('wa.me', notice)
            self.assertIn('keep.html', (root/'feed.xml').read_text())
            self.assertNotIn('casa-terrea-itanhaem', (root/'feed.xml').read_text())
            self.assertEqual(enforce(root), [])

    def test_generator_preserves_unknown_records_and_never_reseeds(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root/'litoral-prime-imoveis'
            (base/'js').mkdir(parents=True)
            (base/'imoveis').mkdir()
            unknown = {'id': 41, 'slug': 'keep-unverified', 'price': 'R$ 123', 'extra': {'preserve': True}}
            retired = {'id': 1, 'slug': 'santos-vila-nova-venda'}
            dataset = base/'imoveis/properties.json'
            dataset.write_text(json.dumps([retired, unknown]))
            js = base/'js/main.js'
            js.write_text('const properties = '+json.dumps([retired, unknown])+';\nfunction untouched() {}')
            subprocess.run([sys.executable, str(ROOT/'litoral-prime-imoveis/scripts/expand_portfolio.py')], cwd=root, check=True, capture_output=True)
            self.assertEqual(json.loads(dataset.read_text()), [unknown])
            self.assertNotIn(retired['slug'], js.read_text())
            self.assertIn('function untouched() {}', js.read_text())


if __name__ == '__main__':
    unittest.main()
