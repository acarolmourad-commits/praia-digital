#!/usr/bin/env python3
"""Gera follow-up personalizado para lead silencioso a partir do CSV mestre."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'csv-lotes-email' / 'lote-mestre-unificado-2026-07-10.csv'
OUT = BASE / 'docs' / 'sales' / 'followup-lead-silencioso-2026.md'


def main():
    hoje = datetime.now().strftime('%Y-%m-%d')
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    lines = [f'# Follow-up para leads silenciosos — {hoje}', '']
    for i, r in enumerate(rows[:10], 1):
        nome = r.get('nome', '').strip() or 'Lead'
        cidade = r.get('cidade', '').strip() or 'litoral'
        lines.append(f'## Lead {i}: {nome} ({cidade})')
        lines.append('')
        lines.append('Assunto: Um dado rápido sobre captação no litoral')
        lines.append('')
        lines.append(f'Olá, {nome},')
        lines.append('')
        lines.append('Sou Carolina Mourad, CEO da Praia Digital. Vi que você ainda não retornou sobre a parceria.')
        lines.append('')
        lines.append(f'Deixo um dado curto: em {cidade}, captações com SEO local e follow-up automático costumam gerar mais leads qualificados em até 30 dias.')
        lines.append('')
        lines.append('Se quiser, posso enviar um exemplo rápido por aqui ou agendar 15 minutos.')
        lines.append('')
        lines.append('Até breve,')
        lines.append('Carolina Mourad')
        lines.append('(11) 95434-6288')
        lines.append('https://praia.digital')
        lines.append('')
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'GENERATED {OUT}')


if __name__ == '__main__':
    main()
