"""Owner-scoped retirement: remove only confirmed records, preserve the rest."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from html import unescape
from urllib.parse import parse_qs, urlsplit

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
        self.assertEqual([p['id'] for p in records], [22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9])
        # Keep the original preservation proof intact when adding a new listing.
        self.assertEqual(digest([p for p in records if p['id'] in [13, 12, 11, 10, 9]]), fixture['real_catalog_sha256'])
        self.assertEqual(next(p for p in records if p['id'] == 14)['slug'], 'apartamento-indaia-bertioga-84m2')
        for name in ['imoveis/properties.json', 'litoral-prime-imoveis/litoral-prime-imoveis/imoveis/properties.json']:
            self.assertEqual(json.loads((ROOT / name).read_text(encoding='utf-8')), [])
        remaining = json.loads((ROOT / 'litoral-prime-imoveis/imoveis/properties.json').read_text(encoding='utf-8'))
        self.assertEqual(len(remaining), 20)
        self.assertEqual(digest(remaining), fixture['other_twenty_sha256'])
        legacy = (ROOT / 'litoral-prime-imoveis/imoveis.html').read_text(encoding='utf-8')
        self.assertIn('sobrado-geminado-peruibe.html', legacy)
        self.assertIn('apartamento-alto-padrao-bertioga.html', legacy)

    def test_sobrado_indaia_listing_scope_and_metadata(self):
        slug = 'sobrado-indaia-94m2'
        base = 'https://praia.digital'
        route = f'/imoveis/{slug}.html'
        html = (ROOT / route.lstrip('/')).read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'<h1\b', html)), 1)
        self.assertIn(f'rel="canonical" href="{base}{route}"', html)
        self.assertEqual((ROOT / 'sitemap.xml').read_text().count(f'<loc>{base}{route}</loc>'), 1)
        data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[1])
        house, listing = data['@graph']
        self.assertEqual(house['numberOfBedrooms'], 2)
        self.assertEqual(house['floorSize']['value'], 94.36)
        self.assertEqual(house['containedInPlace']['name'], 'Indaiá, Bertioga, SP')
        self.assertEqual(listing['offers']['price'], '1500000')
        for word in ('94,36 m²', '92,96 m²', '1 banheiro + 1 lavabo', 'R$ 193,97/mês'):
            self.assertIn(word, html)
        self.assertNotRegex(html, r'numberOfBathroomsTotal|numberOfParkingSpaces|GeoCoordinates|streetAddress|postalCode|InStock|<iframe')
        for detail in ('cooktop a gás', '9.000 BTU', '7 m de largura por 5,6 m de profundidade',
                       'cobertura de vidro temperado', 'porão', '2 a 3 carros conforme o porte',
                       'registrado em cartório', 'condição a confirmar por verificação técnica',
                       'não garantem ausência de alagamento'):
            self.assertIn(detail, html.lower() if detail == 'porão' else html)
        self.assertNotRegex(html, r'promessa de valoriza[cç][aã]o|salubre|\bCEP\b|geo:|maps/embed|google\.com/maps/(?:place|dir)')
        maps = [urlsplit(unescape(href)) for href in re.findall(r'\bhref="([^"]+)"', html)
                if re.search(r'google\.|goo\.gl|://maps\.', href, re.I)]
        self.assertEqual(len(maps), 2)
        for link, reference in zip(maps, ('Jardim Indaiá, Bertioga SP', 'Praia do Indaiá, Bertioga SP')):
            self.assertEqual((link.scheme, link.netloc, link.path, link.fragment),
                             ('https', 'www.google.com', '/maps/search/', ''))
            self.assertEqual(parse_qs(link.query, keep_blank_values=True),
                             {'api': ['1'], 'query': [reference]})
        self.assertEqual(len(house['image']), 9)
        gallery = re.findall(r'<figure><a href="([^"]+)" target="_blank" rel="noopener".*?</figure>', html)
        self.assertEqual(house['image'], [base + p for p in gallery])
        self.assertEqual(len(set(gallery)), 9)
        self.assertIn('01-varanda-terrea-jardim.webp', gallery[0])
        self.assertIn(f'<meta property="og:image" content="{house["image"][0]}">', html)
        photo_html, other_html = html.split('<h3 id="mapas-galeria">', 1)
        self.assertEqual(photo_html.count('loading="lazy"'), 9)
        map_html = other_html.split('</section>', 1)[0]
        self.assertIn('não marcam a localização do imóvel', map_html)
        self.assertIn('não têm escala, não mostram um trajeto', map_html)
        expected = [f'/assets/{slug}/{name}.svg' for name in ('perto-bairro', 'perto-praia')]
        self.assertEqual(re.findall(r'<img src="([^"]+)"', map_html), expected)
        self.assertEqual(re.findall(r'<a href="([^"]+)" target="_blank" rel="noopener noreferrer"', map_html), expected)
        self.assertEqual(map_html.count('loading="lazy"'), 2)
        self.assertFalse(any(base + path in house['image'] for path in expected))
        for rel in expected:
            svg = (ROOT / rel.lstrip('/')).read_text(encoding='utf-8')
            self.assertRegex(svg, r'<svg\b')
            self.assertNotRegex(svg, r'(?i)<(?:script|foreignObject|image)\b|\bon\w+=|\b(?:xlink:)?href=')
        for n, rel in enumerate(gallery, 1):
            self.assertRegex(rel, rf'^/assets/{slug}/{n:02}-[a-z-]+\.webp$')
            raw = (ROOT / rel.lstrip('/')).read_bytes()
            self.assertEqual(raw[:4], b'RIFF')
            self.assertEqual(raw[8:12], b'WEBP')
            pos = 12
            chunks = set()
            while pos < len(raw):
                kind = raw[pos:pos + 4]
                size = int.from_bytes(raw[pos+4:pos+8], 'little')
                chunks.add(kind)
                pos += 8 + size + size % 2
            self.assertFalse(chunks.intersection({b'EXIF', b'XMP ', b'ICCP'}), rel)
        text = (ROOT / 'js/main.js').read_text(encoding='utf-8')
        records = json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);', text, re.S)[1])
        entry = next(p for p in records if p['slug'] == slug)
        self.assertEqual((entry['id'], entry['slug'], entry['city'], entry['type']), (21, slug, 'Bertioga', 'Venda'))
        self.assertTrue(entry['availabilityUnconfirmed'])
        self.assertEqual(entry['image'], house['image'][0])
        self.assertEqual(entry['bedrooms'], '2')

    def test_saoc_listing_routes_and_gallery(self):
        from urllib.parse import urlsplit, parse_qs
        slug = 'apartamento-vicente-carvalho-ii-saoc-45m2'
        url = f'https://praia.digital/imoveis/{slug}.html'
        text = (ROOT / 'imoveis' / f'{slug}.html').read_text(encoding='utf-8')
        self.assertIn(f'<link rel="canonical" href="{url}">', text)
        self.assertIn('content="index, follow"', text)
        self.assertIn('Corretora de imóveis · CRECI-SP 303939-F', text)
        self.assertIn('Não aceita financiamento bancário', text)
        self.assertIn('Área útil informada', text)
        self.assertNotRegex(text, r'(?i)whatsapp|wa\.me|<form|<iframe|GeoCoordinates|InStock')
        contact = urlsplit(re.search(r'href="(mailto:[^"]+)"', text)[1])
        self.assertEqual(contact.path, 'comercial@praia.digital')
        self.assertEqual(parse_qs(contact.query), {'subject': ['Interesse: Apartamento de 2 dormitórios no Vicente de Carvalho II (SAOC)']})
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text)[1])
        apartment, listing = schema['@graph']
        self.assertEqual(apartment['@type'], 'Apartment')
        self.assertEqual(apartment['floorSize']['value'], 45)
        self.assertEqual(apartment['numberOfBedrooms'], 2)
        self.assertEqual(listing['offers']['price'], '235000')
        gallery = re.findall(r'<figure><a href="(/assets/[^"]+)"', text)
        self.assertEqual(len(gallery), 6)
        self.assertEqual(len(set(gallery)), 6)
        self.assertEqual(gallery[2], '/assets/apartamento-vicente-carvalho-ii-saoc-45m2/dormitorio-janela.webp')
        self.assertEqual(apartment['image'], ['https://praia.digital'+photo for photo in gallery])
        for photo in gallery:
            self.assertTrue(photo.startswith(f'/assets/{slug}/'))
            raw = (ROOT / photo.lstrip('/')).read_bytes()
            self.assertEqual((raw[:4], raw[8:12]), (b'RIFF', b'WEBP'))
            pos, chunks = 12, set()
            while pos < len(raw):
                chunks.add(raw[pos:pos+4])
                size = int.from_bytes(raw[pos+4:pos+8], 'little')
                pos += 8 + size + (size % 2)
            self.assertFalse(chunks.intersection({b'EXIF', b'XMP ', b'ICCP'}))
        js = (ROOT / 'js/main.js').read_text(encoding='utf-8')
        records = json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);', js, re.S)[1])
        entry = next(p for p in records if p['slug'] == slug)
        self.assertEqual((entry['id'], entry['type'], entry['price']), (22, 'Venda', 'R$ 235.000'))
        self.assertTrue(entry['detailsOnly'])
        self.assertTrue(entry['availabilityUnconfirmed'])
        self.assertNotIn('contactEmail', entry)
        self.assertEqual((ROOT / 'sitemap.xml').read_text(encoding='utf-8').count(f'<loc>{url}</loc>'), 1)

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
