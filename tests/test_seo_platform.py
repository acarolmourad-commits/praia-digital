"""SEO platform tests for praia-digital."""
import os
import re
import json
import glob
from pathlib import Path
import pytest

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
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', txt, re.DOTALL | re.IGNORECASE)
        if not blocks:
            failures.append((p.name, "missing script"))
            continue
        valid = False
        for raw in blocks:
            try:
                data = json.loads(raw)
            except Exception:
                continue
            if data.get("@type") != "RealEstateListing":
                continue
            about = data.get("about") or {}
            if isinstance(about, dict) and about.get("@type") != "SingleFamilyResidence":
                continue
            if all(field in data for field in ("price", "priceCurrency", "address", "numberOfRooms", "image", "availability")):
                valid = True
                break
        if not valid:
            failures.append((p.name, "no valid RealEstateListing block"))
    assert not failures, f"Missing valid JSON-LD RealEstateListing: {failures[:10]}"

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
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    lead_file = PROJECT / "api" / "leads" / f"{today}.jsonl"
    assert lead_file.exists(), f"Lead file not created: {lead_file}"
    lines = lead_file.read_text(encoding="utf-8").strip().splitlines()
    found = any(json.loads(l).get("nome") == "Teste QA" for l in lines)
    assert found, "Lead payload not found in JSONL"
