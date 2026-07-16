#!/usr/bin/env python3
"""
Follow-up B2B (Expansao A) — lista no stdout (Telegram) os leads de imobiliarias
que devem receber Msg2 (D+1..2) ou Msg3 (D+3..4) hoje.
Reusa a logica do follow-up WPP, mas lendo o tracker B2B isolado.
Data-base real = coluna Data_Msg1 do tracker. Status fonte de verdade = o proprio tracker.

Uso: python scripts/followup_b2b.py   (stdout vai pro Telegram via cron no_agent)
"""
import csv, os, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
TRACKER = os.path.join(DIR, "tracker-b2b.csv")

def main():
    hoje = date.today()
    if not os.path.exists(TRACKER):
        print(f"Sem tracker B2B ({TRACKER}).")
        return
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    t2 = t3 = 0; saida = []
    for r in rows:
        d = r.get("Data_Msg1", "").strip()
        if not d: continue
        try: base = date.fromisoformat(d)
        except ValueError: continue
        delta = (hoje - base).days
        st = r["Status"]
        m2 = st in ("enviado_msg1", "enviado_msg2") and 1 <= delta <= 2
        m3 = st in ("enviado_msg1", "enviado_msg2", "enviado_msg3") and 3 <= delta <= 4
        if m2:
            t2 += 1; saida.append(f"  • {r['Nome']} ({r['Cidade']}) — {r['Telefone']} [Msg2]")
        elif m3:
            t3 += 1; saida.append(f"  • {r['Nome']} ({r['Cidade']}) — {r['Telefone']} [Msg3]")
    if saida:
        print(f"=== Praia Digital — B2B Imobiliárias {hoje:%d/%m/%Y} ===")
        print(f"Follow-ups: Msg2={t2} | Msg3={t3}")
        print("\n".join(saida))
        print("\nFonte: tracker-b2b.csv (colunas Msg1/Msg2/Msg3 do lote).")
    else:
        print(f"=== Praia Digital — B2B Imobiliárias {hoje:%d/%m/%Y} ===\nSem follow-ups hoje. Nada a enviar.")

if __name__ == "__main__":
    main()
