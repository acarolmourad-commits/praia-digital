import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Parse(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.tags=[]; self.feed(text)
 def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
class Services(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'servicos-ia.html').read_text(); cls.doc=Parse(cls.html)
 def test_semantics(self):
  for tag in ['h1','main','body','html']: self.assertEqual(sum(t==tag for t,a in self.doc.tags),1)
  self.assertIn(('html',{'lang':'pt-BR'}),self.doc.tags)
 def test_links(self):
  ids={a['id'] for t,a in self.doc.tags if 'id' in a}
  for t,a in self.doc.tags:
   href=a.get('href','')
   if href.startswith('#'): self.assertIn(href[1:],ids)
   elif href.startswith('/'):
    path=ROOT/href.lstrip('/'); self.assertTrue(path.exists(),href)
 def test_no_unverified_prices_or_promises(self):
  for term in ['24/7','R$ 99','Testar Grátis','1ª Plataforma','praia-market-ai.ziontechgrou','<form','<script']:
   self.assertNotIn(term,self.html)
  for term in ['sob consulta','não sistemas já conectados','projeto em desenvolvimento','Nenhuma previsão de receita','Nada é enviado automaticamente']:
   self.assertIn(term,self.html)
 def test_contact(self):
  links=[a['href'] for t,a in self.doc.tags if t=='a' and a.get('href','').startswith('mailto:')]
  self.assertEqual(len(links),2)
  self.assertTrue(all(x.startswith('mailto:comercial@praia.digital') for x in links))
 def test_css(self):
  css=(ROOT/'css/servicos-ia-empresas.css').read_text()
  for term in ['max-width:640px','focus-visible','prefers-reduced-motion']:self.assertIn(term,css)
if __name__=='__main__': unittest.main()
