# Governança de Conteúdo — Hermes Agents

> Guia oficial de governança para criação, revisão, atualização e manutenção do conteúdo sobre Hermes Agents no ecossistema Praia Digital.  
> Versão 1.0 — Agosto/2026

---

## 1. Objetivo

Garantir que todo conteúdo relacionado a Hermes Agents seja preciso, atualizado, consistente e alinhado com a voz da marca, reduzindo retrabalho, riscos regulatórios e desvios estratégicos.

---

## 2. Princípios de governança

| Princípio | Descrição |
|-----------|-----------|
| **Precisão acima de velocidade** | Nenhuma publicação sem revisão factual por especialista de produto. |
| **Rastreabilidade total** | Todo documento tem autor, revisor, data e versão. |
| **Revisão humana em conteúdo crítico** | Preço, LGPD, SLA e roadmap passam por aprovação humana antes de publicar. |
| **Atualização cíclica** | Conteúdo técnico e comercial tem prazo de validade explícito. |
| **Single source of truth** | Documentos canônicos (este guia, glossário, roadmap) não são duplicados. |
| **Acesso e transparência** | Docs públicos e internos são mantidos em repositório versionado. |

---

## 3. Tipos de conteúdo

| Tipo | Exemplos | Sensibilidade | Revisão mínima |
|------|----------|---------------|----------------|
| **Canônico** | Glossário, roadmap, arquitetura, governança | Alta | Autor + Revisor técnico + Aprovação de produto |
| **Comercial** | Cases, pitch deck, script de vendas, pricing | Alta | Autor + Revisor comercial + Aprovação de marketing |
| **Técnico** | Integrações, FAQ, guias de implementação | Média | Autor + Revisor técnico |
| **Operacional** | E-mail sequences, onboarding, templates | Média | Autor + Validação de CS/comercial |
| **Educacional** | Ebook, blog, artigos, material de curso | Baixa | Autor + Revisor editorial |

---

## 4. Fluxo de revisão e aprovação

```mermaid
flowchart LR
    CRIACAO[Autor cria PR/draft] --> REVISAO_TEC[Revisor técnico\nou comercial]
    REVISAO_TEC --> APROVACAO[Aprovador de área\n(Produto/Marketing)]
    APROVACAO --> PUBLICACAO[Publicação]\n{ou} REVISAO
    REVISAO --> CRIACAO
```

### 4.1 Regras por tipo

**Canônico**
- Revisão técnica obrigatória.
- Aprovação de Head de Produto ou CTO.
- Não alterar sem issue documentada.

**Comercial**
- Revisão de vendas/marketing.
- Aprovação de Head Comercial ou Marketing.
- Preços e SLA requerem dupla verificação com finanças/operações.

**Técnico**
- Revisão por engenharia/solução.
- Aprovação de tech lead.
- Testes de integração atualizados.

**Operacional**
- Revisão por CS/comercial.
- Aprovação de coordenação.
- Alinhamento com jurídico quando houver dados sensíveis.

**Educacional**
- Revisão editorial.
- Aprovação de conteúdo/SEO.
- Validação factual quando citar números ou cases.

---

## 5. Responsáveis

| Papel | Responsabilidades | Área |
|-------|-------------------|------|
| **Autor** | Criação, atualização, documentação de alterações | Produto/Engenharia/Marketing |
| **Revisor técnico** | Validação de arquitetura, integrações, viabilidade | Engenharia |
| **Revisor comercial** | Validação de claims de mercado, preço, SLA | Comercial/Marketing |
| **Aprovador** | Aprovação final, alinhamento estratégico | Head de Produto / Head Comercial |
| **Guardian de conteúdo** | Manutenção do glossário e da consistência terminológica | PM/Conteúdo |
| **Dono do roadmap** | Atualização do roadmap e comunicação de mudanças | Produto |
| **Compliance/LGPD** | Revisão de seções sensíveis e políticas de dados | Jurídico/Compliance |

---

## 6. Cronograma de atualização

### 6.1 Frequência recomendada

| Conteúdo | Frequência | Trigger obrigatório |
|-----------|------------|---------------------|
| Glossário | Trimestral | Nova feature ou novo termo não documentado |
| Roadmap | Mensal | Atraso de sprint, mudança de prioridade |
| Arquitetura | Por release | Mudança em componentes, contratos ou protocolos |
| FAQ | Quinzenal | Nova pergunta recorrente ou mudança de comportamento |
| Cases | Por case fechado | Resultado quantificado disponível |
| Integrações | Por integração nova/descontinuada | Mudança em API, auth ou versão |
| Pricing | Mensal ou por reajuste | Alteração de valor, plano ou condição |
| E-mail sequences | Mensal | Queda de resposta > 15% ou mudança de oferta |

### 6.2 Calendário fixo

- **Semana 1**: Revisão de FAQ e integrações.
- **Semana 2**: Atualização de roadmap e cases.
- **Semana 3**: Revisão de glossário e material educativo.
- **Semana 4**: Revisão comercial (pricing, SLA, pitch).

---

## 7. Processo de versionamento

- Arquivos canônicos usam `## Versão X.Y — DD/MM/AAAA`.
- Alterações documentadas em seção de changelog no final do arquivo ou em arquivo de changelog próprio.
- Conteúdo obsoleto é arquivado como `filename.archive.md`, não deletado.
- Acesso por git; branches por feature; PR obrigatório; status de aprovação em comentário do PR.

---

## 8. Métricas e qualidade

| Métrica | Alvo | Frequência |
|----------|------|------------|
| Desatualização máxima permitida | 30 dias para docs técnicas; 15 dias para comerciais | Contínua |
| Tempo médio de aprovação (PR) | < 48h | Semanal |
| Conteúdo desatualizado aberto | 0 | Quinzenal |
| Revisões puladas | 0 | Contínua |
| Glossário descoberto em reuniões | < 1 termo/semana | Semanal |

---

## 9. Políticas complementares

### 9.1 LGPD e segurança
- Nunca documentar dados de clientes reais.
- Mascarar exemplos de payloads e logs.
- Revisão obrigatória de Compliance para qualquer conteúdo que mencione dados pessoais.

### 9.2 Tom e voz
- Seguir guia de tom da marca: profissional, direto, sem jargões desnecessários.
- Hermes Agents é tratado como produto/serviço, nunca como pessoa ou entidade senciente.
- Evitar promessas absolutas ("sempre", "nunca", "100%") sem respaldo em SLA documentado.

### 9.3 Consistência terminológica
- Usar sempre termos do glossário oficial.
- Proibir sinônimos não documentados para conceitos centrais (ex: "agente autônomo" sempre que possível, não "robô" em docs técnicas).
- Novos termos passam por registro prévio no glossário antes de uso em docs.

---

## 10. Audit trail

Cada documento canônico deve conter:

```markdown
---
autor: Nome Sobrenome
revisor: Nome Sobrenome
aprovador: Nome Sobrenome
criado_em: DD/MM/AAAA
atualizado_em: DD/MM/AAAA
versao: X.Y
changelog:
  - X.Y — DD/MM/AAAA — Descrição curta da mudança
---
```

---

## 11. Incidentes

- Conteúdo impreciso publicado deve ser corrigido em até 4h úteis.
- Incidente documentado em `docs/ai/incidentes-conteudo.md` com causa, impacto e ação corretiva.
- Revisão de processo após 3 ocorrências no mesmo trimestre.
