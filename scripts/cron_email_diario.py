#!/usr/bin/env python3
"""Cron diario (18h30): avisa follow-ups de EMAIL no stdout.
O consolidar/dashboards ja foi feito pelo cron do WhatsApp (18h) via executar_outbound.py --push.
Aqui so listamos os leads de e-mail que devem receber E2 (+2d) ou E3 (+5d) hoje.
"""
import subprocess, os, glob, re, csv
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD_E = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def main():
    hoje = date.today(); saida = []; t2 = t3 = 0
    for arq in sorted(glob.glob(os.path.join(DIR, "lote-email-proprietarios-*.csv"))):
        m = PAD_E.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        leads = list(csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"))
        datas = [l.get("Data_Email1","").strip() for l in leads if l.get("Data_Email1","").strip()]
        if not datas: continue
        try: base = date.fromisoformat(datas[0])
        except ValueError: continue
        delta = (hoje - base).days
        if delta < 0: continue
        e2 = [l for l in leads if l.get("Status") in ("enviado_email1","enviado_email2") and 2 <= delta <= 3]
        e3 = [l for l in leads if l.get("Status") in ("enviado_email1","enviado_email2","enviado_email3") and 5 <= delta <= 6]
        if not e2 and not e3: continue
        saida.append(f"\n--- Lote {lote} (D+{delta}) ---")
        if e2:
            t2 += len(e2); saida.append(f"Email2 (Solucao/ROI) — {len(e2)}:")
            for l in e2: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Email']}")
        if e3:
            t3 += len(e3); saida.append(f"Email3 (Encerramento) — {len(e3)}:")
            for l in e3: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Email']}")
    print(f"=== Praia Digital — EMAIL Proprietários {hoje:%d/%m/%Y} ===")
    print(f"Follow-ups: E2={t2} | E3={t3}")
    if saida:
        print("\n".join(saida))
        print("\nFonte: lote-email-proprietarios-*.csv (Email_2_Solucao / Email_3_Encerramento).")
    else:
        print("Sem follow-ups hoje. Nada a enviar.")

if __name__ == "__main__":
    main()
