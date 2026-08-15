# Pacote técnico de deploy — Academy

## Variáveis necessárias
Preencher no provedor; **não commitar segredos**.

- `SECRET_KEY`
- `DATABASE_URL`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `PAYMENT_GATEWAY`
- `PAYMENT_SECRET`
- `PAYMENT_WEBHOOK_PATH`
- `BASE_URL`
- `ALLOWED_ORIGINS`
- `MERCADOPAGO_TOKEN`
- `MERCADOPAGO_PUBLIC_KEY`
- `WHATSAPP_API_URL`
- `WHATSAPP_TOKEN`
- `WHATSAPP_PHONE_ID`
- `WHATSAPP_TO_NUMBER`

## URLs/domínios
- Produção: `https://academy.praia.digital`
- Checkout: `https://praia.digital/education/checkout.html`
- Webhook: `https://academy.praia.digital/academy/payments/webhook`

## Rotas críticas
- `/health`
- `/courses`
- `/academy/payments/webhook`
- `/education/cursos/<slug>/index.html`
- `/education/checkout.html`

## Checkout
- Usar `education/checkout.html?slug=<slug>&title=<nome>&price=<valor>`
- Confirmar botão de compra visível
- Confirmar sem mixed content

## Webhook
- Público e acessível
- Validar idempotência
- Confirmar eventos `approved`, `pending`, `rejected`

## Acesso do aluno
- Após pagamento aprovado → matrícula ativa
- Página do curso acessível somente para aluno matriculado
- Link direto sem login → sem acesso

## Tracking
- GA4 snippet presente
- Eventos: checkout iniciado, pagamento iniciado, pagamento aprovado, matrícula ativa, acesso ao curso, erros

## Ambiente de produção
- Railway: `railway.json`
- Render: `render.yaml`
- Ambos com `PYTHONPATH=academy` no startCommand

## Smoke test
- `/health` → 200
- `/courses` → JSON com cursos
- checkout por slug → HTML com título/preço
- webhook público acessível
- e-mail transacional enviado
- `/education/cursos/<slug>/index.html` → 200 para slugs reais
