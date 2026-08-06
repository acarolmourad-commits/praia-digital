# Deploy Manual — Praia Digital Academy no Render

Use este checklist para concluir o deploy no dashboard do Render.

## 1. Criar Web Service
- Repo: `acarolmourad-commits/praia-digital`
- Branch: `main`
- Nome sugerido: `academy-api`
- Runtime: `Python 3`
- Build command: `pip install -r academy/requirements.txt`
- Start command: `cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT`

## 2. Banco de dados
- Criar PostgreSQL nomeado `academy-db`
- Vincular ao Web Service como `DATABASE_URL`

## 3. Variáveis de ambiente
- `SECRET_KEY` = chave forte
- `SMTP_HOST` = host SMTP
- `SMTP_PORT` = porta SMTP
- `SMTP_USER` = usuário SMTP
- `SMTP_PASSWORD` = senha SMTP
- `EMAIL_FROM` = `no-reply@praia.digital`
- `ALLOWED_ORIGINS` = `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`
- `MERCADOPAGO_API_URL` = `https://api.mercadopago.com/v1`
- `MERCADOPAGO_TOKEN` = token do Mercado Pago
- `MERCADOPAGO_PUBLIC_KEY` = chave pública do Mercado Pago
- `WHATSAPP_API_URL` = URL da API WhatsApp
- `WHATSAPP_TOKEN` = token WhatsApp
- `WHATSAPP_PHONE_ID` = phone id
- `WHATSAPP_TO_NUMBER` = número destino
- `BASE_URL` = `https://academy.praia.digital`

## 4. Domínio
- Custom domain: `academy.praia.digital`
- Ajustar DNS conforme instrução do Render

## 5. Validação pós-deploy
- `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30`
- `python scripts/frontend_health_check.py --base https://praia.digital --wait 30`

## 6. Rollback rápido
- Se algo falhar, volte para o último deploy bom pelo dashboard do Render.
