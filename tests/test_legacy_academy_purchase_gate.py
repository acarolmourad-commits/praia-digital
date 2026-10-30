"""Legacy sales gate only: preserve student content, prices and existing destinations."""
import hashlib
import html
import json
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class LegacyAcademyPurchaseGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = sorted((ROOT / 'academy/cursos').glob('*/index.html'))

    def test_no_legacy_stripe_checkout(self):
        self.assertEqual(len(self.pages), 64)
        for page in self.pages:
            with self.subTest(page=page.name, course=page.parent.name):
                self.assertNotIn('buy.stripe.com', page.read_text())

    def test_paused_sales_have_course_specific_contact(self):
        count = 0
        for page in self.pages:
            source = page.read_text()
            if 'academy-purchase-paused' not in source:
                continue  # Three skeletal aliases never had purchase CTAs.
            count += 1
            with self.subTest(course=page.parent.name):
                self.assertIn('Novas compras pausadas.', source)
                self.assertIn('entrega protegida do conteúdo', source)
                self.assertIn('não reserva vaga nem conclui uma compra', source)
                self.assertNotIn('Quero garantir minha vaga', source)
                match = re.search(r'href="(mailto:[^"]+)">Consultar disponibilidade</a>', source)
                self.assertIsNotNone(match)
                target = urlsplit(html.unescape(match[1]))
                self.assertEqual(target.path, 'comercial@praia.digital')
                title = html.unescape(re.search(r'<h1>(.*?)</h1>', source, re.S)[1])
                self.assertEqual(parse_qs(target.query)['subject'], ['Disponibilidade Academy — ' + title])
        self.assertEqual(count, 61)

    def test_query_string_never_confirms_payment_or_promises_access(self):
        count = 0
        for page in self.pages:
            source = page.read_text()
            with self.subTest(course=page.parent.name):
                self.assertNotIn('Pagamento confirmado', source)
                self.assertNotIn('Em até 24h', source)
                if 'academy-purchase-paused' in source:
                    count += 1
                    self.assertIn('Pagamento não verificado', source)
                    self.assertIn('Este endereço não comprova pagamento.', source)
                    self.assertIn('Nenhum acesso é liberado por esta página.', source)
        self.assertEqual(count, 61)

    def test_student_destinations_and_price_labels_preserved(self):
        # Before-change snapshots: all 910 non-Stripe hrefs and 61 price labels.
        links, prices = [], []
        for page in self.pages:
            source = page.read_text()
            relative = page.relative_to(ROOT).as_posix()
            links.extend((relative, html.unescape(url)) for url in re.findall(r'href=[\"\']([^\"\']+)', source)
                         if not url.startswith('mailto:comercial@praia.digital?subject='))
            prices.extend((relative, value) for value in re.findall(r'<p class="price">(.*?)</p>', source, re.S))
        def digest(values):
            return hashlib.sha256(json.dumps(values, ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(len(links), 910)
        self.assertEqual(digest(links), '8b87e2fca9b9c907b5465381ff22e1f6b0e94567965e44f9342926eaae5d9e35')
        self.assertEqual(digest(prices), 'e7ba9d14e2c42e188118c3b82c3d2288bbfc4bd4b22d5a8f37d31382a03da271')


if __name__ == '__main__':
    unittest.main()
