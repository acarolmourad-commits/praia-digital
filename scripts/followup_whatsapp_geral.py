#!/usr/bin/env python3
"""
Cron diario: varre todos os lotes WhatsApp de proprietarios autogestores e avisa
quem deve receber Msg2 (+1 a 2 dias) ou Msg3 (+3 a 4 dias) hoje.
WhatsApp nao tem API/SMTP -> o 'disparo' e o lembrete operacional de envio manual
(copiar do CSV e colar no WhatsApp por contato).

Le todos os arquivos docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-*.csv
e usa a coluna Data_Msg1 para calcular o delta.
"""
import csv, os, re, glob
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
WHATS_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
PAD = re.compile(r"lote-whatsapp-proprietarios-(\d+)-(\d{4}-\d{2}-\d{2})\.csv")

def main():
    hoje = date.today()
    arquivos = glob.glob(os.path.join(WHATS_DIR, "lote-whatsapp-proprietarios-*.csv"))
    if not arquivos:
        print("Nenhum lote WhatsApp encontrado.")
        return

    saida = []
    total2 = total3 = 0
    for arq in sorted(arquivos):
        m = PAD.search(os.path.basename(arq))
        if not m:
            continue
        lote = m.group(1)
        with open(arq, encoding="utf-8-sig") as f:
            leads = list(csv.DictReader(f, delimiter=";"))
        # data-base real do envio: coluna Data_Msg1 do CSV (nao o nome do arquivo)
        datas = [l.get("Data_Msg1","").strip() for l in leads if l.get("Data_Msg1","").strip()]
        if not datas:
            continue
        try:
            base = date.fromisoformat(datas[0])
        except ValueError:
            continue
        delta = (hoje - base).days
        if delta < 0:
            continue
        m2 = [l for l in leads if l.get("Status") in ("enviado_msg1","enviado_msg2") and 1 <= delta <= 2]
        m3 = [l for l in leads if l.get("Status") in ("enviado_msg1","enviado_msg2","enviado_msg3") and 3 <= delta <= 4]
        if not m2 and not m3:
            continue
        saida.append(f"\n--- Lote {lote} (D+{delta}) ---")
        if m2:
            total2 += len(m2)
            saida.append(f"Msg2 (Solucao/ROI) — {len(m2)}:")
            for l in m2:
                saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")
        if m3:
            total3 += len(m3)
            saida.append(f"Msg3 (Encerramento) — {len(m3)}:")
            for l in m3:
                saida.append(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")

    if not saida:
        print(f"Sem follow-ups hoje ({hoje:%d/%m/%Y}). Nada a enviar.")
        return
    print(f"=== Follow-up WhatsApp Proprietários — {hoje:%d/%m/%Y} ===")
    print(f"Total Msg2: {total2} | Total Msg3: {total3}")
    print("\n".join(saida))
    print("\nFonte: docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-*.csv "
          "(colunas Mensagem_2_Solucao / Mensagem_3_Encerramento).")

if __name__ == "__main__":
    main()
