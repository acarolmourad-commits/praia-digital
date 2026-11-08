import json
import re
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    'blog/guia-pet-friendly-riviera-sao-lourenco-bertioga-2026.html',
    'blog/melhor-epoca-para-visitar-riviera-de-sao-lourenco-2026.html',
    'blog/modelo-contrato-aluguel-temporada-litoral.html',
    'blog/itbi-guaruja-2026-aliquota-calculo-quem-paga.html',
]

class Structure(HTMLParser):
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=[]; self.stack=[]; self.errors=[]
        self.feed(text)
        if self.stack: self.errors.append('unclosed tags: '+str(self.stack))
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs); self.tags.append((tag,attrs))
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag not in self.VOID: self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in self.VOID: self.handle_endtag(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID: return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append('unexpected close: '+tag)
        else: self.stack.pop()

class SearchContentRefresh(unittest.TestCase):
    def cases(self):
        for path in PAGES:
            text=(ROOT/path).read_text(encoding='utf-8')
            yield path,text,Structure(text)
    def test_balanced_readable_article_landmarks(self):
        for path,text,s in self.cases():
            with self.subTest(page=path):
                self.assertEqual(s.errors,[])
                for tag in ['html','head','body','main','h1','article']:
                    self.assertEqual(sum(t==tag for t,a in s.tags),1,tag)
                self.assertEqual(len(s.ids),len(set(s.ids)))
                self.assertIn('lang="pt-BR"',text)
    def test_canonical_and_unique_metadata(self):
        for path,text,s in self.cases():
            with self.subTest(page=path):
                canonical=[a for t,a in s.tags if t=='link' and a.get('rel')=='canonical']
                self.assertEqual([a['href'] for a in canonical],['https://praia.digital/'+path])
                self.assertEqual(sum(t=='meta' and a.get('name')=='description' for t,a in s.tags),1)
                self.assertEqual(sum(t=='meta' and a.get('name')=='viewport' for t,a in s.tags),1)
                self.assertNotIn('http-equiv="refresh"',text)
                self.assertNotIn('content="noindex',text)
    def test_json_ld_matches_the_article(self):
        for path,text,s in self.cases():
            with self.subTest(page=path):
                schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)]
                posts=[x for x in schemas if x.get('@type')=='BlogPosting']
                self.assertEqual(len(posts),1)
                self.assertEqual(posts[0]['url'],'https://praia.digital/'+path)
                self.assertEqual(posts[0]['dateModified'],'2026-11-08')
                self.assertEqual(sum(x.get('@type')=='BreadcrumbList' for x in schemas),1)
                self.assertNotIn('aggregateRating',text)
    def test_table_of_contents_and_shared_assets(self):
        for path,text,s in self.cases():
            with self.subTest(page=path):
                for t,a in s.tags:
                    if t=='a' and a.get('href','').startswith('#'):
                        self.assertIn(a['href'][1:],s.ids)
                self.assertEqual(sum(t=='link' and a.get('href')=='/css/reader-guides.css' for t,a in s.tags),1)
                self.assertIn('aria-label="Neste artigo"',text)
                self.assertIn('class="skip-link"',text)
                self.assertIn('name="pd-shared-nav"',text)
                self.assertEqual(sum(t=='meta' and a.get('name')=='pd-shared-footer' for t,a in s.tags),1)
    def test_no_broken_promotional_fragments_or_invented_actions(self):
        for path,text,s in self.cases():
            with self.subTest(page=path):
                for forbidden in ['PLACEHOLDER_SLOT','Garantia e Entrega Rápida','★★★★★','backgr\n<div']:
                    self.assertNotIn(forbidden,text)
                self.assertFalse(any(t=='form' for t,a in s.tags))
                self.assertFalse(any(any(k.lower().startswith('on') for k in a) for t,a in s.tags))
    def test_pet_article_addresses_sand_restriction(self):
        text=(ROOT/PAGES[0]).read_text(encoding='utf-8')
        self.assertIn('art. 14 da Lei Municipal 205/1996',text)
        self.assertIn('proíbe a circulação e permanência',text)
        self.assertNotIn('Prefira horários menos movimentados para passeios na praia',text)
    def test_itbi_basis_and_rate_are_not_misrepresented(self):
        text=(ROOT/PAGES[3]).read_text(encoding='utf-8')
        self.assertIn('Tema 1113',text)
        self.assertIn('processo administrativo',text)
        self.assertIn('não foi possível concluir a conferência da norma municipal vigente',text)
        self.assertIn('Hipótese didática de 3%',text)
        self.assertNotIn('A base costuma ser o maior valor',text)
    def test_contract_model_and_new_checklist_preserved(self):
        text=(ROOT/PAGES[2]).read_text(encoding='utf-8')
        for phrase in ['Modelo didático para adaptação','Caução, aluguel antecipado e devolução','Cancelamento, mudança de data e saída antecipada','Checklist final de anexos e condições','orientação jurídica']:
            self.assertIn(phrase,text)
        self.assertIn('Lei do Inquilinato, arts. 37 e 38',text)
    def test_responsive_keyboard_and_print_styles(self):
        css=(ROOT/'css/reader-guides.css').read_text(encoding='utf-8')
        for expected in ['.pd-reader-page .pd-reader','@media(max-width:600px)',':focus-visible','min-height:44px','overflow-x:auto','@media print']:
            self.assertIn(expected,css)

if __name__=='__main__': unittest.main()
