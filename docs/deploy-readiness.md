# Deploy Readiness — Praia Digital Academy

Status atual
- Repo: `acarolmourad-commits/praia-digital`, branch `main`
- Backend: testado localmente; Fases 1-5 + leads OK
- Produção: **aguardando criação/configuração manual no Render**

Commits recentes enviados em `main`
- `2130bba` fix(academy): permitir checkout público e alinhar BASE_URL
- `25e7b27` fix(education): melhorar UX do checkout e integração com API Academy
- `0ae560f` docs(deploy): atualizar status do deploy da Academy no Render
- `3331362` fix(academy): evitar fallback localhost no BASE_URL
- `1e6df83` docs(deploy): atualizar checklist de deploy
- `307c613` feat(content): melhorar hubs GEO das cidades
- `eb36907` chore(scripts): adicionar amostragem de validação de páginas de cidade
- `1e0c20a` fix(content): normalizar markup em Guarujá academia e corrigir artefato em Bertioga
- `d021031` fix(content): normalizar SEO, schema e acentos em páginas de cidades
- `831cb31` fix(content): normalizar SEO, schema e acentos em todas as páginas de cidades
- `8549148` fix(content): remover título genérico "Guia do Litoral de SP" em cidades
- `3207342` chore(scripts): tornar validação de docs de deploy case-insensitive

O que já está no repo
- `academy/core/security.py` com `get_current_user_optional`
- `academy/routers/payments.py` com checkout público
- `academy/.env.example`
- `academy/.env.production.example`
- `render.yaml`
- `docs/render-academy-manual-steps.md`
- `docs/render-academy-deploy.md`
- `docs/deploy-readiness.md`
- `scripts/deploy_render.bat`
- `scripts/check_academy_deploy.py`
- `scripts/frontend_health_check.py`
- `scripts/check_deploy_docs.py`
- `scripts/wait_for_academy.py`

Passo manual restante
1. Abra https://dashboard.render.com
2. New + Web Service
   - Repo: `acarolmourad-commits/praia-digital`
   - Branch: `main`
   - Build command: `pip install -r academy/requirements.txt`
   - Start command: `cd academy && uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Banco: crie/ative `academy-db` e vincule como `DATABASE_URL`
4. Variáveis de ambiente mínimas:
   - `SECRET_KEY`: chave forte
   - `SMTP_*`: credenciais SMTP
   - `EMAIL_FROM`: `no-reply@praia.digital`
   - `ALLOWED_ORIGINS`: `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`
   - `MERCADOPAGO_*`: credenciais Mercado Pago
   - `WHATSAPP_*`: credenciais WhatsApp
   - `BASE_URL`: `https://academy.praia.digital`
5. DNS: `academy.praia.digital` → URL do Web Service
6. Pós-deploy:
   - `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30`
   - `python scripts/frontend_health_check.py --base https://praia.digital --wait 30`
   - `python scripts/check_deploy_docs.py`

Critérios de sucesso
- `/health` retorna `{"status":"ok","service":"academy-api"}`
- `/docs` acessível
- `/auth/register` retorna token
- `/monitoring/status` retorna checks
- Frontend em `praia.digital` com 200 em rotas principais
