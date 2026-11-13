import unittest,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,parse_qs,unquote
ROOT=Path(__file__).resolve().parents[1]
PAGES=['planos.html','entrega-descricoes-ia.html','entrega-kit-temporada.html','entrega-relatorio-avaliacao.html']
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.main=0;self.h1=0
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='a':self.links.append(a.get('href',''))
  if 'id' in a:self.ids.add(a['id'])
  if t=='main':self.main+=1
  if t=='h1':self.h1+=1
class TestQuotes(unittest.TestCase):
 def test_no_public_prices_or_checkout(self):
  for f in PAGES:
   s=(ROOT/f).read_text();self.assertNotIn('buy.stripe.com',s);self.assertNotIn('R$',s);self.assertIn('cotação',s)
 def test_landmarks(self):
  for f in PAGES:
   p=Parser();p.feed((ROOT/f).read_text());self.assertEqual(p.h1,1);self.assertEqual(p.main,1);self.assertIn('conteudo',p.ids)
 def test_links_resolve(self):
  for f in PAGES:
   p=Parser();p.feed((ROOT/f).read_text())
   for h in p.links:
    u=urlsplit(h)
    if u.scheme:continue
    t=ROOT/u.path.lstrip('/') if u.path else ROOT/f
    if t.is_dir():t=t/'index.html'
    self.assertTrue(t.is_file(),f'{f}: {h}')
    if u.fragment:
     z=Parser();z.feed(t.read_text());self.assertIn(u.fragment,z.ids)
 def test_quote_context_and_manual_transparency(self):
  for f in PAGES:
   p=Parser();s=(ROOT/f).read_text();p.feed(s)
   links=[u for u in p.links if u.startswith('mailto:') and '?' in u];self.assertTrue(links)
   for u in links:
    q=parse_qs(urlsplit(u).query);self.assertTrue(q['subject'][0].startswith('Cotação'));self.assertIn('Quantidade de imóveis',q['body'][0])
   self.assertIn('webmail',s);self.assertIn('não',s)
 def test_existing_customer_instructions(self):
  for f in PAGES:
   s=(ROOT/f).read_text();self.assertIn('direitos',s);self.assertIn('contrat',s)
  for f in PAGES[1:]:self.assertIn('/obrigado-',(ROOT/f).read_text())
 def test_historical_terms_preserved(self):
  # Full prior terms remain verbatim after the two explicit metadata/notice additions.
  s=(ROOT/'termos-sem-fidelidade.html').read_text();self.assertIn('referência histórica',s)
  for price in ['79','249','799','39','49','97']:self.assertIn('R$ '+price,s)
  self.assertIn('Sem multa por cancelamento ou por suspensão. Sem fidelidade.',s)
 def test_no_unconditional_service_promises(self):
  s=(ROOT/'planos.html').read_text()
  for bad in ['Sem setup','24h úteis','Até 50 leads','Assinar Starter','garante recorrência']:self.assertNotIn(bad,s)
  self.assertIn('Não. O serviço não garante',s)
if __name__=='__main__':unittest.main()
