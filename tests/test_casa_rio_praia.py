import unittest,json,re
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
R=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class RioPraia(unittest.TestCase):
 def setUp(self):self.s=(R/'imoveis/casa-rio-da-praia-100m2.html').read_text();self.tags=Parser(self.s).tags
 def test_metadata_facts_privacy(self):
  self.assertEqual(sum(t=='h1' for t,a in self.tags),1)
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.s).group(1))
  self.assertEqual(schema['offers']['price'],'690000');self.assertEqual(schema['floorSize']['value'],100);self.assertEqual(schema['numberOfBedrooms'],3);self.assertEqual(len(schema['image']),14)
  for text in ['196 m²','1 suíte','2 vagas','Aceita financiamento','R$ 1.678','Jardim Rio da Praia']:self.assertIn(text,self.s)
  for text in ['0405','0406','libfile_','bm imobiliária','streetAddress','numberOfBathroomsTotal','6.872','200 m','Maitinga','900.000']:self.assertNotIn(text,self.s)
 def test_gallery_assets(self):
  imgs=[a for t,a in self.tags if t=='img'];self.assertEqual(len(imgs),15);self.assertEqual(len({a['src'] for a in imgs}),14)
  for a in imgs:
   self.assertTrue(a['alt']);p=R/a['src'].lstrip('/');self.assertTrue(p.is_file());Image.open(p).verify()
 def test_catalog_sitemap(self):
  self.assertEqual((R/'js/main.js').read_text().count('"slug": "casa-rio-da-praia-100m2"'),1)
  self.assertEqual((R/'sitemap.xml').read_text().count('https://praia.digital/imoveis/casa-rio-da-praia-100m2.html'),1)
if __name__=='__main__':unittest.main()
