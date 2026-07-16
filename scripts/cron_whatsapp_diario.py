#!/usr/bin/env python3
"""Cron diario (18h): orquestra outbound completo + avisa follow-ups WPP no stdout.
Consolida trackers, gera 3 dashboards com metas, faz commit/push e lista follow-ups do dia.
O envio real (WhatsApp/e-mail) e manual; este script so avisa e atualiza o rastreio.
"""
import subprocess, os, glob, re, csv
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD_W = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def run(py, *a): subprocess.run(["python", os.path.join(REPO, "scripts", py), *a], check=True)

def main():
    # orquestrador (consolida + dashboards + push)
    run("executar_outbound.py", "--push")

    # aviso de follow-ups WhatsApp do dia
    hoje = date.today(); saida = []; t2 = t3 = 0
    for arq in sorted(glob.glob(os.path.join(DIR, "lote-whatsapp-proprietarios-*.csv"))):
        m = PAD_W.search(os.path.basename(arq))
        if not m: continue
        lote = m.group(1)
        try: base = date.fromisoformat(m.group(2))
        except ValueError: continue
        delta = (hoje - base).days
        if delta < 0: continue
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
    print(f"Dashboards atualizados e commitados. Follow-ups: Msg2={t2} | Msg3={t3}")
    if saida:
        print("\n".join(saida))
        print("\nFonte: lote-whatsapp-proprietarios-*.csv (Mensagem_2_Solucao / Mensagem_3_Encerramento).")
    else:
        print("Sem follow-ups hoje. Nada a enviar.")

if __name__ == "__main__":
    main()
