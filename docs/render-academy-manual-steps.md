# Deploy — Praia Digital Academy no Render

Status atual: **pronto para configurar manualmente no Render**
Pré-condições validadas: `python scripts/pre_deploy_check.py` → PASSED

## Passo a passo rápido

1. Abra: https://dashboard.render.com/web/new
2. Tipo: **Web Service**
3. Repo: `acarolmourad-commits/praia-digital`
4. Branch: `main`
5. Nome: `academy-api`
6. Runtime: `Python 3`
7. Build command:
   ```
   pip install -r academy/requirements.txt
   ```
8. Start command:
   ```
   cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
9. Banco de dados: **Add PostgreSQL**
   - Nome: `academy-db`
   - Vincule como `DATABASE_URL`
10. Variáveis de ambiente: copie de `academy/.env.production.example`
    - `SECRET_KEY`, `SMTP_*`, `EMAIL_FROM`, `ALLOWED_ORIGINS`
    - `MERCADOPAGO_*`, `WHATSAPP_*`, `BASE_URL=https://academy.praia.digital`
    - `DATABASE_URL` preenchida pelo Render ao criar o Postgres
11. Custom domain: `academy.praia.digital`
    - Siga a instrução do Render para DNS/verificação

## Validação pós-deploy

```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
python scripts/frontend_health_check.py --base https://praia.digital --wait 30
```

## Rollback

- Se algo falhar, reverta para o último deploy bom pelo dashboard do Render.

## Notas

- Não comitar segredos; usar variáveis de ambiente.
- Branch `main` é o deploy efetivo.
- Após o deploy, confirme se `/health`, `/auth/login`, `/auth/register` e `/checkout/status` retornam `200`.
