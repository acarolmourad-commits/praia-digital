# Guia LGPD para Hermes Agents

> Referência completa para equipes de produto, jurídico, compliance e operações que utilizam agentes autônomos de IA em ambientes regulados pela LGPD (Lei nº 13.709/2018).  
> Última atualização: Agosto/2026.

---

## 1. Objetivo e escopo

Este documento estabelece regras e recomendações para o uso de **Hermes Agents** em operações que envolvam dados pessoais de titulares brasileiros. O guia abrange:

- Classificação de dados sensíveis e não sensíveis;
- Bases legais e consentimento;
- Minimização, retenção e descarte;
- Direitos do titular e fluxos de atendimento;
- Responsabilidades do controlador e do operador;
- Medidas técnicas e administrativas;
- Registro de incidentes e notificação à ANPD.

A conformidade não é um recurso opcional: em caso de auditoria, a ANPD pode questionar tanto o **controlador** (cliente final que define as finalidades) quanto o **operador** (Praia Digital/Hermes, que processa em nome do controlador).

---

## 2. Classificação de dados

### 2.1 Dados pessoais comuns
Informações que permitem identificar uma pessoa natural, mas não são sensíveis por si sós.

Exemplos em contexto de atendimento automatizado:
- Nome completo;
- E-mail e telefone;
- Endereço e cidade;
- Histórico de interações e preferências;
- Dados de navegação e dispositivo (IP, user-agent).

### 2.2 Dados pessoais sensíveis
Categoria protegida pelo art. 5º, II, da LGPD. O tratamento exige **base legal específica** e medidas reforçadas.

Exemplos relevantes para agentes autônomos:
- Saúde física ou mental (ex.: prontuários, sintomas relatados, exames);
- Origem racial ou étnica, convicções religiosas;
- Opiniões políticas, filiação a sindicatos;
- Dados genéticos ou biométricos (impressão digital, voz para identificação única);
- Vida sexual ou orientação sexual;
- Dados de menores de idade.

### 2.3 Dados anonimizados vs pseudonimizados
- **Anonimizados**: não permitem identificação do titular, mesmo por meios complementares. Saem do escopo da LGPD quando irreversíveis.
- **Pseudonimizados**: substituem identificadores diretos por pseudônimos, mas podem ser reidentificados com dados auxiliares. Continuam sendo dados pessoais.

> Recomendação: sempre documentar a técnica usada e o risco residual de reidentificação.

---

## 3. Bases legais para tratamento

O agente autônomo deve operar apenas dentro das bases legais declaradas pelo controlador. Não confunda "consentimento do usuário" com "aceite do termo de uso".

| Base legal | Quando usar | Exemplo prático |
|---|---|---|
| **Consentimento** | Tratamento opcional, pode ser revogado. | Envio de ofertas por WhatsApp após opt-in explícito. |
| **Execução de contrato** | Necessário para cumprir um contrato com o titular. | Atendimento pós-venda, agendamento de visita. |
| **Legítimo interesse** | Sem consentimento, desde que não viole direitos fundamentais. | Anti-fraude, segurança da operação, métricas agregadas. |
| **Cumprimento de obrigação legal** | Exigido por lei ou regulamento. | Retenção de registros financeiros, envio de informações ao fisco. |
| **Exercício regular de direitos** | Defesa em processo judicial, administrativo ou arbitral. | Produção de prova em disputa contratual. |

> Hermes Agents devem ser configurados para solicitar apenas os dados estritamente necessários à finalidade declarada, evitando coleta ampla e preventiva.

---

## 4. Consentimento

### 4.1 Requisitos de validade
O consentimento deve ser:
- **Livre**: sem coerção ou condicionamento indevido;
- **Informado**: linguagem clara, finalidade específica, tipos de dados e prazo de retenção explicitados;
- ** Inequívoco**: ação afirmativa do titular (ex.: marcar checkbox, enviar mensagem confirmando "aceito").

### 4.2 Registro do consentimento
Armazene, no mínimo:
- Data e hora do aceite;
- Versão do termo ou política apresentada;
- Identificador do canal (ex.: número de WhatsApp, e-mail, sessão web);
- Base legal declarada.

### 4.3 Revogação
O titular deve poder revogar o consentimento a qualquer momento, por meio de canal simples e gratuito. Após a revogação, interrompa o tratamento vinculado a essa base e comunique o time de operações.

---

## 5. Minimização e finalidade

1. **Coleta limitada**: solicite apenas os dados necessários para cumprir a finalidade do fluxo.
2. **Finalidade explícita**: cada agente deve ter um propósito documentado (ex.: "qualificar leads de imobiliária", "confirmar agendamentos médicos").
3. **Proibição de desvio**: não reuse dados para finalidades não declaradas sem nova base legal.

### Exemplo prático
Um agente de captação de leads não deve solicitar dados de saúde ou renda salarial a menos que a venda exija análise de crédito e essa finalidade esteja declarada no consentimento.

---

## 6. Retenção e descarte

### 6.1 Política de retenção padrão
- **Conversas ativas**: manter enquanto houver relação em andamento ou prazo prescricional aplicável.
- **Logs de sistema e métricas**: até 24 meses, salvo exigência legal diversa.
- **Dados sensíveis**: retenção mínima necessária; priorize exclusão automática após 12 meses ou conclusão da finalidade.

### 6.2 Descarte seguro
Quando o prazo expirar, o descarte deve ser:
- **Irreversível** (sobrescrita, desduplicação, exclusão de backups conforme política);
- **Documentado** (data, identificador do registro, método, responsável).

---

## 7. Direitos do titular

A LGPD garante aos titulares os direitos do art. 18. Hermes Agents devem ser integrados a fluxos que atendam a esses direitos dentro dos prazos legais.

| Direito | Prazo | Implementação recomendada |
|---|---|---|
| **Confirmação e acesso** | 15 dias | Endpoint de consulta de dados armazenados por CPF/e-mail/telefone. |
| **Correção** | 15 dias | Fluxo de edição guiada ou encaminhamento para humano. |
| **Anonimização, bloqueio ou eliminação** | 15 dias | Exclusão por solicitação, com confirmação e log. |
| **Portabilidade** | 15 dias | Exportação de dados em formato estruturado (JSON/CSV). |
| **Informação sobre compartilhamento** | 15 dias | Lista de terceiros com os quais o dado foi compartilhado. |
| **Revogação do consentimento** | Imediato | Interrupção do fluxo e notificação ao operador. |
| **Oposição** | 15 dias | Suspensão de tratamento, salvo base legal diversa. |

> Observação: o descumprimento do prazo de 15 dias pode gerar multa administrativa pela ANPD.

---

## 8. Medidas técnicas e administrativas

### 8.1 Segurança da informação
- Criptografia em trânsito (TLS 1.2+);
- Criptografia em repouso para bases de dados e backups;
- Controle de acesso baseado em funções (RBAC);
- Registro de auditoria (logs de acesso, alterações e exclusões).

### 8.2 Anonimização e privacidade desde a concepção
- Aplicar Privacy by Design e Privacy by Default nos fluxos;
- Avaliar necessidade de dados em cada etapa do diálogo;
- Não registrar dados sensíveis sem justificativa legal documentada.

### 8.3 Fornecimento a terceiros
- Não compartilhar dados pessoais sem contrato de processamento (DPA) e base legal compatível;
- Auditar subcontratados periodicamente.

---

## 9. Incidentes e notificação

### 9.1 Definição de incidente
Qualquer acesso não autorizado, destruição, perda, alteração ou divulgação acidental ou ilícita de dados pessoais.

### 9.2 Procedimento interno
1. **Detecção**: monitoramento contínuo e alertas automáticos.
2. **Contenção**: isolar o componente afetado, preservar evidências.
3. **Avaliação**: identificar categorias de dados, quantidade de titulares, risco e causa raiz.
4. **Notificação**: comunicar a ANPD em prazo razoável (recomenda-se até 48h quando houver risco aos direitos do titular).
5. **Comunicação ao titular**: obrigatória quando houver risco relevante.

### 9.3 Registro
Todo incidente deve ser documentado com:
- Data e hora da descoberta;
- Tipos de dados envolvidos;
- Medidas corretivas adotadas;
- Responsável pela resposta.

---

## 10. Papéis e responsabilidades

| Papel | Responsável | Descrição |
|---|---|---|
| **Controlador** | Cliente final | Define finalidades, bases legais, políticas de retenção e responde perante a ANPD e titulares. |
| **Operador** | Praia Digital / Hermes | Processa dados em nome do controlador, seguindo instruções documentadas e medidas de segurança. |
| **Encarregado (DPO)** | Designado pelo controlador | Canal de comunicação entre controlador, titulares e ANPD. |
| **Equipe de produto** | Praia Digital | Constrói fluxos alinhados às regras deste guia. |

> Hermes Agents não eliminam a responsabilidade do controlador. O cliente final continua responsável pela conformidade da operação.

---

## 11. Checklist de conformidade para agentes autônomos

Antes de colocar um agente em produção, confira:

- [ ] Base legal documentada para cada fluxo;
- [ ] Termo de consentimento ou aviso de privacidade atualizado e linkado;
- [ ] Campos de coopo limitados ao mínimo necessário;
- [ ] Política de retenção configurada (TTL, exclusão automática);
- [ ] Fluxos de atendimento a direitos do titular testados;
- [ ] Logs de auditoria ativados;
- [ ] Criptografia (em trânsito e repouso) validada;
- [ ] DPA com subcontratados assinado;
- [ ] DPO contatado e ciente da operação;
- [ ] Plano de resposta a incidentes revisado.

---

## 12. Glossário rápido

- **ANPD**: Autoridade Nacional de Proteção de Dados.
- **DPA**: Acordo de Processamento de Dados.
- **DPO**: Data Protection Officer / Encarregado de dados.
- **LGPD**: Lei Geral de Proteção de Dados (Lei nº 13.709/2018).
- **Pseudonimização**: substituição de identificadores diretos por pseudônimos.
- **TTL**: tempo de vida útil dos dados (time-to-live).
- **RBAC**: Role-Based Access Control.

---

## 13. Referências

- [LGPD — Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [ANPD — Regulamentos e guias](https://www.gov.br/anpd)
- [Hermes Agents — Documentação oficial](https://hermes-agent.nousresearch.com/docs)
