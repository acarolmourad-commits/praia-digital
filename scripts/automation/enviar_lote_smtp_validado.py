#!/usr/bin/env python3
"""
Valida e executa envio automático de e-mails via SMTP.
Uso:
  python scripts/automation/enviar_lote_smtp_validado.py [--csv CAMINHO_CSV] [--limit N]
"""
import os, sys, smtplib, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None

BASE = Path("C:/Users/Carolina/praia-digital")
DEFAULT_CSV = BASE / "csv-lotes-email/lote-20-com-mensagem-pronta-2026-07-11.csv"
ENV_PATH = BASE / ".env"

load_dotenv(dotenv_path=ENV_PATH)

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("SMTP_FROM", SMTP_USER)

def fail(msg):
    print(f"[ERRO] {msg}")
    sys.exit(1)

def main():
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL]):
        fail("Preencha SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD e SMTP_FROM no .env")

    csv_path = DEFAULT_CSV
    limit = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--csv" and i + 1 < len(args):
            csv_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    if not csv_path.exists():
        fail(f"CSV não encontrado: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        fail("CSV vazio")

    if limit:
        rows = rows[:limit]

    print(f"Enviando para {len(rows)} leads via {SMTP_SERVER}:{SMTP_PORT}")
    sent = 0
    errors = 0
    log = []

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        for r in rows:
            to_email = r.get("email", "").strip()
            nome = r.get("nome", "")
            assunto = r.get("assunto", "Parceria Praia Digital")
            corpo = r.get("mensagem", "")
            if not to_email or "@" not in to_email:
                errors += 1
                log.append((r.get("id", ""), to_email, "SKIP", "E-mail inválido"))
                continue

            try:
                msg = MIMEMultipart()
                msg["From"] = FROM_EMAIL
                msg["To"] = to_email
                msg["Subject"] = assunto
                msg.attach(MIMEText(corpo, "plain", "utf-8"))
                server.send_message(msg)
                sent += 1
                log.append((r.get("id", ""), to_email, "OK", ""))
                print(f"[OK] {r.get('id','')} -> {to_email}")
            except Exception as e:
                errors += 1
                log.append((r.get("id", ""), to_email, "ERRO", str(e)))
                print(f"[ERRO] {r.get('id','')} -> {to_email}: {e}")

    out_log = BASE / f"docs/sales/envio-smtp-log-{Path(csv_path).stem}-{os.getpid()}.csv"
    out_log.parent.mkdir(parents=True, exist_ok=True)
    with out_log.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "email", "status", "detalhe"])
        w.writerows(log)

    print(f"\nConcluído: {sent} enviados, {errors} erros.")
    print(f"Log: {out_log}")

if __name__ == "__main__":
    main()
