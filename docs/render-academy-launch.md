# Launch — Praia Digital Academy no Render

Pré-requisito: `python scripts/pre_deploy_check.py` já passou neste repo.

## 1) Crie o banco
- Dashboard: **New** → **PostgreSQL**
- Nome: `academy-db`
- Região: preferencialmente mesma do Web Service
- Copie a connection string interna; o Render vai vinculá-la como `DATABASE_URL` no passo 2

## 2) Crie o Web Service
- **New** → **Web Service**
- Repo: `acarolmourad-commits/praia-digital`
- Branch: `main`
- Nome: `praia-digital-academy`
- Runtime: `Python 3`
- Build command:
  ```bash
  pip install -r academy/requirements.txt
  ```
- Start command:
  ```bash
  cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

## 3) Variáveis de ambiente
Use como base `academy/.env.production.example`.

Obrigatórias para produção:
- `DATABASE_URL`: deixe o Render preencher via vinculo com `academy-db`
- `SECRET_KEY`: gere no Render (`generateValue: true` ou gere uma forte)
- `BASE_URL`: `https://academy.praia.digital`
- `ALLOWED_ORIGINS`: `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`

Opcionais/seguir com integrações:
- SMTP: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_FROM`
- Pagamentos: `MERCADOPAGO_API_URL`, `MERCADOPAGO_TOKEN`, `MERCADOPAGO_PUBLIC_KEY`
- WhatsApp: `WHATSAPP_API_URL`, `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_TO_NUMBER`

## 4) Domínio
- Adicione custom domain: `academy.praia.digital`
- Siga o DNS/verificação indicado pelo Render

## 5) Validação pós-deploy
```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
python scripts/frontend_health_check.py --base https://praia.digital --wait 30
```

Checar manualmente:
- `https://academy.praia.digital/health`
- `https://academy.praia.digital/auth/login`
- `https://academy.praia.digital/auth/register`
- `https://academy.praia.digital/checkout/status`

## 6) Rollback
- Se algo falhar, reverta para o último deploy bom pelo dashboard do Render.
- Este repo está em `main`; use tags se quiser marcar releases.

## Notas rápidas
- Não comitar segredos.
- `main` é o deploy efetivo.
- Frontend atual já aponta para `https://academy.praia.digital` via checkout/docs.
