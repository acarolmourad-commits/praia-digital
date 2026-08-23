# Estrutura de Webinar: Agentes Autônomos para Operações Brasileiras
**Duração:** 45 minutos + 15 minutos de Q&A  
**Formato:** Apresentação ao vivo com slides + demo  
**Público:** Donos de negócio, heads de operação, CTOs de PMEs  
**Slides:** Markdown estruturado (compatível com Reveal.js / Slidev / PDF)

---

## Slide 1 – Abertura (1 min)

**Título:** Agentes Autônomos no Brasil: O Que Realmente Funciona em 2026  
**Subtítulo:** Da teoria à operação — cases, stack e como começar  
**Apresentador:** Carolina Alves — Head de Inovação, Praia Digital  
**Rodapé:** @praiadigital | praia.digital/agentes

---

## Slide 2 – Agenda (1 min)

- O que é um agente autônomo (e o que NÃO é)
- Por que o Brasil está num momento único
- 3 cases reais de operação
- Arquitetura de referência passo a passo
- Mitos que atrasam implementações
- Roadmap: como começar na sua empresa

---

## Slide 3 – O que é um agente autônomo (3 min)

**Headline:** Chatbot ≠ Agente  
**Conteúdo:**
- Chatbot: interface reativa (pergunta → resposta)
- Agente autônomo: sistema ativo com objetivo, ferramentas e memória
- Exemplo: corretor que qualifica leads, agenda visita e atualiza CRM — sem intervenção humana por lead

**Visual:** Diagrama simples: Input → [Agente com Ferramentas] → Ação → Resultado

**Nota de apresentação:**  
“Se o sistema só responde quando perguntam, é chatbot. Se ele toma decisões e executa ações para chegar a um objetivo, é agente.”

---

## Slide 4 – Componentes centrais (4 min)

**Headline:** Os 5 blocos de um agente autônomo

1. **Objetivo (Goal):** o que ele deve alcançar
2. **Percepção (Perception):** como ele entende o mundo (texto, e-mail, WhatsApp, CRM)
3. **Planejamento (Planning):** sequência de ações para chegar ao objetivo
4. **Ação (Action):** execução via ferramentas conectadas (MCP, APIs)
5. **Memória (Memory):** curto prazo (contexto da conversa) e longo prazo (aprendizado)

**Nota:**  
“Sem memória, o agente esquece o que o usuário disse 5 minutos atrás. Sem planejamento, ele age de forma aleatória. Sem objetivo, ele é só um modelo de linguagem.”

---

## Slide 5 – Por que 2026 é diferente (3 min)

**Headline:** Três condições que se alinharam no Brasil

1. **Modelos multilíngues robustos:** LLMs em português com function calling
2. **Protocolos abertos:** MCP, A2A e OpenClaw permitem reuso de ferramentas
3. **Custo viável:** infra e APIs tornam acessível para PMEs

**Visual:** Timeline 2023 → 2024 → 2025 → 2026 com ícones

---

## Slide 6 – Case 1: Imobiliária (5 min)

**Headline:** Prospecção autônoma no litoral paulista  
**Empresa:** Imobiliária parceira Praia Digital (3 corretores)

**Antes:**
- Tempo de resposta: 4h em média
- Leads quentes perdidos para concorrentes
- Corretores gastam 60% do dia com qualificação

**Depois:**
- Agente Hermes no WhatsApp qualifica e classifica leads
- Agenda visitas automaticamente
- Corretores recebem apenas leads quentes

**Resultado:** +186% taxa de resposta | -40% tempo de qualificação

**Demo ao vivo (opcional):**  
Mostrar fluxo de WhatsApp no celular.

---

## Slide 7 – Case 2: Rede de clínicas (4 min)

**Headline:** Reagendamento proativo reduz faltas  
**Empresa:** Rede OdontoVida (12 unidades)

**Fluxo:**
- Agente consulta agenda de amanhã
- Identifica consultas sem confirmação
- Envia WhatsApp com opções de reagendamento
- Confirma ou realoca automaticamente

**Resultado:** -32% faltas | economia de ~R$ 18k/mês em horários ociosos

---

## Slide 8 – Case 3: E-commerce de móveis (4 min)

**Headline:** Pós-venda e garantia sem fila de atendimento  
**Empresa:** LojaMóvel SP

**Fluxo:**
- Cliente envia mensagem sobre garantia/defeito
- Agente abre chamado, consulta policy e envia código de postagem
- Atualiza status e notifica cliente em cada etapa

**Resultado:** CSAT subiu de 3,1 para 4,6/5 | tempo de resposta caiu de 48h para 12min

---

## Slide 9 – Arquitetura de referência (5 min)

**Headline:** Stack enxuta para agentes brasileiros

```
Interface (WhatsApp / Web / E-mail)
        ↓
  Orquestrador (Python + LangGraph / CrewAI)
        ↓
  LLM (GPT-4o / Claude / Llama 3 local)
        ↓
  Camada de Ferramentas (MCP)
        ↓
  Integrações (CRM, Agenda, WhatsApp API, Banco Vetorial)
```

**Princípios:**
- Mínimo viável primeiro (1 processo, não 5)
- Logs e observabilidade desde o dia 1
- Handoff humano explícito para exceções

---

## Slide 10 – Mitos que atrasam (3 min)

**Mito 1:** “Precisa de equipe de elite”  
→ Falso: protótipos em 1 dia com low-code; time sênior só para produção.

**Mito 2:** “LGPD impede”  
→ Falso: desde que haja consentimento, minimização e transparência.

**Mito 3:** “Vai substituir toda a equipe”  
→ Falso: amplifica operação; humanos ficam com o que importa (relacionamento, exceções).

**Mito 4:** “É muito caro”  
→ Falso: ROI em menos de 1 ciclo de venda para a maioria dos casos B2B/B2C.

---

## Slide 11 – Como começar em 5 passos (3 min)

1. **Mapeie** um processo repetitivo com ROI visível
2. **Desenhe** o fluxo ideal (entrada → classificação → ação → handoff → aprendizado)
3. **Escolha** uma ferramenta enxuta (evite “plataforma tudo-em-um” no começo)
4. **Implemente** o MVP em 1 semana
5. **Meça** taxa de sucesso, tempo de resolução e NPS dos usuários

**Nota:**  
“Não comece por um chatbot genérico. Comece por uma tarefa específica que você consegue medir.”

---

## Slide 12 – Roadmap de maturidade (2 min)

- **Nível 1:** Agente reativo (responde perguntas)
- **Nível 2:** Agente com ferramentas (executa ações)
- **Nível 3:** Agente com memória (lembra contexto)
- **Nível 4:** Agente com planejamento (desenha planos)
- **Nível 5:** Agente com aprendizado (melhora com o tempo)

**Mensagem:**  
“Você não precisa chegar no nível 5 no primeiro mês. Nível 2 já entrega valor.”

---

## Slide 13 – Próximos passos (1 min)

- Baixe o e-book gratuito: “Agentes Autônomos no Brasil”
- Participe da comunidade no Telegram
- Teste o template open-source de agente no GitHub
- Agende uma conversa de 15min: `https://praia.digital/contato`

---

## Slide 14 – Q&A (15 min)

**Título:** Perguntas e Respostas  
**Nota para o moderador:**  
- Preparar 3 perguntas-padrão para caso a audiência fique em silêncio
- Disponibilizar link do formulário de contato no chat
- Oferecer envio da gravação e slides por e-mail

---

## Notas Técnicas para Produção

| Item | Detalhe |
|------|---------|
| Plataforma de slides | Reveal.js (HTML) ou Slidev (Markdown) |
| Duração total | 45min apresentação + 15min Q&A |
| Legendas | Sim (acessibilidade + YouTube) |
| Gravação | Cortar intervalos; manter apenas conteúdo |
| Follow-up | E-mail com PDF dos slides + CTA para download do e-book |
