#!/usr/bin/env python3
"""Marca o primeiro envio de EMAIL B2B (E1) no tracker isolado. Idempotente.
Uso: python scripts/marcar_primeiro_envio_email_b2b.py"""
import csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-b2b", "tracker-email-b2b.csv")
HOJE = date.today().isoformat()

def main():
    if not os.path.exists(TRACKER):
        print("Tracker nao existe. Rode consolidar_tracker_email_b2b.py primeiro."); return
    rows=list(csv.DictReader(open(TRACKER,encoding="utf-8-sig"),delimiter=";"))
    n=0
    for r in rows:
        if r["Status"]=="pendente_email1":
            r["Data_Email1"]=HOJE; r["Status"]="enviado_email1"; n+=1
    with open(TRACKER,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter=";"); w.writeheader(); w.writerows(rows)
    print(f"E1 marcado p/ {n} leads B2B (Data_Email1={HOJE}). Restam: {sum(1 for r in rows if r['Status']=='pendente_email1')}")

if __name__=="__main__": main()
