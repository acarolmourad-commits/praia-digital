# Variáveis de Ambiente — Academy no Render

## Obrigatórias em produção
- `DATABASE_URL`: fornecida automaticamente pelo Render ao criar o PostgreSQL `academy-db`
- `SECRET_KEY`: chave forte usada pelo JWT. Gere com `python -c "import secrets; print(secrets.token_urlsafe(64))"`
- `APP_ENV`: `production`
- `BASE_URL`: `https://academy.praia.digital`
- `EMAIL_FROM`: `no-reply@praia.digital`
- `ALLOWED_ORIGINS`: `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`

## SMTP
- `SMTP_HOST`: ex. `smtp.seudominio.com`
- `SMTP_PORT`: `587`
- `SMTP_USER`: usuário SMTP
- `SMTP_PASSWORD`: senha/app password

## Mercado Pago
- `MERCADOPAGO_TOKEN`: access token
- `MERCADOPAGO_PUBLIC_KEY`: public key

## WhatsApp Cloud
- `WHATSAPP_API_URL`: `https://graph.facebook.com/v19.0`
- `WHATSAPP_TOKEN`: token da API
- `WHATSAPP_PHONE_ID`: phone id
- `WHATSAPP_TO_NUMBER`: número destino no formato internacional

## Observações
- Não comitar segredos no repositório.
- `render.yaml` já referencia `fromDatabase` para `DATABASE_URL`.
- `.env.production.example` é o arquivo de referência local.
