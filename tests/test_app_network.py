import hashlib,json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Reviewed versions are pinned; test_site_trust.py executes the four revised calculators.
EXPECTED=json.loads('{"apps/index.html":{"scripts":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","controls":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},"apps/alugar-ou-comprar/index.html":{"scripts":"f6610a56d8dc4f5d70d8b769735606e7d5b50f8c4beea956079138e2abba578d","controls":"0f545ca6cbdc3f9dec5bd4e952301902cfef923a0e0b9db2d198cee4cad11064"},"apps/calculadora-consorcio/index.html":{"scripts":"2599f08ed16b106ab9bc43cf85ab106bdcd5eebdcb3e7881a1eb29315e5275d0","controls":"b2b46634d668c25512695e47fa70535db486a471e26d93bfd1d3229c691f0611"},"apps/calculadora-financiamento/index.html":{"scripts":"75334f5a47679a716cac5ac01d3e04df06b9b1da4f80ef5c48f056f557dbc675","controls":"da02590c0d01820562c837bc38940ab60553d5089400fd7956d1612d07951aa4"},"apps/calculadora-precificacao-shopee/index.html":{"scripts":"85ccaf42c3f959323e9007ef260b524b44c5ca0700f1a7b4fbe27b1bb8b94ef1","controls":"c0764796b820c39bb23f6799ec12505bb918a76dec6445ba4a8adace5116a192"},"apps/calculadora-valorizacao/index.html":{"scripts":"55fc0cdf1c963f2a75302c9c226d23975503b8fd12062357a143e947ec55b718","controls":"d14821b2dac7f85fb2ed548d3f3928ef50cadbc2c20061c792de3fe796f5960a"},"apps/checklist-vistoria/index.html":{"scripts":"b3ca1843675c5a57b308cdc75e1a648979292bd2d69073ebc61b5f67e62ee267","controls":"c4dc930b60bbb564e8dc26ac1c39587e5d50eedac5731abd48cccdcae04a051b"},"apps/comparador-cidades/index.html":{"scripts":"aabde83309fbe2a2600f520bbe844bcba6bb8a312f3d79894645d1817412105f","controls":"58d0b69de5634b0ecd63ed6edb11505db484d8a18a3ef7923ac1466ff6ba020e"},"apps/custo-de-compra/index.html":{"scripts":"85f392f67dc3c29351f3e991eb81914aa4b9fc2481d5281c2ab8b0e3db151747","controls":"e77d811ce385c0f3cd44b78e75731fb9d53cc1daffe2a1e7f1dfae9a80caba97"},"apps/planejador-entrada/index.html":{"scripts":"fd9e872dea2f4372f376f206b98c31d6d0d0feec372392903796476836a68a2d","controls":"27fa4f1c5b0df89deb11cd04feacb1124b72598c0930d8782a7cc50796aa7661"},"apps/renda-para-financiar/index.html":{"scripts":"8427151c53a800a1f66f18fea1d53fe2cbad50d42281888811aab1d5b90c202c","controls":"c11e16fa311513bc84d57204f9ff16b0d29d1959cb51ffe42a54e985ed3acbb6"},"apps/simulador-roi-temporada/index.html":{"scripts":"9f7b8744dc2a024f95884216465312cb33acff253e1cd0b266d71bb435df74d2","controls":"3f8337eadc1410042ed03f6ff1fecfde1297133246fc24a170bffef035969802"},"apps/temporada-ou-anual/index.html":{"scripts":"dd59451db2ce93d9942907583e49813dbf8fd088e79209df4bbb41909c54b14b","controls":"7f523659d871f1b6a60c7491596b001703eb2268e2107762e5857d6b73758588"},"apps/valor-imovel/index.html":{"scripts":"7a6e30e0a0fd94be4674f128b387cffd39d84d4f32c74cb51b1c698fa9eba3b8","controls":"03dba466dc94cb7b445ce8e7bd7c13bf293a0f0998b34ce738b00343a3afaeed"},"index.html":{"scripts":"6a3cf5192354f71615ac51034b3e97c20eda99643fcaf5bbe6d41ad59bd12167","controls":"c510dd96f7d3c8cb58b95cf09e5b486eeb9720ce4237afb88bbd30a452d1d6b4"}}')
SLUGS=['alugar-ou-comprar','calculadora-consorcio','calculadora-financiamento','calculadora-precificacao-shopee','calculadora-valorizacao','checklist-vistoria','comparador-cidades','custo-de-compra','planejador-entrada','renda-para-financiar','simulador-roi-temporada','temporada-ou-anual','valor-imovel']
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
