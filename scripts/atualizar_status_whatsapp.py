#!/usr/bin/env python3
"""
Atualiza o status de um lead no tracker consolidado de WhatsApp.
Uso:
  python scripts/atualizar_status_whatsapp.py --lote 149 --nome "Fernanda Lima" --status fechou --valor 1200
Status: pendente_msg1 | enviado_msg1 | enviado_msg2 | enviado_msg3 | respondeu | fechou | sem_interesse
"""
import argparse, csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-email", "tracker-whatsapp-proprietarios.csv")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lote", required=True)
    p.add_argument("--nome", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--valor", default="")
    p.add_argument("--obs", default="")
    args = p.parse_args()

    if not os.path.exists(TRACKER):
        print("Tracker nao existe. Rode consolidar_tracker_whatsapp.py primeiro.")
        return
    rows = []
    found = False
    with open(TRACKER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r["Lote"] == args.lote and r["Nome"].strip().lower() == args.nome.strip().lower():
                r["Status"] = args.status
                if args.valor:
                    r["Valor_Estimado"] = args.valor
                if args.obs:
                    r["Obs"] = args.obs
                found = True
            rows.append(r)
    if not found:
        print(f"Lead nao encontrado: Lote {args.lote} / {args.nome}")
        return
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    print(f"Atualizado: Lote {args.lote} / {args.nome} -> {args.status}")

if __name__ == "__main__":
    main()
