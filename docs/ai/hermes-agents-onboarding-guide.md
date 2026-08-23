# Guia de Onboarding — Hermes Agents (Praia Digital)

> Última atualização: Agosto/2026  
> Uso: onboarding de novos clientes, handoff comercial → operação, referência para suporte nível 1.

---

## Visão geral do processo

O onboarding de Hermes Agents é dividido em **5 etapas**, com durações e entregas definidas. O objetivo é chegar ao **primeiro valor operacional em até 14 dias**, sem exigir que o cliente pare a operação atual.

| Etapa | Duração | Entregável | Responsável |
|-------|---------|------------|-------------|
| 1. Kick-off | 1 dia | Mapa de processos, lista de ferramentas, definição de sucesso | Sucesso do Cliente + Vendas |
| 2. Arquitetura | 2–3 dias | Diagrama de fluxo, seleção de modelos, lista de permissões | Engenharia + Arquitetura |
| 3. Configuração | 3–5 dias | Agentes funcionando em ambiente de homologação | Engenharia |
| 4. Treinamento | 2–3 dias | Playbooks, sessões com time, vídeos curtos | Sucesso do Cliente |
| 5. Produção | 1 dia (go-live) | Monitoramento ativo, handoff para suporte | Operação + Suporte |

---

## Pré-requisitos do cliente

Antes do kick-off, o cliente precisa fornecer:

1. **Acesso administrativo** aos sistemas que serão integrados (CRM, ERP, WhatsApp Business API, e-mail, etc.).
2. **Mapa de processos** com pelo menos 1 fluxo prioritário (ex.: qualificação de lead, agendamento, suporte pós-venda).
3. **Critérios de sucesso** mensuráveis: taxa de resposta, tempo de resolução, custo por lead, NPS, etc.
4. **Contato(s) interno(s)** com poder de decisão para aprovar fluxos e regras.

> **Dica de vendas:** se o cliente não tem claro o critério de sucesso, comece por um diagnóstico gratuito de 7 dias antes do onboarding pago.

---

## Etapa 1 — Kick-off

**Objetivo:** alinhar expectativas, riscos e prioridades.

**Agenda sugerida (60–90 min):**
- Apresentação do time (sucesso do cliente, engenharia, vendas).
- Revisão do contrato/escopo: o que está incluído, o que é extra.
- Definição do fluxo piloto (sempre começar pequeno).
- Acordo de SLA interno: horários de resposta, canal de urgência, reunião de status.

**Entregáveis:**
- Documento de kick-off com data de go-live alvo.
- Matriz RACI simplificada (quem aprova, quem executa, quem acompanha).
- Canal de comunicação exclusivo (WhatsApp/Slack/Teams).

---

## Etapa 2 — Arquitetura

**Objetivo:** desenhar o fluxo do agente sem código.

**Atividades:**
- Levantar ferramentas existentes e APIs disponíveis.
- Definir o modelo LLM ideal (custo vs. qualidade).
- Mapear permissões: o que o agente pode fazer sozinho, o que precisa de aprovação humana.
- Documentar exceções e fallbacks.

**Entregáveis:**
- Diagrama de arquitetura do agente.
- Lista de ferramentas e permissões.
- Matriz de risco (ações irreversíveis exigem aprovação humana).

> **Pitfall comum:** cliente quer automatizar tudo de uma vez. Resista: um agente bem configurado em um fluxo > 5 agentes mal configurados em fluxos diferentes.

---

## Etapa 3 — Configuração

**Objetivo:** colocar o agente para rodar em homologação.

**Checklist:**
- [ ] Criar instância do agente com prompt base e instruções de segurança.
- [ ] Conectar ferramentas (e-mail, WhatsApp, CRM, banco de dados).
- [ ] Configurar memória de curto e longo prazo.
- [ ] Definir limites de uso (rate limits, custo máximo por dia).
- [ ] Testar com dados fictícios (golden set de 20–50 interações).
- [ ] Ajustar prompt e regras com base nos testes.

**Critério de saída:** o agente resolve 80% dos casos do fluxo piloto sem intervenção humana.

---

## Etapa 4 — Treinamento

**Objetivo:** capacitar o time para operar, supervisionar e evoluir o agente.

**Formato sugerido:**
- **Sessão 1 (1h):** como funciona o agente, o que ele pode e não pode fazer.
- **Sessão 2 (1h):** leitura de logs, detecção de falhas, acionamento do suporte.
- **Material complementar:** vídeos curtos (3–5 min) e cheat sheet em PDF.

**Perguntas que o cliente deve responder antes do go-live:**
- Quem monitora o agente nas primeiras 2 semanas?
- Qual o canal de alerta para falhas?
- Como reportar bugs ou pedidos de ajuste?

---

## Etapa 5 — Produção e Handoff

**Objetivo:** lançar em produção com supervisão ativa e transferir para operação contínua.

**Go-live:**
- Liberar para 10–20% do volume real nos primeiros 3 dias.
- Acompanhar métricas diárias: taxa de resolução, tempo de resposta, exceções.
- Ajustar prompt e regras semanalmente nas primeiras 4 semanas.

**Handoff para suporte:**
- Repassar logs, configurações e playbooks ao time de suporte nível 1.
- Agendar revisão de 30 dias para avaliar expansão de fluxo.

---

## Cronograma de acompanhamento

| Período | Frequência | Atores | Conteúdo |
|---------|-----------|--------|----------|
| Semana 1 (go-live) | Diário | Sucesso do Cliente + Engenharia | Métricas, exceções, ajustes rápidos |
| Semanas 2–4 | 2x por semana | Sucesso do Cliente | Revisão de logs, treinamento de equipe |
| Mês 2 | 1x por semana | Sucesso do Cliente | Expansão de fluxo, otimização de custo |
| Mês 3 em diante | 1x por mês | Sucesso do Cliente + Vendas | Renovação, upsell, roadmap |

---

## Métricas de sucesso do onboarding

Use estas métricas para avaliar se o onboarding foi bem-sucedido:

- **Tempo até primeiro valor:** ≤ 14 dias.
- **Taxa de resolução sem humano:** ≥ 80% no fluxo piloto.
- **SLA de resposta:** cliente tem resposta em ≤ 4h em dias úteis.
- **NPS do onboarding:** ≥ 8/10.
- **Adoção:** ≥ 90% do time monitora o agente regularmente.

---

## Troubleshooting rápido

| Problema | Causa comum | Solução |
|----------|-------------|---------|
| Agente responde errado | Prompt muito amplo | Reforçar regras e exemplos no prompt |
| Agente não escala | Rate limit de API | Aumentar limites ou trocar plano |
| Cliente não confia | Falta de transparência | Mostrar logs e explicar decisões |
| Custo acima do esperado | Memória descontrolada | Ajustar janela de contexto e cache |

---

## Recursos úteis

- [Cases de sucesso](cases.md) — exemplos práticos por segmento.
- [FAQ completa](faq-completa.md) — perguntas frequentes pós-onboarding.
- [Integrations guide](integrations-guide.md) — como conectar ferramentas.
- [LGPD compliance](lgpd-compliance.md) — requisitos legais.
