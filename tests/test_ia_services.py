import unittest
import importlib.util
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qs, unquote
ROOT=Path(__file__).resolve().parents[1]
class Parse(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.tags=[]; self.feed(text)
 def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))
class Services(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'servicos-ia.html').read_text(); cls.doc=Parse(cls.html)
 def test_semantics_and_metadata(self):
  for tag in ['h1','main','body','html']: self.assertEqual(sum(t==tag for t,a in self.doc.tags),1)
  self.assertIn(('html',{'lang':'pt-BR'}),self.doc.tags)
  self.assertIn('https://praia.digital/servicos-ia.html',self.html)
  image=next(a['content'] for t,a in self.doc.tags if a.get('property')=='og:image')
  self.assertTrue((ROOT/urlsplit(image).path.lstrip('/')).exists())
 def test_links(self):
  ids={a['id'] for t,a in self.doc.tags if 'id' in a}
  for t,a in self.doc.tags:
   href=a.get('href','')
   if href.startswith('#'): self.assertIn(href[1:],ids)
   elif href.startswith('/'):
    path=ROOT/unquote(urlsplit(href).path).lstrip('/'); self.assertTrue(path.exists(),href)
 def test_no_unverified_prices_or_promises(self):
  for term in ['24/7','R$ 99','Testar Grátis','1ª Plataforma','praia-market-ai.ziontechgrou','<form','<script']:
   self.assertNotIn(term,self.html)
  for term in ['sob consulta','não sistemas já conectados','projeto em desenvolvimento','Nenhuma previsão de receita','não representam resultados de clientes']:
   self.assertIn(term,self.html)
 def test_proposal_links_preserve_each_service(self):
  links=[a['href'] for t,a in self.doc.tags if t=='a' and a.get('href','').startswith('/solicitar-servico.html')]
  values={parse_qs(urlsplit(link).query)['servico'][0] for link in links}
  self.assertEqual(values,{'Atendimento e relacionamento','Automação de processos','Conteúdo e comunicação','Conhecimento e apoio à equipe','Diagnóstico e capacitação','Projeto personalizado'})
  self.assertEqual(len(links),8)
 def test_css(self):
  css=(ROOT/'css/servicos-ia-empresas.css').read_text()
  for term in ['max-width:640px','focus-visible','prefers-reduced-motion']:self.assertIn(term,css)
 def test_navigation_artifact_preserves_journey_and_skip_link(self):
  spec=importlib.util.spec_from_file_location('nav',ROOT/'scripts/build-navigation.py')
  nav=importlib.util.module_from_spec(spec);spec.loader.exec_module(nav)
  for page in ['servicos-ia.html','solicitar-servico.html']:
   header=nav.header_for_page(page,(ROOT/'partials/header.html').read_text())
   built,_=nav.transform((ROOT/page).read_text(),header)
   self.assertLess(built.index('class="skip skip-link"'),built.index('<header'))
   self.assertEqual(built.count('data-pd-navigation="3"'),1)
   self.assertNotIn('href="/interesse.html"',built)
   self.assertEqual(nav.transform(built,header)[0],built)
if __name__=='__main__': unittest.main()
