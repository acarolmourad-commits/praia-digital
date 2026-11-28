"""Guard the eight municipal event guides against the legacy shared Santos template."""
import json
from pathlib import Path
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
    def test_current_two_local_guides_keep_urls_and_use_primary_sources(self):
        sources = {"bertioga":["Bertioga","https://www.bertioga.sp.gov.br/turismo/noticias","https://www.bertioga.sp.gov.br/wp/wp-content/uploads/2026/11/ATOS-INTERNOS-1322.pdf"],"guaruja":["Guarujá","https://portalguaruja.tur.br/","https://atos.cnj.jus.br/files/original171025202512106939a981ed01c.pdf"]}
        for slug, (city, portal, dates_source) in sources.items():
            with self.subTest(city=slug):
                rel = f"{SECTION}/carnaval-{slug}.html"
                url = "https://praia.digital/" + rel
                raw = (ROOT / rel).read_text(encoding="utf-8")
                doc = EventHTML(raw)
                self.assertEqual(doc.get("html"), [{"lang": "pt-BR"}])
                self.assertEqual(len(doc.get("h1")), 1)
                self.assertEqual([x["href"] for x in doc.get("link") if x.get("rel") == "canonical"], [url])
                self.assertEqual([x["content"] for x in doc.get("meta") if x.get("name") == "robots"], ["index, follow"])
                self.assertIn(f"<title>Eventos em {city}: Carnaval 2026/2027 | Praia Digital</title>", raw)
                self.assertNotRegex(raw, r"Santos|hreflang|>>|wa\.me|btn-whatsapp|lucre|alta demanda|valorização|GA4_MEASUREMENT_ID")
                meta = json.loads(re.search(r'<script type="application/ld\+json">([^<]+)</script>', raw).group(1))
                self.assertEqual([meta["@type"], meta["url"], meta["mainEntityOfPage"], meta["inLanguage"]], ["Article", url, url, "pt-BR"])
                links = [a["href"] for a in doc.get("a")]
                self.assertEqual([href for href in links if href.startswith("https://")], [dates_source, portal])
                self.assertEqual(len([href for href in links if href.startswith("mailto:comercial@praia.digital?")]), 1)
                self.assertTrue(all((ROOT / link[1:]).is_file() for link in (f"/{SECTION}.html", f"/cidades/{slug}.html", f"/{SECTION}/agenda-eventos-{slug}.html")))
                for link in (f"/{SECTION}.html", f"/cidades/{slug}.html", f"/{SECTION}/agenda-eventos-{slug}.html"):
                    self.assertIn(link, links)
                dates = [t["datetime"] for t in doc.get("time")]
                self.assertEqual(dates, ["2027-02-08", "2027-02-09"] + (["2027-02-10"] if slug == "bertioga" else []) + ["2026-11-28"])
                self.assertIn("não localizamos nesses canais a programação detalhada", raw)
                self.assertIn("As datas de referência confirmam os dias de festa?", raw)
                self.assertIn("pontos facultativos do Executivo municipal" if slug == "bertioga" else "não são datas confirmadas de desfiles", raw)


if __name__ == "__main__":
    unittest.main()
