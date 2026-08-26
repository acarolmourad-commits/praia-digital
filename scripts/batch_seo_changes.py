#!/usr/bin/env python3
"""Batch SEO changes: JSON-LD, lazy images, preload, feed XML, form fields, lead endpoint, tests."""
import os
import re
import json
import glob
from datetime import datetime
from pathlib import Path

PROJECT = Path(r"C:\Users\Carolina\praia-digital")
IMOVEIS_DIR = PROJECT / "imoveis"
API_DIR = PROJECT / "api"
ASSETS_DIR = PROJECT / "assets"
TESTS_DIR = PROJECT / "tests"
DEFAULT_IMAGE = "/img/default-property.jpg"

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
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    if m:
        src = m.group(1)
        if src.startswith("http"):
            return src
        return "https://praia.digital" + src
    return "https://praia.digital" + DEFAULT_IMAGE

def extract_description(html: str) -> str:
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']', html)
    if m:
        return m.group(1)
    return ""

def extract_heading(html: str) -> str:
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1))
        return text.strip()
    return ""

def build_jsonld(slug: str, canonical_url: str, html: str) -> str:
    tipo, quartos, cidade, title = parse_slug(slug)
    image = extract_image(html)
    desc = extract_description(html)
    heading = extract_heading(html)
    name = heading if heading else title
    if quartos is None:
        quartos = 1
    schema = {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": name,
        "description": desc,
        "url": canonical_url,
        "image": image,
        "availability": "https://schema.org/InStock",
        "price": "Sob consulta",
        "priceCurrency": "BRL",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": cidade,
            "addressRegion": "SP",
            "addressCountry": "BR"
        },
        "numberOfRooms": quartos,
        "about": {
            "@type": "SingleFamilyResidence",
            "numberOfRooms": quartos
        }
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + '\n  </script>'

def process_imovel(path: Path):
    html = path.read_text(encoding="utf-8")
    original = html
    filename = path.name
    slug = filename.replace(".html", "")
    canonical_url = f"https://praia.digital/imoveis/{filename}"

    # 1) JSON-LD before </head> (only if not already present with required fields)
    new_ld = build_jsonld(slug, canonical_url, html)
    existing_ok = False
    for m in re.finditer(r'<script type="application/ld+json">(.*?)</script>', html, re.DOTALL | re.IGNORECASE):
        try:
            data = json.loads(m.group(1))
            if data.get("@type") == "RealEstateListing" and data.get("about", {}).get("@type") == "SingleFamilyResidence":
                existing_ok = True
                break
        except Exception:
            continue
    if not existing_ok:
        ld_tag = '\n' + new_ld + '\n'
        html = html.replace('</head>', ld_tag + '</head>', 1)

    # 2) lazy + decoding async on imgs (regex-based, no parsing)
    def add_img_attrs(match):
        tag = match.group(0)
        if 'loading=' in tag:
            return tag
        if 'decoding=' in tag:
            return tag
        # Insert after <img
        return tag.replace('<img ', '<img loading="lazy" decoding="async" ', 1)
    html = re.sub(r'<img\s[^>]*>', add_img_attrs, html, flags=re.IGNORECASE)

    # 3) preload for first image in body content
    first_img = None
    for m in re.finditer(r'<img\s[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE):
        src = m.group(1)
        if src and not src.startswith("data:"):
            first_img = src
            break
    if first_img:
        preload_src = first_img if first_img.startswith("http") else "https://praia.digital" + first_img
        preload_tag = f'<link rel="preload" href="{preload_src}" as="image">\n'
        if '<link rel="preload"' not in html.lower():
            html = html.replace('</head>', preload_tag + '</head>', 1)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False

def process_all_imoveis():
    files = sorted(IMOVEIS_DIR.glob("*.html"))
    changed = 0
    for path in files:
        if process_imovel(path):
            changed += 1
    print(f"Processed {len(files)} imovel pages, changed {changed}")

def write_feed_py():
    API_DIR.mkdir(parents=True, exist_ok=True)
    content = '''"""
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
        if re.match(r"^\\d+$", p) and i + 1 < len(parts) and parts[i + 1] in ("quartos", "dorm", "dormitorios"):
            try:
                quartos = int(p)
            except ValueError:
                pass
            break
    cidade = None
    for p in reversed(parts):
        if p and not re.match(r"^\\d+$", p) and p not in ("imovel", "template", "landing", "index"):
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
'''
    (API_DIR / "feed.py").write_text(content, encoding="utf-8")

def update_main_py():
    path = API_DIR / "main.py"
    original = path.read_text(encoding="utf-8")

    # Add imports
    if "from datetime import datetime" not in original:
        original = original.replace("from typing import Optional", "from typing import Optional\nfrom datetime import datetime\nimport json")
    if "from pathlib import Path" not in original:
        original = original.replace("from fastapi import FastAPI, HTTPException", "from fastapi import FastAPI, HTTPException\nfrom pathlib import Path")

    # Keep old LeadRequest as PriorizarRequest
    if "class LeadRequest(BaseModel):\n    origem: str" in original:
        original = original.replace(
            "class LeadRequest(BaseModel):\n    origem: str\n    tempo_resposta: int\n    interacoes: int",
            "class PriorizarRequest(BaseModel):\n    origem: str\n    tempo_resposta: int\n    interacoes: int"
        )
        original = original.replace("@app.post(\"/priorizar\")\ndef priorizar_lead(req: LeadRequest):", "@app.post(\"/priorizar\")\ndef priorizar_lead(req: PriorizarRequest):")

    # Add new LeadRequest
    if "class LeadRequest(BaseModel):\n    nome: str" not in original:
        new_model = '''class LeadRequest(BaseModel):
    nome: str
    email: Optional[str] = ""
    telefone: Optional[str] = ""
    cidade_interesse: Optional[str] = ""
    faixa_orcamento: Optional[str] = ""
    prazo_interesse: Optional[str] = ""
    origem: Optional[str] = ""
    mensagem: Optional[str] = ""
'''
        original = original + "\n\n" + new_model

    # Add /feed.xml route
    if '/feed.xml' not in original:
        original += '\n\nfrom .feed import gerar_feed\n\nfrom fastapi import Response\n\n'
        original += '@app.get("/feed.xml")\ndef feed_xml():\n    xml = gerar_feed()\n    return Response(content=xml, media_type="application/xml")\n'

    # Add /lead endpoint
    if '/lead' not in original:
        lead_endpoint = '''@app.post("/lead")
def salvar_lead(req: LeadRequest):
    data = req.dict()
    data["created_at"] = datetime.utcnow().isoformat() + "Z"
    leads_dir = Path(__file__).resolve().parent / "leads"
    leads_dir.mkdir(exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = leads_dir / f"{date_str}.jsonl"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\\n")
    return {"status": "ok"}
'''
        original += "\n" + lead_endpoint

    path.write_text(original, encoding="utf-8")

def update_form():
    path = ASSETS_DIR / "cadastro-imovel-publico.html"
    html = path.read_text(encoding="utf-8")

    insertion = '''
<label>Faixa de orçamento</label>
<select id="faixa_orcamento" required>
  <option value="">Selecione</option>
  <option>Até R$300k</option>
  <option>R$300k-500k</option>
  <option>R$500k-1M</option>
  <option>Acima de R$1M</option>
</select>

<label>Prazo de interesse</label>
<select id="prazo_interesse" required>
  <option value="">Selecione</option>
  <option>Imediato</option>
  <option>3 meses</option>
  <option>6 meses</option>
  <option>12 meses</option>
</select>
'''
    html = html.replace('<label>Descrição</label>', insertion + '\n<label>Descrição</label>', 1)

    # Update validation
    old_valid = "if (!titulo  !cidade  !tipo  !preco  !dorm  !area  !nome  !whatsapp) {"
    new_valid = "if (!titulo  !cidade  !tipo  !preco  !dorm  !area  !nome  !whatsapp  !faixa_orcamento  !prazo_interesse) {"
    html = html.replace(old_valid, new_valid, 1)

    # Update body text
    old_body_start = (
        "const body = `### 🏠 Novo cadastro de imóvel\\n\\n` +\n"
        "    `- **Título:** ${titulo}\\n` +\n"
        "    `- **Cidade:** ${cidade}\\n` +\n"
        "    `- **Tipo:** ${tipo}\\n` +\n"
        "    `- **Preço:** R$ ${Number(preco).toLocaleString('pt-BR')}\\n` +\n"
        "    `- **Dormitórios:** ${dorm}\\n` +\n"
        "    `- **Área:** ${area} m²\\n` +\n"
        "    `- **Descrição:** ${desc || '-'}\\n\\n` +\n"
    )
    new_body_start = (
        "const body = `### 🏠 Novo cadastro de imóvel\\n\\n` +\n"
        "    `- **Título:** ${titulo}\\n` +\n"
        "    `- **Cidade:** ${cidade}\\n` +\n"
        "    `- **Tipo:** ${tipo}\\n` +\n"
        "    `- **Preço:** R$ ${Number(preco).toLocaleString('pt-BR')}\\n` +\n"
        "    `- **Dormitórios:** ${dorm}\\n` +\n"
        "    `- **Área:** ${area} m²\\n` +\n"
        "    `- **Faixa de orçamento:** ${faixa_orcamento}\\n` +\n"
        "    `- **Prazo de interesse:** ${prazo_interesse}\\n` +\n"
        "    `- **Descrição:** ${desc || '-'}\\n\\n` +\n"
    )
    html = html.replace(old_body_start, new_body_start, 1)

    path.write_text(html, encoding="utf-8")

def write_tests():
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    content = '''"""SEO platform tests for praia-digital."""
import os
import re
import json
import glob
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
IMOVEIS_DIR = PROJECT / "imoveis"

@pytest.fixture(scope="module")
def imovel_files():
    return sorted(IMOVEIS_DIR.glob("*.html"))

def test_jsonld_present_in_multiple_pages(imovel_files):
    pages = imovel_files[:5]
    assert len(pages) >= 5, "Need at least 5 imovel pages"
    found = 0
    for p in pages:
        txt = p.read_text(encoding="utf-8")
        if "application/ld+json" in txt and "RealEstateListing" in txt and "SingleFamilyResidence" in txt:
            found += 1
    assert found >= 5, f"Expected JSON-LD RealEstateListing+SingleFamilyResidence in 5 pages, got {found}"

def test_jsonld_required_fields_in_all_pages(imovel_files):
    failures = []
    for p in imovel_files:
        txt = p.read_text(encoding="utf-8")
        m = re.search(r'<script type="application/ld+json">(.*?)</script>', txt, re.DOTALL | re.IGNORECASE)
        if not m:
            failures.append((p.name, "missing script"))
            continue
        data = json.loads(m.group(1))
        if data.get("@type") != "RealEstateListing":
            failures.append((p.name, "wrong type"))
            continue
        about = data.get("about") or {}
        if isinstance(about, dict) and about.get("@type") != "SingleFamilyResidence":
            failures.append((p.name, "missing about/SingleFamilyResidence"))
            continue
        for field in ("price", "priceCurrency", "address", "numberOfRooms", "image", "availability"):
            if field not in data:
                failures.append((p.name, f"missing {field}"))
    assert not failures, f"Missing required fields: {failures[:10]}"

def test_imgs_have_lazy_and_decoding(imovel_files):
    from bs4 import BeautifulSoup
    bad = []
    for p in imovel_files:
        soup = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
        for img in soup.find_all("img"):
            if img.get("loading") != "lazy":
                bad.append((p.name, img.get("src")))
                break
            if img.get("decoding") != "async":
                bad.append((p.name, img.get("src")))
                break
    assert not bad, f"Images missing lazy/async: {bad[:10]}"

def test_preload_link_present():
    from bs4 import BeautifulSoup
    bad = []
    for p in IMOVEIS_DIR.glob("*.html"):
        txt = p.read_text(encoding="utf-8")
        soup = BeautifulSoup(txt, "html.parser")
        imgs = soup.find_all("img")
        has_img = any(img.get("src") and not img.get("src").startswith("data:") for img in imgs)
        has_preload = bool(soup.find("link", rel="preload", attrs={"as": "image"}))
        if has_img and not has_preload:
            bad.append(p.name)
    assert not bad, f"Missing preload link on: {bad[:10]}"

def test_feed_xml_well_formed():
    import importlib.util
    spec = importlib.util.spec_from_file_location("feed", str(PROJECT / "api" / "feed.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    xml = mod.gerar_feed()
    assert xml.startswith("<?xml")
    assert "<feed" in xml
    assert "</feed>" in xml

def test_feed_xml_fields():
    import importlib.util
    spec = importlib.util.spec_from_file_location("feed", str(PROJECT / "api" / "feed.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    items = []
    xml = mod.gerar_feed()
    for m in re.finditer(r"<entry>(.*?)</entry>", xml, re.DOTALL):
        entry = m.group(1)
        title = re.search(r"<title>(.*?)</title>", entry)
        link = re.search(r'<link href="([^"]+)"', entry)
        preco = re.search(r"<preco>(.*?)</preco>", entry)
        cidade = re.search(r"<cidade>(.*?)</cidade>", entry)
        quartos = re.search(r"<quartos>(.*?)</quartos>", entry)
        imagem = re.search(r"<imagem>(.*?)</imagem>", entry)
        items.append({
            "title": title.group(1) if title else "",
            "link": link.group(1) if link else "",
            "preco": preco.group(1) if preco else "",
            "cidade": cidade.group(1) if cidade else "",
            "quartos": quartos.group(1) if quartos else "",
            "imagem": imagem.group(1) if imagem else "",
        })
    assert len(items) > 0
    for it in items:
        assert it["title"]
        assert it["link"].startswith("https://praia.digital/imoveis/")
        assert it["preco"] == "Sob consulta"
        assert it["cidade"]
        assert it["quartos"]
        assert it["imagem"]

def test_lead_endpoint_returns_200_and_saves_jsonl():
    import sys as _sys
    _sys.path.insert(0, str(PROJECT / "api"))
    import importlib
    if "main" in _sys.modules:
        del _sys.modules["main"]
    main = importlib.import_module("main")
    from fastapi.testclient import TestClient
    client = TestClient(main.app)
    payload = {
        "nome": "Teste QA",
        "email": "teste@example.com",
        "telefone": "11999999999",
        "cidade_interesse": "Santos",
        "faixa_orcamento": "R$300k-500k",
        "prazo_interesse": "Imediato",
        "origem": "teste",
        "mensagem": "Teste automatizado",
    }
    resp = client.post("/lead", json=payload)
    assert resp.status_code == 200, resp.text
    assert resp.json().get("status") == "ok"
    today = datetime.utcnow().strftime("%Y-%m-%d")
    lead_file = PROJECT / "api" / "leads" / f"{today}.jsonl"
    assert lead_file.exists(), f"Lead file not created: {lead_file}"
    lines = lead_file.read_text(encoding="utf-8").strip().splitlines()
    found = any(json.loads(l).get("nome") == "Teste QA" for l in lines)
    assert found, "Lead payload not found in JSONL"
'''
    (TESTS_DIR / "test_seo_platform.py").write_text(content, encoding="utf-8")

# Execute all steps
print("Processing imoveis...")
process_all_imoveis()
print("Writing feed.py...")
write_feed_py()
print("Updating main.py...")
update_main_py()
print("Updating form...")
update_form()
print("Writing tests...")
write_tests()
print("Done.")
