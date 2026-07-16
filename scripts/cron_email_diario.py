#!/usr/bin/env python3
"""Cron diario EMAIL: consolida tracker, regera dashboard e avisa follow-ups (E2 +2d, E3 +5d)."""
import subprocess, os, glob, re, csv
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
EMAIL_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD = re.compile(r"lote-email-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def run(py): subprocess.run(["python", os.path.join(REPO, "scripts", py)], check=True)

def main():
    run("consolidar_tracker_email.py")
    run("gerar_dashboard_email.py")
    hoje = date.today(); saida = []; t2 = t3 = 0
    for arq in sorted(glob.glob(os.path.join(EMAIL_DIR, "lote-email-proprietarios-*.csv"))):
        m = PAD.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        try: base = date.fromisoformat(m.group(2))
        except ValueError: continue
        delta = (hoje - base).days
        if delta < 0: continue
        leads = list(csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"))
        e2 = [l for l in leads if 2 <= delta <= 3]
        e3 = [l for l in leads if 5 <= delta <= 6]
        if not e2 and not e3: continue
        saida.append(f"\n--- Lote {lote} (D+{delta}) ---")
        if e2:
            t2 += len(e2); saida.append(f"Email2 (Solucao/ROI) — {len(e2)}:")
            for l in e2: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Email']}")
        if e3:
            t3 += len(e3); saida.append(f"Email3 (Encerramento) — {len(e3)}:")
            for l in e3: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Email']}")
    print(f"=== Praia Digital — EMAIL Proprietários {hoje:%d/%m/%Y} ===")
    print(f"Dashboard atualizado. Follow-ups: E2={t2} | E3={t3}")
    if saida:
        print("\n".join(saida))
        print("\nFonte: lote-email-proprietarios-*.csv (Email_2_Solucao / Email_3_Encerramento).")
    else:
        print("Sem follow-ups hoje. Nada a enviar.")

if __name__ == "__main__":
    main()
