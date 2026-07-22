#!/usr/bin/env python3
"""
notificar_automacao.py
Checa o CSV de leads do dia do serviço de automação e envia alerta no Telegram.
Também registra evento em docs/sales/batch-sent-log.csv para rastreabilidade operacional.
Uso: python scripts/automation/notificar_automacao.py
"""
import os
import sys
from pathlib import Path
from datetime import date

try:
    import requests
except ImportError:
    print("Instale requests: pip install requests")
    sys.exit(1)

BASE = Path(r'C:\Users\Carolina\praia-digital')
FOLDER = BASE / 'docs' / 'sales' / 'csv-lotes-b2b'
TODAY_STR = date.today().isoformat()
FILE = FOLDER / f'lote-b2b-automacao-{TODAY_STR}.csv'
BATCH_LOG = BASE / 'docs/sales/batch-sent-log.csv'
URL = "https://api.telegram.org/bot{token}/sendMessage"

ENV_PATH = BASE / '.env'
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
if ENV_PATH.exists():
    for line in ENV_PATH.read_text(encoding='utf-8', errors='ignore').splitlines():
        line=line.strip()
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            TELEGRAM_BOT_TOKEN = line.split('=',1)[1].strip().strip('"').strip("'")
        elif line.startswith('TELEGRAM_CHAT_ID='):
            TELEGRAM_CHAT_ID = line.split('=',1)[1].strip().strip('"').strip("'")


def read_csv(path):
    rows = []
    if not path.exists():
        return rows
    with path.open(newline='', encoding='utf-8') as f:
        head = f.readline()
        for line in f:
            line=line.strip()
            if not line:
                continue
            rows.append(line)
    return rows


def append_batch_log(text):
    try:
        exists = BATCH_LOG.exists()
        with BATCH_LOG.open('a', newline='', encoding='utf-8') as f:
            if not exists:
                f.write('data;hora;servico;evento;detalhe\n')
            now = date.today().isoformat() + ' ' + date.today().strftime('%H:%M')
            f.write(f'{now};automacao;notificacao;{text}\n')
    except Exception:
        pass


def main():
    rows = read_csv(FILE)
    total = len(rows)
    if total == 0:
        text = f'Automação: sem leads novos em {TODAY_STR}.'
    else:
        text = f'Automação: {total} leads registrados hoje no lote de automação para imobiliárias.'
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            requests.post(URL.format(token=TELEGRAM_BOT_TOKEN), json={'chat_id': TELEGRAM_CHAT_ID, 'text': text})
            print('Telegram: ok')
        except Exception as e:
            print(f'Telegram: falhou - {e}')
    else:
        print('Telegram não configurado; seguindo apenas com log local.')
    append_batch_log(text)
    print(text)


if __name__ == '__main__':
    main()
