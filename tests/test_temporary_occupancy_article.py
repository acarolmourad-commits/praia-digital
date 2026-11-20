"""Protect the scope, calculations, and preserved canonical URL of the occupancy guide."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "dados-ocupacao-temporada-litoral-sp-2026.html"
URL = "https://praia.digital/" + SLUG
HTML = (ROOT / SLUG).read_text(encoding="utf-8")


class ArticleMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.links, self.metas = [], [], {}
        self.feed(HTML)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a["href"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "meta" and "content" in a:
            self.metas[a.get("name") or a.get("property")] = a["content"]


class TemporaryOccupancyArticleTests(unittest.TestCase):
    def test_original_canonical_and_editorial_metadata(self):
        page = ArticleMetadata()
        schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', HTML, re.S)[1])
        self.assertEqual(page.canonicals, [URL])
        self.assertEqual(page.metas["og:url"], URL)
        self.assertEqual(schema["mainEntityOfPage"], URL)
        title = re.findall(r"<title>([^<]+)</title>", HTML)
        self.assertEqual(len(title), 1)
        self.assertEqual(re.findall(r"<h1>([^<]+)</h1>", HTML), title)
        self.assertEqual(page.metas["og:title"], title[0])
        self.assertEqual(schema["headline"], title[0])
        self.assertEqual(page.metas["description"], page.metas["og:description"])
        self.assertEqual(page.metas["description"], schema["description"])
        self.assertEqual(schema["datePublished"], "2026-09-14")
        self.assertIn(URL, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

    def test_explicit_example_uses_consistent_denominators(self):
        self.assertIn("Exemplo fictício", HTML)
        self.assertIn("30 noites", HTML)
        self.assertIn("6 bloqueadas", HTML)
        self.assertIn("24 comercializáveis", HTML)
        self.assertIn("taxa não se aplica", HTML)
        rows = [(int(n), int(d), int(rate)) for n, d, rate in re.findall(r"(\d+) ÷ (\d+) × 100 = (\d+)%", HTML)]
        self.assertEqual(rows, [(12, 24, 50), (12, 30, 40)])
        for nights, denominator, rate in rows:
            self.assertEqual(nights * 100, denominator * rate)
        self.assertNotRegex(HTML, r"8\.179|58,7%|R\$|2026-2026|Selic|Golden Window|12x cap|GuestFavorites")

    def test_sources_and_tools_are_linked_by_purpose(self):
        links = ArticleMetadata().links
        self.assertIn("https://www.airdna.co/vacation-rental-data/app/br/sao-paulo", links)
        self.assertIn("https://airbtics.com/annual-airbnb-revenue-in-sao-sebastiao-brazil-pt", links)
        for path in ("/guias/conferencia-calendarios-temporada.html", "/apps/simulador-roi-temporada/", "/contato.html"):
            self.assertIn(path, links)
            target = ROOT / path.lstrip("/")
            self.assertTrue((target / "index.html" if path.endswith("/") else target).is_file())
