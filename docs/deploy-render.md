# Deploy Manual — Render
**Repositório:** acarolmourad-commits/praia-digital  
**Branch:** main  
**Arquivo de configuração:** render.yaml

## Passo 1 — Acessar Render
1. Acesse https://render.com e faça login.
2. Clique em **New +** e escolha **Web Service**.
3. Em **Build and deploy from a Git repository**, selecione o repositório `praia-digital`.

## Passo 2 — Configurar Web Service
- **Name:** `praia-digital-academy`
- **Environment:** `Python 3`
- **Branch:** `main`
- **Build Command:** `pip install -r academy/requirements.txt`
- **Start Command:** `cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan:** Free ou Starter

## Passo 3 — Variáveis de ambiente
Adicione as variáveis abaixo na seção **Environment**:

| Chave | Valor |
|------|-------|
| DATABASE_URL | `postgresql://academy:<senha>@<host>:5432/academy` |
| SECRET_KEY | Valor secreto longo |
| SMTP_HOST | `smtp.seudominio.com` |
| SMTP_PORT | `587` |
| SMTP_USER | `no-reply@praia.digital` |
| SMTP_PASSWORD | senha do e-mail |
| EMAIL_FROM | `no-reply@praia.digital` |
| ALLOWED_ORIGINS | `https://praia.digital,https://www.praia.digital,https://academy.praia.digital` |

> Nota: o `DATABASE_URL` pode ser preenchido automaticamente se você criar um banco PostgreSQL no Render antes.

## Passo 4 — Banco de dados
1. No Render, clique em **New +** → **PostgreSQL**.
2. Nome: `academy-db`.
3. Após criado, copie a **Connection String**.
4. Cole no campo `DATABASE_URL` do Web Service.

## Passo 5 — Deploy
1. Clique em **Create Web Service**.
2. Aguarde o build e deploy.
3. Acesse a URL pública fornecida (ex: `https://praia-digital-academy.onrender.com`).
4. Teste o healthcheck: `https://praia-digital-academy.onrender.com/health`.

## Passo 6 — Domínio customizado
1. No serviço criado, vá em **Settings** → **Custom Domains**.
2. Adicione `academy.praia.digital`.
3. Atualize o DNS do seu domínio para apontar para o Render.

## Validação pós-deploy
- Healthcheck OK
- Login do aluno OK
- Páginas `/education/aluno/*` servidas
- Banco conectado
