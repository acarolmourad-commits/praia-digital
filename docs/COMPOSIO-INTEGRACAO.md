# Integração de automações com Composio

Guia de boas práticas (2026) para conectar as automações da Praia Digital
(follow-up de leads, agendamentos, CRM) a apps externos usando o Composio.

## Conceitos-chave

- **Sessions (antes Tool Router)**: crie uma sessão isolada por usuário
  (`composio.create(user_id=...)`) para que cada corretor/imobiliária tenha
  seu próprio contexto e credenciais.
- **Connection management automático**: habilite `manageConnections: true`
  para o agente conduzir o fluxo de autenticação (OAuth) sozinho.
- **Native Tools > MCP em produção**: ferramentas nativas executam mais rápido
  e aceitam *modifiers* (pré/pós-processamento). Use MCP só para prototipar.
- **Segurança**: desabilite ferramentas perigosas em produção via config de
  `tools`; verifique slugs com o CLI (`composio search`) antes de implementar.
- **SDKs de framework**: use o provider dedicado (`@composio/openai-agents`,
  `@composio/vercel`, etc.) em vez de imports genéricos.

## Casos de uso para a Praia Digital

| Automação | Apps conectados | Fluxo |
|---|---|---|
| Follow-up de leads WhatsApp | Gmail + Calendar | Novo lead → e-mail de boas-vindas + sugestão de visita |
| Agendamento de visitas | Google Calendar + Meet | Lead escolhe horário → evento + link de vídeo |
| CRM de prospecção | Google Sheets | Leads das landings → linha na planilha de prospecção |
| Alertas de novos imóveis | Gmail + Sheets | Cadastro de imóvel → notificação para lista segmentada |
| Conteúdo e SEO | Docs + Drive | Pautas (`relatorio-pautas-litoral-2026.md`) → rascunho no Docs |
| Tarefas da equipe | Linear / Notion | Issue de bug do site → card no tracker |

## Exemplo mínimo (TypeScript)

```ts
import { Composio } from '@composio/core';

const composio = new Composio({ apiKey: process.env.COMPOSIO_API_KEY });

// 1. Sessão isolada por usuário
const session = await composio.create({
  userId: lead.id,
  manageConnections: true,
});

// 2. Verificar conexões antes de executar
const toolkits = await session.toolkits();

// 3. Executar ferramenta (ex.: enviar e-mail de follow-up)
await session.execute('GMAIL_SEND_EMAIL', {
  to: lead.email,
  subject: 'Sua visita ao imóvel no litoral',
  body: '...',
});
```

## Checklist de produção

- [ ] `COMPOSIO_API_KEY` em variável de ambiente (nunca no código)
- [ ] Sessões com `user_id` único por cliente
- [ ] Tools destrutivas (delete/pay) desabilitadas ou com confirmação humana
- [ ] Logs de execução com `log_id` para auditoria
- [ ] Retry com backoff para HTTP 429 em buscas

## Referências

- https://docs.composio.dev/reference/api-reference/tool-router
- https://github.com/ComposioHQ/skills
