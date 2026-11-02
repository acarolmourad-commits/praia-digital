"""Focused regressions for the three practical host guides (2026-11-02)."""
import json
import re
import unittest
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
SLUGS = ('locacao-temporada-pet-friendly-litoral-2026', 'pricelabs-airbnb-preco-minimo-maximo-temporada', 'checklist-anuncio-perfeito-airbnb-booking-litoral-2026')
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.tags=[]; self.ids=[]; self.text=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if 'id' in attrs:self.ids.append(attrs['id'])
    def handle_data(self,data):self.text.append(data)
    def select(self,tag,**attrs):return [a for t,a in self.tags if t==tag and all(a.get(k)==v for k,v in attrs.items())]
class HostArticles(unittest.TestCase):
    def setUp(self):self.raw={s:(ROOT/'blog'/f'{s}.html').read_text() for s in SLUGS};self.pages={s:Page(v) for s,v in self.raw.items()}
    def test_guides_discoverable_from_blog(self):
        index=(ROOT/'blog/index.html').read_text()
        for slug in SLUGS:self.assertEqual(index.count(f'href="/blog/{slug}.html"'),1)
    def test_single_semantic_structure(self):
        for p in self.pages.values():
            for tag in ('html','head','body','main','h1','article','title'):self.assertEqual(len(p.select(tag)),1,tag)
            self.assertEqual(len(p.ids),len(set(p.ids)))
    def test_unique_metadata(self):
        for s,p in self.pages.items():
            for name in ('description','robots','viewport','twitter:card','twitter:title','twitter:description','twitter:image'):self.assertEqual(len(p.select('meta',name=name)),1)
            for prop in ('og:type','og:title','og:description','og:url','og:image'):self.assertEqual(len(p.select('meta',property=prop)),1)
            self.assertEqual(p.select('link',rel='canonical')[0]['href'],f'https://praia.digital/blog/{s}.html')
            self.assertTrue(110<=len(p.select('meta',name='description')[0]['content'])<=165)
    def test_schema_truthful_and_consistent(self):
        for s,raw in self.raw.items():
            blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',raw,re.S)
            self.assertEqual(len(blocks),1); d=json.loads(blocks[0]);p=self.pages[s]
            self.assertEqual(d['@type'],'BlogPosting');self.assertEqual(d['dateModified'],'2026-11-02')
            self.assertLess(d['datePublished'],d['dateModified']);self.assertEqual(d['headline'],p.select('meta',property='og:title')[0]['content'])
            self.assertNotIn('Offer',blocks[0]);self.assertNotIn('FAQPage',blocks[0]);self.assertIn('<time datetime="2026-11-02">',raw)
    def test_internal_links_assets_and_fragments_exist(self):
        for s,p in self.pages.items():
            for tag,a in p.tags:
                value=a.get('href') if tag in ('a','link') else a.get('src') if tag=='script' else None
                if not value:continue
                u=urlsplit(value)
                if u.netloc and u.netloc!='praia.digital':continue
                if u.scheme and u.scheme not in ('http','https'):continue
                path=ROOT/unquote(u.path).lstrip('/') if u.path else ROOT/'blog'/f'{s}.html'
                if path.is_dir():path=path/'index.html'
                self.assertTrue(path.exists(),f'{s}: {value}')
                if u.fragment:self.assertIn(unquote(u.fragment),Page(path.read_text()).ids,value)
    def test_shared_navigation_and_footer(self):
        for p in self.pages.values():
            self.assertEqual(len(p.select('meta',name='pd-shared-nav')),1);self.assertEqual(len(p.select('meta',name='pd-shared-footer')),1)
            self.assertEqual(len(p.select('script',src='/js/shared.js?v=2.0')),1)
    def test_substantive_content_and_sources(self):
        for s,raw in self.raw.items():
            body=raw.split('<article>',1)[1].split('</article>',1)[0]
            self.assertGreater(len(re.findall(r'\b\w+\b',' '.join(Page(body).text))),800,s)
            self.assertIn('Fontes e critérios de atualização',body);self.assertIn('2 de novembro de 2026',body)
            self.assertGreaterEqual(len(self.pages[s].select('h2')),7)
    def test_no_placeholder_or_fake_results(self):
        for raw in self.raw.values():
            for bad in ('gtag(\'config\', \'\'','headline": ""','Semanalmente com conteúdo','visualizações ÷ reservas','garantia de lucro','entrega automática'):self.assertNotIn(bad,raw)
    def test_commercial_scope_and_security(self):
        for raw in self.raw.values():self.assertRegex(raw.lower(),r'senhas?')
        for s in (SLUGS[0],SLUGS[2]):
            self.assertIn('R$ 499',self.raw[s]);self.assertIn('uma plataforma',self.raw[s]);self.assertIn('/servicos/anuncios-airbnb-booking.html#como-funciona',self.raw[s])
        self.assertIn('escopo e valor sob consulta',self.raw[SLUGS[1]])
    def test_pricing_worked_examples(self):
        D=Decimal;fixed=D(1800);nights=D(15);variable=D(30);clean=D(150);stay=D(3);deduct=D('.20')
        floor=(fixed/nights+variable+clean/stay)/(1-deduct)
        self.assertEqual(floor,D(250));self.assertEqual(nights*floor*(1-deduct)-fixed-nights*variable-nights/stay*clean,D(0))
        self.assertEqual((fixed/D(10)+variable+clean/stay)/(1-deduct),D(325))
        self.assertIn('R$ 325',self.raw[SLUGS[1]]);self.assertIn('R$ 250',self.raw[SLUGS[1]])
    def test_pet_cost_example(self):self.assertEqual(210-160,50);self.assertIn('custo adicional é R$ 50',self.raw[SLUGS[0]])
    def test_metrics_correct_direction_and_denominator(self):
        raw=self.raw[SLUGS[2]];self.assertIn('reservas ÷ visualizações × 100',raw);self.assertIn('Sem visualizações',raw)
        self.assertEqual(10/500*100,2);self.assertEqual(12/20*100,60);self.assertEqual(3600/12,300)
    def test_sitemap_existing_targets_updated(self):
        tree=ET.parse(ROOT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
        rows={u.find('s:loc',ns).text:u.find('s:lastmod',ns).text for u in tree.findall('s:url',ns)}
        for s in SLUGS:self.assertEqual(rows[f'https://praia.digital/blog/{s}.html'],'2026-11-02')
if __name__=='__main__':unittest.main()
