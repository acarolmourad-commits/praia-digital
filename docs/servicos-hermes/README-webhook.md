# Serviços Hermes — Arquitetura de Pagamento e Webhook

## Visão geral
Página pública de venda de serviços Hermes (`/servicos-hermes.html`) com checkout Stripe via payment links e confirmação pós-pagamento.

## Fluxo
1. Usuário clica em "Pagar no Stripe" em um dos planos.
2. Stripe Checkout abre com o item referente ao serviço.
3. Após pagamento aprovado, o usuário é redirecionado para:
   `https://praia.digital/servicos-hermes.html?status=success`
4. A página exibe um banner de confirmação amigável.

## Backend / Webhook
- Endpoint: `POST https://academy.praia.digital/academy/payments/webhook`
- Evento inscrito: `checkout.session.completed`
- Segredo de assinatura: `STRIPE_SECRET` armazenado no `.env` local.
- Código responsável: `academy/core/payments/webhooks.py`
- Router: `academy/routers/payments.py`

## Variáveis de ambiente
- `STRIPE_SECRET_KEY` — chave secreta da conta Stripe.
- `STRIPE_SECRET` — segredo de assinatura do webhook do Stripe.

## Segurança
- O arquivo `.env` está ignorado pelo `.gitignore` e não deve ser commitado.
- Os links de checkout são públicos; dados sensíveis não são expostos no frontend.

## Status
- Página: `https://praia.digital/servicos-hermes.html`
- Links Stripe: `buy.stripe.com/...` válidos e testados via API.
- Webhook Stripe: configurado via API.
