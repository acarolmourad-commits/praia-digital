"""The approved 84 m² listing is separate from the existing 88 m² apartment."""
import hashlib
import json
import re
import unittest
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
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

class StudyTables(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.rows = []; self.row = None; self.cell = None; self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = {'attrs': dict(attrs), 'cells': []}
        elif tag in ('td', 'th'):
            self.cell = []
    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.row is not None and self.cell is not None:
            self.row['cells'].append(''.join(self.cell).strip()); self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row); self.row = None

def brl(value, decimals=2):
    quantized = Decimal(value).quantize(Decimal('0.01') if decimals else Decimal('1'), rounding=ROUND_HALF_UP)
    return 'R$ ' + f'{quantized:,.{decimals}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

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

    def test_study_scope_sources_and_accessibility(self):
        sections = [a for t, a in self.tags if a.get('id') == 'estudo-rentabilidade']
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]['aria-labelledby'], 'estudo-titulo')
        self.assertIn('href="#estudo-rentabilidade"', self.text)
        self.assertLess(self.text.index('id="fotos"'), self.text.index('id="estudo-rentabilidade"'))
        self.assertLess(self.text.index('id="estudo-rentabilidade"'), self.text.index('id="contato"'))
        regions = [a for t, a in self.tags if 'study-table-wrap' in a.get('class', '')]
        self.assertEqual(len(regions), 3)
        self.assertTrue(all(a.get('role') == 'region' and a.get('aria-label') and a.get('tabindex') == '0' for a in regions))
        self.assertEqual(sum(t == 'caption' for t, _ in self.tags), 3)
        self.assertTrue(all(a.get('scope') in ('row', 'col') for t, a in self.tags if t == 'th'))
        self.assertFalse(any(t in ('form', 'iframe') for t, _ in self.tags))
        self.assertTrue(all(a.get('type') == 'application/ld+json' for t, a in self.tags if t == 'script'))
        links = [a['href'] for t, a in self.tags if t == 'a' and 'href' in a]
        for url in ['https://www.airbnb.com.br/help/article/1857', 'https://www.bertioga.sp.gov.br/itbi-perguntas-e-respostas']:
            self.assertIn(url, links)
        self.assertEqual(sum('temporadalivre.com/aluguel-temporada/' in u for u in links), 2)
        self.assertEqual(sum('stj.jus.br/' in u for u in links), 2)
        self.assertIn('datetime="2026-11-06"', self.text)
        rows = {r['attrs']['data-reference']: r['cells'] for r in StudyTables(self.text).rows if 'data-reference' in r['attrs']}
        self.assertEqual(rows['55878'][1:], ['6 a 12 de novembro de 2026', 'R$ 500'])
        self.assertEqual(rows['120519'][1:], ['6 a 19 de novembro de 2026', 'R$ 700'])
        for phrase in ['não reservas realizadas no Airbnb', 'não constituem média anual', 'todos os anfitriões já migraram', 'Esse piso não entrega 6% de retorno líquido', 'não é o investimento total', 'não foi confirmada', 'hipóteses arbitrárias', 'resultado pode ser baixo ou negativo', 'convenção, regimento e atas']:
            self.assertIn(phrase, self.text)

    def test_study_acquisition_and_income_floor_math(self):
        a = next(a for _, a in self.tags if a.get('id') == 'estudo-rentabilidade')
        price, capital = Decimal(a['data-price']), Decimal(a['data-capital'])
        self.assertEqual(capital, price * (1 + Decimal(a['data-itbi-rate']) / 100))
        target = capital * Decimal(a['data-target-rate']) / 100
        self.assertEqual(target, Decimal(a['data-target-result']))
        factor = 1 - Decimal(a['data-platform-rate']) / 100
        floor = (target / factor).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        self.assertEqual(floor, Decimal(a['data-gross-floor']))
        for amount in [brl(price/84), brl(capital, 0), brl(target, 0), brl(floor)]:
            self.assertIn(amount, self.text)
        rows = [r for r in StudyTables(self.text).rows if 'data-target-daily' in r['attrs']]
        self.assertEqual(len(rows), 2)
        for row in rows:
            a = row['attrs']; daily = Decimal(a['data-target-daily'])
            nights = (target / (daily * factor)).to_integral_value(rounding=ROUND_CEILING)
            gross, after = daily * nights, daily * nights * factor
            self.assertEqual(Decimal(a['data-target-nights']), nights)
            self.assertEqual(Decimal(a['data-target-gross']), gross)
            self.assertEqual(Decimal(a['data-target-after-fee']), after)
            self.assertGreaterEqual(after, target)
            self.assertLess(daily * (nights - 1) * factor, target)
            self.assertEqual(row['cells'], [brl(daily, 0), f'{nights} noites', brl(gross, 0), brl(after, 0)])

    def test_study_appreciation_math_and_downside(self):
        rows = [r for r in StudyTables(self.text).rows if 'data-value-rate' in r['attrs']]
        self.assertEqual([r['attrs']['data-value-rate'] for r in rows], ['-3', '0', '3'])
        for row in rows:
            a = row['attrs']; rate, years = Decimal(a['data-value-rate']), int(a['data-value-years'])
            self.assertEqual(years, 5)
            value = Decimal(960000) * (1 + rate / 100) ** years
            change = value - Decimal(960000)
            self.assertEqual(Decimal(a['data-future-value']), value.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
            self.assertEqual(Decimal(a['data-value-change']), change.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
            sign = '−' if change < 0 else '+' if change > 0 else ''
            self.assertEqual(row['cells'][2:], [brl(value), sign + brl(abs(change))])
        self.assertIn('Valorização patrimonial não é renda disponível', self.text)
        self.assertIn('sem descontar inflação, corretagem, tributos e despesas de venda', self.text)

    def test_original_photo_bytes_preserved(self):
        expected = {'01-varanda-vista-parcial-mar.jpeg': 'e6157a958ef5f23baa62232918852c246c892b62d5d11fe66de2dfed7ffe850a', '02-sala-cozinha-integradas.jpeg': '4c3a6a294dab190e1b962f0f50f74c8a923e2ea35031054374497385452fb80f', '03-sala-estar-jantar.jpeg': 'aa0f3945ed89b602b731ea9094d1d9ea268700673882b166d0a6753a7df347a6', '04-sala-estar.jpeg': '772cd4d18f196a3f9190935a2b0dbc44ec17e775aec250f2144532b72cd9bc24', '05-sala-jantar.jpeg': '7f7caea49be555c5531f2e214c0f87fa519f7c5e487c1fe6ae90f6ee20b1af13', '06-cozinha-armarios.jpeg': '3a607ec126b78266dce3454bd5459753aa406f117585663cff130e4c200e821a', '07-quarto.jpeg': 'f41f31ba28d579667d695ef3ab3fb7399f5214a81e18733f30c08a11b9af1375', '08-quarto-outro-angulo.jpeg': 'a4cfc8d3c90e849d33f820101f96e80892e8ed20a4809a522624f3b05280fe0d', '09-mercado-condominio.jpeg': 'a88e42c87048a74fb509bcf21061f71893b02c4e41d23d816218a0297726cf59', '10-area-externa-condominio.jpeg': '30e0416fc06eda2138ab3089a3707c30033ce27968b0da50d3fc81e1e68657bc'}
        actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'assets'/SLUG).glob('*.jpeg')}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
