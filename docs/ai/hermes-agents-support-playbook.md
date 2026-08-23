# Playbook de Suporte ao Cliente — Hermes Agents

> Última atualização: Agosto/2026  
> Uso: suporte nível 1 e 2, time de sucesso do cliente, handoff operacional.  
> Objetivo: resolver problemas comuns em até 4h, escalar corretamente e evitar ruído.

---

## Princípios

1. **Transparência primeiro:** mostre logs antes de concluir.
2. **Menos intervenção:** ajuste prompt/configuração antes de culpar o cliente.
3. **Escala por gravidade:** problemas de produção > dúvidas > melhorias.
4. **Documente tudo:** toda intervenção gera um registro no CRM.

---

## Níveis de suporte

| Nível | Responsável | Tipos de problema | SLA |
|-------|-------------|-------------------|-----|
| N1 — Autoatendimento | Cliente / Docs | Dúvidas de uso, configuração básica | 4h úteis |
| N2 — Suporte especializado | Sucesso do Cliente | Ajustes de prompt, regras, relatórios | 4h úteis |
| N3 — Engenharia | Engenharia | Bugs, quedas, integrações quebradas | 1h (produção) / 4h (homologação) |
| N4 — Arquitetura | Arquitetura + Vendas | Expansão, mudança de modelo, novos fluxos | Sob demanda |

---

## Playbooks por categoria

### 1. Dúvidas de uso

**Sintomas:** cliente pergunta como fazer X, onde encontrar Y, o que significa Z.

**Ação N1:**
- Encaminhar para docs relevantes:
  - [FAQ iniciantes](faq-iniciantes.md)
  - [Glossário](glossario.md)
  - [Integrations guide](integrations-guide.md)
- Se a dúvida persistir, agendar call curta (15 min) com Sucesso do Cliente.

**Não faça:** alterar configurações sem pedido explícito.

---

### 2. Ajustes de prompt ou regra

**Sintomas:** agente responde de forma errada, esquece informação, usa tom inadequado.

**Ação N2:**
1. Pedir ao cliente exemplos de interações ruins (prints ou logs).
2. Identificar se o problema é prompt, memória ou ferramenta.
3. Propor ajuste e testar em homologação.
4. Aplicar em produção e acompanhar por 48h.

**Tempo estimado:** 30–90 min por ajuste.

---

### 3. Queda ou lentidão

**Sintomas:** agente não responde, timeout, erro 500/429.

**Ação N3:**
1. Verificar status da API de LLM (dashboard do provedor).
2. Verificar rate limits e consumo diário.
3. Verificar integrações (WhatsApp, e-mail, CRM) — testar conectividade.
4. Se for queda do provedor: avisar cliente, ativar fallback manual, acompanhar status page.
5. Se for configuração: corrigir e validar.

**Comunicação:** enviar aviso proativo ao cliente a cada 30 min até restauração.

---

### 4. Erro de integração

**Sintomas:** agente não envia mensagem, não atualiza CRM, não consulta banco.

**Ação N3:**
1. Verificar credenciais e tokens (expirados? revogados?).
2. Testar integração isoladamente (cURL/Postman).
3. Verificar logs de erro do agente.
4. Aplicar fix ou solicitar nova credencial ao cliente.
5. Validar em homologação antes de produção.

---

### 5. Problema de qualidade (resposta errada recorrente)

**Sintomas:** cliente reporta que o agente “alucina”, envia informação incorreta ou ignora regra.

**Ação N2 → N3 (se persistir):**
1. Coletar 10+ exemplos de falha.
2. Mapear padrão: é sempre o mesmo tipo de pergunta? Falta de contexto?
3. Ajustar prompt ou adicionar few-shot examples.
4. Se for problema do modelo: avaliar troca de modelo (ex.: GPT-4o → Claude Sonnet).

---

### 6. Expansão ou novo fluxo

**Sintomas:** cliente quer automatizar mais um processo.

**Ação N4:**
1. Revisar contrato/escopo atual.
2. Apresentar proposta de expansão (esforço, custo, prazo).
3. Se aprovado, seguir fluxo de onboarding para novo fluxo.

---

## Escalação

```
N1 (cliente) → N2 (sucesso do cliente) → N3 (engenharia) → N4 (arquitetura + vendas)
```

**Regras de escalação:**
- Se não houver resposta em 4h úteis, escalar automaticamente.
- Problemas de produção (queda, erro em massa) sobem direto para N3.
- Clientes enterprise têm canal direto com N3.

---

## Templates de comunicação

### Aviso de indisponibilidade

> Olá, [Nome]. Estamos investigando uma intermitência no agente [nome].  
> Status atual: [descrição].  
> Previsão de normalização: [horário].  
> Qualquer dúvida, responda este canal.  
> — Equipe Praia Digital

### Resolução confirmada

> Olá, [Nome]. O problema no agente [nome] foi resolvido.  
> Causa raiz: [breve explicação].  
> Ações preventivas: [se houver].  
> Se notar algo diferente nas próximas 2h, avise-nos.  
> — Equipe Praia Digital

### Pedido de informação

> Olá, [Nome]. Para continuar o atendimento do chamado [número], precisamos de:  
> - [item 1]  
> - [item 2]  
> Prazo de retorno: [data/hora].  
> — Equipe Praia Digital

---

## Métricas do suporte

Acompanhe semanalmente:

- **Volume de chamados** por categoria.
- **Tempo médio de resolução** (MTTR).
- **SLA cumprido** (%).
- **NPS do suporte** (pesquisa após fechamento).
- **Reincidência** (% de chamados reabertos).

---

## Recursos úteis

- [Onboarding guide](hermes-agents-onboarding-guide.md) — referência para novos clientes.
- [FAQ completa](faq-completa.md) — base de conhecimento.
- [Cases](cases.md) — exemplos práticos para contextualizar soluções.
- [Glossário](glossario.md) — termos técnicos simplificados.
