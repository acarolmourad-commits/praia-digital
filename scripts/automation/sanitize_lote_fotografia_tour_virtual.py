#!/usr/bin/env python3
"""
sanitize_lote_fotografia_tour_virtual.py
Audita e prepara o lote B2B de Fotografia e Tour Virtual para imobiliárias.
Uso: python scripts/automation/sanitize_lote_fotografia_tour_virtual.py
"""

import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-fotografia-tour-virtual-2026-07-22.csv"
SAIDA = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-fotografia-tour-virtual-sanitizado-2026-07-22.csv"


def normalizar(v):
    return " ".join(str(v or "").split()).strip().lower()


def main():
    rows = []
    with ENTRADA.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rows.append(row)

    campos = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status", "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao", "Msg1", "Msg2", "Msg3", "Email", "Imobiliaria"]

    telefones = Counter(normalizar(r.get("Telefone", "")) for r in rows)
    duplicados = {t for t, c in telefones.items() if c > 1 and t}

    sane = []
    for r in rows:
        tel = normalizar(r.get("Telefone", ""))
        if not tel or tel in duplicados:
            continue
        sane.append(r)

    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        writer.writeheader()
        for row in sane:
            writer.writerow(row)

    print(f"Sanitizado fotografia_tour_virtual: {len(rows)} -> {len(sane)} leads")


if __name__ == "__main__":
    main()
