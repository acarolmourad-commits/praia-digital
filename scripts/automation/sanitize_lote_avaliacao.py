#!/usr/bin/env python3
"""
sanitize_lote_avaliacao.py
Sanitiza o lote de leads de Avaliação de Preço de Imóvel.
"""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
SOURCE = FOLDER / 'lote-b2b-avaliacao-2026-07-22.csv'
OUT = FOLDER / 'lote-b2b-avaliacao-sanitizado-2026-07-22.csv'

fields = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']

with SOURCE.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

seen = set()
clean = []
for r in rows:
    key = ((r.get('Nome') or '').strip().lower(), (r.get('Telefone') or '').strip())
    if key in seen:
        continue
    seen.add(key)
    clean.append(r)

with OUT.open('w', newline='', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames=fields, delimiter=';')
    wr.writeheader()
    for r in clean:
        wr.writerow({
            'Lote': (r.get('Lote') or 'avaliacao').strip(),
            'Nome': (r.get('Nome') or '').strip(),
            'Telefone': (r.get('Telefone') or '').strip(),
            'Cidade': (r.get('Cidade') or '').strip(),
            'Data_Msg1': (r.get('Data_Msg1') or '').strip(),
            'Status': (r.get('Status') or 'pendente_msg1').strip(),
            'Resposta': (r.get('Resposta') or '').strip(),
            'Valor_Estimado': (r.get('Valor_Estimado') or '').strip(),
            'Obs': (r.get('Obs') or '').strip(),
            'Acao_Conversao': (r.get('Acao_Conversao') or '').strip(),
            'Msg1': (r.get('Msg1') or '').strip(),
            'Msg2': (r.get('Msg2') or '').strip(),
            'Msg3': (r.get('Msg3') or '').strip(),
            'Email': (r.get('Email') or '').strip() or 'comercial@praia.digital',
            'Imobiliaria': ((r.get('Imobiliaria') or r.get('Nome') or '').strip()),
        })

print(f'Entrada: {SOURCE}\nSaída: {OUT}\nLeads: {len(rows)}\nDuplicatas bloqueadas: {len(rows)-len(clean)}\nStatus final:\n - pendente_msg1: {len(clean)}')
