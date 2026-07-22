#!/usr/bin/env python3
"""
disparar_lote_avaliacao.py
Prepara o pacote de disparo do lote de Avaliação de Preço de Imóvel.
"""
import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
TODAY = date.today().isoformat()

SOURCE = FOLDER / 'lote-b2b-avaliacao-2026-07-22.csv'
BREVO_OUT = FOLDER / f'para-brevo-avaliacao-{TODAY}.csv'
WA_OUT = FOLDER / f'para-whatsapp-avaliacao-{TODAY}.csv'
CHECK_OUT = BASE / 'docs' / 'sales' / f'checklist-envio-avaliacao-{TODAY}.txt'

with SOURCE.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

email_rows, wa_rows = [], []
for r in rows:
    tel = (r.get('Telefone') or '').strip()
    if tel:
        wa_rows.append(r)
    email_rows.append(r)

if email_rows:
    with BREVO_OUT.open('w', newline='', encoding='utf-8') as f:
        fieldnames = ['nome', 'email', 'telefone', 'cidade', 'imobiliaria']
        wr = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        wr.writeheader()
        for r in email_rows:
            wr.writerow({
                'nome': r.get('Nome', ''),
                'email': r.get('Email') or 'comercial@praia.digital',
                'telefone': r.get('Telefone', ''),
                'cidade': r.get('Cidade', ''),
                'imobiliaria': r.get('Imobiliaria', r.get('Nome', '')),
            })

if wa_rows:
    with WA_OUT.open('w', newline='', encoding='utf-8') as f:
        fieldnames = ['nome', 'telefone', 'cidade', 'imobiliaria', 'msg1']
        wr = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        wr.writeheader()
        for r in wa_rows:
            wr.writerow({
                'nome': r.get('Nome', ''),
                'telefone': r.get('Telefone', ''),
                'cidade': r.get('Cidade', ''),
                'imobiliaria': r.get('Imobiliaria', r.get('Nome', '')),
                'msg1': r.get('Msg1', ''),
            })

with CHECK_OUT.open('w', encoding='utf-8') as f:
    f.write(f'Checklist de envio — Avaliação de Preço — {TODAY}\n')
    f.write('='*60 + '\n')
    f.write(f'Leads prontos: {len(rows)}\n')
    f.write(f'WhatsApp: {len(wa_rows)}\n')
    f.write(f'E-mail: {len(email_rows)}\n')
    f.write('\nArquivos gerados:\n')
    f.write(f'- {BREVO_OUT}\n')
    f.write(f'- {WA_OUT}\n')
    f.write(f'- {CHECK_OUT}\n')
    f.write('\nCTAs padrão:\n')
    f.write('- E-mail: comercial@praia.digital\n')
    f.write('- WhatsApp: (11) 95434-6288\n')

print(f'Pronto: {len(rows)} leads')
print(f'WhatsApp CSV: {WA_OUT}')
print(f'E-mail CSV: {BREVO_OUT}')
print(f'Checklist: {CHECK_OUT}')
