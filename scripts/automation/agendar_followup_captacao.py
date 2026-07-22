#!/usr/bin/env python3
"""
agendar_followup_captacao.py
Gera follow-ups automáticos para o lote de captação digital.
Uso: python scripts/automation/agendar_followup_captacao.py
"""
import csv
from pathlib import Path
from datetime import date, timedelta

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
TODAY = date.today().isoformat()

SOURCE = FOLDER / 'lote-b2b-captacao-2026-07-22.csv'
FOLLOWUP_OUT = FOLDER / 'followup-pairs-captacao-2026-07-22.csv'
TRACKER_OUT = FOLDER / 'tracker-captacao-2026-07-22.csv'

with SOURCE.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

followup_rows = []
tracker_rows = []
for r in rows:
    nome = (r.get('Nome') or '').strip()
    cidade = (r.get('Cidade') or '').strip()
    telefone = (r.get('Telefone') or '').strip()
    imobiliaria = (r.get('Imobiliaria') or nome).strip()
    if not nome or not telefone:
        continue
    base_q1 = date.fromisoformat('2026-07-22')
    q1 = base_q1.strftime('%Y-%m-%d') + ' 09:00'
    q2 = (base_q1 + timedelta(days=2)).strftime('%Y-%m-%d') + ' 09:00'
    q3 = (base_q1 + timedelta(days=5)).strftime('%Y-%m-%d') + ' 09:00'
    msg1 = f"Olá {nome}! Aqui é da Praia Digital. Queremos ajudar a captar imóveis qualificados em {cidade}. Posso enviar um exemplo rápido?"
    msg2 = f"Olá {nome}! Segue um exemplo prático de captação para {cidade}. Se curtir, a gente detalha o plano."
    msg3 = f"Olá {nome}! Para não insistir: quando for a melhor hora para captar imóveis, avise que abro o plano."
    followup_rows.append({
        'Lote': 'captacao',
        'Nome': nome,
        'Telefone': telefone,
        'Cidade': cidade,
        'Data_Msg1': q1,
        'Status': 'pendente_q1',
        'Resposta': '',
        'Valor_Estimado': r.get('Valor_Estimado', ''),
        'Obs': r.get('Obs', ''),
        'Acao_Conversao': '',
        'Msg1': msg1,
        'Msg2': msg2,
        'Msg3': msg3,
        'Email': r.get('Email', 'comercial@praia.digital'),
        'Imobiliaria': imobiliaria,
    })
    tracker_rows.append({
        'Lote': 'captacao',
        'Nome': nome,
        'Telefone': telefone,
        'Cidade': cidade,
        'Data_Msg1': q1,
        'Status': 'pendente_q1',
        'Resposta': '',
        'Valor_Estimado': r.get('Valor_Estimado', ''),
        'Obs': r.get('Obs', ''),
        'Acao_Conversao': '',
        'Msg1': msg1,
        'Msg2': msg2,
        'Msg3': msg3,
        'Email': r.get('Email', 'comercial@praia.digital'),
        'Imobiliaria': imobiliaria,
    })

with FOLLOWUP_OUT.open('w', newline='', encoding='utf-8') as f:
    fieldnames = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']
    wr = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    wr.writeheader()
    wr.writerows(followup_rows)

with TRACKER_OUT.open('w', newline='', encoding='utf-8') as f:
    fieldnames = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']
    wr = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    wr.writeheader()
    wr.writerows(tracker_rows)

print(f'Pares: {FOLLOWUP_OUT}')
print(f'Tracker: {TRACKER_OUT}')
print(f'Total leads: {len(followup_rows)}')
print('Status final:')
print(f' - pendente_q1: {len(followup_rows)}')
