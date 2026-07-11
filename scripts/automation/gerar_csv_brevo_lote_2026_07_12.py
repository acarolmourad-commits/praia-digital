#!/usr/bin/env python3
"""
Gera CSV de importação Brevo para o lote de prospecção 2026-07-12.
Lê os templates .md existentes em docs/sales/lote-dia-2026-07-12/ e extrai
dados de lead para formato compatível com Brevo.
Saída: docs/sales/csv-lotes-email/lote-brevo-2026-07-12.csv
"""
import os, re, csv
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
LOTE_DIR = BASE / "docs/sales/lote-dia-2026-07-12"
OUTPUT_DIR = BASE / "docs/sales/csv-lotes-email"
OUTPUT_FILE = OUTPUT_DIR / "lote-brevo-2026-07-12.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REGEXES = {
    "lead_id": re.compile(r"Lead ID[:\s]+(\d+)", re.I),
    "nome_imobiliaria": re.compile(r"Imobili[áa]ria[:\s]+(.+)", re.I),
    "cidade": re.compile(r"Cidade[:\s]+(.+)", re.I),
    "contato_nome": re.compile(r"Contato[:\s]+(.+)", re.I),
    "email": re.compile(r"[Ee]-?mail[:\s]+([^\s]+@[^\s]+)"),
    "telefone": re.compile(r"Telefone[:\s]+(.+)", re.I),
    "site": re.compile(r"Site[:\s]+(https?://[^\s]+)", re.I),
}

def parse_md(path: Path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    data = {}
    for k, pat in REGEXES.items():
        m = pat.search(txt)
        data[k] = m.group(1).strip() if m else ""
    if not data.get("lead_id"):
        m = re.search(r"(\d{3})", path.stem)
        data["lead_id"] = m.group(1) if m else path.stem
    return data

files = sorted(LOTE_DIR.glob("lote-2026-07-12-*.md"))
rows = []
for f in files:
    d = parse_md(f)
    nome = d.get("contato_nome", "").strip()
    partes = nome.split(" ", 1)
    first = partes[0] if partes else nome
    last = partes[1] if len(partes) > 1 else ""
    rows.append({
        "EMAIL": d.get("email", ""),
        "FIRST_NAME": first,
        "LAST_NAME": last,
        "COMPANY": d.get("nome_imobiliaria", ""),
        "CITY": d.get("cidade", ""),
        "STATE": "SP",
        "PHONE": d.get("telefone", "").replace("(", "").replace(")", "").replace(" ", "").replace("-", ""),
        "WEBSITE": d.get("site", ""),
        "SOURCE": "lote-2026-07-12",
   })

headers = ["EMAIL", "FIRST_NAME", "LAST_NAME", "COMPANY", "CITY", "STATE", "PHONE", "WEBSITE", "SOURCE"]
with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=headers)
    w.writeheader()
    w.writerows(rows)

print(f"Gerado {OUTPUT_FILE}")
print(f"Total leads: {len(rows)}")
print("Preview:")
for r in rows[:5]:
    print(r)
