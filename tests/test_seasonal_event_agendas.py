"""Guard the eight municipal event guides against the legacy shared Santos template."""
import json
from pathlib import Path
from xml.etree import ElementTree
import re
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
SECTION = "eventos-litoral-paulista-2026-2027"
SOURCES = {
    "bertioga": "https://www.bertioga.sp.gov.br/turismo/noticias",
    "guaruja": "https://portalguaruja.tur.br/",
    "itanhaem": "https://www2.itanhaem.sp.gov.br/turismo/calendario.html",
    "mongagua": "https://mongagua.sp.gov.br/noticias/cultura",
    "peruibe": "https://cultura.peruibe.sp.gov.br/eventos",
    "praia-grande": "https://turismo.praiagrande.sp.gov.br/eventos-oficiais-novo/",
    "santos": "https://www.turismosantos.com.br/pt-br/eventos",
    "sao-vicente": "https://www.saovicente.sp.gov.br/visite-sao-vicente-1"
}
BERTIOGA_DECEMBER_SOURCES = (
    "https://www.bertioga.sp.gov.br/turma-adulta-de-teatro-da-casa-da-cultura-apresenta-espetaculo-o-cortico-com-entrada-gratuita",
    "https://bertioga.sp.gov.br/bertioga-celebra-o-natal-com-ballet-circo-shows-e-grandes-eventos-de-4-a-23-de-dezembro",
)

class EventHTML(HTMLParser):
    def __init__(self, raw):
        super().__init__()
        self.nodes = []
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))

    def get(self, tag):
        return [attrs for name, attrs in self.nodes if name == tag]


class MunicipalEventGuideTests(unittest.TestCase):
    def test_all_agenda_urls_and_own_metadata(self):
        expected = {f"agenda-eventos-{key}.html" for key in SOURCES}
        self.assertEqual({item.name for item in (ROOT / SECTION).glob("agenda-eventos-*.html")}, expected)
        for key in SOURCES:
            with self.subTest(city=key):
                rel = f"{SECTION}/agenda-eventos-{key}.html"
                raw = (ROOT / rel).read_text(encoding="utf-8")
                doc = EventHTML(raw)
                url = f"https://praia.digital/{rel}"
                self.assertEqual(doc.get("html"), [{"lang": "pt-BR"}])
                self.assertEqual(len(doc.get("h1")), 1)
                self.assertEqual([a.get("href") for a in doc.get("link") if a.get("rel") == "canonical"], [url])
                self.assertNotRegex(raw, r"\bhreflang=|>>")
                props = {a.get("property"): a.get("content") for a in doc.get("meta") if a.get("property")}
                self.assertEqual(props["og:url"], url)
                self.assertEqual(props["og:locale"], "pt_BR")
                matches = re.findall(r'<script type="application/ld\+json">([^<]+)</script>', raw)
                self.assertEqual(len(matches), 1)
                entity = json.loads(matches[0])
                self.assertEqual((entity["@type"], entity["url"], entity["mainEntityOfPage"], entity["inLanguage"]),
                                 ("Article", url, url, "pt-BR"))

    def test_sources_local_routes_and_no_sales_promises(self):
        for key, source in SOURCES.items():
            with self.subTest(city=key):
                raw = (ROOT / SECTION / f"agenda-eventos-{key}.html").read_text(encoding="utf-8")
                doc = EventHTML(raw)
                anchors = [a["href"] for a in doc.get("a")]
                ids = [attrs["id"] for _, attrs in doc.nodes if "id" in attrs]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(all(ref[1:] in ids for ref in anchors if ref.startswith("#")))
                self.assertIn(source, anchors)
                self.assertIn(f"/{SECTION}.html", anchors)
                self.assertIn(f"/cidades/{key}.html", anchors)
                expected_external = [source]
                if key == "bertioga":
                    expected_external.extend(BERTIOGA_DECEMBER_SOURCES)
                if key == "praia-grande":
                    expected_external += [
                        "https://p-www2.praiagrande.sp.gov.br/noticia/estacao-verao-praia-tera-8-arenas-em-pg-com-muita-musica-esporte-e-diversao",
                        "https://p-www2.praiagrande.sp.gov.br/noticia/estacao-verao-2027-recebe-grandes-nomes-da-musica-e-programacao-gratuita-nas-praias-de-pg",
                    ]
                self.assertEqual([href for href in anchors if href.startswith(("http:", "https:"))], expected_external)
                self.assertRegex(raw, r"não é um calendário atualizado nem confirma datas")
                self.assertNotRegex(raw, r"(?i)lucr[eo]|alto impacto|valorização|ocupação|btn-whatsapp|ga4_measurement")
                if key != "santos":
                    self.assertNotRegex(raw, r"(?i)\bSantos\b")
                if key == "praia-grande":
                    self.assertIn("/bairros/index.html#praia-grande", anchors)
                    self.assertIn("/apps/simulador-roi-temporada/", anchors)


    def test_bertioga_december_selection(self):
        raw = (ROOT / SECTION / "agenda-eventos-bertioga.html").read_text(encoding="utf-8")
        section = re.search(r'<section id="dezembro-2026">([\s\S]*?)</section>', raw).group(1)
        self.assertEqual([a["href"] for a in EventHTML(section).get("a")], list(BERTIOGA_DECEMBER_SOURCES))
        self.assertEqual([a["datetime"] for a in EventHTML(section).get("time")], [
            "2026-12-08T20:30:00-03:00", "2026-12-20", "2026-12-23", "2026-12-23T20:00:00-03:00",
        ])
        for text in ("O Cortiço", "Espaço Cultural Praia", "Sinfonia das Águas", "às 19h",
                     "não informa embarque do público", "Banda Paralela", "na Feira do Bem",
                     "confira nos comunicados se houve alterações"):
            self.assertIn(text, section)
        self.assertNotIn("Parada de Natal", section)
        self.assertEqual(raw.count('href="#dezembro-2026"'), 1)


class NewYearGuideTests(unittest.TestCase):
    def test_seven_existing_urls_use_only_city_sources_and_routes(self):
        date_markers = ["2026-12-31", "2027-01-01"]
        central = f"/{SECTION}.html"
        cities = {slug: source for slug, source in SOURCES.items() if slug != "santos"}
        for slug, official in cities.items():
            with self.subTest(city=slug):
                url = f"https://praia.digital/{SECTION}/reveillon-{slug}.html"
                raw = (ROOT / SECTION / f"reveillon-{slug}.html").read_text(encoding="utf-8")
                doc = EventHTML(raw)
                self.assertEqual(doc.get("html"), [{"lang": "pt-BR"}])
                self.assertEqual(len(doc.get("h1")), 1)
                self.assertEqual([a.get("href") for a in doc.get("link") if a.get("rel") == "canonical"], [url])
                self.assertEqual([a["datetime"] for a in doc.get("time")], date_markers)
                self.assertFalse(any(a.get("hreflang") for a in doc.get("link")))
                self.assertEqual([m["content"] for m in doc.get("meta") if m.get("property") == "og:url"], [url])
                article = json.loads(re.search(r'<script type="application/ld\+json">([^<]+)</script>', raw).group(1))
                self.assertEqual([article[k] for k in ("@type", "url", "mainEntityOfPage", "inLanguage")],
                                 ["Article", url, url, "pt-BR"])
                anchors = [a["href"] for a in doc.get("a")]
                ids = [attrs["id"] for _, attrs in doc.nodes if "id" in attrs]
                self.assertEqual(len(ids), len(set(ids)))
                self.assertTrue(all(ref[1:] in ids for ref in anchors if ref.startswith("#")))
                for target in (official, central, f"/{SECTION}/agenda-eventos-{slug}.html", f"/cidades/{slug}.html"):
                    self.assertIn(target, anchors)
                expected_external = [official]
                if slug == "praia-grande":
                    expected_external.append(
                        "https://www2.praiagrande.sp.gov.br/noticia/"
                        "sucesso-no-ultimo-verao-cubos-de-led-estao-de-volta-a-orla-de-praia-grande"
                    )
                self.assertEqual([href for href in anchors if href.startswith(("http:", "https:"))], expected_external)
                self.assertNotRegex(raw, r"(?i)\bsantos\b|lucre|valorização|alto impacto|wa\.me")
                self.assertIn("não é a programação oficial deste Réveillon", raw)
                if slug == "praia-grande":
                    self.assertIn("Comunicado da Prefeitura sobre os cubos de LED, de 30/09/2026", raw)
                    self.assertIn("a Prefeitura anunciou que os cubos de LED voltariam no Réveillon", raw)
                    self.assertIn("O comunicado deixou a localização e os detalhes para outra divulgação.", raw)


class RegionalNewYearNavigationTests(unittest.TestCase):
    def test_regional_guide_links_to_the_seven_revised_city_guides(self):
        raw = (ROOT / f"{SECTION}.html").read_text(encoding="utf-8")
        doc = EventHTML(raw)
        anchor = "reveillon-guias"
        self.assertEqual(sum(node.get("id") == anchor for node in doc.get("section")), 1)
        self.assertEqual(sum(node.get("href") == f"#{anchor}" for node in doc.get("a")), 1)
        section = re.search(r'<section id="reveillon-guias">([\s\S]*?)</section>', raw).group(1)
        links = [node["href"] for node in EventHTML(section).get("a")]
        expected = [
            "bertioga", "guaruja", "itanhaem", "mongagua", "peruibe", "praia-grande", "sao-vicente",
        ]
        self.assertEqual(links, [f"/{SECTION}/reveillon-{slug}.html" for slug in expected])
        for link in links:
            self.assertTrue((ROOT / link.lstrip("/")).is_file(), link)
        self.assertIn("não confirmação de festas, fogos, locais ou horários", section)


class CarnavalGuideTests(unittest.TestCase):
    # These sources establish different levels of detail for the 2027 edition.
    evidence = {
        "bertioga": ("www.bertioga.sp.gov.br/wp/wp-content/uploads/2026/11/ATOS-INTERNOS-1322.pdf", "pontos facultativos do Executivo municipal"),
        "guaruja": ("www.guaruja.sp.gov.br/apos-11-anos-guaruja-anuncia-retorno-dos-desfiles-competitivos-de-carnaval-em-2027", "volta dos desfiles competitivos"),
        "itanhaem": ("www.itanhaem.sp.gov.br/wp-content/uploads/2026/11/1006.pdf", "região central ficou fora"),
        "mongagua": ("www.mongagua.sp.gov.br/turismo/calendario-de-eventos", "grade municipal com dias, locais e horários para 2027 seguia em aberto"),
        "peruibe": ("www.peruibe.sp.gov.br/portal/wp-content/uploads/2026/11/DOM-E_-_884_assinado.pdf", "17 blocos classificados"),
        "praia-grande": ("www2.praiagrande.sp.gov.br/noticiaNP/id/5075", "Estação Verão"),
        "santos": ("www.santos.sp.gov.br/?q=node/172165", "15 escolas de samba"),
        "sao-vicente": ("www.saovicente.sp.gov.br/informacao/sao-vicente-abre-credenciamento-para-blocos-e-bandas-do-carnaval-2026", "credenciamento encontrado é da edição de 2026"),
    }

    def test_existing_urls_metadata_and_unique_editorial_content(self):
        files = sorted((ROOT / SECTION).glob("carnaval-*.html"))
        self.assertEqual({f.name for f in files}, {f"carnaval-{city}.html" for city in SOURCES})
        sitemap = ElementTree.parse(ROOT / "sitemap.xml")
        locs = [node.text for node in sitemap.findall(".//{*}loc")]
        headlines, descriptions = [], []
        for path in files:
            with self.subTest(page=path.name):
                url = "https://praia.digital/" + path.relative_to(ROOT).as_posix()
                raw = path.read_text(encoding="utf-8")
                doc = EventHTML(raw)
                meta = {m.get("name") or m.get("property"): m.get("content") for m in doc.get("meta")}
                self.assertEqual(doc.get("html"), [{"lang": "pt-BR"}])
                for tag in ("title", "h1"):
                    self.assertEqual(len(doc.get(tag)), 1)
                headline = re.search(r"<h1>([^<]+)</h1>", raw).group(1)
                self.assertIn(f"<title>{headline} | Praia Digital</title>", raw)
                headlines.append(headline)
                descriptions.append(meta["description"])
                self.assertTrue(meta["description"].strip())
                self.assertEqual([m["href"] for m in doc.get("link") if m.get("rel") == "canonical"], [url])
                self.assertEqual(locs.count(url), 1)
                self.assertEqual((meta["robots"], meta["og:url"], meta["og:locale"]), ("index, follow", url, "pt_BR"))
                for field in ("og", "twitter"):
                    self.assertEqual(meta[field + ":title"], headline)
                    self.assertEqual(meta[field + ":description"], meta["description"])
                entities = [json.loads(blob) for blob in re.findall(r'<script type="application/ld\+json">([^<]+)</script>', raw)]
                self.assertEqual(len(entities), 1)
                article = entities[0]
                self.assertEqual([article[key] for key in ("@type", "url", "mainEntityOfPage", "inLanguage", "headline", "description")],
                                 ["Article", url, url, "pt-BR", headline, meta["description"]])
                self.assertIn(article["dateModified"], [t["datetime"] for t in doc.get("time")])
                self.assertNotRegex(raw, r"(?i)hreflang=|>>|FAQPage|wa\.me|whatsapp|lucre na temporada|GA4_MEASUREMENT_ID")
        self.assertEqual(len(set(headlines)), len(files))
        self.assertEqual(len(set(descriptions)), len(files))

    def test_sources_local_destinations_and_email(self):
        self.assertEqual(set(self.evidence), set(SOURCES))
        for city, (source, fact) in self.evidence.items():
            with self.subTest(city=city):
                raw = (ROOT / SECTION / f"carnaval-{city}.html").read_text(encoding="utf-8")
                doc = EventHTML(raw)
                links = [a["href"] for a in doc.get("a")]
                ids = [attrs["id"] for _, attrs in doc.nodes if "id" in attrs]
                self.assertEqual(len(set(ids)), len(ids))
                self.assertTrue(all(link[1:] in ids for link in links if link.startswith("#")))
                self.assertIn("https://" + source, links)
                self.assertIn(fact, raw)
                self.assertEqual([link for link in links if link.startswith("mailto:")], ["mailto:comercial@praia.digital"])
                self.assertFalse(any(link.endswith("/santos.html") or link == "santos.html" for link in links
                                     if link != f"/cidades/{city}.html"))
                targets = (f"/{SECTION}.html#carnaval-guias", f"/{SECTION}/agenda-eventos-{city}.html", f"/cidades/{city}.html",
                           "/apps/comparador-cidades/", "/compras/verao.html#carnaval-2027", "/apps/simulador-roi-temporada/")
                for target in targets:
                    self.assertEqual(links.count(target), 1)
                    path, _, fragment = target.partition("#")
                    destination = ROOT / path.lstrip("/")
                    if destination.is_dir():
                        destination /= "index.html"
                    self.assertTrue(destination.is_file(), target)
                    if fragment:
                        self.assertIn(f'id="{fragment}"', destination.read_text(encoding="utf-8"))

    def test_dates_are_attributed_to_the_right_activity(self):
        def body(city):
            return (ROOT / SECTION / f"carnaval-{city}.html").read_text(encoding="utf-8").split("<main", 1)[1]

        self.assertRegex(body("guaruja"), r'[Oo] lançamento[^<.]*<time datetime="2026-11-29">')
        self.assertRegex(body("santos"), r'nas noites de <time datetime="2027-01-29">29</time> e <time datetime="2027-01-30">')
        self.assertIn("Passarela do Samba Dráuzio da Cruz", body("santos"))
        self.assertIn("não traz a ordem de saída, o horário nem o percurso", body("peruibe"))
        self.assertIn('prazo de inscrição terminou em <time datetime="2026-11-19">', body("itanhaem"))


class RegionalCarnavalNavigationTests(unittest.TestCase):
    def test_regional_toc_and_municipal_round_trip(self):
        raw = (ROOT / f"{SECTION}.html").read_text(encoding="utf-8")
        doc = EventHTML(raw)
        self.assertEqual(sum(node.get("id") == "carnaval-guias" for node in doc.get("section")), 1)
        toc = re.search(r'<nav class="article-toc"[^>]*>(.*?)</nav>', raw, re.S).group(1)
        self.assertEqual(sum(node.get("href") == "#carnaval-guias" for node in EventHTML(toc).get("a")), 1)
        section = re.search(r'<section id="carnaval-guias">(.*?)</section>', raw, re.S).group(1)
        self.assertCountEqual([node["href"] for node in EventHTML(section).get("a")],
                              [f"/{SECTION}/carnaval-{slug}.html" for slug in SOURCES])
        # The two existing agenda pages also link back to their Carnaval guides.
        for slug in ("bertioga", "guaruja"):
            agenda = (ROOT / SECTION / f"agenda-eventos-{slug}.html").read_text(encoding="utf-8")
            self.assertEqual(sum(a["href"] == f"/{SECTION}/carnaval-{slug}.html" for a in EventHTML(agenda).get("a")), 1)


if __name__ == "__main__":
    unittest.main()
