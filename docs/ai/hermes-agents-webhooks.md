# Webhooks — Hermes Agents

> Configure webhooks para receber eventos em tempo real.

## Eventos
- message.received
- message.sent
- agent.created

## Configuração
POST /webhooks
{
  "url": "https://seudominio.com/webhook",
  "events": ["message.received"]
}
