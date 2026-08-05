# Ativação Pós-Deploy — Academy
Use este checklist após criar o Web Service no Render.

## 1. Variáveis mínimas obrigatórias
- `DATABASE_URL`
- `SECRET_KEY`
- `EMAIL_FROM`
- `BASE_URL`
- `ALLOWED_ORIGINS`

## 2. Para pagamentos funcionarem
- `MERCADOPAGO_TOKEN`
- `MERCADOPAGO_PUBLIC_KEY`
- Testar preferência: usar o script `scripts/test_mercadopago.py` ou `.bat`

## 3. Para notificações funcionarem
- `WHATSAPP_API_URL`
- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_ID`
- `WHATSAPP_TO_NUMBER`
- Rotas esperadas:
  - `POST /automation/whatsapp-notify/{enrollment_id}`
  - `POST /automation/whatsapp-payment-confirmed/{enrollment_id}`
  - `POST /automation/whatsapp-certificate/{enrollment_id}`

## 3.1. Leads e automação
- `POST /leads`
- `POST /leads/{lead_id}/events`
- `POST /automation/email-confirmation/{enrollment_id}`

## 4. Validação final
- `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30`
- `python scripts/frontend_health_check.py --base https://praia.digital --wait 30`
- `python scripts/post_deploy_sanity_check.bat`
