#!/usr/bin/env python3
"""Marca Msg1 (WhatsApp) e Email1 (e-mail) como enviados em todos os lotes E nos trackers.
Uso: python scripts/marcar_primeiro_envio.py
"""
import csv, os, glob, re
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD_W = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
PAD_E = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
TRACKER_W = os.path.join(DIR, "tracker-whatsapp-proprietarios.csv")
TRACKER_E = os.path.join(DIR, "tracker-email-proprietarios.csv")

def marcar_csv(arq, col, de, novo):
    rows = []
    with open(arq, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r.get(col) == de:
                r[col] = novo
            rows.append(r)
    with open(arq, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)

def marcar_tracker(tracker, novo):
    if not os.path.exists(tracker): return 0
    rows = []
    n = 0
    with open(tracker, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            if r.get("Status") in ("pendente_msg1", "pendente_email1"):
                r["Status"] = novo; n += 1
            rows.append(r)
    with open(tracker, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    return n

def main():
    nlot = 0
    for arq in glob.glob(os.path.join(DIR, "lote-whatsapp-proprietarios-*.csv")):
        if PAD_W.search(os.path.basename(arq)):
            marcar_csv(arq, "Status", "contato_inicial_pendente", "enviado_msg1"); nlot += 1
    for arq in glob.glob(os.path.join(DIR, "lote-email-proprietarios-*.csv")):
        if PAD_E.search(os.path.basename(arq)):
            marcar_csv(arq, "Status", "pendente_email1", "enviado_email1"); nlot += 1
    nw = marcar_tracker(TRACKER_W, "enviado_msg1")
    ne = marcar_tracker(TRACKER_E, "enviado_email1")
    print(f"Primeiro envio marcado: {nlot} lotes | trackers WPP={nw} e-mail={ne}.")
    print("Agora rode: python scripts/executar_outbound.py --push")

if __name__ == "__main__":
    main()
