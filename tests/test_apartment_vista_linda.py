import json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class VistaLinda(unittest.TestCase):
 def test_listing(self):
  slug='apartamento-vista-linda-65m2';s=(ROOT/f'imoveis/{slug}.html').read_text();tags=Tags(s).tags
  self.assertEqual(sum(t=='h1' for t,a in tags),1)
  ids=[a['id'] for t,a in tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for t,a in tags:
   if t=='input':self.assertIn(a['id'],[b.get('for') for u,b in tags if u=='label'])
   for key in ['src','href']:
    link=a.get(key,'')
    if link.startswith('/') and not link.startswith('//'):self.assertTrue((ROOT/link.lstrip('/')).exists(),link)
    if link.startswith('#'):self.assertIn(link[1:],ids)
  photos=list((ROOT/'assets'/slug).glob('*'));self.assertEqual(len(photos),16)
  self.assertEqual({p.name for p in photos},{f'IMG_{n:04}.jpeg' for n in range(332,348)})
  for p in photos:
   with Image.open(p) as im:self.assertEqual(len(im.getexif()),0);im.verify()
  imgs=[a for t,a in tags if t=='img'];self.assertEqual(len(imgs),17);self.assertEqual(len(set(a['src'] for a in imgs)),16)
  self.assertTrue(all(a.get('alt') for a in imgs))
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))
  self.assertEqual(len(schema['image']),16)
  self.assertEqual(set(schema['image']),{'https://praia.digital'+a['src'] for a in imgs})
  for url in schema['image']:self.assertTrue((ROOT/url.removeprefix('https://praia.digital/')).is_file(),url)
  self.assertEqual(schema['offers']['price'],'425000');self.assertEqual(schema['floorSize']['value'],65);self.assertEqual(schema['numberOfBedrooms'],2);self.assertEqual(schema['numberOfBathroomsTotal'],1)
  for phrase in ['Vista Linda','65 m² úteis','1 vaga fixa','Totalmente mobiliado','beliches','Condomínio e IPTU não foram informados']:self.assertIn(phrase,s)
  for phrase in ['libfile_','950.000','88 m²','R$ 920','5º andar','1 suíte','IMG_0182','IMG_0183']:self.assertNotIn(phrase,s)
  self.assertFalse(any(t=='input' or t=='form' for t,a in tags))
  for phrase in ['id="simulador"', '/js/imovel-cenarios.js', 'rental-form', 'value-form', 'Simulações são ilustrativas']:
   self.assertNotIn(phrase,s)
  self.assertEqual((ROOT/'js/main.js').read_text().count('"slug": "'+slug+'"'),1)
if __name__=='__main__':unittest.main()
