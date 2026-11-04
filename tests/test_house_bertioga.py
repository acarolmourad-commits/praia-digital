import json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class House(unittest.TestCase):
 def test_listing_privacy_photos_and_catalog(self):
  slug='casa-terrea-bertioga-675m2';s=(ROOT/f'imoveis/{slug}.html').read_text();tags=Tags(s).tags
  self.assertEqual(sum(t=='h1' for t,a in tags),1)
  ids=[a['id'] for t,a in tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for t,a in tags:
   if t=='input':self.assertIn(a['id'],[b.get('for') for u,b in tags if u=='label'])
   for key in ['src','href']:
    link=a.get(key,'')
    if link.startswith('/') and not link.startswith('//'):self.assertTrue((ROOT/link.lstrip('/')).exists(),link)
    if link.startswith('#'):self.assertIn(link[1:],ids)
  photos=list((ROOT/'assets'/slug).glob('*'));self.assertEqual(len(photos),20)
  for p in photos:
   with Image.open(p) as im:self.assertEqual(len(im.getexif()),0);im.verify()
  imgs=[a for t,a in tags if t=='img'];self.assertEqual(len(imgs),21);self.assertEqual(len(set(a['src'] for a in imgs)),20)
  self.assertTrue(all(a.get('alt') for a in imgs))
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))
  self.assertEqual(schema['offers']['price'],'1800000');self.assertEqual(schema['floorSize']['value'],234);self.assertEqual(schema['numberOfBedrooms'],3)
  for phrase in ['675 m²','234 m²','10 vagas','duas suítes','aproximadamente 350 m da Praia da Enseada','R$ 7.692,31/m²']:self.assertIn(phrase,s)
  for phrase in ['libfile_','70,53','600.000','· aceita financiamento','Permanecem os armários','placeholder']:self.assertNotIn(phrase,s)
  self.assertEqual((ROOT/'js/main.js').read_text().count('"slug": "'+slug+'"'),1)
  self.assertEqual((ROOT/'sitemap.xml').read_text().count('https://praia.digital/imoveis/'+slug+'.html'),1)
  self.assertIn('js/main.js?v=20261103-indaia-88m2',(ROOT/'imoveis.html').read_text())
if __name__=='__main__':unittest.main()
