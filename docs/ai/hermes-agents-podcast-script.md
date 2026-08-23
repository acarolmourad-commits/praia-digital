# Roteiro de Podcast: Agentes Autônomos no Brasil — O Futuro dos Negócios em 30 Minutos

**Formato:** Podcast / Entrevista  
**Duração:** ~30 minutos  
**Host:** Lucas Mendes (Host do "Tech Brasil Hoje")  
**Convidado:** Carolina Alves (Head de Inovação — Praia Digital / Hermes)  
**Tom:** Informativo, acessível, sem jargão desnecessário  
**Público-alvo:** Empreendedores, gerentes de operações, entusiastas de IA

---

## Abertura (0:00 – 2:00)

**Host:**  
— Olá e bem-vindos a mais um episódio do *Tech Brasil Hoje*. Eu sou Lucas Mendes. Hoje vamos falar de um tema que parece ficção, mas já está mudando negócios no país: agentes autônomos. Não os chatbots de antes, que respondiam perguntas fixas, mas agentes que operam, vendem, follow up e resolvem problemas sem precisar de um humano no meio de cada passo. Para entender como isso funciona na prática aqui no Brasil, quem está construindo essa realidade na Praia Digital, e o que o mercado ainda precisa aprender, eu conversei com Carolina Alves, Head de Inovação da Praia Digital e responsável pelo ecossistema Hermes Agents. Carolina, muito obrigado por vir.

**Carolina:**  
— Obrigada, Lucas. É um prazer estar aqui. E já começo dizendo: o Brasil não está só consumindo IA — está criando casos de uso de agentes autônomos que fazem sentido para a nossa realidade.

**Host:**  
— Perfeito. Vamos direto ao ponto. O que é, de verdade, um "agente autônomo", sem a buzzword?

**Carolina:**  
— Eu gosto de explicar assim: um agente autônomo é um sistema de IA que tem um objetivo, um contexto e a capacidade de agir por conta própria para chegar lá — não um humano apertando botão a cada etapa. Ele lê e-mails, qualifica leads, agenda reuniões, dispara follow-ups, enriquece dados e até escala operações inteiras — tudo em fluxos contínuos.

---

## Bloco 1: O que mudou em 2025/2026 (2:00 – 9:00)

**Host:**  
— Por que agora? Por que 2025/2026 é diferente dos anos anteriores de "vamos automatizar"?

**Carolina:**  
— Três fatores. Primeiro: os LLMs (Large Language Models) finalmente entendem ambiguidade e contexto em português com qualidade. Segundo: ferramentas como MCP, tool-use nativo e memória persistente tornaram viável fazer agentes que lembram de conversas e mantêm estado. Terceiro: casos de sucesso sinalizaram ROI real — não é só hype, é ponto de equilíbrio econômico para pequenas e médias empresas.

**Host:**  
— E no Brasil, especificamente, onde você vê mais impacto?

**Carolina:**  
— Dois setores fortes: **imobiliárias** e **prestadores de serviço**. Porque têm operação repetitiva, alto volume de atendimento e precisam de follow-up rápido. O Hermes Agents, por exemplo, hoje roda prospecção de WhatsApp, qualificação de leads e agendamento para imobiliárias do litoral — sem que o corretor precise escrever cada mensagem.

**Host:**  
— Então não é só "criar um chatbot"?

**Carolina:**  
— Não. Chatbot é interface. Agente autônomo é **operador**. Ele tem permissão para executar ações: abrir ticket, atualizar CRM, enviar e-mail, mudar status de lead. Isso muda tudo.

---

## Bloco 2: Casos práticos brasileiros (9:00 – 17:00)

**Host:**  
— Conte um caso real que você acompanhou.

**Carolina:**  
— Um exemplo concreto: uma imobiliária de Bertioga com 3 corretores estava perdendo leads por demora no retorno. Implementamos um agente autônomo que recebe o WhatsApp, faz perguntas de qualificação (tipo de imóvel, local, orçamento), classifica o lead como "quente" ou "morno" e agenda automaticamente uma visita. Resultado: taxa de resposta subiu de 22% para 68% em 30 dias, e os corretores gastam menos tempo com leads frios.

**Host:**  
— E os corretores não rejeitaram por "perder o toque humano"?

**Carolina:**  
— Pelo contrário: eles passaram a atender só leads quentes. O agente filtra o ruído. A humanização ficou onde realmente importa — na negociação e no fechamento.

**Host:**  
— E fora de imobiliária?

**Carolina:**  
— Outro caso: uma rede de clínicas odontológicas usando agente para reagendamento proativo. O agente analisa faltas, envia WhatsApp com opções de horário e confirma em tempo real. Redução de 30% em faltas. Esse tipo de automação não substitui a recepcionista; ela deixa a recepcionista fazer o que importa — receber o paciente.

---

## Bloco 3: Como começar sem dor (17:00 – 23:00)

**Host:**  
— Para o ouvinte que quer implementar agora, qual o primeiro passo? Porque todo mundo quer "um agente autônomo" de uma vez.

**Carolina:**  
— Eu sempre digo: comece por **um processo**, não por uma tecnologia. Mapeie uma tarefa repetitiva que custa tempo e dinheiro — follow-up de lead, qualificação de chamados, agendamento. Depois, desenhe o fluxo ideal em 5 passos: entrada, classificação, ação, handoff e aprendizado. Só então escolha a ferramenta.

**Host:**  
— Ferramenta no Brasil... vocês usam o quê?

**Carolina:**  
— Stack comum por aqui: Python para o núcleo do agente, LLM com function calling (OpenAI, Anthropic ou até Llama/ Mistral rodando local por LGPD), MCP para conectar ferramentas externas (CRM, WhatsApp, e-mail) e um banco vetorial pequeno para memória de curto prazo. Para WhatsApp, APIs como o Twilio ou soluções nacionais homologadas pela Anatel.

**Host:**  
— E o tal do MCP... explique para quem está ouvindo.

**Carolina:**  
— O Model Context Protocol é um padrão que permite ao agente "chamar ferramentas" de forma padronizada. Em vez de escrever código customizado para cada API, você cria um conector MCP e o agente já sabe usar. Isso acelera muito o desenvolvimento e reduz retrabalho.

**Host:**  
— E custa caro?

**Carolina:**  
— Depende. Um agente simples de qualificação de leads pode sair de R$ 500 a R$ 2 mil por mês em infra, incluindo API de LLM e WhatsApp. Para PMEs, isso se paga em menos de um ciclo de venda. O barato sai caro quando você perde lead por demora.

---

## Bloco 4: Mitos e desafios (23:00 – 27:00)

**Host:**  
— Quais os maiores mitos sobre agentes autônomos no Brasil?

**Carolina:**  
— Mito 1: "Precisa de uma equipe de engenheiros caros". Não para casos básicos. Hoje existem frameworks no-code/low-code que permitem prototipar em um dia. Mito 2: "Vai substituir todo mundo". Não. Vai amplificar a operação existente. Mito 3: "LGPD impede". Desde que o agente trate dados com consentimento, transparência e minimização, está dentro da lei.

**Host:**  
— E os desafios reais?

**Carolina:**  
— **Integração com legado:** muitos CRMs no Brasil são ruins de integrar. **Confiabilidade:** agentes erram se o fluxo não estiver bem desenhado. **Métrica:** você precisa medir taxa de sucesso, tempo de resolução e handoff humano — não só "quantos agentes eu tenho".

---

## Encerramento (27:00 – 30:00)

**Host:**  
— Carolina, obrigado. Onde as pessoas encontram mais conteúdo e cases da Praia Digital sobre isso?

**Carolina:**  
— No blog praia.digital, na seção de IA, e no canal do YouTube com tutoriais curtos. Também temos um repositório público com arquiteturas de referência para agentes autônomos em operações brasileiras.

**Host:**  
— Vou deixar todos os links na descrição. Carolina Alves, Head de Inovação da Praia Digital, muito obrigada.

**Carolina:**  
— Eu que agradeço, Lucas. Vamos construir o futuro — e ele é autônomo.

**Host:**  
— E por hoje é isso. Na semana que vem, vamos falar de como pequenas construtoras estão usando IA para reduzir custo de obra. Não percam. Até lá.

---

## Notas de Produção

- **Duração por bloco:** abertura 2min | mudança de paradigma 7min | casos práticos 8min | como começar 6min | mitos/desafios 4min | encerramento 3min.
- **Trilha sonora:** instrumental suave de fundo; sem cortes durante a fala da convidada.
- **CTA final:** link para `https://praia.digital/blog/agentes-autonomos-tutorial-tecnico-2026` e para o e-book "Agentes Autônomos no Brasil".
- **Reverência de marca:** mencionar "Hermes Agents" pelo menos duas vezes no episódio.
