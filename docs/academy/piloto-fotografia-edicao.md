# Piloto Academy — Fotografia e Edição de Imóveis para Temporada

## Status
- Estrutura auditada
- Checkout validado via `/academy/checkout`
- Regra de liberação confirmada: somente após confirmação do gateway/webhook
- Testes do piloto passando
- Próximo passo: configurar gateway/webhook/SMTP externos

## Arquitetura
- Backend: FastAPI
- Modelos: Course, Enrollment, Payment, Order, OrderItem, User
- Checkout: `education/checkout.html`
- Pagamento/gateway: `academy/core/payments/`
- Webhook: `/academy/payments/webhook`
- E-mail: `academy/core/email_service.py`
- Área do aluno: `/education/aluno`

## Regra de segurança
- Não liberar acesso apenas porque o interessado disse que pagou
- A liberação depende de confirmação financeira do gateway
- E-mail envia link para área autenticada, nunca anexo com conteúdo

## Fluxo
1. Interesse
2. Checkout cria Enrollment pending + Payment pending + Order
3. Pagamento no gateway
4. Webhook confirma status paid
5. Enrollment vira active
6. E-mail de boas-vindas
7. Acesso liberado

## Dependências externas
- `PAYMENT_GATEWAY`: hotmart | mercadopago | stripe
- Tokens/secrets do gateway
- SMTP configurado
- Webhook público acessível

## Arquivos alterados
- `academy/core/conversion.py`
- `education/checkout.html`
- `academy/tests/test_pilot_fotografia_edicao.py`
- `docs/academy/fluxo-conversao-matricula-automatica.md`
