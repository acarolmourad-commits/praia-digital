import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.tags=[]; self.feed(text)
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
class HomepageContent(unittest.TestCase):
    def setUp(self): self.html=(ROOT/'index.html').read_text(); self.tags=Tags(self.html).tags
    def test_search_and_landmark(self):
        form=next(a for t,a in self.tags if t=='form' and a.get('id')=='smartsearch')
        self.assertEqual(form['action'],'/imoveis.html'); self.assertEqual(form['method'],'get')
        self.assertEqual(sum(t=='main' for t,a in self.tags),1)
        self.assertEqual(sum(t=='h1' for t,a in self.tags),1)
        self.assertNotIn("this.action=",self.html)
    def test_navigation_paths_and_products(self):
        ids={a['id'] for t,a in self.tags if 'id' in a}
        for ident in ['imoveis','analise','central-airbnb-booking','produtos-comparacao']: self.assertIn(ident,ids)
        for slug in ['airbnb-booking','pricelabs']: self.assertIn('/interesse.html?produto='+slug,self.html)
        for price in ['R$ 39 / imóvel / mês','R$ 97 / pacote','R$ 499 / anúncio / plataforma','R$ 79/mês','R$ 249/mês','R$ 799/mês']: self.assertIn(price,self.html)
        self.assertNotIn('Resultados de quem já usa',self.html)
    def test_links_and_schema(self):
        ids={a['id'] for t,a in self.tags if 'id' in a}
        from urllib.parse import urlsplit
        for tag,a in self.tags:
            if tag!='a' or not a.get('href','').startswith(('/', '#')): continue
            url=urlsplit(a['href']); path=url.path
            if not path:
                self.assertIn(url.fragment,ids); continue
            target=ROOT/path.lstrip('/')
            if path.endswith('/'): target=target/'index.html'
            self.assertTrue(target.is_file(),a['href'])
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>',self.html,re.S): json.loads(blob)
        self.assertIn('https://praia.digital/imoveis.html?q={search_term_string}',self.html)
    def test_polish_and_pricelabs_scope(self):
        self.assertNotRegex(self.html,r'<div class="ai-q"')
        self.assertNotIn('outline:0',self.html)
        self.assertNotIn('class="cols" style=',self.html)
        pl=(ROOT/'anfitrioes/central-priceplabs.html').read_text()
        self.assertIn('id="gestao-pricelabs"',pl)
        self.assertIn('Ele não representa o preço de gestão contínua',pl)
        self.assertIn('/interesse.html?produto=pricelabs',pl)
if __name__=='__main__': unittest.main()
