#!/usr/bin/env python3
"""Consolida lotes EMAIL B2B num tracker unico isolado (docs/sales/csv-lotes-b2b/tracker-email-b2b.csv).
Preserva Status/Resposta/Valor/Obs dos leads ja registrados (Lote+Nome)."""
import csv, os, glob, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
PAD = re.compile(r"lote-email-b2b-([\w-]+)-(\d{4}-\d{2}-\d{2})\.csv")
TRACKER = os.path.join(DIR, "tracker-email-b2b.csv")
CAMPOS = ["Lote","Nome","Email","Imobiliaria","Cidade","Data_Email1","Status","Resposta","Valor_Estimado","Obs","Acao_Conversao"]

def carregar_existente():
    if not os.path.exists(TRACKER): return {}
    e={}
    with open(TRACKER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            e[(r["Lote"], r["Nome"])] = r
    return e

def main():
    exist = carregar_existente()
    arqs = glob.glob(os.path.join(DIR, "lote-email-b2b-*.csv"))
    linhas=[]
    for arq in sorted(arqs):
        m = PAD.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        with open(arq, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                chave=(lote, r["Nome"])
                if chave in exist:
                    linhas.append(exist[chave]); continue
                linhas.append({"Lote":lote,"Nome":r["Nome"],"Email":r["Email"],"Imobiliaria":r["Imobiliaria"],
                    "Cidade":r["Cidade"],"Data_Email1":r.get("Data_Email1",""),"Status":r.get("Status","pendente_email1"),
                    "Resposta":"","Valor_Estimado":"","Obs":"","Acao_Conversao":""})
    with open(TRACKER,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=CAMPOS,delimiter=";"); w.writeheader(); w.writerows(linhas)
    print(f"Tracker EMAIL B2B: {TRACKER}\n{len(linhas)} leads consolidados (isolado do B2C).")

if __name__=="__main__": main()
