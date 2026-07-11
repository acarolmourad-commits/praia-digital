#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automático de relatório diário de prospecção.
Lê docs/sales/followup-registro.md e gera painel HTML resumo.
"""

import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACKER = os.path.join(ROOT, 'docs/sales/followup-registro.md')
OUTPUT = os.path.join(ROOT, 'docs/sales/relatorio-diario-outbound.html')


def parse_tracker():
    rows = []
    if not os.path.exists(TRACKER):
        return rows
    for line in open(TRACKER, 'r', encoding='utf-8').read().splitlines():
        if not line.strip().startswith('|'):
            continue
        parts = [p.strip() for p in line.strip().split('|')]
        if len(parts) < 7:
            continue
        rows.append({
            'nome': parts[1],
            'imobiliaria': parts[2],
            'canal': parts[3],
            'tipo': parts[4],
            'd0': parts[5],
            'd3': parts[6],
            'd7': parts[7] if len(parts) > 7 else '',
        })
    return rows


def build_report(rows):
    today = datetime.now().strftime('%d/%m/%Y %H:%M')
    counts = {'email': 0, 'whatsapp': 0, 'parceria': 0, 'venda': 0, 'teste': 0}
    for r in rows:
        counts[r['canal'].lower()] = counts.get(r['canal'].lower(), 0) + 1
        counts[r['tipo'].lower()] = counts.get(r['tipo'].lower(), 0) + 1

    lines = [
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Relatório Diário Outbound</title>',
        '<style>body{font-family:Arial,sans-serif;background:#f6f8fb;color:#222;margin:0;padding:20px}',
        '.card{background:#fff;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.08)}',
        'h1{font-size:22px;margin:0 0 12px}h2{font-size:16px;margin:18px 0 8px}',
        'pre{background:#f1f3f6;padding:14px;border-radius:8px;overflow:auto}',
        'table{width:100%;border-collapse:collapse}th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}th{background:#f3f4f6}'
        '</style></head><body>',
        f'<div class="card"><h1>Relatório Diário — Prospecção Praia Digital</h1><p>Gerado em {today}</p>'
        f'<p>Total de leads no tracker: <strong>{len(rows)}</strong></p>'
    ]

    lines.append('<h2>Resumo</h2><ul>')
    for k, v in counts.items():
        if v:
            lines.append(f'<li>{k}: {v}</li>')
    lines.append('</ul>')

    lines.append('<h2>Detalhamento</h2><table><tr><th>Nome</th><th>Imobiliária</th><th>Canal</th><th>Tipo</th><th>D0</th><th>D3</th><th>D7</th></tr>')
    for r in rows:
        lines.append(f"<tr><td>{r['nome']}</td><td>{r['imobiliaria']}</td><td>{r['canal']}</td><td>{r['tipo']}</td><td>{r['d0']}</td><td>{r['d3']}</td><td>{r['d7']}</td></tr>")
    lines.append('</table>')
    lines.append('<p>Próxima atualização sugerida: amanhã às 08h.</p>')
    lines.append('</div></body></html>')
    return '\n'.join(lines)


def main():
    rows = parse_tracker()
    report = build_report(rows)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'Relatório gerado: {OUTPUT}')
    print(f'Leads no tracker: {len(rows)}')


if __name__ == '__main__':
    main()
