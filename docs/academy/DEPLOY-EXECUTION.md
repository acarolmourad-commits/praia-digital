# Deploy Academy — Execução prática

## Objetivo
Colocar a Academy em produção com os 64 cursos PRONTO_PARA_VENDA e validar o caminho comercial.

## Provedores suportados
- Railway: `railway.json`
- Render: `render.yaml`

Ambos já estão com `PYTHONPATH=academy` no startCommand.

## Pré-requisito humano
Preencher no provedor as variáveis de ambiente obrigatórias. Somente humano pode definir:
- `DATABASE_URL`
- `SECRET_KEY`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
- `EMAIL_FROM`
- `PAYMENT_GATEWAY`
- `PAYMENT_SECRET`
- `PAYMENT_WEBHOOK_PATH`
- `BASE_URL`
- `ALLOWED_ORIGINS`
- `MERCADOPAGO_TOKEN`
- `MERCADOPAGO_PUBLIC_KEY`
- `WHATSAPP_API_URL`, `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `WHATSAPP_TO_NUMBER`

## Sequência recomendada
1. Aplicar variáveis no provedor
2. Deploy/Redeploy
3. Esperar `/health` retornar 200
4. Rodar migrations/setup do banco
5. Seed dos 64 cursos aprovados
6. Validação pós-deploy

## Validação pós-deploy
- `/health`
- `/courses`
- Checkout real por slug
- Webhook público acessível
- E-mail transacional enviado
- `education/auditoria-final.json` coerente com banco

## Observações
Não subir SQLite em produção; usar banco gerenciado pelo provedor.
Confirmar que `academy.db` local não é usado em produção.
