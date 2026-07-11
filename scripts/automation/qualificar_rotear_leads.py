#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qualificador e roteador automático de leads.
Classifica respostas e sugere próxima ação comercial com base em regras simples.
"""

import os, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACKER = os.path.join(ROOT, 'docs/sales/followup-registro.md')
OUT = os.path.join(ROOT, 'docs/sales/qualificacao-roteamento-leads.md')


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


def classify(text):
    t = text.lower()
    if any(k in t for k in ['interessado', 'demo', 'demonstração', 'horário', 'agendar']):
        return 'quente', 'Agendar demo de 15min e enviar proposta comercial'
    if any(k in t for k in ['orçamento', 'preço', 'valor', 'quanto custa']):
        return 'morno', 'Enviar proposta comercial + follow-up em 24h'
    if any(k in t for k in ['já tenho', 'não agora', 'depois']):
        return 'frio', 'Follow-up curto em 7d com case relevante'
    return 'novo', 'Enviar first contact e agendar follow-up em 72h'


def build(rows):
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    lines = ['# Qualificação e Roteamento de Leads\n', f'Gerado em {today}\n']
    for r in rows:
        exemplo_resposta = ''  # aqui poderíamos ler respostas reais
        bucket, acao = classify(exemplo_resposta or r['tipo'])
        lines.append(f"## {r['nome']} — {r['imobiliaria']}")
        lines.append(f"- Canal: {r['canal']}")
        lines.append(f"- Tipo: {r['tipo']}")
        lines.append(f"- Classificação: **{bucket}**")
        lines.append(f"- Próxima ação: {acao}")
        lines.append('')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Relatório gerado: {OUT}')


def main():
    rows = read_tracker()
    build(rows)


if __name__ == '__main__':
    main()
