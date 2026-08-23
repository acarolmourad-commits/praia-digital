# Guia de Integrações — Hermes Agents

> Conectores, padrões e configuração para WhatsApp Business API, Telegram, E-mail, CRM, ERP e ferramentas brasileiras.  
> Versão 1.0 — 2026-08-23

---

## 1. Princípios gerais de integração

Todo conector segue o padrão **Adapter**:
- Entrada: schema canônico do Hermes.
- Saída: schema nativo da ferramenta.
- Autenticação: OAuth2, API Key ou mTLS com segredos gerenciados por vault.
- Resiliência: retry com backoff exponencial, circuit breaker, timeout configurável.
- Idempotência: chave de correlação (`message_id`) para evitar duplicidade.

Fluxo padrão de integração:
```
Evento canônico → Adapter transforma → HTTP/Webhook nativo → Parse resposta → Mapeia para canônico → Confirmação
```

---

## 2. WhatsApp Business API

### 2.1 Visão geral
Canal prioritário para operações comerciais no Brasil. O WhatsApp Business API exige:
- Conta Business verificada no Meta Business Manager.
- Número de telefone aprovado.
- Template messages pré-aprovadas para comunicação proativa.

### 2.2 Configuração do webhook

Endpoint: `POST /v1/webhooks/whatsapp`

Payload de verificação (challenge):
```json
{
  "hub_mode": "subscribe",
  "hub_challenge": "string",
  "hub_verify_token": "string"
}
```

Resposta esperada: `hub_challenge` com status 200.

### 2.3 Envio de mensagens

Limites por conta (2026):
- Até 250 mensagens proativas/dia para contatos que interagiram nas últimas 24h.
- Templates aprovados para proativas fora da janela.
- Suporte a texto, imagem, documento, áudio, vídeo e botões interativos.

Exemplo de payload de envio (texto):
```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "text",
  "text": {
    "body": "Olá! Vi seu interesse no imóvel na praia. Posso enviar mais fotos?"
  }
}
```

### 2.4 Tratamento de status
Webhook envia `delivery`, `read`, `failed`.  
O Hermes atualiza o status da mensagem e registra `delivered_at`, `read_at`, `failed_reason`.

### 2.5 Considerações LGPD
- Não usar dados do usuário para treinar modelos do Meta.
- Oferecer opt-out via comando "PARAR" (exigido pela Meta).
- Logs devem mascarar número de telefone após sessão encerrada.

---

## 3. Telegram

### 3.1 Visão geral
Canal complementar com baixa fricção técnica. Ideal para times internos e notificações.

### 3.2 Configuração
1. Criar bot via @BotFather → obter `BOT_TOKEN`.
2. Configurar webhook: `https://api.telegram.org/bot<TOKEN>/setWebhook?url=<HERMES_WEBHOOK_URL>/v1/webhooks/telegram`
3. Ou usar polling (`getUpdates`) em ambiente de desenvolvimento.

### 3.3 Payload recebido
```json
{
  "update_id": 12345,
  "message": {
    "message_id": 1,
    "from": {"id": 123456789, "first_name": "João"},
    "chat": {"id": 123456789, "type": "private"},
    "text": "Quero agendar uma visita"
  }
}
```

### 3.4 Envio de mensagens
```json
{
  "chat_id": 123456789,
  "text": "Visita agendada para 15/01 às 14h. Confirma?",
  "reply_markup": {
    "inline_keyboard": [[{"text": "Sim", "callback_data": "confirm"}], [{"text": "Não", "callback_data": "cancel"}]]
  }
}
```

### 3.5 Limites
- 30 mensagens/segundo por bot.
- Mensagens proativas: enviar apenas após interação do usuário nas últimas 24h.

---

## 4. E-mail

### 4.1 Visão geral
Canal assíncrono para follow-up estruturado, contratos e relatórios.

### 4.2 Arquitetura de envio
```
Agente de prospecção → SMTP Adapter → Provedor de e-mail (Amazon SES / SendGrid / Mailgun) → Inbox
```

### 4.3 Métricas essenciais
- Taxa de entrega (bounce rate < 2%).
- Taxa de abertura.
- Taxa de clique.
- Spam complaints.

### 4.4 Boas práticas
- Usar domínio verificado com SPF, DKIM e DMARC.
- Limitar a 100 e-mails/dia por conta em warm-up inicial.
- Personalizar `reply-to` por corretor quando houver equipe.
- Anexos máximos: 10MB por mensagem.

---

## 5. CRM

### 5.1 Objetivo da integração
Sincronizar contatos, leads, oportunidades e histórico de interações entre o Hermes e o CRM.

### 5.2 Entidades mapeadas
| Entidade Hermes | Entidade CRM | Ações |
|---|---|---|
| `lead` | `Lead` / `Contato` | create, update, get |
| `opportunity` | `Oportunidade` | create, update, stage_change |
| `interaction` | `Atividade` | create |
| `property` | `Imóvel` | get, search |

### 5.3 Padrão de sincronização
- **Write-through:** toda ação relevante do agente escreve no CRM antes de responder ao usuário.
- **Read-through:** antes de responder, agente consulta CRM para carregar contexto.
- **Webhook de eventos:** CRM notifica Hermes quando lead é atualizado externamente (ex.: corretor move oportunidade).

### 5.4 CRMs brasileiros comuns
- **RD Station:** REST API + webhooks. Mapeamento de lead_score e lifecycle_stage.
- **HubSpot:** REST + GraphQL. Suporte nativo a custom objects.
- **Pipedrive:** REST API. Boa para funis de vendas visuais.
- **Zoho CRM:** REST + deluge functions. Custom fields via API.
- **Salesforce:** SOAP/REST. Melhor performance com Bulk API.

---

## 6. ERP

### 6.1 Objetivo da integração
Consultar e atualizar dados financeiros, contratos, estoque de imóveis e comissões.

### 6.2 Padrões de acesso
- **Leitura:** consultas via REST/SOAP para obter status de contrato, número do processo, valor de entrada.
- **Escrita:** ações restritas a corretores ou modo human-in-the-loop. O agente propõe, humano aprova.
- **Batching:** atualizações em lote durante a noite para reduzir carga.

### 6.3 ERPs brasileiros comuns
| ERP | Método | Observações |
|---|---|---|
| **Totvs Protheus / RM** | REST (appserver) ou SOAP | Exigir pool de conexões; usar smart-client com moderação |
| **Senior** | REST + OAuth2 | Boa documentação; suporte a webhooks |
| **SAP** | OData / RFC | Necessário middleware para mTLS e certificados ANA |
| **Sankhya** | REST + WSDL | Autenticação por login/senha com token |
| **Conta Azul / Nibo** | REST API | Foco em pequenas operações; boas para iniciantes |

### 6.4 Regras de ouro
- Nunca expor credenciais no código. Usar vault com rotação automática.
- Testar em ambiente de homologação antes de escrever no banco de produção.
- Registrar toda operação de escrita em tabela de auditoria.

---

## 7. Ferramentas brasileiras complementares

### 7.1 Prospecção e anúncios
- **Google Ads API:** criar campanhas, extrair métricas.
- **Meta Marketing API:** gerenciar anúncios no Facebook/Instagram.
- **LinkedIn Ads API:** para prospecção B2B de alto ticket.

### 7.2 Calendário e agendamento
- **Google Calendar API:** criar eventos, verificar conflitos.
- **Cal.com API:** agendamento público com fluxo de confirmação.

### 7.3 Mensageria e atendimento
- **Zendesk:** abertura e atualização de tickets.
- **Intercom:** mensagens in-app e onboarding.
- **Blip:** plataforma brasileira de bots com bridge para WhatsApp.

### 7.4 Pagamentos
- **Mercado Pago / PagSeguro:** gerar cobrança, confirmar pagamento.
- **Stripe Brasil:** assinaturas e split de pagamento.

---

## 8. Segurança em integrações

### 8.1 Autenticação
- Preferir OAuth2 com PKCE para integrações de frontend.
- API Keys devem ter escopo mínimo e expiração.
- mTLS para integrações entre servidores (ERP, bancos).

### 8.2 Rate limiting
- Implementar por tenant e por endpoint.
- Respeitar limites nativos de cada API (ex.: WhatsApp 1 msg/s por número, Telegram 30 msg/s).
- Fila de retry com exponential backoff e jitter.

### 8.3 Validação
- Validar webhook signatures (ex.: `X-Hub-Signature-256` do WhatsApp, `X-Telegram-Bot-Api-Secret-Token`).
- Sanitizar todos os inputs antes de repassar a LLMs (injeção de prompt).
- Rejeitar payloads com schema inválido.

---

## 9. Testes de integração

### 9.1 Testes unitários
- Mock de cada adapter para validar transformação de schema.
- Testar retry e circuit breaker com simulação de falha.

### 9.2 Testes de contrato
- Validar que o payload enviado ao WhatsApp/Telegram/CRM está em conformidade com a especificação oficial.
- Usar ferramentas como Pact ou schemathesis.

### 9.3 Testes de ponta a ponta
- Ambiente de homologação com contas de teste (WhatsApp Business Test, Telegram test bot, CRM sandbox).
- Simular fluxo completo: canal → agente → ferramenta → resposta → canal.
- Validar idempotência: reenviar o mesmo `message_id` não duplica ações.

---

## 10. Troubleshooting comum

| Sintoma | Causa provável | Solução |
|---|---|---|
| Webhook do WA retorna 403 | Token de verificação errado ou número não aprovado | Revisar `verify_token` e status no Meta Business Manager |
| CRM não atualiza | Campo mapeado errado ou permissão insuficiente | Verificar log de request/response do conector |
| E-mail cai em spam | SPF/DKIM/DMARC não configurados | Usar ferramenta de teste (mail-tester.com) |
| Agente demora > 5s | Timeout em tool call ou vector store lento | Aumentar timeout, adicionar cache, reindexar embeddings |
| Duplicidade de mensagens | Retry sem idempotência | Implementar `message_id` como chave única no log de envio |
