#!/usr/bin/env python3
"""
agendar_followup_avaliacao.py
Gera follow-ups automáticos para o lote de Avaliação de Preço de Imóvel.
"""
import csv
from pathlib import Path
from datetime import date, timedelta

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
SOURCE = FOLDER / 'lote-b2b-avaliacao-2026-07-22.csv'
FOLLOWUP_OUT = FOLDER / 'followup-pairs-avaliacao-2026-07-22.csv'
TRACKER_OUT = FOLDER / 'tracker-avaliacao-2026-07-22.csv'

fields = ['Lote','Nome','Telefone','Cidade','Data_Msg1','Status','Resposta','Valor_Estimado','Obs','Acao_Conversao','Msg1','Msg2','Msg3','Email','Imobiliaria']

with SOURCE.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

followup_rows = []
for r in rows:
    nome = (r.get('Nome') or '').strip()
    cidade = (r.get('Cidade') or '').strip()
    telefone = (r.get('Telefone') or '').strip()
    imobiliaria = ((r.get('Imobiliaria') or r.get('Nome') or '').strip())
    if not nome or not telefone:
        continue
    base_q1 = date.fromisoformat('2026-07-22')
    q1 = base_q1.strftime('%Y-%m-%d') + ' 09:00'
    q2 = (base_q1 + timedelta(days=2)).strftime('%Y-%m-%d') + ' 09:00'
    q3 = (base_q1 + timedelta(days=5)).strftime('%Y-%m-%d') + ' 09:00'
    msg1 = f"Olá {nome}! Fazemos avaliação de preço de imóvel com IA para imobiliárias em {cidade}. Posso enviar um exemplo?"
    msg2 = f"Olá {nome}! Segue exemplo de avaliação de preço para {cidade}. Se curtir, detalhamos o investimento."
    msg3 = f"Olá {nome}! Quando quiser vender ou alunar com preço certo, avise que abro a proposta."
    followup_rows.append({
        'Lote': 'avaliacao',
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
    wr = csv.DictWriter(f, fieldnames=fields, delimiter=';')
    wr.writeheader()
    wr.writerows(followup_rows)
with TRACKER_OUT.open('w', newline='', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames=fields, delimiter=';')
    wr.writeheader()
    wr.writerows(followup_rows)

print(f'Pares: {FOLLOWUP_OUT}\nTracker: {TRACKER_OUT}\nTotal leads: {len(rows)}\nStatus final:\n - pendente_q1: {len(followup_rows)}')
