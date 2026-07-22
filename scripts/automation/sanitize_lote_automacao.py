#!/usr/bin/env python3
"""
sanitize_lote_automacao.py
Audita e prepara o lote B2B de automação para imobiliárias.
Uso: python scripts/automation/sanitize_lote_automacao.py
"""

import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-automacao-2026-07-22.csv"
SAIDA = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-automacao-sanitizado-2026-07-22.csv"


def normalizar(v):
    return " ".join(str(v or "").split()).strip().lower()


def main():
    rows = []
    with ENTRADA.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rows.append(row)

    campos = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status", "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao", "Msg1", "Msg2", "Msg3", "Email", "Imobiliaria"]

    # Duplicatas por telefone
    telefones = Counter(normalizar(r.get("Telefone", "")) for r in rows)
    duplicados = {t for t, c in telefones.items() if c > 1 and t}

    sane = []
    for r in rows:
        tel = normalizar(r.get("Telefone", ""))
        if not tel or tel in duplicados:
            r["Status"] = "bloqueado_duplicidade" if tel in duplicados else r.get("Status", "pendente_msg1")
            sane.append(r)
        else:
            sane.append(r)

    # Garantir campos padrão
    for r in sane:
        r.setdefault("Lote", "automacao")
        r.setdefault("Data_Msg1", "2026-07-22")
        r.setdefault("Status", "pendente_msg1")
        r.setdefault("Acao_Conversao", "")
        r.setdefault("Imobiliaria", r.get("Nome", ""))

    saida_fields = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status", "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao", "Msg1", "Msg2", "Msg3", "Email", "Imobiliaria"]
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=saida_fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(sane)

    print(f"Entrada: {ENTRADA}")
    print(f"Saída: {SAIDA}")
    print(f"Leads: {len(rows)}")
    print(f"Duplicatas bloqueadas: {len(duplicados)}")
    print(f"Status final:")
    for status, qty in Counter(r.get("Status", "") for r in sane).most_common():
        print(f" - {status or 'vazio'}: {qty}")

if __name__ == "__main__":
    main()
