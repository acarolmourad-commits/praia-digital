#!/usr/bin/env python3
"""
enviar_emails_automatico.py
Envia e-mails personalizados em lote para leads da Praia Digital.
Uso: python scripts/automation/enviar_emails_automatico.py
"""

import csv
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Configurações SMTP (preencher com dados reais antes de usar)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "seu-email@gmail.com"
SMTP_PASSWORD = "sua-senha-app"
FROM_NAME = "Carolina Mourad"
FROM_EMAIL = "comercial@praia.digital"

# Caminhos
BASE = Path(__file__).resolve().parents[2]
LEADS_CSV = BASE / "docs/sales/leads-litoral-enriquecido.csv"
TRACKER_CSV = BASE / "docs/sales/tracker_envios.csv"
LOG_CSV = BASE / "docs/sales/log_envios.csv"


def load_leads(path):
    leads = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def build_email(to_name, to_email, city, imovel_url, tool_url):
    subject = f"Ferramentas gratuitas e parceria para imobiliária em {city}"
    body = f"""Olá {to_name},

tudo bem?

A Praia Digital criou ferramentas gratuitas para corretores no litoral paulista:
- página profissional por imóvel
- SEO local
- follow-up automático
- assistente virtual para compradores

Exemplo prático: {imovel_url}

Também pode ser útil: {tool_url}

Quer testar sem custo inicial?

Abraço,
{FROM_NAME} | Praia Digital
https://praia.digital
"""
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg, subject


def send_batch(limit=10):
    leads = load_leads(LEADS_CSV)[:limit]
    results = []
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        for lead in leads:
            msg, subject = build_email(
                lead.get("nome", "Parceiro"),
                lead.get("email", ""),
                lead.get("cidade", "litoral"),
                lead.get("imovel_url", ""),
                "https://praia.digital",
            )
            try:
                server.sendmail(FROM_EMAIL, lead.get("email", ""), msg.as_string())
                status = "enviado"
            except Exception as e:
                status = f"erro: {e}"
            results.append(
                {
                    "data": datetime.now().isoformat(),
                    "lead": lead.get("nome"),
                    "email": lead.get("email"),
                    "cidade": lead.get("cidade"),
                    "subject": subject,
                    "status": status,
                }
            )
            time.sleep(1)
    return results


if __name__ == "__main__":
    print("Enviando lote de e-mails...")
    results = send_batch(limit=10)
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        if LOG_CSV.stat().st_size == 0:
            writer.writeheader()
        writer.writerows(results)
    print(f"Concluído. {len(results)} e-mails processados.")
