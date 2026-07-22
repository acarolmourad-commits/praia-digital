#!/usr/bin/env python3
"""
relatorio_performance_b2b.py
Gera relatório de performance dos lotes B2B do dia.
Uso: python scripts/automation/relatorio_performance_b2b.py
"""
import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
OUT = BASE / 'docs' / 'sales' / f'relatorio-performance-b2b-{date.today().isoformat()}.html'

# Lotes a medir
lotes = {
    'Automacao': FOLDER / 'lote-b2b-automacao-2026-07-22.csv',
    'Captacao': FOLDER / 'lote-b2b-captacao-2026-07-22.csv',
}

resumo = []
for servico, path in lotes.items():
    if not path.exists():
        continue
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    total = len(rows)
    enviados = sum(1 for r in rows if (r.get('Status') or '').startswith('enviado'))
    respostas = sum(1 for r in rows if (r.get('Resposta') or '').strip())
    fechados = sum(1 for r in rows if 'fechado' in (r.get('Status') or '').lower())
    valores = []
    for r in rows:
        v = r.get('Valor_Estimado', '').strip()
        if v and v.startswith('R$'):
            try:
                valores.append(float(v.replace('R$', '').replace('.', '').replace(',', '.')))
            except ValueError:
                pass
    valor_total = sum(valores)
    resumo.append((servico, total, enviados, respostas, fechados, valor_total))

# HTML
lines = [
    '<!DOCTYPE html>',
    '<html lang="pt-BR">',
    '<head>',
    '  <meta charset="UTF-8">',
    '  <title>Relatório de Performance B2B — Litoral SP | Praia Digital</title>',
    '  <style>',
    '    body{font-family:system-ui;background:#f8fafc;color:#0f172a;padding:18px}',
    '    .wrap{max-width:1100px;margin:0 auto}',
    '    .card{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:18px;margin:14px 0}',
    '    table{width:100%;border-collapse:collapse;font-size:13px}',
    '    th{background:#eef2ff;color:#0a58ca;text-align:left;padding:8px;border-bottom:1px solid #e5e7eb}',
    '    td{padding:8px;border-bottom:1px solid #f1f5f9}',
    '    .ok{color:#047857;font-weight:700}',
    '  </style>',
    '</head>',
    '<body>',
    '  <div class="wrap">',
    '    <div class="card">',
    f'      <h1 style="font-size:20px;font-weight:900;margin:6px 0">Relatório de Performance B2B — {date.today().isoformat()}</h1>',
    '      <p style="color:#475569;margin-top:6px">Métricas consolidadas dos lotes de serviços da Praia Digital.</p>',
    '    </div>',
    '    <div class="card">',
    '      <table>',
    '        <tr><th>Serviço</th><th>Leads</th><th>Enviados</th><th>Respostas</th><th>Fechados</th><th>Valor estimado</th></tr>',
]

for servico, total, enviados, respostas, fechados, valor_total in resumo:
    lines.append(f'        <tr><td>{servico}</td><td>{total}</td><td>{enviados}</td><td class="ok">{respostas}</td><td>{fechados}</td><td>R$ {valor_total:,.2f}</td></tr>')

lines += [
    '      </table>',
    '    </div>',
    '  </div>',
    '</body>',
    '</html>',
]

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'Relatório gerado: {OUT}')
for servico, total, enviados, respostas, fechados, valor_total in resumo:
    print(f' - {servico}: {total} leads, {enviados} enviados, {respostas} respostas, {fechados} fechados, R$ {valor_total:,.2f}')
