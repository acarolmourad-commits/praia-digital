"""Keep consórcio guidance's two public routes accurate and linked without transactions."""
import json
import re
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = 'consorcio-imobiliario-costeiro-litoral-sem-juros-2026.html'
LANDING = 'consorcio.html'
CALCULATOR = '/apps/calculadora-consorcio/'
MAILTO = 'mailto:comercial@praia.digital?subject=Simulação%20de%20Consórcio'
PAGES = {name: (ROOT / name).read_text(encoding='utf-8') for name in (GUIDE, LANDING)}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ConsorcioEditorial(unittest.TestCase):
    def test_routes_seo_and_original_contact(self):
        for name, source in PAGES.items():
            tags = Page(source).tags
            self.assertIn(('link', {'rel': 'canonical', 'href': 'https://praia.digital/' + name}), tags)
            self.assertEqual(sum(t == 'h1' for t, _ in tags), 1)
            self.assertEqual(sum(t == 'main' and a.get('id') == 'main' for t, a in tags), 1)
            hrefs = {a.get('href') for t, a in tags if t == 'a'}
            self.assertIn('#main', hrefs)
            self.assertIn(CALCULATOR, hrefs)
            self.assertNotIn('noindex', source)
        self.assertIn(f'href="/{GUIDE}"', PAGES[LANDING])
        self.assertIn('href="https://praia.digital/consorcio.html"', PAGES[GUIDE])
        app = (ROOT / 'apps/calculadora-consorcio/index.html').read_text(encoding='utf-8')
        self.assertIn(f'href="/{GUIDE}"', app)
        self.assertIn('Guia: custos e regras do consórcio no litoral', app)
        self.assertIn(f'href="{MAILTO}"', PAGES[LANDING])
        self.assertIn('sem enviar a mensagem automaticamente', PAGES[LANDING])
        self.assertIn('Por Carla Melo', PAGES[GUIDE])

    def test_guide_and_landing_separate_evidence_from_simulation(self):
        for page in PAGES.values():
            for term in ('fundo comum', 'sorteio ou lance', 'reajuste', 'moradia própria',
                         'taxa de administração', 'lance embutido', 'calculadora'):
                if term == 'fundo comum' and page == PAGES[LANDING]:
                    continue
                self.assertIn(term, page)
            for forbidden in (r'ademicon', r'white.label', r'nosso portal', r'casos reais', r'loop do consórcio',
                              r'90%', r'60.80%', r'R\$\s*\d', r'contemplação garantida no prazo',
                              r'menor custo total', r'valor integral para comprar', r'economia estimada'):
                self.assertNotRegex(page.lower(), forbidden)
            self.assertIn('www.bcb.gov.br/meubc/faqs/s/consorcio', page)
            self.assertIn('www.fgts.gov.br/Paginas/trabalhador/fgts-na-moradia.aspx', page)
        self.assertIn('resolu%C3%A7%C3%A3o+bcb', PAGES[GUIDE])
        self.assertIn('crédito restante para a compra', PAGES[GUIDE])
        self.assertIn('sem custo', PAGES[GUIDE])
        self.assertIn('Não presuma devolução integral ou imediata', PAGES[LANDING])

    def test_commercial_visible_faq_matches_structured_data(self):
        page = PAGES[LANDING]
        tags = Page(page).tags
        description = [a['content'] for t, a in tags if t == 'meta' and a.get('name') == 'description']
        self.assertEqual(len(description), 1)
        for key,value in [('property','og:description'),('name','twitter:description')]:
            self.assertIn(('meta',{key:value,'content':description[0]}), tags)
        schema = [json.loads(block) for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]
        faq = next(x for x in schema if x['@type'] == 'FAQPage')
        section = page.split('id="faq"', 1)[1].split('</section>', 1)[0]
        visible = re.findall(r'<div class="card"><h3>(.*?)</h3><p>(.*?)</p></div>', section)
        self.assertEqual([(unescape(q), unescape(a)) for q, a in visible],
                         [(q['name'], q['acceptedAnswer']['text']) for q in faq['mainEntity']])
        self.assertNotIn('em até 24 horas', page.lower())
