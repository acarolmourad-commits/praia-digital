#!/usr/bin/env python3
"""
preparar_trackers_performance.py
Refaça os trackers e gere relatório consolidado com placeholders prontos para atualização manual.
Uso: python scripts/automation/preparar_trackers_performance.py
"""
import csv
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
TODAY = date.today().isoformat()

services = {
    'Automacao': 'automacao',
    'Captacao': 'captacao',
    'Solucao Proptech': 'proptech',
    'Descricao Imoveis': 'descricao',
    'SEO Local': 'seo-local',
    'Consultoria': 'consultoria',
    'Avaliacao Preco': 'avaliacao',
}

for nome, kw in services.items():
    tracker_path = FOLDER / f'tracker-{kw}-2026-07-22.csv'
    if not tracker_path.exists():
        continue
    with tracker_path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    for r in rows:
        r['Resposta'] = ''
        r['Status'] = r.get('Status', 'pendente_msg1')
        r['Acao_Conversao'] = r.get('Acao_Conversao', '')
        r['Valor_Estimado'] = r.get('Valor_Estimado', '')
    fields = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']
    with tracker_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    print(f'reset tracker {nome}: {len(rows)} leads')

print('Concluido.')
