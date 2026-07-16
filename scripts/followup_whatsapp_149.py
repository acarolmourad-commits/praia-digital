#!/usr/bin/env python3
"""Cron helper: digere quem deve receber Msg2/Msg3 do lote WhatsApp 149 hoje.
WhatsApp nao tem API/SMTP -> o 'disparo' e o lembrete operacional de envio manual.
Le o CSV do lote e calcula com base na data de Msg1 (15/07/2026).
"""
import csv, os
from datetime import date, timedelta

BASE = date(2026, 7, 15)  # Msg1 enviada em 15/07
CSV = r"C:/Users/Carolina/praia-digital/docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-149-2026-07-15.csv"

def load():
    with open(CSV, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))

def main():
    hoje = date.today()
    delta = (hoje - BASE).days
    if delta < 0:
        print(f"Ainda nao iniciou. Msg1 em {BASE:%d/%m}. Hoje: {hoje:%d/%m/%Y}.")
        return
    leads = load()
    msg2 = [l for l in leads if 1 <= delta <= 2]
    msg3 = [l for l in leads if 3 <= delta <= 4]
    if not msg2 and not msg3:
        print(f"Sem follow-ups hoje ({hoje:%d/%m/%Y}, D+{delta}). Nada a enviar.")
        return
    print(f"=== Follow-up WhatsApp Lote 149 — {hoje:%d/%m/%Y} (D+{delta}) ===")
    if msg2:
        print(f"\nMensagem 2 (Solucao/ROI) — {len(msg2)} lead(s):")
        for l in msg2:
            print(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")
    if msg3:
        print(f"\nMensagem 3 (Encerramento) — {len(msg3)} lead(s):")
        for l in msg3:
            print(f"  • {l['Nome']} ({l['Cidade']}) — {l['Telefone']}")
    print("\nFonte das mensagens: lote-whatsapp-proprietarios-149-2026-07-15.csv (colunas Mensagem_2_Solucao / Mensagem_3_Encerramento).")

if __name__ == "__main__":
    main()
