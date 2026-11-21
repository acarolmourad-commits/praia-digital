"""Keep the Airbnb guidance scoped to the right reservations and policy exceptions."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = 'blog/alugar-imovel-temporada-guia-proprietario-litoral-2026.html'
PAGE = (ROOT / PATH).read_text(encoding='utf-8')
RISK = PAGE.split('<h2>Redução de risco</h2>', 1)[1].split('<h2>Conclusão</h2>', 1)[0]


class AirbnbReservationRequirementsTests(unittest.TestCase):
    def test_booking_date_and_other_channels(self):
        self.assertIn('reservas feitas no Airbnb a partir de <time datetime="2026-11-20">20/11/2026', RISK)
        self.assertIn('não a data da estadia', RISK)
        self.assertIn('reservas anteriores, consulte a versão anterior', RISK)
        self.assertIn('reservas por outros canais', RISK)
        self.assertIn('https://www.airbnb.com.br/help/article/4169', RISK)

    def test_distinguishes_contract_guest_data_and_payment(self):
        for text in ('não exija como regra', 'norma aplicável da associação de moradores',
                     'seguradora do anfitrião', 'comodidade opcional', '28 noites ou mais',
                     'acomodações Luxe', 'seção indicada do anúncio antes da reserva',
                     'norma documentada', 'assinatura de um contrato permitido',
                     'regras adicionais do anúncio o que se exige e por quê',
                     'Limite a solicitação ao necessário', 'presencialmente no check-in',
                     'sem guardar cópia fora das exceções', 'não peça retenção no cartão por rotina',
                     'https://www.airbnb.com.br/help/article/2799'):
            self.assertIn(text, RISK)
        self.assertNotIn('Exigência de documento e pré-autorização', RISK)
        self.assertNotIn('Contrato simplificado com regras claras', RISK)
        self.assertIn('Seguro residencial para temporada', RISK)

    def test_preserves_canonical_and_external_cta(self):
        self.assertIn(f'<link rel="canonical" href="https://praia.digital/{PATH}"', PAGE)
        self.assertRegex(PAGE, re.compile(r'https://wa\.me/[^"]+"[^>]*>Fale com um especialista'))
        self.assertEqual(len(re.findall(r'www\.airbnb\.com\.br/help/article/', RISK)), 2)
