# Render Academy — passo a passo executável

1. Abra https://dashboard.render.com/new
2. Conecte o GitHub repo `acarolmourad-commits/praia-digital` na branch `main`
3. Crie um serviço `Web Service` com:
   - name: `praia-digital-academy`
   - runtime: `Python`
   - build: `pip install -r academy/requirements.txt`
   - start: `PYTHONPATH=academy uvicorn academy.main:app --host 0.0.0.0 --port $PORT`
   - auto-deploy: `on`
4. Crie um `PostgreSQL`:
   - name: `academy-db`
   - db: `academy`
   - user: `academy`
5. Vincule `academy-db` em `praia-digital-academy` como `DATABASE_URL`
6. Preencha env vars restantes (existem placeholders no render.yaml):
   - `SECRET_KEY`
   - `SMTP_HOST`
   - `SMTP_USER`
   - `SMTP_PASSWORD`
   - `MERCADOPAGO_TOKEN`
   - `MERCADOPAGO_PUBLIC_KEY`
   - `WHATSAPP_API_URL`
   - `WHATSAPP_TOKEN`
   - `WHATSAPP_PHONE_ID`
   - `WHATSAPP_TO_NUMBER`
7. Deploy -> validar:
   - `GET /health`
   - `GET /docs`
   - `POST /auth/register`
