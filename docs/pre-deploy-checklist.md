# Pré-Deploy Checklist — Praia Digital Academy
Execute antes de abrir o Render para garantir deploy limpo.

## Repositório
- [x] Código no GitHub: `acarolmourad-commits/praia-digital`, branch `main`
- [x] Último commit: `acec54e`
- [x] Sem arquivos grandes indevidos no histórico

## Backend
- [x] `academy/main.py` com routers: auth, courses, academy, payments, admin, recommendations, automation, automation_whatsapp, certificates
- [x] `academy/requirements.txt` com `fpdf==1.7.2`
- [x] Banco configurado para SQLite (dev) e PostgreSQL (produção)
- [x] CORS configurável via `ALLOWED_ORIGINS`
- [x] SECRET_KEY obrigatória em produção

## Frontend
- [x] `/education/index.html` — hub Academy
- [x] `/education/vendas.html` — página de vendas
- [x] `/education/cursos/index.html` — catálogo
- [x] `/education/checkout.html` — checkout unificado
- [x] `/education/aluno/` — dashboard, login, player, admin
- [x] SEO técnico em 97 páginas: title, description, canonical, OG, schema, robots, preconnect
- [x] 24 páginas de bairro com SEO local
- [x] CTAs de compra em todas as páginas de curso

## Marketing
- [x] 64 cursos com `kit-completo.md`
- [x] 64 cursos com `instagram-posts.md`
- [x] 64 cursos com `meta-ads.md`
- [x] 494 variantes de marketing por cidade

## Deploy
- [x] `render.yaml` configurado
- [x] `docs/quick-deploy.md` com passo a passo
- [x] `docs/manual-render.md` com manual operacional
- [x] `docs/deploy-render.md` com guia de deploy
- [x] `scripts/check_academy_deploy.py` — sanity check pós-deploy
- [x] `academy/run_local.bat` — execução local Windows

## Testes
- [x] Fase 1: health, auth, courses
- [x] Fase 2: cart, checkout, payments, webhook, enrollment
- [x] Fase 3: frontend student area
- [x] Fase 4: admin panel, email service
- [x] Fase 5: recommendations, automation
- [x] Checkout público testado
- [x] Certificado PDF testado

## Variáveis de ambiente necessárias no Render
```
DATABASE_URL=postgresql://academy:<senha>@<host>:5432/academy
SECRET_KEY=<gere-uma-chave-forte>
SMTP_HOST=smtp.seudominio.com
SMTP_PORT=587
SMTP_USER=no-reply@praia.digital
SMTP_PASSWORD=<senha-smtp>
EMAIL_FROM=no-reply@praia.digital
ALLOWED_ORIGINS=https://praia.digital,https://www.praia.digital,https://academy.praia.digital
APP_ENV=production
```

## Comandos úteis
```bash
# Local
python academy/tests/test_phase1.py
python academy/tests/test_phase2.py
python academy/tests/test_phase3.py
python academy/tests/test_phase4.py
python academy/tests/test_phase5.py

# Deploy check
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
```

## Contatos
- Render: https://render.com/support
- Domínio: registro.br ou provedor DNS
- GitHub: https://github.com/acarolmourad-commits/praia-digital
