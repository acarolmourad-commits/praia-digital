#!/usr/bin/env python3
"""Follow-up EMAIL B2B (Expansao E) — varre tracker-email-b2b.csv e monta aviso Telegram
dos leads que devem receber E2 (D+2) ou E3 (D+5). Requer as colunas Data_Email1/Status.
Uso: python scripts/followup_email_b2b.py"""
import csv, os
from datetime import date, datetime

REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-b2b", "tracker-email-b2b.csv")

def dias(data):
    try: return (date.today() - datetime.strptime(data, "%Y-%m-%d").date()).days
    except: return 999

def main():
    if not os.path.exists(TRACKER):
        print("Sem tracker-email-b2b.csv"); return
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    e2, e3 = [], []
    for r in rows:
        d = dias(r.get("Data_Email1",""))
        if r["Status"] == "enviado_email1" and d == 2: e2.append(r)
        elif r["Status"] == "enviado_email2" and d == 5: e3.append(r)
    linhas = [f"📧 FOLLOW-UP EMAIL B2B — {date.today():%d/%m/%Y}", ""]
    if e2:
        linhas.append(f"▶️ E2 (D+2) — {len(e2)} imobiliárias:")
        for r in e2[:12]: linhas.append(f"  • {r['Nome']} ({r['Imobiliaria']} / {r['Cidade']})")
    else: linhas.append("▶️ E2 (D+2): nenhum hoje")
    if e3:
        linhas.append(f"▶️ E3 (D+5) — {len(e3)} imobiliárias:")
        for r in e3[:12]: linhas.append(f"  • {r['Nome']} ({r['Imobiliaria']} / {r['Cidade']})")
    else: linhas.append("▶️ E3 (D+5): nenhum hoje")
    if e2 or e3:
        linhas.append("")
        linhas.append("Copie a coluna Email_2_Solucao / Email_3_Encerramento do lote e envie.")
    print("\n".join(linhas))

if __name__ == "__main__":
    main()
