# Checklist de Deploy/Ativação da Academy — Produção

## Objetivo
Liberar a Praia Digital Academy para vendas reais somente após validação completa.

## 1. Variáveis de ambiente obrigatórias
Definir no provedor de hospedagem/deploy (Render/Railway/VPS):

- `SECRET_KEY`: chave secreta forte para JWT.
- `DATABASE_URL`: URL do banco de produção (não usar SQLite em produção).
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`: e-mail transacional.
- `EMAIL_FROM`: remetente dos e-mails da Academy.
- `PAYMENT_GATEWAY`: `sandbox`, `hotmart`, `mercadopago` ou `stripe`.
- `PAYMENT_SECRET`: segredo do gateway para validação de webhook.
- `PAYMENT_WEBHOOK_PATH`: caminho público do webhook, ex: `/academy/payments/webhook`.
- `BASE_URL`: URL pública da Academy, ex: `https://academy.praia.digital`.
- `ALLOWED_ORIGINS`: origens permitidas para CORS.

## 2. Banco de dados
- [ ] Rodar `python -m academy.core.setup_database` no ambiente de produção.
- [ ] Confirmar tabelas `courses`, `modules`, `lessons`, `payments`, `enrollments` criadas.
- [ ] Rodar `python academy/scripts/seed_approved_courses.py` para popular os 64 cursos aprovados.
- [ ] Validar `SELECT count(*) FROM courses WHERE status='published'` = 64.

## 3. Webhook público
- [ ] Garantir que a rota `/academy/payments/webhook` está acessível publicamente.
- [ ] Configurar no gateway a entrega de webhooks para `https://academy.praia.digital/academy/payments/webhook`.
- [ ] Validar recebimento de eventos de teste do gateway (`approved`, `pending`, `rejected`).

## 4. E-mail transacional
- [ ] Enviar e-mail de teste para um endereço válido.
- [ ] Confirmar entrega e ausência de spam.
- [ ] Validar template `send_enrollment_confirmation`.

## 5. Checkout e fluxo de pagamento
- [ ] Abrir `education/checkout.html?slug=<slug>&title=<nome>&price=<valor>`.
- [ ] Confirmar exibição do nome e preço do curso.
- [ ] Simular pagamento aprovado no gateway sandbox → matrícula ativa.
- [ ] Simular pagamento pendente → sem acesso.
- [ ] Simular pagamento recusado → sem acesso.
- [ ] Simular webhook duplicado → idempotente (apenas uma matrícula).
- [ ] Confirmar e-mail de liberação enviado após confirmação.

## 6. Testes automatizados
- [ ] `pytest academy/tests/test_delivery_flow.py` — 5/5 passando.
- [ ] `pytest academy/tests/` — demais testes OK.

## 7. Conteúdo e integridade
- [ ] `education/auditoria-final.json` → 64 PRONTO_PARA_VENDA.
- [ ] `docs/academy/auditoria-prontidao-cursos.md` coerente.
- [ ] 64 slugs ativos no banco.
- [ ] Nenhum arquivo essencial ausente em `education/cursos/*`.

## 8. Liberação
- [ ] Após aprovação deste checklist, considerar vendas liberadas.
- [ ] Monitorar métricas iniciais: conversão, taxa de pagamento aprovado, e-mail entregue.
