#!/usr/bin/env python3
"""
Marca Msg1 do lote B2B como enviado (one-click) e grava Data_Msg1=hoje no tracker B2B.
Uso: python scripts/marcar_primeiro_envio_b2b.py
So marcar — o disparo manual (copiar/colar) e feito pelo operador humano.
"""
import csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
LOTE = os.path.join(DIR, "lote-b2b-reativacao-2026-07-16.csv")
TRACKER = os.path.join(DIR, "tracker-b2b.csv")
COLS = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status",
        "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao"]

def marcar_csv(arq, novo):
    rows = list(csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"))
    n = 0
    for r in rows:
        if r["Status"] == "pendente_msg1":
            r["Status"] = novo; r["Data_Msg1"] = date.today().isoformat(); n += 1
    with open(arq, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter=";"); w.writeheader(); w.writerows(rows)
    return n

def marcar_tracker():
    if not os.path.exists(TRACKER): return 0
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    n = 0
    for r in rows:
        if r["Status"] == "pendente_msg1":
            r["Status"] = "enviado_msg1"; r["Data_Msg1"] = date.today().isoformat(); n += 1
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter=";"); w.writeheader(); w.writerows(rows)
    return n

if __name__ == "__main__":
    n1 = marcar_csv(LOTE, "enviado_msg1")
    n2 = marcar_tracker()
    print(f"B2B marcado: lote={n1} | tracker={n2}. Agora rode o disparo manual copia-e-cola.")
