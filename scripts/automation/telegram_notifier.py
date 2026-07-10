#!/usr/bin/env python3
"""Envia notificaçoes no Telegram para follow-ups e respostas."""
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Instale requests: pip install requests")
    sys.exit(1)

BASE = Path(r'C:\Users\Carolina\praia-digital')
URL = "https://api.telegram.org/bot{token}/sendMessage"


def send(token: str, chat_id: str, text: str):
    if not token or not chat_id:
        print("Missing token or chat_id")
        return
    requests.post(URL.format(token=token), json={"chat_id": chat_id, "text": text})


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("Defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID")
        return
    send(token, chat_id, "Notificacao Praia Digital: follow-ups e respostas ativos.")


if __name__ == '__main__':
    main()
