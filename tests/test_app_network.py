import hashlib,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Published markup at adfe3d10, after the catalog filters and calculator revisions.
EXPECTED=json.loads('{"apps/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "05bec951f3a748ef1d9bcd0e1b27af6e7705d50e481e9ac8a6079ee5d961ee08"}, "apps/alugar-ou-comprar/index.html": {"scripts": "545c38b0922de19734fbffde62792c37c2aef6a3216cfa472449173165220f7d", "controls": "5ff241044449365d84a244149e2c76c616e37f43b7368a200eaefe9df63f53fc"}, "apps/calculadora-consorcio/index.html": {"scripts": "4126640b9075281da2b29910a5fb418429b8719bddf63c21b1f5525a9a5df33e", "controls": "0f8039cc84c7c0240316515572797f632aa5d130916f7cc7ea63debd2ca148a0"}, "apps/calculadora-financiamento/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "d62c57239c421b04103c0f19c1d2fc82fbfe1d6f86468dcc3968bb5e47c81ffd"}, "apps/calculadora-precificacao-shopee/index.html": {"scripts": "1c4a2c1f1cdbb5bfc3fbec4b2ed85e8ccda1adfebff8b7c09738208778a022e6", "controls": "c0764796b820c39bb23f6799ec12505bb918a76dec6445ba4a8adace5116a192"}, "apps/calculadora-valorizacao/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "f9f9475c8ce071ac42ae7cb718b6880406c99008ed9dca6c99972ee7305914a6"}, "apps/checklist-vistoria/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "3bdfe1d64c16439a2e2b3eb1b863da2dfbf7ca027d821722e7fabc645e9c95f9"}, "apps/comparador-cidades/index.html": {"scripts": "b6f6d6902476a3e254d6d44a41e458e9d0220b65ed2f2c98c0dd3f56121c5706", "controls": "010cc7d60074ee4be8f27507eebd937587b28db3cf1a24f489b8fd9d57e370de"}, "apps/custo-de-compra/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "e49d21b2d9f0eeeb09ee6be73165581b72817ef88b263a23f02235031784b326"}, "apps/planejador-entrada/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "cc44781db6d303d3a207744da97e3fe8351c7b2ae3db1e0cda8f4d6d795e0188"}, "apps/renda-para-financiar/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "fbe896500f4e30d6723220deb8d56c0e76d36c2a8e7e4d8040476b377b7cc107"}, "apps/simulador-roi-temporada/index.html": {"scripts": "6a3cf5192354f71615ac51034b3e97c20eda99643fcaf5bbe6d41ad59bd12167", "controls": "a20443c2c6277d4479c370bf43b1488728510776ce71796a490a7d464d5b253d"}, "apps/temporada-ou-anual/index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "9e04350f8feaf40605253e5f5f6da850e945e999678b8762e589127583b95f5c"}, "apps/valor-imovel/index.html": {"scripts": "be84b3ded3387b072b2d2aabb51db444e6077d9e0179181de79ef04d8cf4b9c9", "controls": "e55c3e618fcb0da165009ce16d2a8606a495704d3b58c5935bdb5cdf9381af69"}, "index.html": {"scripts": "75a11da44c802486bc6f65640aa48a730f0f684c5c07a42ba3cd1735eb3fb070", "controls": "aad2660a982013312634c947feac4cd0fa41dcecf690a0b563a270c74a7118fb"}}')
SLUGS=json.loads('["alugar-ou-comprar", "calculadora-consorcio", "calculadora-financiamento", "calculadora-precificacao-shopee", "calculadora-valorizacao", "checklist-vistoria", "comparador-cidades", "custo-de-compra", "planejador-entrada", "renda-para-financiar", "simulador-roi-temporada", "temporada-ou-anual", "valor-imovel"]')
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.labels=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='label' and 'for' in a:self.labels.append(a['for'])
        if tag=='h1':self.h1+=1
class NetworkTests(unittest.TestCase):
    def test_structure_and_targets(self):
        for path in EXPECTED:
            with self.subTest(path=path):
                text=(ROOT/path).read_text();page=Page(text)
                self.assertEqual(page.h1,1);self.assertEqual(len(page.ids),len(set(page.ids)))
                self.assertTrue(set(page.labels)<=set(page.ids));self.assertNotIn('//',page.links)
                self.assertIn('/css/app-network.css',text)
                if path.startswith('apps/'):
                    self.assertIn('pd-network-title',page.ids);self.assertIn('pd-app-title',page.ids)
                    for slug in SLUGS:
                        if path!='apps/'+slug+'/index.html':self.assertIn('/apps/'+slug+'/',page.links)
    def test_executable_scripts_preserved(self):
        for path,expected in EXPECTED.items():
            text=(ROOT/path).read_text()
            scripts=[m.group(1) for m in re.finditer(r'<script\b(?![^>]*type=[\"\']application/ld\+json)[^>]*>([\s\S]*?)</script>',text,re.I)]
            self.assertEqual(hashlib.sha256('\n'.join(scripts).encode()).hexdigest(),expected['scripts'],path)
    def test_controls_preserved(self):
        for path,expected in EXPECTED.items():
            controls=re.findall(r'<(?:input|select|textarea|button)\b[^>]*>',(ROOT/path).read_text(),re.I)
            self.assertEqual(hashlib.sha256('\n'.join(controls).encode()).hexdigest(),expected['controls'],path)
    def test_home_has_single_journeys_section(self):
        text=(ROOT/'index.html').read_text();page=Page(text)
        self.assertEqual(page.ids.count('jornadas-apps'),1)
        for slug in SLUGS:self.assertIn('/apps/'+slug+'/',page.links)
if __name__=='__main__':unittest.main()
