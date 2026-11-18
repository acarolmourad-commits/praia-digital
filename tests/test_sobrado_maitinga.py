import unittest,json,re
from pathlib import Path
from PIL import Image
from html.parser import HTMLParser
R=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class Maitinga(unittest.TestCase):
 def test_listing(self):
  s=(R/'imoveis/sobrado-maitinga-217m2.html').read_text();tags=Parser(s).tags
  self.assertEqual(sum(t=='h1' for t,a in tags),1)
  imgs=[a for t,a in tags if t=='img'];self.assertEqual(len(imgs),21);self.assertEqual(len({a['src'] for a in imgs}),20)
  for a in imgs:
   self.assertTrue(a['alt']);p=R/a['src'].lstrip('/');self.assertTrue(p.is_file());Image.open(p).verify()
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s).group(1))
  self.assertEqual(schema['offers']['price'],'900000');self.assertEqual(schema['floorSize']['value'],217);self.assertEqual(schema['numberOfBedrooms'],5);self.assertEqual(len(schema['image']),20)
  for x in ['240 m²','3 suítes','3 vagas','Aceita financiamento','manutenção','aproximadamente 200 metros']:self.assertIn(x,s)
  for x in ['0386','0387','libfile_','bmtp','Bruno Nicola','streetAddress','numberOfBathroomsTotal']:self.assertNotIn(x,s)
  self.assertEqual((R/'js/main.js').read_text().count('"slug": "sobrado-maitinga-217m2"'),1)
  self.assertEqual((R/'sitemap.xml').read_text().count('https://praia.digital/imoveis/sobrado-maitinga-217m2.html'),1)
if __name__=='__main__':unittest.main()
