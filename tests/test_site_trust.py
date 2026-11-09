"""Exercise committed calculators and trust markup without network, payment or submission."""
import functools,json,re,shutil,subprocess,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SLUGS=['alugar-ou-comprar','calculadora-consorcio','calculadora-financiamento','calculadora-precificacao-shopee','calculadora-valorizacao','checklist-vistoria','comparador-cidades','custo-de-compra','planejador-entrada','renda-para-financiar','simulador-roi-temporada','temporada-ou-anual','valor-imovel']
@functools.lru_cache(None)
def read(p):return (ROOT/p).read_text(encoding='utf-8')
class Tags(HTMLParser):
    def __init__(self,t):super().__init__();self.tags=[];self.feed(t)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
    def handle_startendtag(self,t,a):self.handle_starttag(t,a)
def tags(p):return Tags(read(p)).tags
NODE=r'''const fs=require('node:fs'),vm=require('node:vm');const p=JSON.parse(fs.readFileSync(0,'utf8')),el={};for(const id of p.ids)el[id]={value:'',checked:false,textContent:'',innerHTML:'',style:{},addEventListener(){},scrollIntoView(){}};for(const [id,v] of Object.entries(p.values||{})){if(!el[id])throw Error('Missing input '+id);el[id].value=String(v);}const alerts=[];const c=vm.createContext({Intl,Math,Number,Object,alert:m=>alerts.push(m),document:{getElementById:id=>{if(!el[id])throw Error('Unknown DOM id '+id);return el[id];}},window:{}});for(const s of p.scripts)vm.runInContext(s,c);vm.runInContext(p.action,c);const out={alerts,elements:{}};for(const [id,e] of Object.entries(el))out.elements[id]={text:e.textContent,style:e.style,value:e.value};process.stdout.write(JSON.stringify(out));'''
def run(slug,values,action):
    text=read('apps/'+slug+'/index.html');scripts=[m.group(1) for m in re.finditer(r'<script\b(?![^>]*type=["\']application/ld\+json)[^>]*>([\s\S]*?)</script>',text,re.I) if m.group(1).strip()]
    payload={'ids':[a['id'] for _,a in Tags(text).tags if 'id' in a],'scripts':scripts,'values':values,'action':action}
    p=subprocess.run([shutil.which('node') or 'node','-e',NODE],input=json.dumps(payload),text=True,capture_output=True,timeout=15)
    if p.returncode:raise AssertionError(p.stderr)
    return json.loads(p.stdout)
def money(s):return float(re.sub(r'[^0-9,.-]','',s).replace('.','').replace(',','.'))
class TrustStructure(unittest.TestCase):
    def test_home_routes(self):
        text=read('index.html');ids=[a['id'] for _,a in tags('index.html') if 'id' in a]
        for ident in ['apps','jornadas-apps']:self.assertEqual(ids.count(ident),1)
        for slug in SLUGS:self.assertIn('/apps/'+slug+'/',text)
        self.assertIn('/parcerias-imobiliarias-litoral.html',text);self.assertNotIn('Veja imóveis no mapa',text)
    def test_service_prices_preserved(self):
        for p in ['R$ 39 / imóvel / mês','R$ 97 / pacote','R$ 499 / anúncio / plataforma','R$ 79/mês','R$ 249/mês','R$ 799/mês']:self.assertIn(p,read('index.html'))
    def test_search_contract(self):
        tt=tags('index.html');f=next(a for t,a in tt if t=='form' and a.get('id')=='smartsearch');self.assertEqual(f['action'],'/imoveis.html');self.assertEqual(f['method'],'get')
        purpose=next(a for t,a in tt if t=='select' and a.get('name')=='finalidade');self.assertIn('required',purpose)
        self.assertIn('/js/property-search.js',read('index.html'));self.assertIn('/js/home-search.js',read('index.html'))
    def test_catalogue_handoff(self):
        text=read('apps/index.html').lower();self.assertIn('/#apps',text);self.assertRegex(text,r'não.{0,80}(transfer|compartilh)')
    def test_institutional_structure(self):
        for p in ['sobre.html','metodologia.html','cases.html','parcerias-imobiliarias-litoral.html','contato.html','politica-de-privacidade.html','solucoes/hermes-agents.html']:
            with self.subTest(path=p):
                tt=tags(p);ids=[a['id'] for _,a in tt if 'id' in a];self.assertEqual(sum(t=='h1' for t,_ in tt),1);self.assertEqual(sum(t=='main' for t,_ in tt),1);self.assertEqual(len(ids),len(set(ids)));self.assertEqual([a['href'] for t,a in tt if t=='link' and a.get('rel')=='canonical'],['https://praia.digital/'+p])
    def test_partner_form(self):
        p='parcerias-imobiliarias-litoral.html';tt=tags(p);f=next(a for t,a in tt if t=='form');ids={a['id'] for _,a in tt if 'id' in a}
        self.assertEqual(f['action'],'https://formsubmit.co/comercial@praia.digital');self.assertEqual(f['method'],'POST');self.assertTrue(all(a['for'] in ids for t,a in tt if t=='label' and 'for' in a));self.assertIn('name="_next"',read(p));self.assertIn('FormSubmit',read(p))
    def test_no_invented_customer_evidence(self):
        for p in ['cases.html','parcerias-imobiliarias-litoral.html']:
            for bad in ['Porto da Lua','Costa Verde','+35 leads','60% menos','+28%','ROI positivo em 90 dias']:self.assertNotIn(bad,read(p))
    def test_ai_fallibility(self):
        text=read('solucoes/hermes-agents.html');self.assertNotIn('O agente não inventa informações.',text);self.assertIn('pode produzir respostas incorretas',text)
    def test_privacy_not_certification(self):
        text=read('politica-de-privacidade.html');self.assertNotIn('está em conformidade com a Lei Geral',text);self.assertIn('não constitui certificação',text)
    def test_contact_responsibility(self):
        text=read('contato.html');self.assertNotIn('Assessoria completa para vender ou comprar',text);self.assertIn('profissional responsável',text)
    def test_financial_app_structure(self):
        for slug in ['custo-de-compra','valor-imovel','calculadora-valorizacao','simulador-roi-temporada']:
            p='apps/'+slug+'/index.html';tt=tags(p);ids=[a['id'] for _,a in tt if 'id' in a]
            with self.subTest(slug=slug):
                self.assertEqual(sum(t=='h1' for t,_ in tt),1);self.assertEqual(len(ids),len(set(ids)));self.assertTrue(all(a['for'] in ids for t,a in tt if t=='label' and 'for' in a))
                for ident in ['pd-app-title','pd-guide-title','pd-network-title']:self.assertIn(ident,ids)
                self.assertEqual([a['href'] for t,a in tt if t=='link' and a.get('rel')=='canonical'],['https://praia.digital/apps/'+slug+'/'])
    def test_market_claims_removed(self):
        for slug in ['custo-de-compra','valor-imovel','calculadora-valorizacao','simulador-roi-temporada']:
            text=read('apps/'+slug+'/index.html')
            for bad in ['Valorização anual por cidade','Preço médio por m² no litoral de SP','ITBI por cidade do litoral','Diária e ocupação por cidade','Faixa provável:','Excelente investimento para temporada']:self.assertNotIn(bad,text)
    def test_legacy_comparator_opt_in(self):
        text=read('apps/comparador-cidades/index.html');tt=tags('apps/comparador-cidades/index.html')
        for ident in ['legacy-ranking','legacy-reference-table']:
            d=next(a for t,a in tt if t=='details' and a.get('id')==ident);self.assertNotIn('open',d)
        self.assertRegex(text.lower(),r'não.{0,80}(auditad|validad)')
    def test_legacy_roi_no_current_market_promises(self):
        text=read('ferramentas/calculadora-roi-temporada.html')
        for bad in ['Dados reais de referência','Informações reais e atuais','Preencher com dados reais','Selic out/2026:']:self.assertNotIn(bad,text)
        self.assertIn('function calcular()',text)
    def test_no_private_payment_account_payload(self):
        for p in ['sobre.html','cases.html','metodologia.html','parcerias-imobiliarias-litoral.html','politica-de-privacidade.html']:
            for token in ['routing_number','monthly_estimated_revenue','external_accounts','acct_1','person_1','ba_1']:self.assertNotIn(token,read(p))
class CalculatorBehavior(unittest.TestCase):
    def test_cost_example(self):
        r=run('custo-de-compra',{},'exemplo();calc()');self.assertFalse(r['alerts']);self.assertAlmostEqual(money(r['elements']['total']['text']),19500)
    def test_cost_supplied_base(self):self.assertAlmostEqual(money(run('custo-de-compra',{'valor':500000,'base':400000,'aliquota':3},'calc()')['elements']['itbi']['text']),12000)
    def test_cost_missing_base(self):
        r=run('custo-de-compra',{'valor':500000,'base':'','aliquota':''},'calc()');self.assertTrue(r['alerts']);self.assertNotEqual(r['elements']['res']['style'].get('display'),'block')
    def test_cost_no_assumed_bank_charge(self):
        r=run('custo-de-compra',{'valor':500000,'base':500000,'aliquota':2},'calc()');self.assertAlmostEqual(money(r['elements']['total']['text']),10000);self.assertAlmostEqual(money(r['elements']['tarifa']['text']),0)
    def test_cost_negative_fee(self):self.assertTrue(run('custo-de-compra',{'valor':500000,'base':500000,'aliquota':2,'banco':-1},'calc()')['alerts'])
    def test_price_example(self):self.assertAlmostEqual(money(run('valor-imovel',{},'exemplo();calc()')['elements']['valor']['text']),400000)
    def test_price_positive_adjustment(self):self.assertAlmostEqual(money(run('valor-imovel',{'area':80,'m2':5000,'ajuste':10},'calc()')['elements']['valor']['text']),440000)
    def test_price_negative_adjustment(self):self.assertAlmostEqual(money(run('valor-imovel',{'area':80,'m2':5000,'ajuste':-10},'calc()')['elements']['valor']['text']),360000)
    def test_price_invalid_input(self):
        for v in [{'area':0,'m2':5000,'ajuste':0},{'area':80,'m2':5000,'ajuste':-100}]:self.assertTrue(run('valor-imovel',v,'calc()')['alerts'])
    def test_compound_growth(self):self.assertAlmostEqual(money(run('calculadora-valorizacao',{'valor':100000,'taxa':7,'anos':10,'cdi':4,'cenario':'custom'},'calcular()')['elements']['vfImo']['text']),100000*1.07**10,places=2)
    def test_compound_zero_rate(self):self.assertAlmostEqual(money(run('calculadora-valorizacao',{'valor':100000,'taxa':0,'anos':5,'cdi':0,'cenario':'custom'},'calcular()')['elements']['vfImo']['text']),100000)
    def test_compound_negative_rate(self):self.assertAlmostEqual(money(run('calculadora-valorizacao',{'valor':100000,'taxa':-2,'anos':3,'cdi':4,'cenario':'custom'},'calcular()')['elements']['vfImo']['text']),94119.2)
    def test_scenario_selection(self):
        r=run('calculadora-valorizacao',{'valor':100000,'taxa':7,'anos':1,'cdi':4,'cenario':4},'aplicar();calcular()');self.assertEqual(r['elements']['taxa']['value'],'4');self.assertAlmostEqual(money(r['elements']['vfImo']['text']),104000)
    def test_roi_math(self):
        v={'valor':500000,'adr':500,'ocup':50,'noites':200,'custos':20000,'plataforma':10,'iptu':2000,'cond':6000,'ir':10};r=run('simulador-roi-temporada',v,'calcular()');self.assertAlmostEqual(money(r['elements']['rBruta']['text']),50000);self.assertAlmostEqual(money(r['elements']['rLiq']['text']),15300)
    def test_roi_negative_cashflow(self):
        v={'valor':100000,'adr':100,'ocup':10,'noites':100,'custos':2000,'plataforma':0,'iptu':0,'cond':0,'ir':20};r=run('simulador-roi-temporada',v,'calcular()');self.assertAlmostEqual(money(r['elements']['rIR']['text']),0);self.assertAlmostEqual(money(r['elements']['rLiq']['text']),-1000);self.assertEqual(r['elements']['rPayback']['text'],'—')
class InvalidInputs(unittest.TestCase):
    def test_roi_occupancy_over_100(self):self.assertTrue(run('simulador-roi-temporada',{'valor':500000,'adr':500,'ocup':101,'noites':200},'calcular()')['alerts'])
    def test_roi_excess_nights(self):self.assertTrue(run('simulador-roi-temporada',{'valor':500000,'adr':500,'ocup':50,'noites':367},'calcular()')['alerts'])
    def test_roi_negative_cost(self):self.assertTrue(run('simulador-roi-temporada',{'valor':500000,'adr':500,'ocup':50,'noites':200,'custos':-1},'calcular()')['alerts'])
    def test_growth_rate_below_total_loss(self):self.assertTrue(run('calculadora-valorizacao',{'valor':100000,'taxa':-101,'anos':1,'cdi':4},'calcular()')['alerts'])
    def test_growth_overflow(self):self.assertTrue(run('calculadora-valorizacao',{'valor':100000,'taxa':1000,'anos':1000,'cdi':4},'calcular()')['alerts'])
    def test_price_overflow(self):self.assertTrue(run('valor-imovel',{'area':'1e308','m2':'1e308','ajuste':0},'calc()')['alerts'])
if __name__=='__main__':unittest.main()
