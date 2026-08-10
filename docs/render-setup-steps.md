# Setup Render — Academy passo a passo

## Pré-requisitos
- Acesso a https://dashboard.render.com
- Repositório: `acarolmourad-commits/praia-digital`
- Branch: `main`
- Domínio: `academy.praia.digital`

## 1) Criar PostgreSQL
1. Dashboard → **New +** → **PostgreSQL**
2. Nome: `academy-db`
3. Plano: teste/dev ou Starter
4. Após criar, copie a **Connection String**

## 2) Criar Web Service
1. Dashboard → **New +** → **Web Service**
2. Repo: `acarolmourad-commits/praia-digital`
3. Branch: `main`
4. Nome: `praia-digital-academy`
5. Environment: `Python 3`
6. Build command: `pip install -r academy/requirements.txt`
7. Start command: `cd academy && PYTHONPATH=academy uvicorn academy.main:app --host 0.0.0.0 --port $PORT`

## 3) Variáveis de ambiente
No Web Service → Environment, adicione:

| Chave | Valor |
|---|---|
| DATABASE_URL | connection string do PostgreSQL |
| SECRET_KEY | gere uma chave forte |
| APP_ENV | production |
| EMAIL_FROM | no-reply@praia.digital |
| ALLOWED_ORIGINS | https://praia.digital,https://www.praia.digital,https://academy.praia.digital |
| BASE_URL | https://academy.praia.digital |
| SMTP_HOST | smtp.seudominio.com |
| SMTP_PORT | 587 |
| SMTP_USER | usuário SMTP |
| SMTP_PASSWORD | senha SMTP |
| MERCADOPAGO_TOKEN | token MP |
| MERCADOPAGO_PUBLIC_KEY | public key MP |
| WHATSAPP_API_URL | https://graph.facebook.com/v19.0 |
| WHATSAPP_TOKEN | token WhatsApp |
| WHATSAPP_PHONE_ID | phone id |
| WHATSAPP_TO_NUMBER | número destino internacional |

## 4) Deploy
1. Clique em **Create Web Service**
2. Aguarde build/deploy
3. Teste a URL pública do Render: `/health`

## 5) DNS customizado
1. Web Service → Settings → Custom Domains
2. Adicione: `academy.praia.digital`
3. Siga o registro DNS indicado pelo Render

## 6) Pós-deploy
```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
python scripts/frontend_health_check.py --base https://praia.digital --wait 30
```
