#!/usr/bin/env python3
"""
Consolida todos os lotes EMAIL de proprietarios autogestores num tracker unico.
docs/sales/csv-lotes-email/tracker-email-proprietarios.csv
Preserva Status/Resposta/Valor/Obs dos leads ja registrados (Lote+Nome).
"""
import csv, os, glob, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
EMAIL_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
TRACKER = os.path.join(EMAIL_DIR, "tracker-email-proprietarios.csv")
CAMPOS = ["Lote","Nome","Email","Cidade","Data_Email1","Status","Resposta","Valor_Estimado","Obs"]

def carregar_existente():
    if not os.path.exists(TRACKER):
        return {}
    exist = {}
    with open(TRACKER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            exist[(r["Lote"], r["Nome"])] = r
    return exist

def main():
    exist = carregar_existente()
    arquivos = glob.glob(os.path.join(EMAIL_DIR, "lote-email-proprietarios-*.csv"))
    linhas = []
    for arq in sorted(arquivos):
        m = PAD.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        with open(arq, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                nome = r["Nome"].strip()
                if not nome: continue
                key = (lote, nome)
                if key in exist:
                    linhas.append(exist[key])
                else:
                    linhas.append({"Lote":lote,"Nome":nome,"Email":r["Email"],"Cidade":r["Cidade"],
                        "Data_Email1":r["Data_Email1"],"Status":"pendente_email1","Resposta":"",
                        "Valor_Estimado":"","Obs":""})
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader(); w.writerows(linhas)
    print(f"Tracker consolidado: {TRACKER}\nLeads: {len(linhas)} | ja monitorados: {len(exist)}")

if __name__ == "__main__":
    main()
