#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador automático de relatório diário de prospecção.
Lê docs/sales/followup-registro.md e gera painel HTML resumo.
"""

import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE)
TRACKER = os.path.join(ROOT, 'docs', 'sales', 'followup-registro.md')
RESPONDERS = os.path.join(ROOT, 'docs', 'sales', 'respostas-leads.csv')
TODAY = datetime.now().strftime('%Y-%m-%d')
OUTPUT = os.path.join(ROOT, 'docs', 'sales', f'relatorio-diario-outbound-{TODAY}.html')
FOLLOWUP_SCRIPT = 'scripts/automation/followup_auto_gatilho_resposta.py'
PENDING_SCRIPT = 'scripts/automation/gerar_convite_demo_15min.py'
NEXT_STEPS = [
    'Enviar follow-up de D3 para leads que inicializam contato hoje',
    'Rodar followup_auto_gatilho_resposta para leads com resposta',
    'Enviar convites de demo para respostas de interesse alto'
]


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
    today_label = datetime.now().strftime('%d/%m/%Y %H:%M')
    counts = {'email': 0, 'whatsapp': 0, 'parceria': 0, 'venda': 0, 'teste': 0}
    for r in rows:
        counts[r['canal'].lower()] = counts.get(r['canal'].lower(), 0) + 1
        counts[r['tipo'].lower()] = counts.get(r['tipo'].lower(), 0) + 1

    responder_lines = []
    responder_count = 0
    if os.path.exists(RESPONDERS):
        responder_lines.append('<h2>Respostas recebidas</h2><table><tr><th>Nome</th><th>Empresa</th><th>Cidade</th><th>Resposta</th></tr>')
        for line in open(RESPONDERS, 'r', encoding='utf-8').read().splitlines()[1:]:
            if not line.strip() or line.strip().startswith('#'):
                continue
            parts = [p.strip() for p in line.split(';')]
            if len(parts) < 4:
                continue
            responder_count += 1
            responder_lines.append(f"<tr><td>{parts[0]}</td><td>{parts[1]}</td><td>{parts[2]}</td><td>{parts[3]}</td></tr>")
        responder_lines.append('</table>')
    else:
        responder_lines.append('<h2>Respostas recebidas</h2><p>Nenhuma resposta registrada em <code>respostas-leads.csv</code>.</p>')

    enc = 'UTF-8'
    followup_block = f''.join([
        '<h2>Ações sugeridas hoje</h2><ol>',
        ''.join([f'<li>{s}</li>' for s in NEXT_STEPS]),
        f'<li>Executar: <code>{FOLLOWUP_SCRIPT}</code> se houver respostas.</li>',
        f'<li>Executar: <code>{PENDING_SCRIPT}</code> para respostas de interesse alto.</li>',
        '</ol>'
    ])

    lines = [
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Relatório Diário Outbound</title>',
        '<style>body{font-family:Arial,sans-serif;background:#f6f8fb;color:#222;margin:0;padding:20px}',
        '.card{background:#fff;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,.08)}',
        'h1{font-size:22px;margin:0 0 12px}h2{font-size:16px;margin:18px 0 8px}pre{background:#f1f3f6;padding:14px;border-radius:8px;overflow:auto}',
        'ul{line-height:1.8}code{background:#eef2ff;padding:6px 10px;border-radius:8px;border:1px solid #d4d7f7}',
        'table{width:100%;border-collapse:collapse}th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}th{background:#f3f4f6}',
        '</style></head><body>',
        f'<div class="card"><h1>Relatório Diário — Prospecção Praia Digital</h1><p>Gerado em {today_label}</p>',
        f'<p>Processing date: <strong>{TODAY}</strong></p>',
        f'<p>Total de leads no tracker: <strong>{len(rows)}</strong></p>',
    ]
    if responder_count:
        lines.append(f'<p>Respostas pendentes: <strong>{responder_count}</strong></p>')
    lines.append('<h2>Resumo</h2><ul>')
    for k, v in counts.items():
        if v:
            lines.append(f'<li>{k}: {v}</li>')
    lines.append('</ul>')

    lines.append(followup_block)
    lines.append('<h2>Detalhamento</h2><table><tr><th>Nome</th><th>Imobiliária</th><th>Canal</th><th>Tipo</th><th>D0</th><th>D3</th><th>D7</th></tr>')
    for r in rows[:200]:
        lines.append(f"<tr><td>{r['nome']}</td><td>{r['imobiliaria']}</td><td>{r['canal']}</td><td>{r['tipo']}</td><td>{r['d0']}</td><td>{r['d3']}</td><td>{r['d7']}</td></tr>")
    lines.append('</table>')
    if len(rows) > 200:
        lines.append(f'<p>Mostrando 200 de {len(rows)} registros no detalhamento.</p>')
    lines.extend(['<p>Próxima atualização sugerida: amanhã às 08h.</p>', '<h2>Respostas recebidas</h2>'])
    lines.extend(responder_lines)
    lines.append('<p>Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a> | Ferramentas: <a href="https://praia.digital">praia.digital</a></p>')
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
