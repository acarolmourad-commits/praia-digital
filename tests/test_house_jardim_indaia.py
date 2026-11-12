"""Approved house facts, original photos and neighborhood-only public location."""
import hashlib,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SLUG='casa-jardim-indaia-180m2'
URL='https://praia.digital/imoveis/'+SLUG+'.html'
class Tags(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class HouseIndaia(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.text=(ROOT/'imoveis'/f'{SLUG}.html').read_text();cls.tags=Tags(cls.text).tags
  cls.catalog=json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);',(ROOT/'js/main.js').read_text(),re.S)[1])
 def test_confirmed_facts_and_private_location(self):
  self.assertEqual(sum(t=='h1' for t,a in self.tags),1)
  self.assertEqual(sum(t=='main' for t,a in self.tags),1)
  self.assertEqual([a['href'] for t,a in self.tags if t=='link' and a.get('rel')=='canonical'],[URL])
  for s in ['R$ 400.000','180 m²','109,91 m²','Jardim Indaiá','IPTU de 2025','churrasqueira']:self.assertIn(s,self.text)
  for s in ['streetAddress','postalCode','latitude','longitude','numberOfBedrooms','numberOfBathroomsTotal','libfile_','sediment://','valor venal','2 quartos','2 vagas','Aceita financiamento','Bertioga']:self.assertNotIn(s,self.text)
  graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.text,re.S)[1])['@graph']
  house=next(x for x in graph if x['@type']=='House');listing=next(x for x in graph if x['@type']=='RealEstateListing')
  self.assertEqual(house['floorSize']['value'],109.91);self.assertEqual(house['containedInPlace']['name'],'Jardim Indaiá')
  self.assertEqual((listing['offers']['price'],listing['offers']['priceCurrency']),('400000','BRL'))
  self.assertEqual(len(house['image']),11)
 def test_rental_study_math_sources_and_privacy(self):
  for value in ['estudo-rentabilidade','R$ 2.200','R$ 412.000','R$ 26.400','6,41%','R$ 24.200','5,87%','R$ 22.000','5,34%','47.645','64.188','34,72%','ref. 542','p. 12','não comprovam valorização','responsável técnico','não equivale a área livre edificável','Não é retorno líquido','informações do proprietário e ficha fornecida']:
   self.assertIn(value,self.text)
  self.assertEqual(round(400000*1.03),412000)
  for months,gross,pct in [(12,26400,'6,41'),(11,24200,'5,87'),(10,22000,'5,34')]:
   row=re.search(rf'<tr data-paid-months="{months}" data-gross="{gross}">(.*?)</tr>',self.text,re.S)
   self.assertIsNotNone(row)
   self.assertIn(f'<td>{pct}%</td>',row[1])
   self.assertEqual(2200*months,gross)
   self.assertEqual(f'{gross/412000*100:.2f}'.replace('.',','),pct)
  self.assertEqual(f'{(64188/47645-1)*100:.2f}'.replace('.',','),'34,72')
  self.assertNotRegex(self.text,re.compile(r'bertioga|streetAddress|postalCode|latitude|longitude',re.I))
  self.assertEqual(sum(a.get('id')=='estudo-rentabilidade' for _,a in self.tags),1)
  self.assertIn('href="#estudo-rentabilidade"',self.text)
 def test_eleven_original_photos_no_location_metadata(self):
  photos=list((ROOT/'assets'/SLUG).glob('*'));self.assertEqual(len(photos),11)
  self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in photos}),11)
  for p in photos:
   self.assertEqual(p.suffix,'.jpeg')
   with Image.open(p) as im:self.assertEqual(len(im.getexif()),0);self.assertNotIn('xmp',im.info);im.verify()
  images=[a for t,a in self.tags if t=='img'];self.assertEqual(len(images),12);self.assertEqual(len({a['src'] for a in images}),11)
  self.assertTrue(all(a.get('alt') and a.get('width') and a.get('height') for a in images))
 def test_links_and_contact(self):
  ids=[a['id'] for t,a in self.tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for _,attrs in self.tags:
   for k in ['src','href']:
    v=attrs.get(k,'')
    if v.startswith('/') and not v.startswith('//'):self.assertTrue((ROOT/urlsplit(v).path.lstrip('/')).is_file(),v)
    if v.startswith('#'):self.assertIn(v[1:],ids)
  links=[a['href'] for t,a in self.tags if t=='a' and a.get('href','').startswith('https://wa.me/')]
  self.assertEqual(len(links),2)
  for v in links:self.assertEqual(urlsplit(v).path,'/5511954346288');self.assertIn('400.000',unquote(v));self.assertIn('Jardim Indaiá',unquote(v))
 def test_catalog_and_sitemap(self):
  self.assertEqual(len({p['id'] for p in self.catalog}),len(self.catalog))
  p=next(p for p in self.catalog if p['slug']==SLUG)
  self.assertEqual((p['id'],p['price'],p['area']),(15,'R$ 400.000','109,91 m² construídos'))
  self.assertIsNone(p['bedrooms']);self.assertEqual(p['locationLabel'],'Jardim Indaiá')
  self.assertEqual((ROOT/'sitemap.xml').read_text().count(URL),1)
  self.assertRegex((ROOT/'imoveis.html').read_text(), r'js/main\.js\?v=[A-Za-z0-9_-]+')
if __name__=='__main__':unittest.main()
