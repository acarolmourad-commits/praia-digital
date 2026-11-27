import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = "blog/passo-a-passo-pos-compra-imovel-matricula-itbi-2026.html"
CITIES = "blog/itbi-registro-imoveis-santos-guaruja-bertioga-2026.html"
CTN = "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm"
APP = "/apps/custo-de-compra/"


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def read(path):
    return (ROOT / path).read_text()


class BuyerGuides(unittest.TestCase):
    def test_itbi_does_not_use_a_blanket_higher_of_two_rule(self):
        for path in (POST, CITIES):
            with self.subTest(path=path):
                html = read(path)
                for mark in (CTN, "art. 38", "227/2026", "valor venal", "à vista",
                             "condições normais de mercado", "critérios técnicos",
                             "avaliação contraditória", "prefeitura"):
                    self.assertIn(mark, html)
                self.assertNotRegex(html.lower(), r"o que for maior|deve ser (?:pago|quitado) antes do registro")

    def test_post_purchase_document_and_counsel_are_conditional(self):
        html = read(POST)
        for mark in ("Título apto a registro", "se exigida", "art. 108", "1.245",
                     "/leis/l9514.htm", "alienação fiduciária",
                     "instrumento particular pode ter efeitos de escritura pública",
                     "/leis/l6015compilada.htm", "216-A", "via judicial",
                     "representação por advogado", "art. 42"):
            self.assertIn(mark, html)
        self.assertNotIn("exige ação judicial", html)
        self.assertNotIn("Providencie a Escritura Pública", html)
        self.assertNotIn("salvo disposição contratual em contrário", html)

    def test_budget_link_uses_actual_label_and_input_contract(self):
        app = read("apps/custo-de-compra/index.html")
        self.assertIn("Orçamento de Custos de Compra", app)
        for path in (POST, CITIES):
            with self.subTest(path=path):
                html = read(path)
                self.assertIn(f'href="{APP}">Orçamento de Custos de Compra</a>', html)
                self.assertRegex(html, r"não (?:calcula|determina) o (?:ITBI|imposto)")
                self.assertNotIn("12 cidades", html)

    def test_canonical_indexability_and_faq_match_text(self):
        for path in (POST, CITIES):
            html = read(path)
            tags = Links(html).tags
            self.assertEqual([a["href"] for t, a in tags if t == "link" and a.get("rel") == "canonical"],
                             ["https://praia.digital/" + path])
            self.assertFalse(any(t == "meta" and a.get("name") == "robots" and "noindex" in a.get("content", "")
                                 for t, a in tags))
            docs = [json.loads(d) for d in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)]
            article, = [doc for doc in docs if doc["@type"] == "BlogPosting"]
            self.assertEqual(article["url"], "https://praia.digital/" + path)
            self.assertEqual(article["dateModified"], "2026-11-22")
            if path == POST:
                faq, = [doc for doc in docs if doc["@type"] == "FAQPage"]
                visible = re.findall(r"<h3>\d+\. ([^<]+)</h3>\s*<p>([^<]+)</p>", html)
                self.assertEqual(len(visible), 5)
                self.assertEqual(visible, [(x["name"], x["acceptedAnswer"]["text"]) for x in faq["mainEntity"]])


if __name__ == "__main__":
    unittest.main()
