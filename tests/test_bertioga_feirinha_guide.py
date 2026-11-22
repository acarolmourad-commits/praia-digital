import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "/blog/onde-fazer-compras-feirinhas-artesanato-bertioga-2026.html"
NEWS = "https://www.bertioga.sp.gov.br/turismo/noticias/feirinha-do-bem-ganha-vitrine-para-o-ecoturismo-de-bertioga"
TRAILS = "https://www.bertioga.sp.gov.br/turismo/pontos-turisticos/trilhas"


class Tags(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, name, attrs):
        self.tags.append((name, dict(attrs)))


class FeirinhaGuide(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / URL.lstrip("/")).read_text()
        self.block = re.search(r'<section id="feirinha-do-bem".*?</section>', self.html, re.S)[0]

    def test_venue_is_separate_and_attributed(self):
        self.assertLess(self.html.index("<h2>Feira de Artesanato da Enseada</h2>"),
                        self.html.index('id="feirinha-do-bem"'))
        self.assertLess(self.html.index('id="feirinha-do-bem"'), self.html.index("<h2>Shopping Riviera</h2>"))
        for evidence in ("Avenida Vicente de Carvalho, 44", "Canal de Bertioga", "artesãos locais",
                         "dentro do próprio espaço", "ABECOTUR", "AMOLB"):
            self.assertIn(evidence, self.block)
        self.assertNotIn("Casa da Cultura", self.block)

    def test_official_next_step_does_not_promise_hours_or_booking(self):
        links = [a["href"] for tag, a in Tags(self.block).tags if tag == "a"]
        self.assertEqual(links, [NEWS, TRAILS, "/cidades/bertioga.html#visita"])
        self.assertIn("Confirme", self.block)
        self.assertIn("disponibilidade e os requisitos", self.block)
        self.assertNotRegex(self.block, r"R\$|\b\d{1,2}h\b|\d{1,2}:\d{2}|garantid[ao]|reserve aqui")
        city = Tags((ROOT / "cidades/bertioga.html").read_text())
        self.assertEqual(sum(a.get("id") == "visita" for _, a in city.tags), 1)

    def test_heading_and_canonical_are_stable(self):
        tags = Tags(self.html).tags
        self.assertEqual(
            [a["href"] for t, a in tags if t == "link" and a.get("rel") == "canonical"],
            ["https://praia.digital" + URL],
        )
        self.assertEqual(sum(a.get("id") == "feirinha-do-bem-titulo" for _, a in tags), 1)
        self.assertIn('aria-labelledby="feirinha-do-bem-titulo"', self.block)


if __name__ == "__main__":
    unittest.main()
