# Tracking Academy — Eventos recomendados

## Objetivo
Garantir observabilidade do funil de matrícula da Academy.

## Eventos a capturar

### 1. Checkout iniciado
- Disparar ao carregar `education/checkout.html`
- Payload sugerido: `{ slug, title, price, source }`

### 2. Pagamento iniciado
- Disparar ao clicar no botão de compra
- Payload sugerido: `{ slug, payment_method, gateway }`

### 3. Pagamento aprovado
- Disparar no redirecionamento de sucesso ou via webhook confirmado
- Payload sugerido: `{ slug, transaction_id, amount, status }`

### 4. Matrícula ativa
- Disparar quando enrollment for criado/ativado
- Payload sugerido: `{ slug, user_id, enrolled_at }`

### 5. Acesso ao curso
- Disparar ao acessar página do curso
- Payload sugerido: `{ slug, user_id }`

### 6. E-mail enviado
- Disparar em cada e-mail transacional
- Payload sugerido: `{ type, slug, user_id, status }`

### 7. Erros
- Disparar em falhas de pagamento/webhook/email
- Payload sugerido: `{ step, error, slug }`

## Implementação sugerida
- Incluir snippets no checkout.html e páginas de curso
- Incluir log estruturado no backend em `email_service.py` e webhooks
- Usar `BASE_URL` + endpoint interno `/academy/analytics/event` quando disponível
