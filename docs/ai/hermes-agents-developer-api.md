# Guia do Desenvolvedor — Hermes Agents

> API REST, Webhooks, SDK Python/JS e exemplos de integração para desenvolvedores.  
> Versão 1.0 — 2026-08-23

---

## 1. Visão geral da API

A API do Hermes Agents é RESTful, usa JSON, autenticação por Bearer Token e segue a versão `v1`.  
Base URL:

```
https://api.praiadigital.com/v1
```

Todas as requisições exigem:

```
Authorization: Bearer <token>
Content-Type: application/json
```

Princípios:

- **Stateless** — cada requisição carrega o contexto necessário via headers ou body.
- **Idempotente** — requisições com mesmo `X-Idempotency-Key` retornam o mesmo resultado.
- **Paginação** — `limit` e `offset` ou `cursor` em listagens.
- **Rate limit** — 1.000 req/min por token (ajustável por plano).

---

## 2. Autenticação

### 2.1 Obter token (Client Credentials)

```bash
curl -X POST https://api.praiadigital.com/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "seu-client-id",
    "client_secret": "seu-client-secret",
    "scope": "agents:read agents:write webhooks:read webhooks:write"
  }'
```

Resposta:

```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "agents:read agents:write webhooks:read webhooks:write"
}
```

### 2.2 Rotação de segredos

- Segredos com até 90 dias de idade devem ser rotacionados via `/v1/auth/rotate`.
- Tokens antigos permanecem válidos por até 24h após a rotação (grace period).
- Nunca commitar `client_secret` em repositórios.

---

## 3. Endpoints principais

### 3.1 Agentes

Listar agentes:

```bash
curl https://api.praiadigital.com/v1/agents \
  -H "Authorization: Bearer <token>"
```

Criar agente:

```bash
curl -X POST https://api.praiadigital.com/v1/agents \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Atendimento Imobiliário",
    "persona": "Corretor digital especializado em imóveis no litoral paulista.",
    "tools": ["crm.lookup", "crm.create_lead", "calendar.schedule"],
    "model": "hermes-pro-v2",
    "temperature": 0.3,
    "language": "pt-BR"
  }'
```

Disparar execução:

```bash
curl -X POST https://api.praiadigital.com/v1/agents/{agent_id}/execute \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "channel": "whatsapp",
      "user_id": "5511999999999",
      "message": "Quero agendar uma visita no apartamento em Ubatuba",
      "context": {"property_id": "ubatuba-apt-42"}
    },
    "run_mode": "async",
    "webhook_url": "https://seudominio.com/webhooks/hermes"
  }'
```

Resposta assíncrona:

```json
{
  "run_id": "run_8f3k2...",
  "status": "queued",
  "estimated_ms": 1200,
  "webhook_url": "https://seudominio.com/webhooks/hermes"
}
```

Consultar status do run:

```bash
curl https://api.praiadigital.com/v1/runs/{run_id} \
  -H "Authorization: Bearer <token>"
```

### 3.2 Ferramentas (Tools)

Listar ferramentas disponíveis:

```bash
curl https://api.praiadigital.com/v1/tools \
  -H "Authorization: Bearer <token>"
```

Registrar ferramenta customizada:

```bash
curl -X POST https://api.praiadigital.com/v1/tools \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "crm.lookup_client",
    "description": "Busca cliente no CRM por CPF ou e-mail.",
    "input_schema": {
      "type": "object",
      "properties": {
        "cpf": {"type": "string", "pattern": "^\\d{11}$"},
        "email": {"type": "string", "format": "email"}
      },
      "oneOf": [{"required": ["cpf"]}, {"required": ["email"]}]
    },
    "endpoint": "https://seudominio.com/crm/api/client",
    "method": "POST",
    "auth": {
      "type": "bearer",
      "token": "${CRM_API_TOKEN}"
    },
    "timeout_ms": 3000,
    "retry": {"max": 2, "backoff": "exponential"}
  }'
```

### 3.3 Memória (Memory)

Salvar fato na memória de longo prazo:

```bash
curl -X POST https://api.praiadigital.com/v1/memory/facts \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agente-123",
    "user_id": "5511999999999",
    "fact": "Cliente prefere apartamentos com vista mar e varanda",
    "confidence": 0.95,
    "source": "whatsapp.message",
    "tags": ["preference", "imovel"]
  }'
```

Buscar memória por similaridade:

```bash
curl "https://api.praiadigital.com/v1/memory/search?agent_id=agente-123&user_id=5511999999999&q=prefer%C3%AAncia+vista+mar" \
  -H "Authorization: Bearer <token>"
```

---

## 4. Webhooks

### 4.1 Eventos disponíveis

| Evento | Descrição | Payload |
|---------|-----------|---------|
| `agent.run.started` | Execução iniciada | `{ run_id, agent_id, input, timestamp }` |
| `agent.run.completed` | Execução concluída com sucesso | `{ run_id, output, duration_ms, tool_calls }` |
| `agent.run.failed` | Erro durante execução | `{ run_id, error_code, error_message, stack_trace }` |
| `agent.run.approval_required` | Ação humana necessária | `{ run_id, approval_type, data, expires_at }` |
| `tool.called` | Ferramenta invocada | `{ run_id, tool_name, args, result, latency_ms }` |
| `memory.stored` | Fato armazenado | `{ agent_id, user_id, fact, confidence }` |
| `billing.limit_reached` | Limite de uso atingido | `{ tenant_id, limit, current_usage }` |

### 4.2 Registro de webhook

```bash
curl -X POST https://api.praiadigital.com/v1/webhooks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://seudominio.com/webhooks/hermes",
    "events": [
      "agent.run.completed",
      "agent.run.failed",
      "tool.called"
    ],
    "secret": "whsec_abc123...",
    "active": true
  }'
```

### 4.3 Segurança do webhook

- **HMAC SHA256**: cada payload inclui header `X-Hermes-Signature`.
- **Timestamp replay protection**: header `X-Hermes-Timestamp` deve estar dentro de ±5 min.
- **Validação obrigatória**: rejeitar webhooks sem `signature` válida.

Exemplo de validação em Python:

```python
import hmac
import hashlib
import time

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    """Valida HMAC do webhook Hermes."""
    ts = int(time.time())
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

### 4.4 Retry policy

Se o endpoint retornar status fora de `2xx`:

- 1ª tentativa: imediata.
- 2ª tentativa: +30s.
- 3ª tentativa: +120s.
- Após 3 falhas: evento marcado como `dead_letter` e notificado via e-mail.

---

## 5. SDK Python

Instalação:

```bash
pip install hermes-agents-sdk
```

Uso básico:

```python
from hermes_agents import HermesClient, Agent

client = HermesClient(
    base_url="https://api.praiadigital.com/v1",
    token="eyJ..."
)

# Criar agente
agent = client.agents.create(
    name="Atendimento Imobiliário",
    persona="Corretor digital especializado no litoral.",
    tools=["crm.lookup", "calendar.schedule"],
    model="hermes-pro-v2"
)

# Executar de forma síncrona
result = agent.run(
    input={
        "channel": "whatsapp",
        "user_id": "5511999999999",
        "message": "Quero agendar visita"
    }
)
print(result.output)

# Executar assíncrono com webhook
run = agent.run_async(
    input={"channel": "web", "user_id": "user-42", "message": "..."},
    webhook_url="https://meusite.com/hook"
)
print(f"Run ID: {run.id}")
```

Streaming de respostas:

```python
for chunk in agent.run_stream(
    input={"channel": "web", "message": "Liste 10 imóveis na praia"}
):
    print(chunk.delta, end="", flush=True)
```

### 5.1 Context managers e sessões

```python
from hermes_agents import Session

with Session(client, agent_id="agente-123") as session:
    reply1 = session.send("Olá, quero imóvel em Ubatuba")
    reply2 = session.send("Com varanda, por favor")
    print(session.memory.search("preferência vista mar"))
```

---

## 6. SDK JavaScript / TypeScript

Instalação:

```bash
npm install @praiadigital/hermes-agents
```

Uso básico:

```typescript
import { HermesClient } from '@praiadigital/hermes-agents';

const client = new HermesClient({
  baseUrl: 'https://api.praiadigital.com/v1',
  token: process.env.HERMES_TOKEN
});

const agent = await client.agents.create({
  name: 'Atendimento Imobiliário',
  persona: 'Corretor digital especializado no litoral.',
  tools: ['crm.lookup', 'calendar.schedule']
});

const result = await agent.run({
  input: {
    channel: 'whatsapp',
    user_id: '5511999999999',
    message: 'Quero agendar visita'
  }
});

console.log(result.output);
```

### 6.1 Middleware Express para webhooks

```typescript
import express from 'express';
import { HermesWebhook } from '@praiadigital/hermes-agents';

const app = express();
const webhook = new HermesWebhook({ secret: process.env.HERMES_WEBHOOK_SECRET });

app.post('/webhooks/hermes', webhook.verify(), (req, res) => {
  const event = req.body;

  switch (event.type) {
    case 'agent.run.completed':
      console.log('Run completado:', event.data.run_id, event.data.output);
      break;
    case 'agent.run.failed':
      console.error('Run falhou:', event.data.run_id, event.data.error_message);
      break;
    default:
      console.log('Evento:', event.type);
  }

  res.status(200).send({ received: true });
});

app.listen(3000);
```

---

## 7. Exemplos de código

### 7.1 Qualificação de lead com CRM

```python
from hermes_agents import HermesClient

client = HermesClient(token=os.environ["HERMES_TOKEN"])
agent = client.agents.get("qualificador-leads")

def on_run_completed(event):
    run = event.data
    if run.output.get("lead_score", 0) >= 8:
        # Lead quente → criar oportunidade no CRM
        crm = client.tools.call("crm.create_deal", {
            "lead_id": run.output["lead_id"],
            "stage": "qualificado",
            "score": run.output["lead_score"]
        })
        print(f"Oportunidade criada: {crm['deal_id']}")

webhook.subscribe("agent.run.completed", on_run_completed)
```

### 7.2 Envio de mensagem proativa via WhatsApp

```python
from hermes_agents import HermesClient
from datetime import datetime, timedelta

client = HermesClient(token=os.environ["HERMES_TOKEN"])

# Agendar mensagem proativa para 24h após a visita
visit_date = datetime.now() - timedelta(days=1)
lead = client.tools.call("crm.lookup", {
    "cpf": "12345678900",
    "context": "visited_property"
})

if lead.get("last_visit_date") == visit_date.strftime("%Y-%m-%d"):
    client.channels.whatsapp.send(
        to=lead["phone"],
        template="pos_visita",
        params={"nome": lead["name"], "imovel": lead["property_name"]}
    )
```

### 7.3 Integração multi-agente (Router)

```python
from hermes_agents import Router, Agent

router = Router(client)

router.add_route(
    intent="suporte_tecnico",
    agent=Agent(client, "suporte-tech"),
    confidence_threshold=0.85
)
router.add_route(
    intent="vendas_imovel",
    agent=Agent(client, "vendas-imovel"),
    confidence_threshold=0.75
)

result = router.dispatch({
    "channel": "web",
    "message": "O ar condicionado do apartamento não funciona",
    "user_id": "user-789"
})
print(result.agent_used, result.output)
```

---

## 8. Tratamento de erros

Códigos HTTP:

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Criado |
| 204 | Sem conteúdo |
| 400 | Payload inválido (veja `error.details`) |
| 401 | Token ausente ou expirado |
| 403 | Escopo insuficiente |
| 404 | Recurso não encontrado |
| 429 | Rate limit excedido |
| 500 | Erro interno |
| 503 | Manutenção programada |

Estrutura de erro:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Campo 'persona' excede 2.000 caracteres.",
    "details": [
      {"field": "persona", "constraint": "max_length", "limit": 2000, "received": 2150}
    ],
    "request_id": "req_9k2m..."
  }
}
```

---

## 9. Testes e sandbox

- **Sandbox**: `https://sandbox.praiadigital.com/v1` — ambiente isolado com dados fictícios.
- **Test tokens**: gerados via dashboard, válidos por 24h.
- **Mock de ferramentas**: use `tool.simulate` para testar integrações sem chamar APIs externas.

```bash
curl -X POST https://sandbox.praiadigital.com/v1/tools/simulate \
  -H "Authorization: Bearer <test-token>" \
  -d '{
    "tool": "crm.create_lead",
    "response": {
      "lead_id": "mock-123",
      "status": "created"
    }
  }'
```

---

## 10. Links úteis

- [Postman Collection](https://api.praiadigital.com/postman)
- [OpenAPI Spec](https://api.praiadigital.com/openapi.json)
- [SDK Python no PyPI](https://pypi.org/project/hermes-agents-sdk)
- [SDK JS no npm](https://www.npmjs.com/package/@praiadigital/hermes-agents)
- [Status da API](https://status.praiadigital.com)
