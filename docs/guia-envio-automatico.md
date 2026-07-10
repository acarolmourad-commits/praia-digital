# Guia Rápido — Envio Automático de E-mails

## Passo 1: Configurar .env
Crie um arquivo `.env` na raiz do projeto com:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-de-app

## Passo 2: Executar envio
python scripts/enviar_emails_smtp.py csv-lotes-email/batch-30-emails-2026-07-10.csv

## Passo 3: Acompanhar
- Brevo: https://www.brevo.com
- Follow-up: docs/sales/followup-registro.md
- Templates: outreach/resposta-interesse-agendar-call.txt

## Observações
- Gmail: use senha de app, não senha normal
- Outlook: smtp.office365.com, porta 587
- Hotmail: smtp.live.com, porta 587
