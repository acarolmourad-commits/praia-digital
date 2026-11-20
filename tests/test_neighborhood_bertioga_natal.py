"""Verify the dated municipal notice and stable next-step link in the Bertioga guide."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NeighborhoodBertiogaNatalTests(unittest.TestCase):
    def test_local_notice_is_dated_and_distinguishes_agenda_from_rental_planning(self):
        html = (ROOT / "bairros/bertioga/centro-historico.html").read_text(encoding="utf-8")
        notice = html.split("<h3>🎉 Natal em Bertioga:", 1)[1].split("</div>", 1)[0]
        self.assertIn('datetime="2026-12-19T20:00:00-03:00"', notice)
        self.assertIn("Parada de Natal na Avenida Tomé de Souza", notice)
        self.assertIn('datetime="2026-12-20"', notice)
        self.assertIn('datetime="2026-12-23"', notice)
        self.assertIn("a partir das 19h", notice)
        self.assertIn("Sinfonia das Águas", notice)
        self.assertIn('https://www.bertioga.sp.gov.br/bertioga-celebra-o-natal-com-ballet-circo-shows-e-grandes-eventos-de-4-a-23-de-dezembro', notice)
        self.assertIn("horários e locais podem mudar", notice)
        self.assertNotRegex(notice, r"(?i)demanda|ocupação|valorização|rentabilidade|embarque")
        self.assertIn('href="/guias/conferencia-calendarios-temporada.html"', notice)
        self.assertTrue((ROOT / "guias/conferencia-calendarios-temporada.html").is_file())
