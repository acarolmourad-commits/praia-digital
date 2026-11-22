import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = "/blog/fgts-financiamento-sbpe-mcmv-imovel-litoral-2026.html"
LEGACY = "/ferramentas/pre-qualificacao-credito-2026.html"
FINANCE = "/apps/calculadora-financiamento/"
INCOME = "/apps/renda-para-financiar/"
COST = "/apps/custo-de-compra/"
MINISTRY = "https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/programa-minha-casa-minha-vida/mcmv-fgts"
FGTS = "https://www.fgts.gov.br/Paginas/trabalhador/fgts-na-moradia.aspx"


def read(url):
    path = ROOT / url.lstrip("/")
    return (path / "index.html" if url.endswith("/") else path).read_text()


class FinancingJourney(unittest.TestCase):
    def test_home_analysis_uses_maintained_simulator(self):
        analysis = re.search(r'<section id="analise">(.*?)</section>', read("/"), re.S)[1]
        self.assertIn(f'<a class="card" href="{FINANCE}"><h3>Financiamento</h3>', analysis)
        self.assertIn("Compare parcelas SAC e Price com suas premissas.", analysis)
        self.assertNotIn(LEGACY, analysis)

    def test_official_limits_subsidy_and_nominal_rates(self):
        html = read(ARTICLE)
        for marker in (MINISTRY, FGTS, "28/10/2026", "4,25% a 5,25%", "5,00% a 7,00%",
                       "R$ 9.600", "7,66%", "8,16%", "R$ 400 mil", "R$ 13 mil",
                       "R$ 600 mil", "10,00%", "R$ 210 mil a R$ 275 mil", "até R$ 55 mil",
                       "não é um valor garantido", "não o CET"):
            self.assertIn(marker, html)
        for obsolete in ("R$ 47,5 mil", "7,16%", "R$ 3,4 mil", "R$ 720 mil", "10% a 12%"):
            self.assertNotIn(obsolete, html)

    def test_hypothetical_sbpe_first_sac_payment(self):
        html = read(ARTICLE)
        start = html.index("Exemplo hipotético de SBPE")
        end = html.index("Erros comuns ao financiar", start)
        example = html[start:end]
        self.assertIn("passa do teto da Faixa 3", example)
        self.assertIn("recursos próprios", example)
        self.assertIn("sem FGTS ou subsídio", example)
        self.assertIn("360 meses", example)
        self.assertIn("10,5% ao ano", example)
        self.assertIn("seguros ou tarifas", example)
        financed = Decimal(480000 - 96000)
        first_sac = (financed / 360 + financed * Decimal("0.105") / 12).quantize(Decimal("0.01"))
        formatted = f"{first_sac:,.2f}".translate(str.maketrans(",.", ".,"))
        self.assertIn(f"R$ {formatted}", example)

    def test_legacy_is_static_decision_page_not_credit_scoring(self):
        html = read(LEGACY)
        self.assertIn('id="main"', html)
        for marker in ("sugestão inicial de 30% é ajustável", "não fazem análise ou aprovação",
                       "https://wa.me/5511954346288", ARTICLE):
            self.assertIn(marker, html)
        for obsolete in ("Selic 15%", "Escore de elegibilidade", "Perfil compatível", "<input", "parcelaPrice", "onclick="):
            self.assertNotIn(obsolete, html)

    def test_canonicals_faq_and_links_match_visible_content(self):
        for route in (ARTICLE, LEGACY):
            with self.subTest(route=route):
                html = read(route)
                self.assertIn(f'<link rel="canonical" href="https://praia.digital{route}">', html)
                docs = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S)]
                faq, = [d for d in docs if d["@type"] == "FAQPage"]
                visible = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", html)
                self.assertEqual(visible, [(item["name"], item["acceptedAnswer"]["text"]) for item in faq["mainEntity"]])
                for target in (FINANCE, INCOME, COST):
                    self.assertIn(f'href="{target}"', html)
                    self.assertTrue(read(target).strip())


if __name__ == "__main__":
    unittest.main()
