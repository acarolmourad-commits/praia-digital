#!/usr/bin/env python3
"""
Prepara o DISPARO B2B (Expansao A/C) — consolida os lotes B2B num CSV unico de envio.
Nao marca como enviado (preserva o funil); apenas gera a planilha de trabalho do operador.
Colunas: Nome, Telefone, Cidade, Imobiliaria, Msg1, tipo (reativacao/whitelabel).

Uso: python scripts/preparar_disparo_b2b.py [--out ARQUIVO]
"""
import csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
OUT = os.path.join(DIR, "disparo-b2b-consolidado-2026-07-16.csv")
LOTES = [
    ("lote-b2b-reativacao-2026-07-16.csv", "reativacao"),
    ("lote-b2b-whitelabel-2026-07-16.csv", "whitelabel"),
]

def main():
    out = []
    for arq, tipo in LOTES:
        p = os.path.join(DIR, arq)
        if not os.path.exists(p):
            print(f"  (ignorado) {arq} nao existe")
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig"), delimiter=";"):
            if r["Status"] != "pendente_msg1":
                continue
            out.append({
                "Nome": r["Nome"], "Telefone": r["Telefone"], "Cidade": r["Cidade"],
                "Imobiliaria": r.get("Imobiliaria", ""), "Msg1": r["Msg1"],
                "tipo": tipo,
            })
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["Nome", "Telefone", "Cidade", "Imobiliaria", "Msg1", "tipo"], delimiter=";")
        w.writeheader(); w.writerows(out)
    print(f"Disparo B2B consolidado: {OUT}\n{len(out)} leads pendentes (Msg1) prontos p/ envio manual/Brevo.")

if __name__ == "__main__":
    main()
