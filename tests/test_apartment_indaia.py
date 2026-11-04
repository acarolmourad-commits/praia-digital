import json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class Indaia(unittest.TestCase):
 def test_listing(self):
  slug='apartamento-indaia-88m2';s=(ROOT/f'imoveis/{slug}.html').read_text();tags=Tags(s).tags
  self.assertEqual(sum(t=='h1' for t,a in tags),1)
  ids=[a['id'] for t,a in tags if 'id' in a];self.assertEqual(len(ids),len(set(ids)))
  for t,a in tags:
   if t=='input':self.assertIn(a['id'],[b.get('for') for u,b in tags if u=='label'])
   for key in ['src','href']:
    link=a.get(key,'')
    if link.startswith('/') and not link.startswith('//'):self.assertTrue((ROOT/link.lstrip('/')).exists(),link)
    if link.startswith('#'):self.assertIn(link[1:],ids)
  photos=list((ROOT/'assets'/slug).glob('*'));self.assertEqual(len(photos),28)
  expected={f'IMG_{n:04}.jpeg' for n in range(142,171) if n!=169}
  self.assertEqual({p.name for p in photos},expected)
  for p in photos:
   with Image.open(p) as im:self.assertEqual(len(im.getexif()),0);im.verify()
  imgs=[a for t,a in tags if t=='img'];self.assertEqual(len(imgs),29);self.assertEqual(len(set(a['src'] for a in imgs)),28)
  self.assertTrue(all(a.get('alt') for a in imgs))
  gallery=[int(n) for n in re.findall(r'<figure>.*?src="/assets/apartamento-indaia-88m2/IMG_0(\d+)\.jpeg"',s,re.S)]
  self.assertEqual(gallery,[142,143,145,144,149,153,154,151,146,147,150,155,152,159,148,156,158,157,170,160,161,162,164,165,167,168,163,166])
  schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1))
  self.assertEqual(schema['@type'],'Apartment');self.assertEqual(schema['offers']['price'],'950000');self.assertEqual(schema['floorSize']['value'],88);self.assertEqual(schema['numberOfBedrooms'],2);self.assertEqual(schema['numberOfBathroomsTotal'],2)
  for phrase in ['Indaiá','88 m² úteis','2 vagas','100% mobiliado','5º andar','R$ 920/mês','R$ 2.400/ano','R$ 10.795,45/m²','R$ 65.700','R$ 35.835','regras do condomínio','demais custos fixos']:self.assertIn(phrase,s)
  for phrase in ['IMG_0169','IMG_0171','IMG_0172','IMG_0173','IMG_0174','libfile_','675 m²','1.800.000','350 m','aceita financiamento</','qa-','placeholder']:self.assertNotIn(phrase,s)
  inputs={a['id']:a.get('value') for t,a in tags if t=='input'}
  self.assertEqual({k:inputs[k] for k in ['price','daily','occupancy','variable','fixed']},{'price':'950000','daily':'600','occupancy':'30','variable':'25','fixed':'1120'})
  self.assertEqual((ROOT/'js/main.js').read_text().count('"slug": "'+slug+'"'),1)
  self.assertEqual((ROOT/'sitemap.xml').read_text().count('https://praia.digital/imoveis/'+slug+'.html'),1)
  catalog_tags=Tags((ROOT/'imoveis.html').read_text()).tags
  self.assertTrue(any(t=='script' and re.fullmatch(r'js/main\.js\?v=[\w-]+',a.get('src','')) for t,a in catalog_tags))
if __name__=='__main__':unittest.main()
