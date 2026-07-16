#!/usr/bin/env python3
"""Marca a acao de conversao de um lead no tracker (evita re-lembrete diario).
Uso:
  python scripts/marcar_acao_conversao.py --canal wpp --lote 149 --nome "Fernanda Lima" --acao msg25_feita
  python scripts/marcar_acao_conversao.py --canal email --lote 149 --nome "Fernanda Lima" --acao onboarding_feito
Acoes: msg25_feita | onboarding_feito
"""
import argparse, csv, os
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
TRACKERS = {"wpp": os.path.join(DIR,"tracker-whatsapp-proprietarios.csv"),
            "email": os.path.join(DIR,"tracker-email-proprietarios.csv")}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--canal", required=True, choices=["wpp","email"])
    p.add_argument("--lote", required=True); p.add_argument("--nome", required=True)
    p.add_argument("--acao", required=True, choices=["msg25_feita","onboarding_feito"])
    args = p.parse_args()
    arq = TRACKERS[args.canal]
    if not os.path.exists(arq):
        print("Tracker ausente."); return
    rows = []; found = False
    for r in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
        if r["Lote"] == args.lote and r["Nome"].strip().lower() == args.nome.strip().lower():
            r["Acao_Conversao"] = args.acao; found = True
        rows.append(r)
    if not found:
        print(f"Lead nao encontrado: {args.canal} / {args.lote} / {args.nome}"); return
    with open(arq, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print(f"Acao de conversao marcada: {args.canal} / {args.lote} / {args.nome} -> {args.acao}")

if __name__ == "__main__":
    main()
