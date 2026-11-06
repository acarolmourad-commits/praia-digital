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
        catalog=(ROOT/'imoveis.html').read_text()
        self.assertNotIn('<h3>Case real</h3>',catalog)
        self.assertIn('Cenário hipotético de captação',catalog)
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
    def test_academy_purpose_and_evidence(self):
        self.assertIn('62 kits e 8 trilhas',self.html)
        self.assertIn('compra assistida por contato',self.html)
        self.assertIn('PDF/DOCX',self.html)
        self.assertIn('href="/education/kits-2026.html"',self.html)
        self.assertIn('href="/cidades/index.html">Cidades',self.html)
        self.assertNotIn('href="/cidades/bertioga.html">Cidades',self.html)
        catalog=(ROOT/'imoveis.html').read_text()
        for claim in ['500+','1.200+','98%']: self.assertNotIn(claim,catalog)
        purposes=[a for t,a in self.tags if t=='select' and a.get('name')=='finalidade']
        self.assertEqual(len(purposes),1)
        self.assertIn('required',purposes[0])
        for file in ['index.html','imoveis.html','ferramentas/assistente-virtual.html']:
            tags=Tags((ROOT/file).read_text()).tags
            self.assertEqual(sum(t=='h1' for t,a in tags),1,file)
            self.assertEqual(sum(t=='link' and a.get('rel')=='canonical' for t,a in tags),1,file)
            self.assertTrue(any(t=='meta' and a.get('name')=='viewport' for t,a in tags),file)

class HomepageSocialPreview(unittest.TestCase):
    def test_institutional_image_and_accessible_metadata(self):
        from urllib.parse import urlsplit
        import struct
        tags=Tags((ROOT/'index.html').read_text()).tags
        def meta(key):
            values=[a.get('content') for t,a in tags if t=='meta' and (a.get('property')==key or a.get('name')==key)]
            self.assertEqual(len(values),1,key)
            return values[0]
        url=meta('og:image')
        self.assertEqual(url,'https://praia.digital/assets/social/praia-digital-institucional-v1.png')
        self.assertEqual(meta('twitter:image'),url)
        self.assertEqual(meta('twitter:card'),'summary_large_image')
        self.assertEqual(meta('og:image:type'),'image/png')
        self.assertEqual(meta('og:image:alt'),meta('twitter:image:alt'))
        self.assertIn('Praia Digital',meta('og:image:alt'))
        self.assertEqual(meta('og:locale'),'pt_BR')
        data=(ROOT/urlsplit(url).path.lstrip('/')).read_bytes()
        self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack('>II',data[16:24]),(1200,630))
        self.assertEqual((meta('og:image:width'),meta('og:image:height')),('1200','630'))
        self.assertLess(len(data),300000)
        svg=(ROOT/'assets/social/praia-digital-institucional-v1.svg').read_text()
        self.assertIn('Inteligência imobiliária para o litoral',svg)
        self.assertNotIn('<image',svg) # Original vector artwork; no unlicensed external photography.
        import xml.etree.ElementTree as ET
        root=ET.fromstring(svg)
        texts=root.findall('.//{http://www.w3.org/2000/svg}text')
        self.assertEqual(len(texts),5)
        self.assertTrue(all(t.get('x')=='600' for t in texts))
        self.assertIn('text-anchor="middle"',svg)


class HomepageAppJourneys(unittest.TestCase):
    def setUp(self):
        self.html=(ROOT/'index.html').read_text()
        self.tags=Tags(self.html).tags

    def test_restored_home_anchors_resolve_network_backlinks(self):
        from urllib.parse import urlsplit
        ids=[a['id'] for t,a in self.tags if 'id' in a]
        for anchor in ['apps','jornadas-apps']:
            self.assertEqual(ids.count(anchor),1,anchor)
        checked=0
        pages=[ROOT/'apps/index.html',*sorted((ROOT/'apps').glob('*/index.html'))]
        for page in pages:
            for tag,attrs in Tags(page.read_text()).tags:
                if tag!='a': continue
                url=urlsplit(attrs.get('href',''))
                if url.netloc not in ('','praia.digital'): continue
                if url.path in ('','/') and url.fragment in ('apps','jornadas-apps'):
                    self.assertIn(url.fragment,ids,str(page))
                    checked+=1
        self.assertGreater(checked,0)

    def test_journeys_link_every_public_app_with_canonical_paths(self):
        links={a.get('href') for t,a in self.tags if t=='a'}
        apps=sorted((ROOT/'apps').glob('*/index.html'))
        self.assertGreater(len(apps),0)
        for app in apps:
            self.assertIn('/apps/'+app.parent.name+'/',links)
        self.assertNotRegex(self.html,r'href=["\']/apps/[^"\']+/index\.html')

    def test_four_accessible_routes_and_clear_simulation_limits(self):
        import html
        match=re.search(r'<section id="apps"[^>]*>(.*?)</section>',self.html,re.S)
        self.assertIsNotNone(match)
        section=match.group(0)
        tags=Tags(section).tags
        attrs=next(a for t,a in tags if t=='section')
        self.assertEqual(attrs['aria-labelledby'],'apps-titulo')
        self.assertTrue(any(t=='h2' and a.get('id')=='apps-titulo' for t,a in tags))
        self.assertEqual(sum(t=='article' for t,a in tags),4)
        self.assertEqual(sum(t=='ol' for t,a in tags),4)
        text=html.unescape(re.sub('<[^>]+>',' ',section))
        self.assertIn('não transferem dados automaticamente',text)
        self.assertIn('não garantem retorno ou aprovação de crédito',text)
        self.assertNotRegex(text,r'R\$\s*\d|renda garantida|garantimos reservas')
        self.assertFalse(any(t in ('script','form','input') for t,a in tags))

    def test_journey_styles_are_responsive_and_keyboard_accessible(self):
        css=(ROOT/'css/app-network.css').read_text()
        self.assertIn('#jornadas-apps .grid.g2',css)
        self.assertIn('@media(max-width:640px)',css)
        self.assertIn('#jornadas-apps .app-steps a',css)
        self.assertIn('min-height:44px',css)
        self.assertIn('#jornadas-apps a:focus-visible',css)
        self.assertIn('outline:3px solid #0e7c7b',css)

if __name__=='__main__': unittest.main()
