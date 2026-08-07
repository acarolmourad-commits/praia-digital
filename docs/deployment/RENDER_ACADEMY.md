# Render deploy checklist — Academy

## 1) Repo
- Conectar repo: `acarolmourad-commits/praia-digital`
- Branch para deploy: `main`

## 2) Serviço web
- Nome: `praia-digital-academy`
- Runtime: `python`
- Build command: `pip install -r academy/requirements.txt`
- Start command: `PYTHONPATH=academy uvicorn academy.main:app --host 0.0.0.0 --port $PORT`
- Auto-deploy: `on`

## 3) Banco
- Criar banco `academy-db`
- Usar como `DATABASE_URL` (Render faz o bind automaticamente via `fromDatabase`)

## 4) Env vars
Preencher no Render, pois no YAML estão vazias:

| variavel | valor recomendado |
|---|---|
| `DATABASE_URL` | usar `fromDatabase` |
| `SECRET_KEY` | gerar segredo forte |
| `SMTP_HOST` | smtp do dominio |
| `SMTP_PORT` | 587 |
| `SMTP_USER` | no-reply@praia.digital |
| `SMTP_PASSWORD` | senha do e-mail |
| `EMAIL_FROM` | no-reply@praia.digital |
| `APP_ENV` | production |
| `ALLOWED_ORIGINS` | https://praia.digital,https://www.praia.digital,https://academy.praia.digital |
| `MERCADOPAGO_TOKEN` | token Mercado Pago |
| `MERCADOPAGO_PUBLIC_KEY` | public key MP |
| `BASE_URL` | https://academy.praia.digital |
| `WHATSAPP_API_URL` | URL do provedor WhatsApp |
| `WHATSAPP_TOKEN` | token WhatsApp |
| `WHATSAPP_PHONE_ID` | phone ID |
| `WHATSAPP_TO_NUMBER` | numero destino |

## 5) Validacao apos deploy
- `GET https://academy.praia.digital/health` -> `{"status":"ok","service":"academy-api"}`
- `GET https://academy.praia.digital/docs` -> Swagger UI
- `POST https://academy.praia.digital/auth/register` -> cria usuario
- `GET https://academy.praia.digital/admin/leads` -> 401 esperado sem auth

## 6) Observabilidade
- Verificar logs do primeiro build no Render
- Se houver falha no start, checar env vars e `DATABASE_URL`
