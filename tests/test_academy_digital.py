"""Public Academy consistency checks: actual pages, curriculum and delivery, not readiness flags."""
import unittest,json,re,hashlib,subprocess,html,importlib.util
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.scripts=[];self.in_json=False;self.buf='';self.links=[];self.h1=0;self.titles=[];self.in_title=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.in_title=True;self.titles.append('')
  if tag=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.buf=''
  if tag=='a' and 'href' in a:self.links.append(a['href'])
 def handle_data(self,d):
  if self.in_json:self.buf+=d
  if self.in_title:self.titles[-1]+=d
 def handle_endtag(self,tag):
  if tag=='script' and self.in_json:self.scripts.append(json.loads(self.buf));self.in_json=False
  if tag=='title':self.in_title=False
class AcademyTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.plans=json.loads((ROOT/'docs/academy/course-learning-plans.json').read_text());cls.catalog=json.loads((ROOT/'education/assets/catalog.json').read_text());cls.prices=json.loads((ROOT/'docs/academy/course-prices.json').read_text())
 def test_release_manifest_matches_sources(self):
  release=json.loads((ROOT/'education/assets/release.json').read_text())
  self.assertEqual(release['offerings'],len(self.catalog))
  self.assertEqual(release['catalog_sha256'],hashlib.sha256((ROOT/'education/assets/catalog.json').read_bytes()).hexdigest())
  self.assertEqual(release['learning_plan_sha256'],hashlib.sha256((ROOT/'docs/academy/course-learning-plans.json').read_bytes()).hexdigest())
 def test_generator_rejects_incomplete_instruction(self):
  spec=importlib.util.spec_from_file_location('academy_builder',ROOT/'scripts/build_academy_digital.py')
  builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
  builder.read=lambda p: {'courses':{'unfinished':{}},'aliases':{}} if 'learning-plans' in p else {'courses':{'unfinished':29}}
  with self.assertRaisesRegex(ValueError,'Instructional applications'):builder.build()
 def test_inventory_reconciled(self):
  old=json.loads((ROOT/'docs/academy/inventory-64-cursos.json').read_text()); offered={c['slug'] for c in self.catalog};aliases=self.plans.get('aliases',{})
  self.assertEqual(len(old),64)
  self.assertFalse(set(aliases)&offered)
  for x in old:self.assertTrue(x['slug'] in offered or x['slug'] in aliases,x['slug'])
  self.assertEqual(len(offered),len(self.catalog))
 def test_differentiated_materials(self):
  signatures=set()
  for slug,c in self.plans['courses'].items():
   if slug in self.plans.get('aliases',{}):continue
   self.assertGreaterEqual(len(c['lessons']),3,slug)
   self.assertGreaterEqual(len(c['objectives']),3,slug)
   self.assertGreaterEqual(len(c['practice']['steps']),3,slug)
   self.assertTrue(c.get('worked_example',{}).get('walkthrough'),slug)
   self.assertGreaterEqual(len(c.get('worksheet',[])),4,slug)
   application=c.get('application',{})
   self.assertGreaterEqual(len(application.get('procedure',[])),3,slug)
   self.assertGreaterEqual(len(application.get('filled_template',[])),3,slug)
   self.assertEqual(set(application.get('failure_case',{})),{'scenario','diagnosis','correction','verification'},slug)
   def words(value):
    if isinstance(value,str):return len(value.split())
    if isinstance(value,list):return sum(words(v) for v in value)
    if isinstance(value,dict):return sum(words(v) for v in value.values())
    return 0
   self.assertGreaterEqual(words(application),350,slug)
   self.assertGreaterEqual(words({key:c[key] for key in ['lessons','worked_example','practice','worksheet','application']}),750,slug)
   paragraphs=[]
   for lesson in c['lessons']:
    body=lesson['body']; paragraphs.extend([body] if isinstance(body,str) else body)
   text=' '.join(paragraphs)
   self.assertGreaterEqual(len(text.split()),180,slug)
   sig=hashlib.sha256(text.encode()).hexdigest();self.assertNotIn(sig,signatures,slug);signatures.add(sig)
   delivery=ROOT/f'docs/academy/delivery/{slug}.html'
   self.assertTrue(delivery.is_file(),slug)
   self.assertNotIn('href="/education/assets/academy.css"',delivery.read_text())
   self.assertIn('<style>',delivery.read_text())
   for step in application['procedure']:
    self.assertIn(html.escape(step['title'],quote=True),delivery.read_text())
    body=step['body'] if isinstance(step['body'],list) else [step['body']]
    for paragraph in body:self.assertIn(html.escape(paragraph,quote=True),delivery.read_text())
 def test_generated_pages_schema_links_and_prices(self):
  for c in self.catalog:
   p=ROOT/c['path'].lstrip('/');text=p.read_text();doc=Page(text)
   self.assertEqual(doc.h1,1,str(p));self.assertEqual(len(doc.titles),1,str(p));self.assertLess(len(doc.titles[0]),160,str(p));self.assertTrue(doc.scripts)
   self.assertIn('100% digital',text);self.assertIn('R$ '+f'{c["price"]:.2f}'.replace('.',','),text)
   self.assertNotIn('imediato e vitalício',text);self.assertNotIn('Pagamento confirmado',text)
   for link in doc.links:
    if link.startswith('/education/'):
     self.assertTrue((ROOT/link.split('?')[0].split('#')[0].lstrip('/')).exists(),link)
   if c['kind']=='Curso curto digital':
    sales=(p.parent/'vendas.html').read_text();self.assertEqual(text,sales)
    sample=(p.parent/'amostra.html').read_text();self.assertNotIn('docs/academy/delivery',sample)
 def test_legacy_alias_pages(self):
  for old,target in self.plans.get('aliases',{}).items():
   for kind in ('index.html','vendas.html'):
    page=Page((ROOT/f'education/cursos/{old}/{kind}').read_text())
    self.assertEqual(page.h1,1)
    self.assertIn(f'/education/cursos/{target}/index.html',page.links)
 def test_bundles_deduplicate_and_discount(self):
  for slug,f in self.plans.get('formations',{}).items():
   if f.get('same_product'):continue
   self.assertEqual(len(f['courses']),len(set(f['courses'])))
   subtotal=sum(self.prices['courses'][x] for x in f['courses'])
   self.assertEqual(self.prices['formations'][slug],int(subtotal*.8))
 def test_delivery_not_publicly_uploaded(self):
  deploy=(ROOT/'.github/workflows/deploy.yml').read_text()
  self.assertIn('scripts/prepare_academy_publication.py',deploy)
  self.assertLess(deploy.index('scripts/prepare_academy_publication.py'),deploy.index('actions/upload-pages-artifact'))
  script=(ROOT/'scripts/prepare_academy_publication.py').read_text()
  self.assertIn("ROOT/'docs/academy/delivery'",script)
  self.assertIn("course-application-*.json",script)
  self.assertIn("COLLATERAL=('marketing','email-sequence','instagram','seo-articles')",script)
if __name__=='__main__':unittest.main()
