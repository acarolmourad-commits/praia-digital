# Arquitetura de Conversão, Matrícula e Entrega Automática — Praia Digital Academy

## Visão geral
Este documento descreve o fluxo completo, reutilizável e seguro de conversão para qualquer curso da Academy, usando a formação **Fotografia e Edição de Imóveis para Temporada** como caso piloto.

## Componentes principais
- **Interesse público**: `education/formacoes/formacao-fotografia-edicao-imoveis-temporada-2026.html`
- **Checkout unificado**: `education/checkout.html`
- **API Academy**: FastAPI em `academy/main.py`
- **Operador de conversão genérico**: `academy/core/conversion.py`
- **Pagamento/gateway**: `academy/core/payments/service.py`, `webhooks.py`, `routers/payments.py`
- **E-mail transacional**: `academy/core/email_service.py`
- **Autenticação**: JWT em `academy/core/security.py`
- **Área do aluno**: frontend estático em `/education/aluno` e API em `/academy/me`

## Modelo de dados relevante
- `Course` — curso/slug/título/preço/status
- `Enrollment` — matrícula do usuário no curso
- `Payment` — pagamento associado à matrícula
- `Order` + `OrderItem` — pedido de compra
- `User` — aluno com e-mail/role
- `Certificate`, `Progress` — entrega pós-matrícula

## Fluxo desejado (genérico)
1. **INTERESSE** — interessado clica em "Quero me inscrever" na página da formação
2. **RESPOSTA** — Hermes envia e-mail com a formação + benefícios + link do checkout oficial
3. **CHECKOUT** — interessado preenche dados no checkout e confirma pagamento
4. **PAGAMENTO** — gateway cria pagamento e redireciona
5. **WEBHOOK/CONFIRMAÇÃO FINANCEIRA** — gateway notifica `/academy/payments/webhook`
6. **ATIVAÇÃO** — backend marca `Payment.status = paid` e ativa matrícula
7. **E-MAIL** — `send_enrollment_confirmation` envia acesso à área autenticada
8. **ACESSO** — aluno acessa `/education/aluno` com JWT

## Regra crítica
- **Nunca liberar conteúdo apenas porque o usuário afirmou que pagou.**
- A liberação depende de confirmação financeira do gateway/webhook/status oficial.

## Generalização sem duplicar lógica
- Não crie checkouts por curso.
- Não crie fluxos paralelos.
- Reutilize `academy/core/conversion.py` para qualquer curso via `course_id` ou `slug`.
- Documente a origem da conversão em `Enrollment.source` e em eventos futuros.

## O que já funciona
- Checkout unificado já resolve `slug → course_id`
- Pagamentos já criam `Order`, `Enrollment` e `Payment`
- Webhook já valida gateway e ativa matrícula
- E-mail transacional já envia acesso

## O que ainda depende de configuração externa
- Gateway real: `PAYMENT_GATEWAY`
- Tokens/secrets: `HOTMART_TOKEN`, `HOTMART_SECRET`, `MERCADOPAGO_TOKEN`, `STRIPE_SECRET`
- SMTP: `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`
- Webhook público acessível
- Cursos publicados no banco (`status=published`)

## Piloto: Fotografia e Edição
- Página: `education/formacoes/formacao-fotografia-edicao-imoveis-temporada-2026.html`
- Checkout: `education/checkout.html`
- Operador: `academy/core/conversion.py`
