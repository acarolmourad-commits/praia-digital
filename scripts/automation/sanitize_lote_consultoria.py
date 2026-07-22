#!/usr/bin/env python3
"""
sanitize_lote_consultoria.py
Sanitiza o lote de leads da Consultoria de Transformação Digital.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
SOURCE = FOLDER / 'lote-b2b-consultoria-2026-07-22.csv'
OUT = FOLDER / 'lote-b2b-consultoria-sanitizado-2026-07-22.csv'

with SOURCE.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

seen = set()
clean = []
for r in rows:
    key = (r.get('Nome','').strip().lower(), r.get('Telefone','').strip())
    if key in seen:
        continue
    seen.add(key)
    clean.append(r)

with OUT.open('w', newline='', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames=['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria'], delimiter=';')
    wr.writeheader()
    for r in clean:
        wr.writerow({
            'Lote': r.get('Lote','consultoria'),
            'Nome': r.get('Nome','').strip(),
            'Telefone': r.get('Telefone','').strip(),
            'Cidade': r.get('Cidade','').strip(),
            'Data_Msg1': r.get('Data_Msg1',''),
            'Status': r.get('Status','pendente_msg1'),
            'Resposta': r.get('Resposta',''),
            'Valor_Estimado': r.get('Valor_Estimado',''),
            'Obs': r.get('Obs',''),
            'Acao_Conversao': r.get('Acao_Conversao',''),
            'Msg1': r.get('Msg1',''),
            'Msg2': r.get('Msg2',''),
            'Msg3': r.get('Msg3',''),
            'Email': r.get('Email','comercial@praia.digital'),
            'Imobiliaria': ((r.get('Imobiliaria') or r.get('Nome') or '').strip()),
        })

print(f'Entrada: {SOURCE}')
print(f'Saída: {OUT}')
print(f'Leads: {len(rows)}')
print(f'Duplicatas bloqueadas: {len(rows)-len(clean)}')
print('Status final:')
print(f' - pendente_msg1: {len(clean)}')
