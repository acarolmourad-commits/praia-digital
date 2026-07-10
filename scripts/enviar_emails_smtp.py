import os, smtplib, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)

def enviar_emails(csv_path, assunto_template, corpo_template):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads = list(reader)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        for lead in leads:
            msg = MIMEMultipart()
            msg["From"] = FROM_EMAIL
            msg["To"] = lead["email"]
            msg["Subject"] = assunto_template.format(**lead)
            corpo = corpo_template.format(**lead)
            msg.attach(MIMEText(corpo, "plain", "utf-8"))
            server.send_message(msg)
            print(f"Enviado para {lead['nome']} <{lead['email']}>")

if __name__ == "__main__":
    import sys
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "csv-lotes-email/lote-envio-top5-2026-07-10.csv"
    assunto = "Parceria Praia Digital — {cidade}"
    corpo = "Olá {nome}, queremos fazer um piloto gratuito de IA para imobiliárias em {cidade}. 15min de call? comercial@praia.digital"
    enviar_emails(csv_path, assunto, corpo)
