# 🚀 Deploy Checklist — Academy Backend no Render

## Status atual
- Backend: Fases 1-5 validadas localmente
- Testes: 4/4 passaram
- Pré-deploy: PASSED
- Config: `render.yaml` + `academy/.env.production.example` prontos
- **Bloqueio atual:** deploy manual no Render não executado

---

## 1. Pré-requisitos
- [ ] Conta no Render com acesso ao repo `praia-digital`
- [ ] Domínio `academy.praia.digital` apontando para Render (DNS)
- [ ] Banco PostgreSQL criado no Render (nome: `academy-db`)

---

## 2. Configurar banco de dados
1. No Render Dashboard → **New** → **PostgreSQL**
2. Nome: `academy-db`
3. Plano: Free/Starter (para teste)
4. Após criação, copiar a `connectionString` (formato: `postgresql://user:pass@host:5432/academy`)

---

## 3. Deploy do serviço web
1. No Render Dashboard → **New** → **Web Service**
2. Conectar repo: `acarolmourad-commits/praia-digital`
3. Branch: `main`
4. Nome: `praia-digital-academy`
5. Runtime: **Python 3**
6. Build command: `pip install -r academy/requirements.txt`
7. Start command: `cd academy && PYTHONPATH=. uvicorn academy.main:app --host 0.0.0.0 --port $PORT`

---

## 4. Variáveis de ambiente
Preencher no Render Dashboard → **Environment**:

| Key | Value | Observação |
|-----|-------|-----------|
| `DATABASE_URL` | (from database) | Auto-populated se o banco estiver no mesmo Render |
| `SECRET_KEY` | Gerar valor forte | `generateValue: true` no render.yaml |
| `SMTP_HOST` | `smtp.seudominio.com` | Ajustar para provedor real |
| `SMTP_PORT` | `587` | |
| `SMTP_USER` | `no-reply@praia.digital` | |
| `SMTP_PASSWORD` | `<SECRET_c29f77ec>aDigital2026` | Senha real do e-mail |
| `EMAIL_FROM` | `no-reply@praia.digital` | |
| `ALLOWED_ORIGINS` | `https://praia.digital,https://www.praia.digital,https://academy.praia.digital` | |
| `MERCADOPAGO_TOKEN` | (vazio por enquanto) | Preencher após integração |
| `MERCADOPAGO_PUBLIC_KEY` | (vazio por enquanto) | Preencher após integração |
| `BASE_URL` | `https://academy.praia.digital` | |
| `WHATSAPP_API_URL` | (vazio por enquanto) | Preencher após integração |
| `WHATSAPP_TOKEN` | (vazio por enquanto) | Preencher após integração |
| `WHATSAPP_PHONE_ID` | (vazio por enquanto) | Preencher após integração |
| `WHATSAPP_TO_NUMBER` | (vazio por enquanto) | Preencher após integração |

---

## 5. Verificações pós-deploy
- [ ] `GET https://academy.praia.digital/` → 200 OK
- [ ] `GET https://academy.praia.digital/health` → `{"status":"ok"}`
- [ ] `POST https://academy.praia.digital/leads` com payload de teste → 200 + JSON
- [ ] Testar checkout público: `POST https://academy.praia.digital/checkout/public`
- [ ] Verificar logs no Render: sem erros de import/migração

---

## 6. Migrações do banco
Após deploy bem-sucedido:
```bash
# Opção A: via Render Shell
render shell praia-digital-academy
cd academy && PYTHONPATH=. python -m alembic upgrade head

# Opção B: localmente com DATABASE_URL de produção
export DATABASE_URL="postgresql://user:pass@host:5432/academy"
cd academy && PYTHONPATH=. python -m alembic upgrade head
```

---

## 7. Rollback
Se algo der errado:
1. Render Dashboard → **Deploys** → selecionar deploy anterior → **Rollback**
2. Ou forçar redeploy do commit `4c76621` (último estável)

---

## 8. Contatos
- Carolina: `comercial@praia.digital` / `(11) 95434-6288`
- Repo: https://github.com/acarolmourad-commits/praia-digital

---

**Última atualização:** 2026-08-07
**Branch:** `main`
**Commit atual:** `20dcb24`
