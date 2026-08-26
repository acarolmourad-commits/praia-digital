"""
Feed XML para portais (ZAP, OLX, VivaReal, Imovelweb).
"""
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from xml.dom import minidom

IMOVEIS_DIR = Path(__file__).resolve().parent.parent / "imoveis"
BASE_URL = "https://praia.digital"

def parse_slug(filename: str):
    slug = filename.replace(".html", "")
    parts = slug.split("-")
    tipo = parts[0] if parts else slug
    quartos = None
    for i, p in enumerate(parts):
        if p in ("quartos", "dorm", "dormitorios") and i > 0:
            try:
                quartos = int(parts[i - 1])
            except ValueError:
                pass
            break
        if re.match(r"^\d+$", p) and i + 1 < len(parts) and parts[i + 1] in ("quartos", "dorm", "dormitorios"):
            try:
                quartos = int(p)
            except ValueError:
                pass
            break
    cidade = None
    for p in reversed(parts):
        if p and not re.match(r"^\d+$", p) and p not in ("imovel", "template", "landing", "index"):
            cidade = p.capitalize()
            break
    if not cidade:
        cidade = "Litoral Paulista"
    title = slug.replace("-", " ").capitalize()
    return tipo, quartos, cidade, title

def extract_image(html: str) -> str:
    m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+name="twitter:image"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'<img[^>]+src="([^"]+)"', html)
    if m:
        src = m.group(1)
        if src.startswith("http"):
            return src
        return BASE_URL + src
    return BASE_URL + "/img/default-property.jpg"

def extract_description(html: str) -> str:
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html)
    if m:
        return m.group(1)
    return ""

def extract_heading(html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if m:
        from bs4 import BeautifulSoup
        return BeautifulSoup(m.group(1), "html.parser").get_text().strip()
    return ""

def build_item(filename: str):
    path = IMOVEIS_DIR / filename
    html = path.read_text(encoding="utf-8")
    tipo, quartos, cidade, title = parse_slug(filename)
    image = extract_image(html)
    desc = extract_description(html)
    heading = extract_heading(html)
    nome = heading if heading else title
    link = f"{BASE_URL}/imoveis/{filename}"
    preco = "Sob consulta"
    return {
        "id": filename.replace(".html", ""),
        "titulo": nome,
        "tipo": tipo,
        "cidade": cidade,
        "quartos": quartos or 1,
        "preco": preco,
        "linkcanonico": link,
        "imagem": image,
        "descricao": desc,
    }

def gerar_feed() -> str:
    root = ET.Element("feed", xmlns="http://www.w3.org/2005/Atom")
    title = ET.SubElement(root, "title")
    title.text = "Praia Digital — Imóveis Litoral Paulista"
    link_el = ET.SubElement(root, "link", href="https://praia.digital/feed.xml", rel="self")
    link_el2 = ET.SubElement(root, "link", href="https://praia.digital/imoveis/")
    updated = ET.SubElement(root, "updated")
    updated.text = datetime.utcnow().isoformat() + "Z"
    author = ET.SubElement(root, "author")
    name = ET.SubElement(author, "name")
    name.text = "Praia Digital"
    id_el = ET.SubElement(root, "id")
    id_el.text = "https://praia.digital/feed.xml"

    files = sorted(IMOVEIS_DIR.glob("*.html"))
    for path in files:
        item = build_item(path.name)
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "title").text = item["titulo"]
        ET.SubElement(entry, "link", href=item["linkcanonico"])
        ET.SubElement(entry, "id").text = item["id"]
        ET.SubElement(entry, "updated").text = datetime.utcnow().isoformat() + "Z"
        summary = ET.SubElement(entry, "summary")
        summary.text = item["descricao"] or item["titulo"]
        for tag, val in [
            ("tipo", item["tipo"]),
            ("cidade", item["cidade"]),
            ("quartos", str(item["quartos"])),
            ("preco", item["preco"]),
            ("imagem", item["imagem"]),
        ]:
            el = ET.SubElement(entry, tag)
            el.text = val
    rough = ET.tostring(root, encoding="utf-8")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

if __name__ == "__main__":
    xml = gerar_feed()
    print(xml)
