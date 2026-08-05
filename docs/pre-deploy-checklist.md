# Pré-Deploy Checklist — Praia Digital Academy
Execute antes de abrir o Render para garantir deploy limpo.

## Repositório
- [x] Código no GitHub: `acarolmourad-commits/praia-digital`, branch `main`
- [x] Sem alterações não commitadas
- [x] `.gitignore` cobre arquivos gerados

## Backend Academy
- [x] `render.yaml` atualizado
- [x] `academy/.env.example` com variáveis de produção
- [x] `academy/core/config.py` carregando variáveis
- [x] `academy/requirements.txt` com `requests==2.32.3` e `fpdf==1.7.2`
- [x] Roteadores registrados em `academy/main.py`:
  - auth, courses, academy, admin
  - payments (checkout público)
  - automation_whatsapp
  - certificates
  - recommendations
  - monitoring
- [x] Endpoints prontos:
  - `/health`
  - `/monitoring/status`
  - `/auth/register`
  - `/payments/checkout`
  - `/payments/checkout/status`
  - `/payments/mercadopago/webhook`
  - `/automation/whatsapp-notify/{enrollment_id}`

## Frontend
- [x] `education/index.html`
- [x] `education/vendas.html`
- [x] `education/cursos/index.html`
- [x] `education/checkout.html`
- [x] `education/aluno/index.html`
- [x] `education/aluno/login.html`
- [x] 64 páginas de curso com SEO técnico
- [x] CTAs “Comprar agora” em páginas de curso
- [x] 24 páginas de SEO local por bairro
- [x] Schema.org aplicado

## Deploy docs
- [x] `docs/deploy-render.md`
- [x] `docs/deploy-summary.md`
- [x] `docs/quick-deploy.md`
- [x] `docs/monitoramento-pos-deploy.md`
- [x] `docs/pre-deploy-checklist.md`
- [x] `scripts/check_academy_deploy.py`
- [x] `scripts/frontend_health_check.py`
- [x] `scripts/validate_render_deploy.py`
- [x] `scripts/generate_production_env.py`
- [x] `scripts/deploy_render.bat`
- [x] `scripts/test_mercadopago.bat`
- [x] `scripts/test_mercadopago.py`
