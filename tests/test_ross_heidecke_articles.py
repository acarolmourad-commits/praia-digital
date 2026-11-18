import unittest,json,re
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['tabela-ross-heidecke-como-ler','ross-heidecke-formulas-valor-residual','valorizacao-imovel-depreciacao-construcao']
class RossArticles(unittest.TestCase):
 def test_no_invented_scenarios(self):
  for slug in SLUGS:
   text=(ROOT/"blog"/f"{slug}.html").read_text()
   for forbidden in ("R$", "0,7184", "0,648", "Premissas ilustrativas", "Imagine dois cenários", "30%", "70%"):
    self.assertNotIn(forbidden,text)
 def test_metadata_discovery_and_warnings(self):
  index=(ROOT/'blog/index.html').read_text();search=json.loads((ROOT/'data/content-search.json').read_text());sitemap=(ROOT/'sitemap.xml').read_text()
  for slug in SLUGS:
   path='/blog/'+slug+'.html';s=(ROOT/path.lstrip('/')).read_text()
   self.assertEqual(s.count('<h1>'),1);self.assertEqual(s.count('<main '),1)
   schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)[1]);self.assertEqual(schema['url'],'https://praia.digital'+path)
   self.assertIn('Não substitui vistoria',s);self.assertNotIn('1555102190',s);self.assertNotIn('RELATED',s)
   self.assertIn(path,index);self.assertEqual(sum(i['url']==path for i in search),1);self.assertIn('https://praia.digital'+path,sitemap)
 def test_internal_links(self):
  for slug in SLUGS:
   s=(ROOT/'blog'/f'{slug}.html').read_text()
   for path in re.findall(r'(?:href|src)="(/[^"#?]*)',s):
    target=ROOT/path.lstrip('/');self.assertTrue(target.exists(),path)
if __name__=='__main__':unittest.main()
