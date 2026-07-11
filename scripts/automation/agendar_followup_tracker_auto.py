#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agendador automático de follow-ups no tracker.
Lê leads do CSV e programa D3/D7/D14 por perfil e cidade.
"""
import os
import csv
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEADS_CSV = os.path.join(BASE, "docs", "sales", "leads-litoral-enriquecido.csv")
TRACKER = os.path.join(BASE, "docs", "sales", "followup-registro.md")


def schedule_for_lead(nome, imob, canal, tipo, data_ref):
    ref = datetime.strptime(data_ref, "%Y-%m-%d")
    d0 = ref
    d3 = ref + timedelta(days=3)
    d7 = ref + timedelta(days=7)
    d14 = ref + timedelta(days=14)
    line = f"| {nome} | {imob} | {canal} | {tipo} | {d0.strftime('%Y-%m-%d')} | {d3.strftime('%Y-%m-%d')} | {d7.strftime('%Y-%m-%d')} |"
    with open(TRACKER, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line


def main():
    if not os.path.exists(LEADS_CSV):
        print(f"Arquivo não encontrado: {LEADS_CSV}")
        return
    rows = []
    with open(LEADS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for r in reader:
            rows.append(r)
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    for r in rows:
        status = (r.get("status") or "").strip().lower()
        if status in ["parceria_fechada", "resposta_recebida"]:
            continue
        nome = r.get("pessoa_de_contato") or r.get("nome") or "Lead"
        imob = r.get("nome_da_imobiliaria") or "Imobiliária"
        cidade = r.get("cidade") or "Litoral"
        canal = "email"
        tipo = "parceria"
        schedule_for_lead(nome, imob, canal, tipo, today)
        count += 1
    print(f"Agendados follow-ups para {count} leads em {TRACKER}")


if __name__ == "__main__":
    main()
