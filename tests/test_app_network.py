import hashlib,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXPECTED=json.loads('{"apps/index.html": {"scripts": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b", "controls": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}, "apps/alugar-ou-comprar/index.html": {"scripts": "f6610a56d8dc4f5d70d8b769735606e7d5b50f8c4beea956079138e2abba578d", "controls": "0f545ca6cbdc3f9dec5bd4e952301902cfef923a0e0b9db2d198cee4cad11064"}, "apps/calculadora-consorcio/index.html": {"scripts": "2599f08ed16b106ab9bc43cf85ab106bdcd5eebdcb3e7881a1eb29315e5275d0", "controls": "b2b46634d668c25512695e47fa70535db486a471e26d93bfd1d3229c691f0611"}, "apps/calculadora-financiamento/index.html": {"scripts": "75334f5a47679a716cac5ac01d3e04df06b9b1da4f80ef5c48f056f557dbc675", "controls": "da02590c0d01820562c837bc38940ab60553d5089400fd7956d1612d07951aa4"}, "apps/calculadora-precificacao-shopee/index.html": {"scripts": "85ccaf42c3f959323e9007ef260b524b44c5ca0700f1a7b4fbe27b1bb8b94ef1", "controls": "c0764796b820c39bb23f6799ec12505bb918a76dec6445ba4a8adace5116a192"}, "apps/calculadora-valorizacao/index.html": {"scripts": "6f785987e2f73cbaefd191b89f8e7d876c219a13e746c0d0b75a3e478b3e0f42", "controls": "a579805a29c40bab9b63443ad0579a6c5dd8acf771d1d884f268e6bcf44deb6a"}, "apps/checklist-vistoria/index.html": {"scripts": "b3ca1843675c5a57b308cdc75e1a648979292bd2d69073ebc61b5f67e62ee267", "controls": "c4dc930b60bbb564e8dc26ac1c39587e5d50eedac5731abd48cccdcae04a051b"}, "apps/comparador-cidades/index.html": {"scripts": "50b8fe3c2d447dfb516b92ec6981ccab44bf789e529f1a6c802de9dafba2913c", "controls": "493c4d896f0537cfd232392dd457a889b694ff1006296e9b8df2c91a63069af4"}, "apps/custo-de-compra/index.html": {"scripts": "fb8b04362329c2f95bbd69e2ef9235884482bb3a16468958eade2c8e8127f89f", "controls": "d5c0be47b74831d59304d41ed3fa2f308247efe4b25eec64140fa8e0b271b94c"}, "apps/planejador-entrada/index.html": {"scripts": "fd9e872dea2f4372f376f206b98c31d6d0d0feec372392903796476836a68a2d", "controls": "27fa4f1c5b0df89deb11cd04feacb1124b72598c0930d8782a7cc50796aa7661"}, "apps/renda-para-financiar/index.html": {"scripts": "8427151c53a800a1f66f18fea1d53fe2cbad50d42281888811aab1d5b90c202c", "controls": "c11e16fa311513bc84d57204f9ff16b0d29d1959cb51ffe42a54e985ed3acbb6"}, "apps/simulador-roi-temporada/index.html": {"scripts": "a9c0e59642765114053c3fdb65b7b4ad840e6048cb8a58f3bccd2f2a920af649", "controls": "f8f627012f7ecb5f7f14b3a25d94b90f83164dd7fd0980768dcbd87f1df55ac0"}, "apps/temporada-ou-anual/index.html": {"scripts": "dd59451db2ce93d9942907583e49813dbf8fd088e79209df4bbb41909c54b14b", "controls": "7f523659d871f1b6a60c7491596b001703eb2268e2107762e5857d6b73758588"}, "apps/valor-imovel/index.html": {"scripts": "be84b3ded3387b072b2d2aabb51db444e6077d9e0179181de79ef04d8cf4b9c9", "controls": "e55c3e618fcb0da165009ce16d2a8606a495704d3b58c5935bdb5cdf9381af69"}, "index.html": {"scripts": "bcc165292cb50abaa98ef2807c423707163281b78e2464b5d89ef40792064c08", "controls": "7ce0d3d2ee32e1499c07e180a25457023dc9ac70c09e93698901b31563d798b4"}}')
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
