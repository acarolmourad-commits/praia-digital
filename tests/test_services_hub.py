import json
import re
import unittest
from html import unescape
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class ServicesHubTests(unittest.TestCase):
    def test_faq_schema_matches_visible_content(self):
        source = (ROOT / 'servicos.html').read_text()
        faq = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', source, re.S)[1])
        visible = re.findall(r'<summary>([^<]+)</summary>\s*<p>(.*?)</p>', source, re.S)
        schema = [(x['name'], x['acceptedAnswer']['text']) for x in faq['mainEntity']]
        self.assertEqual(len(schema), 6)
        self.assertEqual(schema, [(unescape(q), unescape(a)) for q, a in visible])

    def test_listing_scope_is_consistent(self):
        source = (ROOT / 'servicos.html').read_text()
        self.assertNotIn('precificação dinâmica para gerar reservas', source)
        self.assertNotIn('enchem sua agenda', source)
        self.assertNotIn('sem fidelidade', source)
        for value in ['fotos fornecidas', 'orientação inicial de tarifa', 'gestão contínua', 'R$ 499 por anúncio, por plataforma', 'R$ 998']:
            self.assertIn(value, source)
        self.assertIn('roteiro de distribuição', source)
        self.assertIn('Publicação e distribuição não estão incluídas automaticamente', source)

    def test_payment_link_and_amount_preserved(self):
        for page in ['servicos.html', 'servicos/propaganda-imobiliaria.html']:
            source = (ROOT / page).read_text()
            self.assertIn('https://buy.stripe.com/bJe28sd4c0XdfxZ19e4ZR1Y', source)
            self.assertIn('R$ 499', source)
            self.assertIn('Ziontechgroup', source)
            self.assertNotIn('R$ 500', source)
        self.assertNotIn('cartão, Pix ou boleto', (ROOT / 'servicos/propaganda-imobiliaria.html').read_text())

    def test_photography_has_no_unverified_statistics(self):
        source = (ROOT / 'servico-fotografia-edicao.html').read_text()
        for claim in ['3x', '2x', '40%', '95%', 'Resultados comprovados', 'Dados que comprovam']:
            self.assertNotIn(claim, source)
        self.assertEqual(source.count('<main id="main">'), 1)
        self.assertEqual(source.count('</main>'), 1)
        self.assertNotIn('<nav aria-label="Navegação principal" class="navbar">', source)
        for term in ['R$ 150/imóvel', '20 fotos editadas/mês', 'Desconto de 30%']:
            self.assertIn(term, source)

    def test_footer_labels_and_delivery_handler(self):
        source = (ROOT / 'partials/footer.html').read_text()
        for name in ['pdFlNome', 'pdFlEmail']:
            self.assertIn(f'<label for="{name}"', source)
            self.assertEqual(source.count(f'id="{name}"'), 1)
        self.assertIn('https://formsubmit.co/ajax/comercial@praia.digital', source)
        self.assertIn('if(!r.ok||d.success===false)', source)

if __name__ == '__main__':
    unittest.main()
