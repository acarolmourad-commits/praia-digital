#!/usr/bin/env python3
"""
notificar_vendas_b2b.py
Resumo diário B2B para Telegram, usando o mesmo padrão do notificar_automacao.py.
"""
import csv
import os
from pathlib import Path
from datetime import date

try:
    import requests
except ImportError:
    print("Instale requests: pip install requests")
    raise SystemExit(1)

BASE = Path(__file__).resolve().parents[2]
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
TODAY = date.today().isoformat()
URL = "https://api.telegram.org/bot{token}/sendMessage"

ENV_PATH = BASE / '.env'
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding='utf-8', errors='ignore').splitlines():
        line = line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            TELEGRAM_BOT_TOKEN = line.split('=', 1)[1].strip().strip('"').strip("'")
        elif line.startswith('TELEGRAM_CHAT_ID='):
            TELEGRAM_CHAT_ID = line.split('=', 1)[1].strip().strip('"').strip("'")

services = {
    'Automacao': 'automacao',
    'Captacao': 'captacao',
    'Solucao Proptech': 'proptech',
    'Descricao Imoveis': 'descricao',
    'SEO Local': 'seo-local',
    'Consultoria': 'consultoria',
    'Avaliacao Preco': 'avaliacao',
}

resumo = []
for nome, kw in services.items():
    tracker = FOLDER / f'tracker-{kw}-2026-07-22.csv'
    if not tracker.exists():
        continue
    with tracker.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    total = len(rows)
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
    resumo.append((nome, total, respostas, fechados, valor_total))

total_leads = sum(r[1] for r in resumo)
total_respostas = sum(r[2] for r in resumo)
total_fechados = sum(r[3] for r in resumo)
total_valor = sum(r[4] for r in resumo)

text = (
    f'📊 Vendas B2B — {TODAY}\n'
    f'Leads: {total_leads} | Respostas: {total_respostas} | Fechados: {total_fechados} | Valor estimado: R$ {total_valor:,.2f}\n'
)
for nome, total, respostas, fechados, valor_total in resumo:
    text += f'• {nome}: {total} leads, {respostas} respostas, {fechados} fechados, R$ {valor_total:,.2f}\n'

if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    try:
        requests.post(
            URL.format(token=TELEGRAM_BOT_TOKEN),
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': text},
            timeout=20,
        )
        print('Telegram: ok')
    except Exception as e:
        print(f'Telegram: falhou - {e}')
else:
    print('Telegram não configurado; seguindo apenas com log local.')

print(text)
