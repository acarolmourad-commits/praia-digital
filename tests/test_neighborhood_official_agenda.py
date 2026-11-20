"""Guard against repeating stale, unverified agendas for Itanhaém and Ilhabela."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENDAS = {
    "itanhaem": (("centro-historico", "centro", "gaivota", "jardim-mariana", "jardim-sao-paulo", "praia", "suarao", "vila-sao-joao", "vila-veneza"),
                 "https://www2.itanhaem.sp.gov.br/turismo/calendario.html"),
    "ilhabela": (("armacao", "bonete", "fumaca", "itaguacu", "jardim-sao-paulo", "praia-da-enseada", "saco-da-capela", "vila-veneza", "vila"),
                "https://www.ilhabela.sp.gov.br/portal/agenda"),
}
STALE = re.compile(r"fim de 2026\)</h3>|Itaverão Food Fest|25/out–15/nov|Réveillon oficial com shows gratuitos|Réveillon Isla Parador|Réveillon Vila Salga")


class NeighborhoodOfficialAgendaTests(unittest.TestCase):
    def test_all_former_copies_link_to_official_source_and_have_no_stale_editions(self):
        for city, (slugs, agenda) in AGENDAS.items():
            for page in sorted((ROOT / "bairros" / city).glob("*.html")):
                with self.subTest(page=page.relative_to(ROOT)):
                    html = page.read_text(encoding="utf-8")
                    self.assertNotRegex(html, STALE)
                    if page.stem in slugs:
                        self.assertIn(f'href="{agenda}"', html)
                        self.assertIn("Agenda oficial —", html)
                        self.assertIn(f'<link rel="canonical" href="https://praia.digital/bairros/{city}/{page.name}"', html)
