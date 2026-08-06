# Praia Digital Academy — Deploy Readiness

## Status
- Fases 1 a 5 validadas localmente.
- Servidor de teste rodou em `http://127.0.0.1:8000`.
- Endpoint `/health` retornou `{"status":"ok","service":"academy-api"}`.
- Fluxo público testado: registro, login, criação de lead.

## Endpoints essenciais
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `POST /leads`
- `POST /leads/{lead_id}/events`
- `GET /admin/leads`
- `GET /admin/leads/{lead_id}/events`
- `PATCH /admin/leads/{lead_id}/status`
- `POST /academy/checkout`
- `POST /academy/payments/{payment_id}/webhook`
- `POST /automation/email-lead-magnet/{lead_id}`

## Variáveis obrigatórias no Render
- `DATABASE_URL`
- `SECRET_KEY`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `APP_ENV=production`
- `ALLOWED_ORIGINS`
- `MERCADOPAGO_TOKEN`
- `MERCADOPAGO_PUBLIC_KEY`
- `BASE_URL=https://academy.praia.digital`
- `WHATSAPP_API_URL`
- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_ID`
- `WHATSAPP_TO_NUMBER`

## Próxima ação
- Criar Web Service no Render com build/start do `render.yaml`.
- Ajustar DNS para `academy.praia.digital`.
- Validar `/health` em produção.
