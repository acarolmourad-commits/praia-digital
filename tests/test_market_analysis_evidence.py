"""Ensure the market guide does not present unverified outcomes or a daily send."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = "blog/analise-mercado-imobiliario-litoral-2026.html"
CANONICAL = "https://praia.digital/" + PATH
HTML = (ROOT / PATH).read_text(encoding="utf-8")


class MarketAnalysisEvidenceTests(unittest.TestCase):
    def test_case_discloses_limits_and_cites_evidence(self):
        self.assertNotRegex(HTML, r"9 imóveis em 30 dias|tempo de venda em 18%")
        case = HTML.split("<h2>Caso técnico:", 1)[1].split("<h2>", 1)[0]
        for value in (
            "/pull/191",
            "impede copiar ou baixar um resultado antigo",
            "não mede ganhos de captação ou prazo de venda",
            'href="/cases.html#evolucao-aplicativos"',
            'href="/apps/guia-de-uso.html#anunciar"',
        ):
            self.assertIn(value, case)

    def test_public_bulletin_and_primary_links_match_destinations(self):
        self.assertEqual(HTML.count("CTA-BOLETIM-PRAIA-DIGITAL"), 1)
        self.assertNotRegex(HTML, r"Receba toda manhã|Assine o Boletim|Ler boletim de hoje|Acessar curso")
        self.assertIn("Ler a edição mais recente", HTML)
        for path, fragment in (
            ("docs/inteligencia/boletim-diario.html", "acompanhar"),
            ("apps/guia-de-uso.html", "anunciar"),
            ("cases.html", "evolucao-aplicativos"),
        ):
            self.assertIn(f'href="/{path}#{fragment}"', HTML)
            self.assertIn(f'id="{fragment}"', (ROOT / path).read_text(encoding="utf-8"))

    def test_canonical_and_method_not_rankings(self):
        self.assertIn(f'<link rel="canonical" href="{CANONICAL}"', HTML)
        self.assertIn(CANONICAL, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn('content="index, follow" name="robots"', HTML)
        self.assertIn("perguntas de pesquisa, não um ranking", HTML)
        self.assertNotIn("<td>Alta</td>", HTML)
        blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', HTML, re.S)
        markup = [json.loads(block) for block in blocks]
        faq = next(block for block in markup if block["@type"] == "FAQPage")
        for row in faq["mainEntity"]:
            self.assertIn(row["name"] + "</strong><br/>" + row["acceptedAnswer"]["text"], HTML)
