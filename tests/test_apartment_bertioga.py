import json, re, unittest
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,t,a): self.tags.append((t,dict(a)))
class Apartment(unittest.TestCase):
 def test_structure_photos_privacy_and_links(self):
  p=ROOT/'imoveis/apartamento-bertioga-70m2.html';s=p.read_text();tags=Tags(s).tags
  self.assertEqual(sum(t=='h1' for t,a in tags),1)
  ids=[a['id'] for t,a in tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for t,a in tags:
   if t=='input':self.assertIn(a['id'],[b.get('for') for u,b in tags if u=='label'])
   for key in ['src','href']:
    link=a.get(key,'')
    if link.startswith('/') and not link.startswith('//'):self.assertTrue((ROOT/link.lstrip('/')).exists(),link)
    if link.startswith('#'):self.assertIn(link[1:],ids)
  photos=list((ROOT/'assets/apartamento-bertioga-70m2').glob('*'))
  self.assertEqual(len(photos),19)
  for photo in photos:
   self.assertNotIn('0065',photo.name)
   with Image.open(photo) as im:im.verify()
  images=[a for t,a in tags if t=='img'];self.assertEqual(len(images),20)
  self.assertEqual(len(set(a['src'] for a in images)),19)
  self.assertTrue(all(a.get('alt') for a in images))
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))
  self.assertEqual(schema['offers']['price'],'600000');self.assertEqual(schema['numberOfBedrooms'],2)
  self.assertNotIn('0065',s);self.assertNotIn('libfile_',s);self.assertNotIn('placeholder',s)
  self.assertEqual((ROOT/'js/main.js').read_text().count('"slug": "apartamento-bertioga-70m2"'),1)
  self.assertEqual((ROOT/'sitemap.xml').read_text().count('https://praia.digital/imoveis/apartamento-bertioga-70m2.html'),1)
if __name__=='__main__':unittest.main()
