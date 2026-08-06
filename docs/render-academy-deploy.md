# Deploy — Praia Digital Academy no Render

## Pré-requisitos
- Repo: `acarolmourad-commits/praia-digital`
- Branch: `main`
- Domínio: `academy.praia.digital`
- Banco: PostgreSQL `academy-db`

## Passo a passo
1. No Render, crie um novo **Web Service** a partir do repo acima, branch `main`.
2. Crie/ligue um banco PostgreSQL chamado `academy-db` e vincule como `DATABASE_URL`.
3. Em **Environment Variables**, adicione:
   - `SECRET_KEY` = chave forte
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
   - `EMAIL_FROM` = `no-reply@praia.digital`
   - `ALLOWED_ORIGINS` = `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`
   - `MERCADOPAGO_TOKEN`, `MERCADOPAGO_PUBLIC_KEY`
   - `WHATSAPP_API_URL`, `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_TO_NUMBER`
   - `BASE_URL` = `https://academy.praia.digital`
4. Em **Custom Domains**, adicione `academy.praia.digital` e aponte o DNS.
5. Valide:
   - `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30`
   - `python scripts/frontend_health_check.py --base https://praia.digital --wait 30`

## Comandos locais úteis
- Testes: `PYTHONPATH=. python academy/tests/test_phase1.py`
- Build check: `python scripts/frontend_health_check.py --base https://praia.digital --wait 0`
- Env check: `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 0`
