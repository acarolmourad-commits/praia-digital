#!/usr/bin/env python3
"""
Valida conexão SMTP sem enviar e-mails.
Uso: python scripts/automation/validar_smtp.py
"""
import os, sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

BASE = Path("C:/Users/Carolina/praia-digital")
ENV_PATH = BASE / ".env"
load_dotenv(dotenv_path=ENV_PATH)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("SMTP_FROM", SMTP_USER)

def main():
    print("== Validação SMTP ==")
    print(f"Servidor: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"Usuário: {SMTP_USER}")
    print(f"From: {FROM_EMAIL}")

    missing = []
    if not SMTP_SERVER:
        missing.append("SMTP_SERVER")
    if not SMTP_PORT:
        missing.append("SMTP_PORT")
    if not SMTP_USER:
        missing.append("SMTP_USER")
    if not SMTP_PASSWORD:
        missing.append("SMTP_PASSWORD")
    if not FROM_EMAIL:
        missing.append("SMTP_FROM")

    if missing:
        print(f"\n[ERRO] Campos faltando no .env: {', '.join(missing)}")
        sys.exit(1)

    import smtplib
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            print("\n[OK] Login SMTP realizado com sucesso!")
            print("Credenciais válidas. Pronto para enviar e-mails.")
    except Exception as e:
        print(f"\n[ERRO] Falha na autenticação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
