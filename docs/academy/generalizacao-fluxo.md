# Generalização do Fluxo Academy — Todos os Cursos

## Objetivo
Reutilizar o mesmo fluxo de conversão + matrícula + liberação automática para qualquer curso da Praia Digital Academy, sem duplicar lógica.

## Arquitetura já unificada
- Operador genérico: `academy/core/conversion.py`
  - `register_interest()` — registra interesse/lead + matrícula pendente
  - `create_order_for_course()` — cria pedido, pagamento e matrícula pendente
  - `confirm_payment_from_gateway()` — confirma pagamento via webhook
- Checkout público: `education/checkout.html`
  - Resolve `course_id` automaticamente por slug antes de criar o pedido
  - Funciona para qualquer curso publicado via `/courses/{slug}`
- Webhook: `/academy/payments/webhook`
  - Suporta sandbox/Hotmart/Mercado Pago/Stripe
  - Mapeia status do gateway para `paid`/`pending`/`failed`/`refunded`
  - Ativa matrícula automaticamente quando status vira `paid`
- E-mail transacional: `academy/core/email_service.py`
  - Enviado automaticamente após ativação da matrícula

## Como usar para qualquer curso novo
1. Cadastrar curso no banco com `status=published`
2. Criar página pública do curso ou ligá-lo em uma formação existente
3. Usar o checkout com `slug` ou `course_id`
4. Nenhuma alteração adicional no backend é necessária

## Regra de segurança
- Liberação de acesso depende exclusivamente de confirmação do gateway/webhook
- Não liberar conteúdo apenas porque o interessado afirmou que pagou
- E-mail envia link para área autenticada, nunca anexo com conteúdo

## Dependências externas
- `PAYMENT_GATEWAY` real (`hotmart`/`mercadopago`/`stripe`)
- Tokens/secrets do gateway
- SMTP configurado
- Webhook público acessível

## Status
- Estrutura generalizada: sim
- Testes do piloto: 3/3 passando
- Produção: aguardando configuração externa
