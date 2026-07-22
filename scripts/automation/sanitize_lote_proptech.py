#!/usr/bin/env python3
"""
sanitize_lote_proptech.py
Sanitiza o lote de leads da Solução Proptech Unificada.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
SOURCE = FOLDER / 'lote-b2b-proptech-unificada-2026-07-22.csv'
OUT = FOLDER / 'lote-b2b-proptech-sanitizado-2026-07-22.csv'

with SOURCE.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria'], delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f'Leads: {len(rows)}')
print(f'Saída: {OUT}')
