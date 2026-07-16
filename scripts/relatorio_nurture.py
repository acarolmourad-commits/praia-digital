#!/usr/bin/env python3
"""Relatorio de NURTURE/WIN-BACK para leads marcados sem_interesse.
Avisa no Telegram (stdout) quem esta nas janelas D+30 / D+60 / D+90.
Gera CSVs prontos (mensagens preenchidas) para copia-e-cola.
Le os trackers WPP+e-mail; coluna Data_Msg1 como base de tempo.
"""
import csv, os, glob
from datetime import date, datetime

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
TRACKERS = {"WhatsApp": os.path.join(DIR,"tracker-whatsapp-proprietarios.csv"),
            "E-mail": os.path.join(DIR,"tracker-email-proprietarios.csv")}
JANELAS = [("D+30 (Msg5)",30),("D+60 (Msg5b)",60),("D+90 (Msg5c)",90)]
CSV_OUT = os.path.join(DIR, "nurture-pendente.csv")

def parse(d):
    try: return datetime.strptime(d.strip(),"%Y-%m-%d").date()
    except: return None

def main():
    hoje = date.today()
    pend = []
    saida = []
    for canal, arq in TRACKERS.items():
        if not os.path.exists(arq): continue
        for r in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
            if r["Status"] != "sem_interesse": continue
            d0 = parse(r.get("Data_Msg1","") or r.get("Data_Email1",""))
            if not d0: continue
            dias = (hoje - d0).days
            for label, j in JANELAS:
                if dias == j:
                    contato = r.get("Telefone") or r.get("Email")
                    pend.append({"Canal":canal,"Lote":r["Lote"],"Nome":r["Nome"],"Cidade":r["Cidade"],
                                 "Contato":contato,"Janela":label})
                    saida.append(f"  • [{canal}] {r['Nome']} ({r['Cidade']}) — {label} — {contato}")
    print(f"=== Nurture / Win-Back — {hoje:%d/%m/%Y} ===")
    if pend:
        print(f"{len(pend)} lead(s) na janela de re-toque:")
        print("\n".join(saida))
        print("\nMensagens: outreach/nurture-proprietarios.md")
        with open(CSV_OUT, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["Canal","Lote","Nome","Cidade","Contato","Janela"], delimiter=";")
            w.writeheader(); w.writerows(pend)
        print(f"\nCSV pronto: {CSV_OUT}")
    else:
        print("Nenhum lead na janela de nurture hoje. 🌱")

if __name__ == "__main__":
    main()
