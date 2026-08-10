# Deploy Amanhã — Academy no Render

Passo a passo exato para pessoa não técnica seguir amanhã. Use apenas valores que já existem neste projeto.

## O que você precisa antes de começar
- Acesso a https://dashboard.render.com
- Este repositório no GitHub: `acarolmourad-commits/praia-digital`
- Domínio `academy.praia.digital` já acessível para alterar DNS

---

## 1) Criar PostgreSQL no Render
1. Abra o Render → **New +** → **PostgreSQL**
2. Preencha:
   - **Name:** `academy-db`
   - **Database:** `academy`
   - **User:** `academy`
3. Clique em **Create Database**
4. Após criado, copie a **Connection String** (ex.: `postgresql://academy:senha@host:5432/academy`)

## 2) Criar Web Service no Render
1. Render → **New +** → **Web Service**
2. Em **Build and deploy from a Git repository**, selecione:
   - **Repo:** `praia-digital`
   - **Branch:** `main`
3. Preencha:
   - **Name:** `praia-digital-academy`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r academy/requirements.txt`
   - **Start Command:** `cd academy && PYTHONPATH=academy uvicorn academy.main:app --host 0.0.0.0 --port $PORT`
4. Clique em **Create Web Service**

## 3) Conectar DATABASE_URL
1. No Web Service criado → aba **Environment**
2. Em **Environment Variables**, adicione:
   - **Key:** `DATABASE_URL`
   - **Value:** cole a connection string do PostgreSQL do passo 1

## 4) Variáveis de ambiente obrigatórias
Ainda na aba **Environment**, adicione estas chaves com os valores abaixo. Use exatamente estes valores quando indicado:

| Chave | Valor exato |
|---|---|
| SECRET_KEY | gere uma chave forte no comando abaixo e cole aqui |
| APP_ENV | `production` |
| EMAIL_FROM | `no-reply@praia.digital` |
| ALLOWED_ORIGINS | `https://praia.digital,https://www.praia.digital,https://academy.praia.digital` |
| BASE_URL | `https://academy.praia.digital` |
| SMTP_HOST | `smtp.seudominio.com` |
| SMTP_PORT | `587` |
| SMTP_USER | usuário do seu e-mail SMTP |
| SMTP_PASSWORD | senha/app password do SMTP |
| MERCADOPAGO_TOKEN | seu access token do Mercado Pago |
| MERCADOPAGO_PUBLIC_KEY | sua public key do Mercado Pago |
| WHATSAPP_API_URL | `https://graph.facebook.com/v19.0` |
| WHATSAPP_TOKEN | token da API WhatsApp Cloud |
| WHATSAPP_PHONE_ID | phone id do WhatsApp Cloud |
| WHATSAPP_TO_NUMBER | número destino no formato internacional |

### Como gerar o SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 5) Deploy
1. No Web Service, clique em **Manual Deploy** se necessário
2. Aguarde o build terminar
3. Acesse a URL pública do Render no formato `https://praia-digital-academy.onrender.com`

## 6) Configurar domínio academy.praia.digital
1. No Web Service → **Settings** → **Custom Domains**
2. Adicione: `academy.praia.digital`
3. O Render mostrará um registro DNS. Atualize no seu provedor de DNS:
   - Tipo: `CNAME`
   - Nome: `academy`
   - Valor: o domínio `onrender.com` indicado pelo Render

## 7) Validação final
Depois de configurar o DNS, aguarde alguns minutos e execute:

```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
python scripts/frontend_health_check.py --base https://praia.digital --wait 30
```

Esperado:
- `/health` retorna `{"status":"ok"}`
- `/docs` acessível
- `/auth/register` e `/payments/checkout` retornam `200`
- Páginas de `/education/*` retornam `200`
- Frontend `praia.digital` com rotas principais OK

## Observações
- Se o build falhar por dependências, verifique se `academy/requirements.txt` foi instalado corretamente
- Se `/monitoring/status` retornar degraded, confira se `DATABASE_URL` está correta
- Não altere o código enquanto o deploy não estiver concluído
