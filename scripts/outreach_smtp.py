#!/usr/bin/env python3
"""
Envio de e-mails de prospecção B2B via SMTP.
Uso:
  1. Edite este arquivo com credenciais reais e lista de leads.
  2. Execute: python scripts/outreach_smtp.py
"""

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
from pathlib import Path

# ----------------- CONFIGURAÇÃO -----------------
SMTP_HOST = ""  # ex: smtp.gmail.com, smtp.office365.com
SMTP_PORT = 587  # 587 para STARTTLS, 465 para SSL
EMAIL_FROM = ""  # ex: comercial@praia.digital
EMAIL_LOGIN = ""  # muitas vezes igual ao EMAIL_FROM
EMAIL_PASSWORD = ""  # app-password/senha SMTP
USE_SSL = False  # True para porta 465 com SSL
# -----------------------------------------------

LEADS_CSV = Path(__file__).resolve().parents[1] / "docs/sales/leads-litoral-enriquecido.csv"
SUBJECT_TEMPLATE = "Parceria B2B em IA para imóveis no litoral"
BODY_TEMPLATE = """Prezado(a),

Escrevo como CEO da Praia Digital com uma proposta de colaboração para {empresa} em {cidade}.

Somos a primeira plataforma do litoral paulista com IA aplicada a imóveis de praia. Hoje ajudamos empresas do setor a captar leads qualificados e fechar mais negócios, sem alterar o site atual.

Serviços em destaque:
• Chatbot de IA no site: atendimento 24/7 com qualificação automática
• Avaliação automática de imóvel com dados locais
• SEO local com conteúdo de IA por cidade/bairro
• Geração de anúncios para portais e temporada
• Relatórios mensais de mercado por bairro

Ferramentas gratuitas para validação prévia: https://praia.digital

Se fizer sentido, proponho uma demonstração de 20 minutos.

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288 | comercial@praia.digital
https://praia.digital
"""


def load_leads():
    with LEADS_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def build_msg(to_email, empresa, cidade):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = SUBJECT_TEMPLATE
    body = BODY_TEMPLATE.format(empresa=empresa or "sua operação", cidade=cidade or "o litoral paulista")
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def send_emails(limit=None):
    if not all([SMTP_HOST, EMAIL_FROM, EMAIL_LOGIN, EMAIL_PASSWORD]):
        raise SystemExit("Preencha SMTP_HOST, EMAIL_FROM, EMAIL_LOGIN e EMAIL_PASSWORD no script.")

    leads = load_leads()
    if limit:
        leads = leads[: int(limit)]

    smtp_cls = smtplib.SMTP_SSL if USE_SSL else smtplib.SMTP
    with smtp_cls(SMTP_HOST, SMTP_PORT) as server:
        if not USE_SSL:
            server.ehlo()
            server.starttls()
        server.login(EMAIL_LOGIN, EMAIL_PASSWORD)

        sent = 0
        for lead in leads:
            email_to = lead.get("email", "").strip()
            empresa = lead.get("nome_da_imobiliaria", "").strip()
            cidade = lead.get("cidade", "").strip()
            if not email_to:
                continue
            msg = build_msg(email_to, empresa, cidade)
            server.sendmail(EMAIL_FROM, [email_to], msg.as_string())
            sent += 1
            print(f"Enviado para {email_to} ({empresa})")
    print(f"Total enviado: {sent}")


if __name__ == "__main__":
    send_emails()
