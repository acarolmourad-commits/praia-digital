"""Keep the neighborhood ferry cards aligned with the appropriate official route."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SANTOS = "https://acquavias.com.br/santos-guaruja/"
ILHABELA = "https://acquavias.com.br/sao-sebastiao-ilhabela/"
VICENTE = "https://acquavias.com.br/santos-vicente-de-carvalho/"
HORA = "https://horamarcada.acquavias.com.br/"
OLD = re.compile(
    r"DERSA|R\$\s*3,10|[Pp]edestres pagam tarifa reduzida|cartões e Pix não são aceitos|"
    r"gratuidade para pedestres está confirmada",
)


class NeighborhoodFerriesTests(unittest.TestCase):
    def test_operator_sources_and_no_obsolete_claims(self):
        for city, official, total, covered in [
            ("santos", SANTOS, 16, 14),
            ("guaruja", SANTOS, 13, 12),
            ("ilhabela", ILHABELA, 11, 9),
            ("sao-sebastiao", ILHABELA, 9, 8),
        ]:
            pages = list((ROOT / "bairros" / city).glob("*.html"))
            self.assertEqual(len(pages), total)
            count = 0
            for page in pages:
                html = page.read_text(encoding="utf-8")
                with self.subTest(page=page.relative_to(ROOT)):
                    self.assertNotRegex(html, OLD)
                    if official not in html:
                        continue
                    count += 1
                    self.assertIn('href="' + HORA + '"', html)
                    self.assertIn("gratuita para pedestres e ciclistas", html)
                    self.assertIn("operadora lista Pix e cartões de débito e crédito", html)
            self.assertEqual(count, covered)

    def test_vicente_de_carvalho_uses_a_separate_terminal_and_terms(self):
        html = (ROOT / "bairros/guaruja/vicente-de-carvalho.html").read_text(encoding="utf-8")
        self.assertIn('href="' + VICENTE + '"', html)
        self.assertIn('href="' + SANTOS + '"', html)
        self.assertRegex(html, r'travessia Santos–Vicente de Carvalho</a> é uma ligação distinta')
        self.assertIn("página desse terminal os horários, as tarifas", html)
        self.assertIn("As câmeras abaixo mostram a balsa Santos–Guarujá", html)
