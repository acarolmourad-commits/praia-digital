#!/usr/bin/env python3
"""Wrapper diario do cron WhatsApp: consolida tracker, regera dashboard e avisa follow-ups."""
import subprocess, os, glob, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
WHATS_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def run(py):
    subprocess.run(["python", os.path.join(REPO, "scripts", py)], check=True)

def main():
    # 1) consolidar tracker (preserva status manuais)
    run("consolidar_tracker_whatsapp.py")
    # 2) regerar dashboard
    run("gerar_dashboard_whatsapp.py")
    # 2b) consolidado multicanal
    run("consolidar_tracker_email.py")
    run("gerar_dashboard_email.py")
    run("gerar_dashboard_outbound.py")
    # 3) aviso de follow-ups
    hoje = date.today()
    arquivos = glob.glob(os.path.join(WHATS_DIR, "lote-whatsapp-proprietarios-*.csv"))
    saida = []
    t2 = t3 = 0
    for arq in sorted(arquivos):
        m = PAD.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        try: base = date.fromisoformat(m.group(2))
        except ValueError: continue
        delta = (hoje - base).days
        if delta < 0: continue
        import csv
        leads = list(csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"))
        m2 = [l for l in leads if 1 <= delta <= 2]
        m3 = [l for l in leads if 3 <= delta <= 4]
        if not m2 and not m3: continue
        saida.append(f"\n--- Lote {lote} (D+{delta}) ---")
        if m2:
            t2 += len(m2); saida.append(f"Msg2 (Solucao/ROI) — {len(m2)}:")
            for l in m2: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")
        if m3:
            t3 += len(m3); saida.append(f"Msg3 (Encerramento) — {len(m3)}:")
            for l in m3: saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")
    print(f"=== Praia Digital — WhatsApp Proprietários {hoje:%d/%m/%Y} ===")
    print(f"Dashboard atualizado. Follow-ups: Msg2={t2} | Msg3={t3}")
    if saida:
        print("\n".join(saida))
        print("\nFonte: lote-whatsapp-proprietarios-*.csv (Mensagem_2_Solucao / Mensagem_3_Encerramento).")
    else:
        print("Sem follow-ups hoje. Nada a enviar.")

if __name__ == "__main__":
    main()
