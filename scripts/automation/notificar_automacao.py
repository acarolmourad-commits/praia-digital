#!/usr/bin/env python3
"""
notificar_automacao.py
Checa o CSV de leads do dia do serviço de automação e envia alerta no Telegram.
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
URL = "https://api.telegram.org/bot{token}/sendMessage"


def read_csv(path):
    rows = []
    if not path.exists():
        return rows
    with path.open(newline='', encoding='utf-8') as f:
        head = f.readline()
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(line)
    return rows


def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    if not token or not chat_id:
        print('Defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID')
        return
    rows = read_csv(FILE)
    total = len(rows)
    if total == 0:
        text = f'Automação: sem leads novos em {TODAY_STR}.'
    else:
        text = f'Automação: {total} leads registrados hoje no lote de automação para imobiliárias.'
    requests.post(URL.format(token=token), json={'chat_id': chat_id, 'text': text})
    print(text)


if __name__ == '__main__':
    main()
