#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advance automático de negociação.
Sugere demo de 15min ou proposta comercial após resposta do lead, integrando tracking.
"""

import os, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACKER = os.path.join(ROOT, 'docs/sales/followup-registro.md')
OUT = os.path.join(ROOT, 'docs/sales/advance-negociacao-auto.md')


def read_tracker():
    rows = []
    if not os.path.exists(TRACKER):
        return rows
    for line in open(TRACKER, 'r', encoding='utf-8').read().splitlines():
        if not line.strip().startswith('|'):
            continue
        parts = [p.strip() for p in line.strip().split('|')]
        if len(parts) < 7:
            continue
        rows.append({'nome': parts[1], 'imobiliaria': parts[2], 'canal': parts[3], 'tipo': parts[4], 'd0': parts[5], 'd3': parts[6], 'd7': parts[7] if len(parts) > 7 else ''})
    return rows


def suggest(lead_type, reply_text=''):
    t = (lead_type + ' ' + reply_text).lower()
    if any(k in t for k in ['interessado', 'demo', 'demonstração', 'horário', 'agendar', 'sim']):
        return 'demo_15min', 'Agendar demonstração de 15 minutos e enviar kit de onboarding'
    if any(k in t for k in ['orçamento', 'preço', 'valor', 'quanto custa', 'proposta']):
        return 'proposta_comercial', 'Enviar proposta comercial padrão + follow-up em 24h'
    if any(k in t for k in ['já tenho', 'não agora', 'depois']):
        return 'followup_7d', 'Enviar follow-up curto em 7 dias com case local'
    return 'first_contact', 'Enviar first contact e follow-up em 72h'


def build(rows):
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    lines = ['# Advance Automático de Negociação\n', f'Gerado em {today}\n']
    for r in rows:
        bucket, acao = suggest(r['tipo'])
        lines.append(f"## {r['nome']} — {r['imobiliaria']}")
        lines.append(f"- Canal: {r['canal']}")
        lines.append(f"- Tipo: {r['tipo']}")
        lines.append(f"- Sugestão: **{bucket}**")
        lines.append(f"- Ação: {acao}")
        lines.append('')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Relatório gerado: {OUT}')


def main():
    rows = read_tracker()
    build(rows)


if __name__ == '__main__':
    main()
