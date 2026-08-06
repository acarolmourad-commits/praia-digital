# Deploy Readiness — Praia Digital Academy

Status atual
- Repo: `acarolmourad-commits/praia-digital`, branch `main`
- Backend: testado localmente; Fases 1-5 + leads OK
- Produção: **aguardando criação do Web Service no Render**

Comites pendentes / enviados
- `2cb5beb` fix(academy): tratar token JWT inválido em get_current_user
- `9508b95` chore(deploy): ajustar BASE_URL para `https://academy.praia.digital`
- `b4d2e0c` feat(education): melhorar página de vendas do curso 65

O que já está no repo
- `render.yaml` com build/start/database/env vars
- `academy/.env.example`
- `academy/.env.production.example`
- `scripts/deploy_render.bat`
- `scripts/check_academy_deploy.py`
- `scripts/frontend_health_check.py`

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
   - `ALLOWED_ORIGINS`: `https://praia.digital,https://www.praia.digital,https://academy.praia.digital`
   - `BASE_URL`: `https://academy.praia.digital`
   - `EMAIL_FROM`: `no-reply@praia.digital`
   - Demais: `SMTP_*`, `MERCADOPAGO_*`, `WHATSAPP_*`
5. DNS: `academy.praia.digital` → URL do Web Service
6. Pós-deploy:
   - `python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30`
   - `python scripts/frontend_health_check.py --base https://praia.digital --wait 30`

Critérios de sucesso
- `/health` retorna `{"status":"ok","service":"academy-api"}`
- `/docs` acessível
- `/auth/register` retorna token
- `/monitoring/status` retorna checks
- Frontend em `praia.digital` com 200 em rotas principais
