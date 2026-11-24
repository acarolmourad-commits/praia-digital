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
        self.assertNotRegex(self.html, r'R\$\s*\d')
        for path in ['/entrega-kit-temporada.html', '/entrega-descricoes-ia.html', '/servicos/anuncios-airbnb-booking.html', '/planos.html']:
            self.assertIn(f'href="{path}"', self.html)
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

class IllustrativeCases(unittest.TestCase):
    def test_examples_are_methods_not_outcomes(self):
        index=(ROOT/'cases.html').read_text(encoding='utf-8')
        cards=index.split('<h2>Cenários hipotéticos de aplicação</h2>',1)[1].split('<h2>Conteúdos recomendados</h2>',1)[0]
        routes=re.findall(r'href="(cases/case-[^"]+\.html)"',cards)
        self.assertEqual(len(routes),5)
        self.assertEqual(len(set(routes)),5)
        self.assertIn('cases/case-imobiliaria-porto-da-lua-35-leads-2026.html',routes)
        invented=r'(?:35\s+leads|(?:25|28|30|35|40|60|70)\s*%|(?:15|30|90)\s+dias|(?:4|6)\s+semanas|12\s+visitas|\bROI\s+positivo\b|\bprocesso acelerado\b)'
        self.assertNotRegex(cards,invented)
        self.assertEqual(cards.count('Métrica a observar:'),5)
        self.assertIn('id="evolucao-aplicativos"',index)
        self.assertIn('id="guia-checklist-acessivel"',index)
        for route in routes:
            with self.subTest(route=route):
                doc=(ROOT/route).read_text(encoding='utf-8')
                tags=Tags(doc).tags
                titles=[re.search(r'<'+tag+r'[^>]*>([^<]*)</'+tag+r'>',doc).group(1) for tag in ('title','h1')]
                self.assertTrue(all(x.startswith('Exemplo ilustrativo:') for x in titles))
                canonical=[x['href'] for tag,x in tags if tag=='link' and x.get('rel')=='canonical']
                self.assertEqual(canonical,['https://praia.digital/'+route])
                for key in ('description','og:title','og:description','twitter:title','twitter:description'):
                    matching=[x['content'] for tag,x in tags if tag=='meta' and (x.get('name')==key or x.get('property')==key)]
                    self.assertEqual(len(matching),1,key)
                    self.assertTrue(matching[0].startswith('Exemplo ilustrativo'),key)
                schemas=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',doc)]
                articles=[s for s in schemas if s.get('@type')=='Article']
                self.assertEqual(len(articles),1)
                self.assertEqual(articles[0]['headline'],titles[0])
                self.assertEqual(articles[0]['url'],canonical[0])
                self.assertTrue(articles[0]['description'].startswith('Exemplo ilustrativo'))
                self.assertTrue(any(q.get('name')=='Qual o conteúdo desta página?'
                    and q.get('acceptedAnswer',{}).get('text')==articles[0]['description']
                    for s in schemas if s.get('@type')=='FAQPage' for q in s.get('mainEntity',[])))
                # Ignore legacy slugs in hrefs/canonical and JSON URL fields, not human-readable claims.
                text=re.sub(r'https://praia\.digital/cases/[^"<\s]+','',doc)
                self.assertNotRegex(text,invented)
                self.assertNotIn('Em até 24 horas',text)
                self.assertIn('<h2>O que medir</h2>',text)
                self.assertNotIn('<h2>Resultado</h2>',text)


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


class AppCatalogKeyboard(unittest.TestCase):
    def test_catalog_keyboard_targets_and_complete_cards(self):
        text=(ROOT/'apps/index.html').read_text()
        tags=Tags(text).tags
        ids=[a['id'] for t,a in tags if 'id' in a]
        self.assertEqual(len(ids),len(set(ids)))
        cards=[a['href'] for t,a in tags if t=='a' and a.get('class')=='card']
        apps={'/apps/'+p.parent.name+'/' for p in (ROOT/'apps').glob('*/index.html')}
        self.assertEqual({p for p in cards if p.startswith('/apps/') and p.endswith('/')},apps)
        self.assertIn('/apps/guia-de-uso.html', cards)
        self.assertEqual(len(cards),len(set(cards)))
        for group in ['grupo-planejar','grupo-comparar','grupo-preparar','grupo-marketplaces']:
            heading=next(a for t,a in tags if t=='h2' and a.get('id')==group)
            self.assertEqual(heading['tabindex'],'-1')
        self.assertEqual(sum(t=='a' and a.get('href')=='#objetivos-apps' for t,a in tags),4)
        main=next(a for t,a in tags if t=='main')
        self.assertEqual(main['id'],'catalogo-apps');self.assertEqual(main['tabindex'],'-1')
        skip=next(a for t,a in tags if t=='a' and 'pd-skip' in a.get('class','').split())
        self.assertIn('skip-link',skip['class'].split());self.assertEqual(skip['href'],'#catalogo-apps')
        for t,a in tags:
            href=a.get('href','')
            if t=='a' and href.startswith('#'):self.assertIn(href[1:],ids)

class HomepageSeasonalSpotlight(unittest.TestCase):
    def test_black_friday_is_editorial_and_points_to_existing_page(self):
        html=(ROOT/'index.html').read_text()
        block=re.search(r'<section id="especial-black-friday".*?</section>',html,re.S).group(0)
        self.assertEqual(html.count('id="especial-black-friday"'),1)
        self.assertIn('aria-labelledby="black-friday-title"',block)
        self.assertIn('id="black-friday-title"',block)
        self.assertIn('href="/compras/black-friday.html"',block)
        self.assertTrue((ROOT/'compras/black-friday.html').is_file())
        self.assertIn('não descontos confirmados',block)
        self.assertIn('links de afiliados',block)
        self.assertIn('podemos receber comissão por compras qualificadas',block)
        self.assertNotRegex(block,r'R\$|\d+%|cupom|menor preço')

class PilotDiscovery(unittest.TestCase):
    def test_pilot_links_are_explicit_simulation_not_an_extra_app(self):
        home=(ROOT/'index.html').read_text()
        catalog=(ROOT/'apps/index.html').read_text()
        home_block=re.search(r'<aside class="pd-practice".*?</aside>',home,re.S).group()
        catalog_block=re.search(r'<nav class="pd-catalog-cards" aria-label="Outros recursos">.*?</nav>',catalog,re.S).group()
        for block in (home_block,catalog_block):
            self.assertIn('href="/ia/marketplaces/piloto/"',block)
            self.assertIn('Laboratório Estoque Vivo',block)
            self.assertIn('produtos fictícios',block)
            self.assertIn('sem conexão com lojas ou estoque real',block.lower())
        groups=re.findall(r'<section class="pd-catalog-group".*?</section>',catalog,re.S)
        self.assertEqual(sum(len(re.findall(r'class="card"',g)) for g in groups),16)
        self.assertNotIn('/ia/marketplaces/piloto/', ''.join(groups))
        self.assertTrue((ROOT/'ia/marketplaces/piloto/index.html').is_file())

if __name__=='__main__': unittest.main()
