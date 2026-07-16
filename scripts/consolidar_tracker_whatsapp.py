#!/usr/bin/env python3
"""
Consolida todos os lotes WhatsApp de proprietarios autogestores num unico tracker.
docs/sales/csv-lotes-email/tracker-whatsapp-proprietarios.csv

Colunas: Lote, Nome, Telefone, Cidade, Data_Msg1, Status, Resposta, Valor_Estimado, Obs
Status possiveis:
  pendente_msg1 | enviado_msg1 | enviado_msg2 | enviado_msg3
  | respondeu | fechou | sem_interesse

Se o tracker ja existir, preserva Status/Resposta/Valor/Obs dos leads ja registrados
(identificados por Lote+Nome) e apenas adiciona leads novos.
"""
import csv, os, glob, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
WHATS_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")
TRACKER = os.path.join(WHATS_DIR, "tracker-whatsapp-proprietarios.csv")

CAMPOS = ["Lote","Nome","Telefone","Cidade","Data_Msg1","Status","Resposta","Valor_Estimado","Obs"]

def carregar_existente():
    if not os.path.exists(TRACKER):
        return {}
    exist = {}
    with open(TRACKER, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            key = (r["Lote"], r["Nome"])
            exist[key] = r
    return exist

def main():
    exist = carregar_existente()
    arquivos = glob.glob(os.path.join(WHATS_DIR, "lote-whatsapp-proprietarios-*.csv"))
    linhas = []
    for arq in sorted(arquivos):
        m = PAD.search(os.path.basename(arq))
        if not m:
            continue
        lote = m.group(1)
        with open(arq, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                nome = r["Nome"].strip()
                if not nome:
                    continue
                key = (lote, nome)
                if key in exist:
                    linhas.append(exist[key])
                else:
                    linhas.append({
                        "Lote": lote, "Nome": nome, "Telefone": r["Telefone"],
                        "Cidade": r["Cidade"], "Data_Msg1": r["Data_Msg1"],
                        "Status": "pendente_msg1", "Resposta": "",
                        "Valor_Estimado": "", "Obs": ""
                    })
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    print(f"Tracker consolidado: {TRACKER}")
    print(f"Leads totais: {len(linhas)} | ja monitorados: {len(exist)}")

if __name__ == "__main__":
    main()
