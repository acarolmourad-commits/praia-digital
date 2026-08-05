# Quick Deploy — Praia Digital Academy no Render
**Tempo estimado:** 5 minutos

---

## 1. Abrir o Render
Acesse https://dashboard.render.com e faça login.

## 2. Novo Web Service
1. Clique em **New +** → **Web Service**
2. Selecione o repositório `praia-digital`
3. Branch: `main`
4. Runtime: **Python 3**
5. Build command: `pip install -r academy/requirements.txt`
6. Start command: `cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Plano: **Starter** (ou Free para teste)

## 3. Variáveis de ambiente
Adicione **todas** estas variáveis no painel **Environment**:

```
DATABASE_URL=postgresql://academy:<senha>@<host>:5432/academy
SECRET_KEY=<gere-uma-chave-forte-aqui>
SMTP_HOST=smtp.seudominio.com
SMTP_PORT=587
SMTP_USER=no-reply@praia.digital
SMTP_PASSWORD=<senha-smtp>
EMAIL_FROM=no-reply@praia.digital
ALLOWED_ORIGINS=https://praia.digital,https://www.praia.digital,https://academy.praia.digital
APP_ENV=production
```

> **Importante:** gere o `SECRET_KEY` com `python -c "import secrets; print(secrets.token_urlsafe(32))"`

## 4. Banco de dados
1. No Render: **New +** → **PostgreSQL**
2. Nome: `academy-db`
3. Database: `academy`
4. User: `academy`
5. Após criado, copie a **Connection String**
6. Cole no campo `DATABASE_URL` do Web Service

## 5. Deploy
1. Clique em **Create Web Service**
2. Aguarde 2-3 minutos
3. O Render fornece uma URL pública, ex: `https://praia-digital-academy.onrender.com`

## 6. Teste rápido
Abra no navegador:
- `https://praia-digital-academy.onrender.com/health` → deve retornar `{"status":"ok"}`
- `https://praia-digital-academy.onrender.com/education/index.html` → hub da Academy
- `https://praia-digital-academy.onrender.com/education/cursos/index.html` → catálogo

## 7. Domínio customizado
1. No serviço: **Settings** → **Custom Domains**
2. Adicione `academy.praia.digital`
3. Atualize o DNS do seu domínio para apontar para o Render
4. SSL/HTTPS é automático

## 8. Validar
```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
```

---

**Pronto!** A Academy estará no ar.
