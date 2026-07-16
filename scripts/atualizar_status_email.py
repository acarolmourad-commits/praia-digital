#!/usr/bin/env python3
"""Atualiza status de um lead no tracker de EMAIL.
Uso: python scripts/atualizar_status_email.py --lote 149 --nome "Fernanda Lima" --status fechou --valor 1200
Status: pendente_email1 | enviado_email1 | enviado_email2 | enviado_email3 | respondeu | fechou | sem_interesse
"""
import argparse, csv, os
REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-email", "tracker-email-proprietarios.csv")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lote", required=True); p.add_argument("--nome", required=True)
    p.add_argument("--status", required=True); p.add_argument("--valor", default="")
    p.add_argument("--obs", default="")
    args = p.parse_args()
    if not os.path.exists(TRACKER):
        print("Tracker ausente. Rode consolidar_tracker_email.py."); return
    rows = []; found = False
    with open(TRACKER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["Lote"] == args.lote and r["Nome"].strip().lower() == args.nome.strip().lower():
                r["Status"] = args.status
                if args.valor: r["Valor_Estimado"] = args.valor
                if args.obs: r["Obs"] = args.obs
                found = True
            rows.append(r)
    if not found:
        print(f"Lead nao encontrado: Lote {args.lote} / {args.nome}"); return
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print(f"Atualizado: Lote {args.lote} / {args.nome} -> {args.status}")

if __name__ == "__main__":
    main()
