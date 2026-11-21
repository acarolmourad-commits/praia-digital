"""Protect the editorial order, transparent links and local references in the beach guide."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = "blog/guia-completo-praias-de-bertioga-2026.html"
HTML = (ROOT / REL).read_text(encoding="utf-8")
AMAZON = "https://www.amazon.com.br/s?k="
EXPECTED = {AMAZON + item + "&tag=praiadigital-20" for item in (
    "cooler+termico+praia", "cadeira+praia+dobravel", "protetor+solar+fps+50",
    "caixa+som+prova+dagua", "automatic+beach+tent", "swim+float+boa", "thermal+cooler+bag",
)}
WEEKLY = "https://sistemasinter.cetesb.sp.gov.br/praias/qualipraias-web.html"


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.amazon = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href", "").startswith(AMAZON):
            self.amazon.append((values, attrs))


class BertiogaBeachesTests(unittest.TestCase):
    def test_article_and_disclosure_precede_every_affiliate_link(self):
        self.assertEqual(HTML.count("<h1>"), 1)
        marker = '<section class="affiliate-showcase" aria-labelledby="recomendacoes-praia"'
        self.assertEqual(HTML.count(marker), 1)
        first = HTML.index(marker)
        for text in ("Guia Completo das Praias", "Riviera de São Lourenço", "Praia do Indaiá",
                     "Praia da Enseada", "São Lourenço", "Guaratuba", "Boracéia", "Dicas gerais"):
            self.assertRegex(HTML[:first], rf"<h[12][^>]*>[^<]*{text}")
        self.assertEqual(HTML.count('class="affiliate-disclosure"'), 1)
        self.assertEqual(HTML.count("comissão por compras qualificadas"), 1)
        self.assertGreater(HTML.index(AMAZON), HTML.index("comissão por compras qualificadas"))

    def test_preserves_exact_targets_and_names_them(self):
        links = Links(HTML).amazon
        self.assertEqual(len(links), 7)
        self.assertEqual({value["href"] for value, _ in links}, EXPECTED)
        self.assertEqual(len({value["aria-label"] for value, _ in links}), 7)
        for value, attrs in links:
            self.assertEqual([v for k, v in attrs if k == "target"], ["_blank"])
            self.assertIn("sponsored", value["rel"].split())
            self.assertIn("noopener", value["rel"].split())
            self.assertIn("abre em nova aba", value["aria-label"])
        self.assertNotIn("Garantia e Entrega Rápida", HTML)
        self.assertNotIn("Compra Segura via Amazon", HTML)

    def test_tips_use_the_official_weekly_table_and_do_not_report_a_rating(self):
        tips = HTML.split("<h2>Dicas gerais</h2>", 1)[1].split("</ul>", 1)[0]
        self.assertIn(f'href="{WEEKLY}"', tips)
        self.assertIn("Procure Bertioga", tips)
        self.assertIn("ponto de amostragem", tips)
        self.assertIn("coluna mais recente com resultado disponível", tips)
        self.assertNotRegex(tips, r"(?i)imprópri[ao]|própri[ao] para banho|garantia de segurança")

    def test_local_cta_and_canonical_remain_and_grid_can_shrink(self):
        self.assertIn(f'rel="canonical" href="https://praia.digital/{REL}"', HTML)
        cta = HTML.split("Oportunidade para corretores</h2>", 1)[1].split("</article>", 1)[0]
        self.assertIn('href="/corretores/cadastrar-imovel.html"', cta)
        self.assertIn("https://wa.me/5511954346288?text=", cta)
        self.assertNotIn("amazon.com.br", cta)
        self.assertIn("minmax(min(100%,240px),1fr)", HTML)
        self.assertIn('content="width=device-width, initial-scale=1.0"', HTML)
