# Checklist Operacional — Envio de E-mails

Quando quiser usar envio automático:
1. Edite `.env` com:
   - SMTP_SERVER=smtp.gmail.com
   - SMTP_PORT=587
   - SMTP_USER=seu-email@gmail.com
   - SMTP_PASSWORD=sua-senha-de-app
2. Execute: `python scripts/email_batch_sender.py`

Para envio manual imediato:
1. Abra o Brevo free: https://www.brevo.com
2. Importe `csv-lotes-email/checklist-envio-hoje-limpo.csv`
3. Crie campanha e cole os textos de `outreach/textos-email-captacao-mini-site.html`
4. Envie em horário comercial
