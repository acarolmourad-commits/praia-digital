#!/usr/bin/env python3
\"\"\"Follow-up seguro para 2 leads novos, sem repetir contatos.\"\"\"
import csv
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'
REG = BASE / 'docs/sales/followup-registro.md'

def contacts_done():
    if not REG.exists():
        return set()
    txt = REG.read_text(encoding='utf-8')
    return {line.split('|')[1].strip() for line in txt.splitlines() if '|' in line and 'ID' not in line}

def next_two():
    with open(CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    done = contacts_done()
    fresh = sorted([r for r in rows if r['id'] not in done], key=lambda r: int(r.get('pontuacao_lead', 0)), reverse=True)[:2]
    return fresh

if __name__ == '__main__':
    leads = next_two()
    print('TARGETS', len(leads))
    for r in leads:
        print(r['id'], r['nome_da_imobiliaria'], r['cidade'], r['email'])
