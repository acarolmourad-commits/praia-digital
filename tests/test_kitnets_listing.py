import unittest,json,re
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
R=Path(__file__).resolve().parents[1]
SLUG='residencial-4-kitnets-864m2'
class Parser(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class Kitnets(unittest.TestCase):
 def setUp(self):self.s=(R/f'imoveis/{SLUG}.html').read_text();self.tags=Parser(self.s).tags
 def test_metadata_facts_privacy(self):
  self.assertEqual(sum(t=='h1' for t,a in self.tags),1)
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',self.s).group(1))
  self.assertEqual(str(schema['offers']['price']),'2000000');self.assertEqual(len(schema['image']),12)
  for text in ['864 m²','4 kitnets','4 vagas','50 m','2.000.000']:self.assertIn(text,self.s)
  for text in ['IMG_0417','libfile_','streetAddress','LOCALIZACAO_CONFIRMAR','690.000','100 m²','retorno garantido']:self.assertNotIn(text,self.s)
  self.assertNotIn('floorSize',schema)
 def test_gallery_assets(self):
  imgs=[a for t,a in self.tags if t=='img'];self.assertEqual(len({a['src'] for a in imgs}),12)
  for a in imgs:
   self.assertTrue(a['alt']);p=R/a['src'].lstrip('/');self.assertTrue(p.is_file());Image.open(p).verify()
 def test_catalog_sitemap(self):
  main=(R/'js/main.js').read_text();records=json.loads(re.search(r'const properties\s*=\s*(\[.*?\]);',main,re.S)[1]);p=[p for p in records if p['slug']==SLUG];self.assertEqual(len(p),1);self.assertEqual(p[0]['price'],'R$ 2.000.000');self.assertEqual(p[0]['bedrooms'],'');self.assertIn('terreno',p[0]['area'])
  self.assertEqual((R/'sitemap.xml').read_text().count(f'https://praia.digital/imoveis/{SLUG}.html'),1)
if __name__=='__main__':unittest.main()
