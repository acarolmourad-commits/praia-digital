# Deploy — Resumo Final para Render
**Repositório:** `acarolmourad-commits/praia-digital`  
**Branch:** `main`  
**Último commit:** `b3a064b`

## Status atual
- `academy-db` criado e `available`
- Web Service `praia-digital-academy` pendente de criação no dashboard do Render
- Criação via API bloqueada por billing (`402 Payment Required`)

## Variáveis de ambiente necessárias no Render
```
DATABASE_URL=<connection string do academy-db>
SECRET_KEY=<gere-uma-chave-forte>
APP_ENV=production
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=no-reply@praia.digital
ALLOWED_ORIGINS=https://praia.digital,https://www.praia.digital,https://academy.praia.digital
MERCADOPAGO_TOKEN=
MERCADOPAGO_PUBLIC_KEY=
BASE_URL=https://academy.praia.digital
WHATSAPP_API_URL=
WHATSAPP_TOKEN=
WHATSAPP_PHONE_ID=
WHATSAPP_TO_NUMBER=
```

## Checklist pré-deploy
- [x] Código no GitHub
- [x] Sem arquivos grandes indevidos no histórico
- [x] `render.yaml` atualizado
- [x] `requirements.txt` com dependências essenciais
- [x] Banco `academy-db` criado e disponível
- [x] Sanity check atualizado

## Passo a passo no Render
1. Criar Web Service apontando para `acarolmourad-commits/praia-digital`, branch `main`
2. Vincular `DATABASE_URL` ao banco existente `academy-db`
3. Configurar variáveis de ambiente listadas acima
4. Deploy e validar `/health`, `/docs`, `/monitoring/status`, `/payments/checkout`
5. Configurar domínio customizado `academy.praia.digital`

## Pós-deploy
```bash
python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
```

## Próximos passos possíveis
1. Ativar billing no Render para criar/alterar serviços via API
2. Configurar Mercado Pago em produção
3. Configurar WhatsApp em produção
4. Monitoramento/alertas pós-deploy
