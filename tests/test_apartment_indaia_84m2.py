"""The approved 84 m² listing is separate from the existing 88 m² apartment."""
import hashlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'apartamento-indaia-bertioga-84m2'
URL = 'https://praia.digital/imoveis/' + SLUG + '.html'

class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags = []; self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class Indaia84(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT/'imoveis'/f'{SLUG}.html').read_text(encoding='utf-8')
        cls.tags = Tags(cls.text).tags

    def test_confirmed_facts_and_metadata(self):
        self.assertEqual(sum(t == 'h1' for t, _ in self.tags), 1)
        self.assertEqual(sum(t == 'main' for t, _ in self.tags), 1)
        canonicals = [a['href'] for t, a in self.tags if t == 'link' and a.get('rel') == 'canonical']
        self.assertEqual(canonicals, [URL])
        for phrase in ['84 m²', 'R$ 960.000', '2 quartos', '1 suíte', '2 vagas', 'vista parcial para o mar', 'quadra do mar', 'Condomínio e IPTU não informados']:
            self.assertIn(phrase, self.text)
        for phrase in ['IMG_0207', 'IMG_0208', 'IMG_0209', 'libfile_', 'frente-mar', 'pé na areia', '100% mobiliado', '88 m²', '950.000', '5º andar', 'Aceita financiamento']:
            self.assertNotIn(phrase, self.text)
        graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', self.text, re.S)[1])['@graph']
        apartment = next(x for x in graph if x['@type'] == 'Apartment')
        listing = next(x for x in graph if x['@type'] == 'RealEstateListing')
        self.assertEqual(apartment['numberOfBedrooms'], 2)
        self.assertEqual(apartment['floorSize']['value'], 84)
        self.assertNotIn('numberOfBathroomsTotal', apartment)
        self.assertEqual(listing['offers']['price'], '960000')
        self.assertEqual(listing['offers']['priceCurrency'], 'BRL')
        self.assertEqual(listing['mainEntity']['@id'], apartment['@id'])
        self.assertEqual(len(apartment['image']), 10)

    def test_ten_distinct_original_photos(self):
        photos = list((ROOT/'assets'/SLUG).glob('*'))
        self.assertEqual(len(photos), 10)
        self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in photos}), 10)
        for p in photos:
            self.assertEqual(p.suffix, '.jpeg')
            with Image.open(p) as im:
                self.assertEqual(len(im.getexif()), 0)
                im.verify()
        images = [a for t, a in self.tags if t == 'img']
        self.assertEqual(len(images), 11)  # Cover repeats the first gallery photo.
        self.assertEqual(len({a['src'] for a in images}), 10)
        self.assertTrue(all(a.get('alt') and a.get('width') and a.get('height') for a in images))
        self.assertIn('01-varanda-vista-parcial-mar.jpeg', images[0]['src'])
        self.assertIn('Quarto mobiliado, outro ângulo', self.text)

    def test_links_and_contact(self):
        ids = [a['id'] for _, a in self.tags if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
        for _, attrs in self.tags:
            for key in ['href', 'src']:
                target = attrs.get(key, '')
                if target.startswith('/') and not target.startswith('//'):
                    self.assertTrue((ROOT / urlsplit(target).path.lstrip('/')).is_file(), target)
                elif target.startswith('#'):
                    self.assertIn(target[1:], ids)
        contacts = [a['href'] for t, a in self.tags if t == 'a' and a.get('href', '').startswith('https://wa.me/')]
        self.assertEqual(len(contacts), 2)
        for contact in contacts:
            self.assertEqual(urlsplit(contact).path, '/5511954346288')
            self.assertIn('84 m²', unquote(contact))
            self.assertIn('960.000', unquote(contact))

    def test_catalog_sitemap_and_existing_listing_preserved(self):
        source = (ROOT/'js/main.js').read_text()
        records = json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);', source, re.S)[1])
        self.assertEqual(len({p['id'] for p in records}), len(records))
        new = [p for p in records if p['slug'] == SLUG]
        self.assertEqual(len(new), 1)
        self.assertEqual((new[0]['id'], new[0]['price'], new[0]['area']), (14, 'R$ 960.000', '84 m² úteis'))
        old = next(p for p in records if p['id'] == 13)
        self.assertEqual((old['slug'], old['price'], old['area']), ('apartamento-indaia-88m2', 'R$ 950.000', '88 m² úteis'))
        self.assertTrue((ROOT/'imoveis/apartamento-indaia-88m2.html').is_file())
        self.assertEqual((ROOT/'sitemap.xml').read_text().count(URL), 1)
        self.assertIn('js/main.js?v=', (ROOT/'imoveis.html').read_text())

if __name__ == '__main__':
    unittest.main()
