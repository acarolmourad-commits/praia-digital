# Especificação — Checkout / Gateway / Agente Financeiro / Academy

## Fluxo alvo
SITE
↓
CHECKOUT
↓
GATEWAY
↓
AGENTE FINANCEIRO
↓
PAGAMENTO_CONFIRMADO
↓
ACADEMY
↓
ENTREGA AUTOMÁTICA

## Estado atual
- Gateway real: NÃO INTEGRADO
- Agente Financeiro: implementado, 24 testes aprovados
- Academy: entrega automática preparada, bloqueada por PAGAMENTO_CONFIRMADO
- Checkout: não integrado ao site

## Especificação

### Estados do pagamento
1. PENDENTE
2. COBRANCA_CRIADA
3. AGUARDANDO_PAGAMENTO
4. PAGAMENTO_RECEBIDO
5. PAGAMENTO_VALIDADO
6. PAGAMENTO_CONFIRMADO
7. PAGAMENTO_REJEITADO
8. PAGAMENTO_NAO_ENCONTRADO
9. PAGAMENTO_ESTORNADO

### Eventos
- checkout.criado
- cobranca.criada
- pagamento.recebido
- pagamento.validado
- pagamento.confirmado
- pagamento.rejeitado
- pagamento.estornado
- entrega.liberada
- entrega.falhou

### Webhooks necessários
- gateway.webhook.pagamento.recebido
- gateway.webhook.pagamento.confirmado
- gateway.webhook.pagamento.rejeitado
- gateway.webhook.pagamento.estornado

### Idempotência
- Cada pagamento tem ID único
- Cada evento de webhook tem idempotency key
- Pagamento confirmado duas vezes não cria duas entregas

### Retry
- Webhook com retry exponencial
- Máximo 3 tentativas
- Backoff: 1s, 5s, 30s
- Falha após 3 tentativas → fila de intervenção humana

### Cancelamento/Estorno
- Estado PAGAMENTO_ESTORNADO
- Reversão de entrega se aplicável
- Auditoria obrigatória

### Falha de entrega
- Estado ENTREGA_FALHOU
- Retry automático limitado
- Após esgotar retries → fila de intervenção humana
- Auditoria obrigatória

### Auditoria
- Registrar: lead, oferta, cobrança, pagamento, confirmação, entrega, erro, retry, intervenção humana
- Separar: potencial, contratado, pago, entregue

## Proteções
- Nunca liberar sem PAGAMENTO_CONFIRMADO
- Nunca considerar fechou/onboarding/proposta como pagamento
- Nunca processar pagamento real sem gateway integrado
- Nunca liberar acesso sem idempotência verificada

## Não fazer agora
- Não inventar gateway
- Não fingir integração real
- Não processar pagamentos reais
- Não alterar Agente Financeiro existente
