#!/usr/bin/env python3
"""
sanitize_lote_crm_imobiliario.py
Audita e prepara o lote B2B de CRM Imobiliário.
Uso: python scripts/automation/sanitize_lote_crm_imobiliario.py
"""
import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "docs/sales/csv-lotes-b2b/para-brevo-crm-imobiliario-2026-07-22.csv"

def normalizar(v):
    return " ".join(str(v or "").split()).strip().lower()

def main():
    rows = []
    with ENTRADA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            rows.append(row)
    telefones = Counter(normalizar(r.get("Telefone", "")) for r in rows)
    duplicados = {t for t, c in telefones.items() if c > 1 and t}
    sane = [r for r in rows if normalizar(r.get("Telefone", "")) not in duplicados]
    print(f"Sanitizado crm_imobiliario: {len(rows)} -> {len(sane)} leads")

if __name__ == "__main__":
    main()