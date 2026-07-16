#!/usr/bin/env python3
"""Marca Msg1 (WhatsApp) e Email1 (e-mail) como enviados em todos os lotes.
Uso: python scripts/marcar_primeiro_envio.py
"""
import csv, os, glob, re
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD_W = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
PAD_E = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def marcar(arq, col_status, novo):
    rows = []
    with open(arq, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r.get(col_status) in ("pendente_msg1", "pendente_email1"):
                r[col_status] = novo
            rows.append(r)
    with open(arq, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)

def main():
    n = 0
    for arq in glob.glob(os.path.join(DIR, "lote-whatsapp-proprietarios-*.csv")):
        if PAD_W.search(os.path.basename(arq)):
            marcar(arq, "Status", "enviado_msg1"); n += 1
    for arq in glob.glob(os.path.join(DIR, "lote-email-proprietarios-*.csv")):
        if PAD_E.search(os.path.basename(arq)):
            marcar(arq, "Status", "enviado_email1"); n += 1
    print(f"Primeiro envio marcado em {n} lotes (WhatsApp Msg1 + Email1).")
    print("Agora rode: python scripts/executar_outbound.py --push  (para consolidar trackers + dashboards)")

if __name__ == "__main__":
    main()
