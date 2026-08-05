# Manual Operacional — Deploy no Render
**Repositório:** https://github.com/acarolmourad-commits/praia-digital  
**Branch:** main  
**Config:** `render.yaml`

---

## Passo 1 — Criar serviço
1. Abra https://dashboard.render.com
2. Clique em **New +** → **Web Service**
3. Selecione o repositório `praia-digital`
4. Branch: `main`
5. Runtime: **Python 3**
6. Build command: `pip install -r academy/requirements.txt`
7. Start command: `cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Plano: Starter ou Free

## Passo 2 — Variáveis de ambiente
Adicione no painel **Environment**:

```
DATABASE_URL=postgresql://academy:<senha>@<host>:5432/academy
SECRET_KEY=<chave_gerada>
SMTP_HOST=smtp.seudominio.com
SMTP_PORT=587
SMTP_USER=no-reply@praia.digital
SMTP_PASSWORD=<senha_smtp>
EMAIL_FROM=no-reply@praia.digital
ALLOWED_ORIGINS=https://praia.digital,https://www.praia.digital,https://academy.praia.digital
APP_ENV=production
```

> Dica: o `DATABASE_URL` pode vir automaticamente se você já criou um PostgreSQL antes no Render.

## Passo 3 — Banco PostgreSQL (se ainda não criou)
1. No Render: **New +** → **PostgreSQL**
2. Nome: `academy-db`
3. Database: `academy`
4. User: `academy`
5. Após criado, copie a **Connection String**
6. Cole no campo `DATABASE_URL` do Web Service

## Passo 4 — Deploy
1. Clique em **Create Web Service**
2. Aguarde o build terminar
3. O Render fornece uma URL pública temporária, ex:
   `https://praia-digital-academy.onrender.com`

## Passo 5 — Teste pós-deploy
Abra no navegador:
- `https://praia-digital-academy.onrender.com/health`
- `https://praia-digital-academy.onrender.com/auth/login`
- `https://praia-digital-academy.onrender.com/education/aluno/login.html`

Tudo deve responder 200.

## Passo 6 — Domínio customizado
1. No serviço criado: **Settings** → **Custom Domains**
2. Adicione `academy.praia.digital`
3. Atualize o DNS do seu domínio para apontar para o Render
4. SSL/HTTPS é automático no Render

## Observações
- CORS já está configurado para `praia.digital`
- SECRET_KEY é obrigatória em produção
- SMTP pode ficar vazio temporariamente
- O frontend do aluno é servido pelo FastAPI em `/education/aluno/`
- Para ver logs: **Logs** no painel do Render

## Comando local alternativo
`run_local.bat` para testar localmente sem o Render.
