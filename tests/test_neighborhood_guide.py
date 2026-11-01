import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / 'bairros/index.html'
ARTICLES = [ROOT / 'blog' / name for name in (
    'riviera-sao-lourenco-seguranca-infraestrutura-valorizacao-2026.html',
    'estudo-rental-yield-apartamentos-1-2-dormitorios-praia-grande-2026.html')]

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.hrefs=[]; self.ids=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a' and 'href' in attrs: self.hrefs.append(attrs['href'])
        if 'id' in attrs: self.ids.append(attrs['id'])

class GuideTests(unittest.TestCase):
    def test_published_catalog_without_alias_duplicates(self):
        links=Links(HUB.read_text(encoding='utf-8')).hrefs
        guides=[x for x in links if re.fullmatch(r'/bairros/[^/]+/[^/]+\.html',x)]
        self.assertEqual(len(guides),123)
        self.assertEqual(len(set(guides)),123)
        files={'/'+p.relative_to(ROOT).as_posix() for p in (ROOT/'bairros').glob('*/*.html') if p.name!='index.html'}
        self.assertEqual(set(guides),files)
        self.assertEqual(len({x.split('/')[2] for x in guides}),12)

    def test_internal_links_and_fragments(self):
        for page in [HUB]+ARTICLES:
            parsed=Links(page.read_text(encoding='utf-8'))
            self.assertEqual(len(parsed.ids),len(set(parsed.ids)))
            for link in parsed.hrefs:
                url=urlsplit(link)
                if url.netloc: continue
                target=(ROOT/url.path.lstrip('/')) if url.path else page
                if target.is_dir(): target=target/'index.html'
                self.assertTrue(target.is_file(),str(target))
                if url.fragment:self.assertIn(unquote(url.fragment),Links(target.read_text(encoding='utf-8')).ids)

    def test_metadata_and_editorial_types(self):
        for page in [HUB]+ARTICLES:
            text=page.read_text(encoding='utf-8')
            self.assertEqual(len(re.findall(r'<h1\b',text)),1)
            self.assertIn('https://praia.digital/'+page.relative_to(ROOT).as_posix(),text)
            for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
                self.assertEqual(json.loads(data)['@context'],'https://schema.org')
        text=ARTICLES[1].read_text(encoding='utf-8')
        for title in re.findall(r'<(?:title|h1)>(.*?)</(?:title|h1)>',text):
            self.assertIn('simulação',title); self.assertNotIn('5,8%',title)
        self.assertIn('bairro aberto',ARTICLES[0].read_text(encoding='utf-8'))
        self.assertNotIn('FAQPage',ARTICLES[0].read_text(encoding='utf-8'))

    def test_financial_example(self):
        price,rate,nights,days,cost_fraction=500000,350,200,365,.22
        gross=rate*nights;cost=gross*cost_fraction;balance=gross-cost
        self.assertEqual(gross,70000);self.assertEqual(cost,15400);self.assertEqual(balance,54600)
        self.assertAlmostEqual(gross/price*100,14)
        self.assertAlmostEqual(balance/price*100,10.92)
        self.assertEqual(round(nights/days*100,1),54.8)
        self.assertAlmostEqual(balance-price*.058,25600)
        text=ARTICLES[1].read_text(encoding='utf-8')
        for value in ['R$ 70.000','R$ 15.400','R$ 54.600','14% a.a.','10,92% a.a.','54,8%','R$ 25.600','165 noites','Não inclui gastos de aquisição']:
            self.assertIn(value,text)

    def test_advertising_deduplicated(self):
        for page in ARTICLES:
            text=page.read_text(encoding='utf-8');links=Links(text).hrefs
            ads=[link for link in links if 'amazon.com.br' in link]
            self.assertEqual(len(ads),4);self.assertEqual(len(set(ads)),4)
            self.assertEqual(text.count('Programa de Associados'),1)
            self.assertGreater(text.index('class="publicity"'),text.index('id="fontes"'))

if __name__=='__main__':unittest.main()
