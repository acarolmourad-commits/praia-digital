#!/usr/bin/env python3
"""
Verifica e-mails em docs/sales/leads-litoral-enriquecido.csv.
Gera:
- docs/sales/leads-litoral-enriquecido-emails-validos.csv
- docs/sales/relatorio-validacao-emails-2026-07-11.md
"""
import csv, re
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
CSV_FILE = BASE / "docs/sales/leads-litoral-enriquecido.csv"
OUTPUT_VALID = BASE / "docs/sales/leads-litoral-enriquecido-emails-validos.csv"
OUTPUT_REPORT = BASE / "docs/sales/relatorio-validacao-emails-2026-07-11.md"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

rows = list(csv.DictReader(CSV_FILE.open(encoding="utf-8", errors="ignore")))
validos = []
invalidos = []
for r in rows:
    email = r.get("email", "").strip()
    if EMAIL_RE.match(email):
        validos.append(r)
    else:
        invalidos.append(r)

with OUTPUT_VALID.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(validos)

report = f"""# Relatório de validação de e-mails

Data: 2026-07-11
Base: docs/sales/leads-litoral-enriquecido.csv

- Total de leads: {len(rows)}
- E-mails válidos: {len(validos)}
- E-mails inválidos: {len(invalidos)}
- % válidos: {len(validos)/len(rows)*100:.1f}%

## Top inválidos
"""
for r in invalidos[:20]:
    report += f"- Lead {r.get('id')} | {r.get('nome_da_imobiliaria')} | {r.get('email')}\n"

report += "\nSaída válida: docs/sales/leads-litoral-enriquecido-emails-validos.csv\n"
OUTPUT_REPORT.write_text(report, encoding="utf-8")
print(f"Válidos: {len(validos)} | Inválidos: {len(invalidos)}")
print(f"CSV válido: {OUTPUT_VALID}")
print(f"Relatório: {OUTPUT_REPORT}")
