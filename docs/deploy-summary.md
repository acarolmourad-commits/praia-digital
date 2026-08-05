# Deploy — Resumo Final para Render
**Repositório:** `acarolmourad-commits/praia-digital`  
**Branch:** `main`  
**Último commit:** `c4cada7`

## Alterações entregues nesta sprint
- **Checkout público** em `academy/routers/payments.py`
  - cria pedido sem auth
  - integração stub com Mercado Pago
  - webhook `/payments/mercadopago/webhook`
  - status consultável em `/payments/checkout/status`
- **WhatsApp stub** em `academy/core/whatsapp_service.py`
  - rota `/automation/whatsapp-notify/{enrollment_id}`
- **Monitoring** em `academy/routers/monitoring.py`
  - endpoint `/monitoring/status` com saúde, contadores e integrações
- **Sanity check** atualizado em `scripts/check_academy_deploy.py`
  - valida health, frontend, register, monitoring e checkout público
- **Deploy docs** atualizados:
  - `docs/deploy-render.md` — variáveis de ambiente atualizadas
  - `render.yaml` — variáveis de ambiente atualizadas
  - `academy/.env.example` — variáveis de ambiente atualizadas
- **Frontend**:
  - `education/checkout.html` — checkout unificado
  - CTAs “Comprar agora” em 64 páginas de curso

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
MERCADOPAGO_TOKEN=<access-token>
MERCADOPAGO_PUBLIC_KEY=<public-key>
BASE_URL=https://academy.praia.digital
WHATSAPP_API_URL=https://graph.facebook.com/v19.0
WHATSAPP_TOKEN=<whatsapp-token>
WHATSAPP_PHONE_ID=<phone-id>
WHATSAPP_TO_NUMBER=<numero-destino>
```

## Checklist pré-deploy
- [x] Código no GitHub
- [x] Sem arquivos grandes indevidos no histórico
- [x] `render.yaml` atualizado com variáveis do Mercado Pago e WhatsApp
- [x] `requirements.txt` com `requests==2.32.3` e `fpdf==1.7.2`
- [x] Banco configurado para SQLite/PostgreSQL
- [x] Frontend com SEO técnico e CTAs
- [x] Sanity check atualizado

## Passo a passo no Render
1. Criar PostgreSQL no Render
2. Criar Web Service apontando para `acarolmourad-commits/praia-digital`, branch `main`
3. Configurar variáveis de ambiente
4. Conectar `DATABASE_URL` do PostgreSQL ao Web Service
5. Deploy e validar `/health`, `/docs`, `/monitoring/status`, `/payments/checkout`
6. Configurar domínio customizado `academy.praia.digital`
7. Atualizar `BASE_URL` para domínio final

## Pós-deploy
```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
```

## Próximos passos possíveis
1. Deploy manual no Render
2. Configurar Mercado Pago em produção
3. Configurar WhatsApp em produção
4. Monitoramento/alertas pós-deploy
