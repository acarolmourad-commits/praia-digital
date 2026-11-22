import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROLE = "em nome próprio pelo corretor de imóveis responsável"
DATASET = re.compile(r'const\s+\w+\s*=\s*(\[\s*\{\s*"id"[\s\S]+?\})\s*\];')
PUBLIC_PAGES = ("index.html", "sobre.html", "contato.html", "imoveis.html", "imoveis/index.html")


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def active_listings():
    # Source of truth used by the public catalogue, not a second maintained inventory.
    rows = json.loads(DATASET.search(read("js/main.js")).group(1) + "]")
    return [
        f"{slug[3:] if slug.startswith('../') else 'imoveis/' + slug}.html"
        for slug in (row["slug"] for row in rows)
    ]


class PortalBrokerRolesTests(unittest.TestCase):
    def test_active_listings_show_broker_handoff_and_keep_canonical_and_contact(self):
        paths = active_listings()
        self.assertIn("imoveis/sobrado-indaia-94m2.html", paths)
        self.assertIn("imoveis/casas-lancamento-sao-lourenco.html", paths)
        for path in paths:
            with self.subTest(path=path):
                html = read(path)
                notice = re.findall(r'<p class="[^"]*property-broker-notice[^"]*">([^<]+)</p>', html)
                self.assertEqual(len(notice), 1)
                self.assertIn("portal que divulga este anúncio", notice[0])
                self.assertIn(ROLE, notice[0])
                self.assertTrue(re.search(
                    rf'<link\b(?=[^>]*\brel="canonical")(?=[^>]*\bhref="https://praia\.digital/{re.escape(path)}")[^>]*>',
                    html,
                ), "missing published canonical")
                self.assertRegex(html, r'href="(?:https://wa\.me/|mailto:)')

    def test_portal_pages_describe_distinct_roles(self):
        for path in PUBLIC_PAGES:
            with self.subTest(path=path):
                html = read(path)
                self.assertIn(ROLE, html)
                self.assertNotIn("Somos uma imobiliária", html)
        self.assertIn("mantém o portal", read("sobre.html"))
        self.assertIn('href="/imoveis.html">Ver o catálogo', read("imoveis/index.html"))

    def test_condominium_no_longer_uses_unverified_performance_as_evidence(self):
        html = read("casa-condominio-fechado-bertioga.html")
        for legacy in ("Valorização 2026-2026", "profissionais certificados", "garante privacidade",
                       "Ocupação média 15% acima", "15-25% de aumento", "Média do Litoral",
                       "praias mais seguras", "Casa em Ubatuba"):
            self.assertNotIn(legacy, html)
        self.assertIn("Cenário ilustrativo de aluguel de temporada", html)
        self.assertIn("não dados de desempenho comprovados deste imóvel", html)
        self.assertIn('id="leadForm"', html)

    def test_vista_linda_financing_is_not_confirmed(self):
        html = read("imoveis/apartamento-vista-linda-65m2.html")
        self.assertIn("condições de financiamento não foram informados", html)
        self.assertIn("<summary>O imóvel aceita financiamento?</summary><p>Não informado.", html)
        self.assertNotIn("Aceita financiamento, conforme informação fornecida", html)


if __name__ == "__main__":
    unittest.main()
