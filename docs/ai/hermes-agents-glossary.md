# Glossário Técnico — Hermes Agents

> Terminologia oficial do ecossistema Hermes Agents.  
> Use este glossário como referência única para evitar ambiguidades em docs, vendas e código.  
> Versão 1.0 — Agosto/2026

---

## A

**Agente autônomo**  
Unidade de software capaz de perceber ambiente, tomar decisões e executar ações para atingir objetivos, com supervisão humana definida por regras.

**Agente de atendimento**  
Agente voltado para recepção, qualificação inicial e resposta a consultas frequentes em canais de comunicação.

**Agente de dados**  
Agente especializado em consultar fontes de dados estruturadas e não estruturadas, gerando relatórios e insights sem intervenção humana.

**Agente de prospecção**  
Agente responsável por identificar, abordar e qualificar leads em canais como WhatsApp, e-mail ou redes sociais.

**Agente de suporte**  
Agente focado em resolução de tickets, dúvidas pós-venda e orientações de uso do produto/serviço.

**Agente vertica pré-treinado**  
Pacote de agente com fluxos, vocabulário e integrações pré-configurados para um segmento específico (ex: imobiliária, clínica).

**API pública**  
Interface de programação exposta para que clientes enterprise integrem seus sistemas diretamente com a plataforma Hermes Agents.

**Aprovação humana (human-in-the-loop)**  
Camada de validação obrigatória antes de ações críticas, como disparo de comunicações externas ou alteração de regras de negócio.

**Arquitetura multiagente**  
Padrão onde múltiplos agentes especializados cooperam sob um orquestrador, com papéis e responsabilidades distintos.

**Audit trail (rastro de auditoria)**  
Registro cronológico e imutável de todas as ações executadas por agentes, incluindo entrada, decisão e saída.

**Automação comercial**  
Conjunto de agentes e fluxos que executam etapas do funil de vendas sem intervenção humana direta.

---

## B

**Backend**  
Camada de servidores, banco de dados e lógica de negócio que sustenta a execução dos agentes.

**Base de conhecimento (knowledge base)**  
Repositório de documentos, FAQs, políticas e procedimentos consultado pelos agentes para contextualizar respostas.

**Batch**  
Execução de múltiplas tarefas em grupo, tipicamente usada em prospecção ou disparos de e-mail/WhatsApp.

**Bot**  
Interface conversacional automatizada. No contexto Hermes, refere-se à frente de interação com usuário final; não deve ser confundido com agente autônomo, que executa fluxos complexos.

**Briefing de agente**  
Documento que define objetivo, papel, restrições e ferramentas disponíveis para um agente específico.

---

## C

**Canal**  
Meio de comunicação por onde o agente interage com usuários finais (ex: WhatsApp Business API, Telegram, e-mail, web chat).

**Changelog**  
Registro estruturado de alterações em um documento ou versão de software.

**Chatbot**  
Sistema que responde mensagens com base em regras ou LLM isolado, sem capacidade de execução autônoma de fluxos complexos.

**CI/CD**  
Integração contínua e entrega contínua; pipeline automatizado de testes e deploy.

**Claims de marketing**  
Afirmações comerciais sobre desempenho, segurança ou conformidade que requerem respaldo documentado.

**Compliance**  
Conformidade com normas, regulamentos e políticas internas, incluindo LGPD.

**Context store**  
Armazenamento do estado da conversação e variáveis de sessão mantidas durante a interação.

**Conversational AI**  
Tecnologia de IA focada em interação em linguagem natural, incluindo compreensão e geração de texto.

**Custo por sessão**  
Métrica financeira que mede o custo operacional de uma conversa completa com agente, incluindo tokens, infra e ferramentas.

---

## D

**Dashboard de observabilidade**  
Painel com métricas, logs e alertas sobre saúde e desempenho dos agentes em produção.

**Dead letter queue (DLQ)**  
Fila de mensagens que falharam no processamento após retries, usada para inspeção manual ou reprocessamento.

**Disparo**  
Envio ativo de mensagem proativa por parte de um agente (ex: follow-up, oferta, lembrete).

**Documentação canônica**  
Documentos considerados fonte oficial e imutável até nova versão aprovada (ex: glossário, arquitetura).

---

## E

**Edge case**  
Cenário raro ou extremo no fluxo do usuário que pode causar falhas ou comportamentos inesperados.

**E-mail sequence**  
Sequência automatizada de e-mails enviados com base em gatilhos ou tempo, geralmente usada em nurturing ou follow-up.

**Engine LLM**  
Modelo de linguagem subjacente que alimenta os agentes (ex: GPT, Claude, Gemini, LLaMA).

**Entidade**  
Pessoa, organização ou sistema com o qual o agente interage (ex: lead, cliente, usuário final).

**Escalação (handoff)**  
Transferência do controle da conversa do agente para um operador humano, tipicamente em casos complexos ou sensíveis.

**Estrutura de prompt**  
Template sistematizado para orientar o LLM, incluindo papel, contexto, regras e formato de saída.

---

## F

**Fallback**  
Comportamento alternativo quando o agente não consegue resolver uma solicitação (ex: transferir para humano, responder com mensagem padrão).

**Feature flag**  
Interruptor que habilita/desabilita funcionalidades em produção sem deploy de código.

**Fila de eventos**  
Buffer assíncrono que organiza mensagens e ações para processamento ordenado e resiliente.

**Fluxo (flow)**  
Sequência definida de passos, decisões e ações que um agente executa para cumprir um objetivo.

**Follow-up**  
Acompanhamento automático ou manual de uma interação anterior, com objetivo de avançar no funil.

---

## G

**Gatilho (trigger)**  
Evento que inicia a execução de um fluxo ou agente (ex: mensagem recebida, formulário preenchido, falha de pagamento).

**Governança de conteúdo**  
Conjunto de políticas, papéis e cronogramas que garantem qualidade, precisão e alinhamento do conteúdo publicado.

**Guardrails**  
Restrições programáticas ou textuais que impedem o agente de executar ações perigosas, ilegais ou fora do escopo.

**Guião (playbook)**  
Conjunto padronizado de passos e regras para execução de um processo por agente ou operador humano.

---

## H

**Handoff**  
Ver Escalação.

**Health score**  
Indicador composto que avalia a saúde da conta de um cliente com base em uso, satisfação e pagamentos.

**Human-in-the-loop**  
Ver Aprovação humana.

---

## I

**IA generativa**  
Modelo de inteligência artificial capaz de gerar texto, imagem, áudio ou código original a partir de instruções.

**Imutabilidade**  
Propriedade de registros que não podem ser alterados após criação; essencial para logs e audit trails.

**Ingest layer**  
Camada responsável por receber, validar e normalizar eventos de diferentes canais antes do processamento.

**Integração nativa**  
Conector oficial e suportado entre Hermes Agents e uma ferramenta externa (CRM, ERP, agenda).

**Intent (intenção)**  
Objetivo subjacente de uma mensagem do usuário, classificado pelo agente para escolher o fluxo correto.

**Invalidação de cache**  
Processo de atualizar ou remover dados cached quando a fonte de verdade mudou.

---

## J

**Jailbreak**  
Tentativa de contornar regras ou guardrails do agente por meio de prompts engenhosos; mitigado por validação contínua.

---

## K

**KPI (Key Performance Indicator)**  
Indicador-chave de desempenho usado para medir sucesso (ex: tempo de resposta, taxa de agendamento).

**Knowledge base**  
Ver Base de conhecimento.

---

## L

**Latência**  
Tempo entre uma entrada (ex: mensagem do usuário) e a resposta do agente.

**Lead**  
Potencial cliente que interage com a marca e pode ser qualificado e nutrido por agentes.

**LGPD**  
Lei Geral de Proteção de Dados (Brasil); conformidade obrigatória no tratamento de dados pessoais.

**LLM (Large Language Model)**  
Modelo de linguagem de grande escala, base de muitos agentes modernos.

**Log estruturado**  
Registro de evento em formato padronizado (ex: JSON), com campos como timestamp, nível, agente, ação e resultado.

**Loop de feedback**  
Ciclo de coleta de avaliações humanas para refinamento contínuo do agente.

---

## M

**Marketplace de integrações**  
Loja de conectores oficiais e comunitários que ampliam as capacidades dos agentes.

**Memória de curto prazo**  
Contexto da sessão atual, descartado após término da interação.

**Memória de longo prazo**  
Dados persistidos (ex: preferências, histórico) que sobrevivem a múltiplas sessões.

**Metric**  
Métrica quantitativa coletada automaticamente (ex: tempo de resposta, taxa de erro, custo por token).

**Modelo de assinatura**  
Modelo de receita recorrente (SaaS) típico de Hermes Agents, com planos baseados em uso ou número de agentes.

**MRR (Monthly Recurring Revenue)**  
Receita recorrente mensal, indicador central de crescimento de negócios SaaS.

**Multiagente**  
Ver Arquitetura multiagente.

---

## N

**NLP (Natural Language Processing)**  
Processamento de linguagem natural; área da IA que permite a computadores entender e gerar texto humano.

**No-code/low-code**  
Abordagem que reduz ou elimina a necessidade de programação para configurar fluxos e agentes.

**NPS (Net Promoter Score)**  
Métrica de satisfação que mede a probabilidade de recomendação em escala de 0 a 10.

---

## O

**Observabilidade**  
Capacidade de entender o estado interno de um sistema a partir de logs, métricas e traces.

**Onboarding**  
Processo de configuração inicial e treinamento do agente para um novo cliente.

**Orquestração**  
Coordenação de múltiplos agentes, ferramentas e fluxos para atingir objetivos complexos.

**Orquestrador**  
Componente central que distribui tarefas, gerencia estado e garante rastreabilidade entre agentes.

---

## P

**Padrão (playbook)**  
Ver Guião.

**Painel (dashboard)**  
Interface visual que consolida métricas e status para operadores e gestores.

**Payload**  
Corpo de dados de uma requisição ou mensagem enviada/recebida por um agente.

**Persona**  
Perfil sintético de usuário final usado para treinar e validar o comportamento do agente.

**Playground**  
Ambiente isolado para testes de fluxos e prompts antes da publicação em produção.

**PM (Product Manager)**  
Responsável por definir prioridades, roadmap e sucesso do produto.

**Pricing**  
Estrutura de preços, planos e condições comerciais do produto.

**Prompt**  
Instrução fornecida ao LLM para guiar a resposta ou ação do agente.

**Prompt engineering**  
Prática de projetar, testar e otimizar prompts para obter resultados consistentes e seguros.

---

## Q

**Qualificação de lead**  
Processo de avaliação do potencial de conversão de um lead, geralmente executado por agente de atendimento/prospecção.

**Queue**  
Fila de espera para processamento de eventos ou mensagens.

---

## R

**RAG (Retrieval-Augmented Generation)**  
Técnica que combina busca em base de conhecimento com geração de texto para respostas fundamentadas.

**Rate limit**  
Limite de requisições ou tokens por período, imposto por modelos LLM ou APIs externas.

**Recall**  
Métrica de busca/recuperação: proporção de documentos relevantes efetivamente retornados.

**Replay**  
Reprodução controlada de interações para auditoria ou depuração.

**Resiliência**  
Capacidade do sistema de se recuperar de falhas sem perda de dados ou interrupção prolongada.

**Retry**  
Tentativa automática de reprocessar uma ação que falhou, com limite e backoff.

**ROI (Return on Investment)**  
Retorno sobre investimento, métrica econômica que compara ganhos e custos.

**Router de intenção**  
Componente que classifica a intenção do usuário e direciona para o agente ou fluxo adequado.

---

## S

**SaaS (Software as a Service)**  
Modelo de distribuição de software por assinatura, com infraestrutura gerenciada pelo provedor.

**Schema validation**  
Validação da estrutura e tipos de dados em eventos ou payloads antes do processamento.

**Sessão**  
Período contíguo de interação entre usuário e agente, com contexto isolado.

**SLA (Service Level Agreement)**  
Acordo de nível de serviço que define metas de disponibilidade, tempo de resposta e suporte.

**Stateful**  
Sistema que mantém estado entre interações; oposto de stateless.

**Stateless**  
Sistema que não mantém estado entre requisições; cada chamada é independente.

**Suporte técnico**  
Serviço de resolução de incidentes, dúvidas e configurações para clientes.

**Summarização**  
Técnica de condensar conteúdo longo (ex: histórico de conversa) em versão compacta para economia de tokens.

---

## T

**TAM (Total Addressable Market)**  
Mercado endereçável total; métrica de sizing de mercado.

**Tempo de resposta**  
Intervalo entre a recepção de uma mensagem e a primeira resposta do agente.

**Token**  
Unidade básica de processamento em LLMs; pode ser palavra, parte de palavra ou caractere.

**Tool use**  
Capacidade do agente de invocar funções externas (busca, cálculo, API) durante a execução.

**Trace**  
Rastro completo de uma execução, ligando entradas, decisões intermediárias e saídas.

**Trigger**  
Ver Gatilho.

---

## U

**UI de playbook**  
Interface gráfica que permite configurar fluxos de agente sem código.

**Uptime**  
Tempo em que o sistema permanece disponível e operacional, geralmente expresso em porcentagem.

**Usuário final**  
Pessoa que interage com o agente por meio de canais (ex: lead, cliente, paciente).

---

## V

**Validação de schema**  
Ver Schema validation.

**Vector store**  
Banco de dados especializado em armazenar e buscar embeddings (representações vetoriais de texto), usado em RAG e memória de longo prazo.

**Versionamento**  
Controle de alterações em documentos e código, permitindo auditoria e rollback.

**Vertical**  
Segmento de mercado com necessidades específicas (ex: imobiliária, clínica, e-commerce).

---

## W

**White-label**  
Produto customizado com marca do cliente, permitindo revenda ou uso como solução própria.

---

## Y

**Yield**  
Taxa de sucesso em uma operação; em prospecção, proporção de respostas positivas por contatos realizados.

---

## Anexo: Siglas frequentes

| Sigla | Significado |
|--------|-------------|
| API | Application Programming Interface |
| CS | Customer Success |
| DLQ | Dead Letter Queue |
| GA | General Availability |
| IA | Inteligência Artificial |
| KPI | Key Performance Indicator |
| LGPD | Lei Geral de Proteção de Dados |
| LLM | Large Language Model |
| MRR | Monthly Recurring Revenue |
| NPS | Net Promoter Score |
| NLP | Natural Language Processing |
| PM | Product Manager |
| RAG | Retrieval-Augmented Generation |
| ROI | Return on Investment |
| SaaS | Software as a Service |
| SLA | Service Level Agreement |
| TAM | Total Addressable Market |
| UI | User Interface |
| UX | User Experience |
| WA | WhatsApp Business API |
