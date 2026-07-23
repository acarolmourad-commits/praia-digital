#!/usr/bin/env python3
"""
disparar_lote_gestao_anuncios.py
Envia lote B2B de gestao_anuncios via integração direta.
Uso: python scripts/automation/disparar_lote_gestao_anuncios.py
"""

import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
LOTE = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-gestao_anuncios-sanitizado-2026-07-22.csv"


def main():
    if not LOTE.exists():
        print(f"[SKIP] gestao_anuncios: sanitizado não encontrado")
        return
    rows = []
    with LOTE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rows.append(row)
    print(f"[{servico}] total {len(rows)}")
    for row in rows:
        print(row.get("Telefone", "-"))


if __name__ == "__main__":
    main()
