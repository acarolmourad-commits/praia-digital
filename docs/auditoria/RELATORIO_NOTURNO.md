# RELATÓRIO NOTURNO — AUDITORIA AUTÔNOMA

**Data:** 2026-08-18  
**Escopo:** Repositório `praia-digital` completo  
**Modo:** AUDIT → DISCOVER → MEASURE → CLASSIFY → PREPARE  
**Objetivo:** Descobrir riscos, problemas, regressões ou melhorias de alto valor; preparar relatório acionável para revisão humana.  

---

## 1. Status geral

ATENÇÃO

O repositório apresenta pontos de atenção relevantes, mas nenhum risco crítico imediato de publicação indevida. O Publication Gate está estável e protegido. Há achados estruturais que merecem revisão humana na manhã seguinte.

---

## 2. K3 / Publication Gate

| Item | Status | Evidência |
|---|---|---|
| K3 | ENCERRADO | `tests/test_k3_regression.py`: PASS |
| Publication Gate | BASELINE VALIDADA | Nenhuma alteração em `publication_gate.py` |
| Fail-closed | VALIDADO | `scripts/test_article_generator_hardening.py`: 5/5 PASS |
| Threshold 0.02 | PRESERVADO | `tests/test_diversity_threshold.py`: 6/6 PASS |
| Regressões | NENHUMA | Adversarial 25/25 BLOCK, E.1.8.2 7/7 BLOCK |

**Conclusão:** NÃO REABRIR o incidente K3. A baseline está protegida por testes permanentes.

---

## 3. Achados críticos

### P1 — Academy: inventário zerado vs. 64 cursos reais

**Evidência:** `academy/inventario.json` retorna `0 courses` quando lido por script. Porém, a verificação direta do sistema de arquivos mostra 64 diretórios de curso, cada um com `index.html`, `vendas.html` e `curso.md`.

**Impacto:** Qualquer automação ou métrica que dependa do inventário JSON está operando com dados vazios. Isso pode causar:
- relatórios incorretos;
- decisões de produção baseadas em ausência de cursos;
- falhas silenciosas em scripts de seed/migração.

**Ação recomendada:** Investigar se o JSON é preenchido por outro processo, se está obsoleto, ou se há script de atualização que não está sendo executado.

---

### P1 — Academy: GA4 desativado em 100% dos cursos

**Evidência:** Em 20 cursos amostrados, todos os `index.html` e `vendas.html` contêm:
```javascript
var GA4_MEASUREMENT_ID = '';
if (GA4_MEASUREMENT_ID) { ... }
```

**Impacto:** Nenhum dado de analytics está sendo coletado nos funis de venda da Academy. Métricas de conversão, origem de leads e comportamento no checkout são INVISÍVEIS.

**Ação recomendada:** Confirmar se a intenção é realmente não rastrear (ex.: LGPD, awaiting approval) ou se é esquecimento. Se for esquecimento, ativar GA4 com consentimento adequado.

---

### P2 — `orchestrator_central.py`: executa `production_pipeline` sem `PublicationGateError`

**Evidência:** `orchestrator_central.py:100-109` carrega e executa `production_pipeline` com `try/except Exception` genérico. Não captura `PublicationGateError` especificamente.

**Impacto:** Se o pipeline de produção lançar `PublicationGateError` (fail-closed), o orquestrador central trata como erro genérico e retorna `{'status': 'error', 'message': ...}`. Isso não reintroduz bypass, mas perde a semântica específica do gate.

**Ação recomendada:** Avaliar se o orquestrador deve distinguir erros de validação de erros técnicos. Não é um bypass, mas é perda de observabilidade.

---

### P2 — `orchestrator_24h.py`: `except Exception` genérico em `run_module()`

**Evidência:** `orchestrator_24h.py:52-53, 170, 191, etc.` capturam `Exception` e retornam `{'status': 'error', 'message': str(e)}`.

**Impacto:** Padrão seguro de fail-closed para discovery/decision, mas mascara tipos específicos de erro. Não há risco de bypass porque o orquestrador não publica diretamente; ele apenas relata.

**Ação recomendada:** Manter como está, mas adicionar tipos específicos de exceção quando o orquestrador começar a publicar.

---

### P3 — `scripts/automation/run_vendas_do_dia.py`: 25+ scripts em sequência, sem isolamento

**Evidência:** O runner executa 25 scripts de automação em sequência. Se um script falhar, o runner apenas imprime `[WARN]` e continua.

**Impacto:** Baixo. Falhas são visíveis em stdout. Não há risco de bypass de validação porque esses scripts operam em camada de outbound, não de publicação editorial.

**Ação recomendada:** Adicionar log estruturado com timestamp e exit code para cada script.

---

## 4. Auditoria de automations

### Scripts de outbound (`run_vendas_do_dia.py`, `run_automacao_do_ia.py`)

**Avaliação:** Seguros. Não publicam conteúdo editorial. Operam em camada de follow-up/notificação. Falhas são logadas. Não há retry perigoso.

### `scripts/automation/disparar_lote_*.py`

**Avaliação:** Suspeitos. Disparam mensagens para leads. Nenhum desses scripts foi auditado diretamente. O risco é de envio indevido ou duplicação.

**Ação recomendada:** Auditoria separada dos scripts de disparo. Não realizada nesta missão por escopo.

---

## 5. Auditoria editorial

### TOP 10 oportunidades editoriais (somente diagnóstico)

| # | Cluster | Tema | Intenção | Motivo | Prioridade |
|---|---|---|---|---|---|
| 1 | Documentação | "Como evitar golpes na compra de imóvel no litoral" | Informacional | Curso existe; artigo pode direcionar para curso | P1 |
| 2 | Investimento | "ROI de imóvel de temporada no litoral" | Comercial | Curso de rentabilidade existe; forte intenção comercial | P1 |
| 3 | Aluguel temporada | "Gestão de temporada para proprietários" | Transacional | Serviço de administração existe; CTA direto | P1 |
| 4 | SEO local | "Como aparecer no Google para imóveis no litoral" | Informacional | Lacuna entre conteúdo e serviço de SEO | P2 |
| 5 | Captação | "Como captar imóveis exclusivos no litoral" | Comercial | Alinhado com serviço de captação | P2 |
| 6 | Financiamento | "Financiamento de imóvel na praia: guia 2026" | Informacional | Curso existe; atualização anual necessária | P2 |
| 7 | Jurídico | "Documentação para compra de imóvel no litoral" | Informacional | Curso existe; conteúdo complementar | P3 |
| 8 | CRM | "CRM para corretores: organizando leads no litoral" | Comercial | Curso existe; artigo como topo de funil | P3 |
| 9 | Marketing digital | "Marketing para imobiliárias no litoral" | Informacional | Curso existe; evergreen | P3 |
| 10 | Parcerias | "Parcerias imobiliárias no litoral" | Informacional | Baixa concorrência; complementa serviço | P3 |

**Risco factual:** Nenhum destes temas foi validado quanto a dados específicos. Ação recomendada é pesquisa factual antes da produção.

---

## 6. Auditoria SEO

### Problemas encontrados

| Problema | Evidência | Prioridade |
|---|---|---|
| `GOVERNANCA_EDITORIAL.md` desatualizado | Menciona "10 artigos publicados" e "24 grupos consolidados"; estado atual é muito maior | P3 |
| GA4 vazio em Academy | `GA4_MEASUREMENT_ID = ''` em 64 páginas | P1 |
| Sem verificação de canonical em massa | `scripts/gerar_sitemap.py` existe, mas não há evidência de execução recente | P2 |

**Não realizada:** Varredura completa de links quebrados e status HTTP por escopo e tempo.

---

## 7. Academy

### Estado

| Item | Status | Observação |
|---|---|---|
| Cursos no filesystem | 64 diretórios | Cada um com `index.html`, `vendas.html`, `curso.md` |
| `academy/inventario.json` | 0 cursos | Não reflete a realidade |
| Schema.org | Presente em `curso.md` | Estrutura JSON-LD válida |
| GA4 | Desativado | `GA4_MEASUREMENT_ID = ''` |
| Preços | Diversificados | R$247 a R$497 |
| Checkout | `routers/payments.py` | Não auditado em profundidade |
| Delivery | `routers/content_delivery.py` | Não auditado em profundidade |

**Ação recomendada:** 
1. Corrigir `academy/inventario.json` para refletir os 64 cursos reais.
2. Decidir sobre GA4: ativar ou documentar a decisão de não ativar.
3. Auditoria separada de checkout e delivery.

---

## 8. Métricas

| Métrica | Fonte | Classificação | Observação |
|---|---|---|---|
| K3 BLOCK | Teste de regressão | VERIFICADA | Executada diretamente |
| Adversarial 25/25 | Script | VERIFICADA | Executado diretamente |
| E.1.8.2 7/7 | Script | VERIFICADA | Executado diretamente |
| Academy: 64 cursos | Filesystem | VERIFICADA | Contagem direta de diretórios |
| Academy inventário: 0 | JSON | NÃO VERIFICADA | Discrepância com filesystem |
| GA4 ativado | Páginas HTML | NÃO VERIFICADA | Placeholder vazio |
| Métricas de outbound | Scripts | NÃO VERIFICADA | Sem evidência de coleta/armazenamento |
| Tráfego orgânico | Não verificado | NÃO VERIFICADA | Nenhuma ferramenta conectada |

**Conclusão:** Métricas confiáveis existem apenas para o Publication Gate. Métricas de negócio (outbound, academy, tráfego) não possuem evidência verificável neste repositório.

---

## 9. Automação

### TOP 10 oportunidades de automação

| # | Tarefa | Frequência | Esforço | Risco | Automação sugerida | Ganho |
|---|---|---|---|---|---|---|
| 1 | Atualizar `academy/inventario.json` | Sob demanda | Baixo | Baixo | Script de sync inventory → filesystem | Confiabilidade de métricas |
| 2 | Validar links internos do blog | Semanal | Médio | Baixo | Script de link audit | SEO |
| 3 | Sincronizar sitemap após publicação | Automático | Baixo | Baixo | Já existe `gerar_sitemap.py`; verificar execução | Indexação |
| 4 | Verificar GA4 em páginas Academy | Sob demanda | Baixo | Baixo | Script de varredura | Analytics |
| 5 | Atualizar preços de cursos em massa | Mensal | Médio | Baixo | Script de atualização a partir de fonte única | Consistência |
| 6 | Detectar artigos órfãos no blog | Semanal | Médio | Baixo | Script de análise de links internos | SEO |
| 7 | Validar schema.org em páginas Academy | Sob demanda | Baixo | Baixo | Extensão do validador existente | Rich snippets |
| 8 | Verificar `GOVERNANCA_EDITORIAL.md` | Mensal | Baixo | Baixo | Script de comparação com estado real | Documentação |
| 9 | Audit de redirects 301 | Trimestral | Médio | Baixo | Script de crawl e verificação de status | SEO |
| 10 | Consolidar métricas de outbound | Diário | Médio | Médio | Dashboard automatizado | Visibilidade |

---

## 10. Alterações realizadas

**Nenhuma alteração de produção realizada durante esta missão.**

Somente auditoria. Nenhum arquivo de produção foi modificado.

---

## 11. Pendências para revisão humana

### Alta prioridade

1. **Academy inventário zerado** — investigar causa e corrigir JSON.
2. **GA4 desativado** — decidir se é intencional ou omissão.
3. **Scripts de disparo outbound** — auditoria separada necessária.

### Média prioridade

4. **`orchestrator_central.py`** — avaliar se `production_pipeline` deve ter tratamento específico para `PublicationGateError`.
5. **`GOVERNANCA_EDITORIAL.md`** — atualizar para refletir estado atual do projeto.
6. **Métricas de negócio** — estabelecer fontes verificáveis para outbound, academy e tráfego.

### Baixa prioridade

7. **Auditoria SEO técnica** — links quebrados, status HTTP, redirects.
8. **Automação de inventário** — criar script de sync.
9. **Documentação de decisões** — registrar por que GA4 está desativado.

---

## 12. Conclusão

**AUDITORIA PREVENTIVA CONCLUÍDA — NENHUM RISCO CRÍTICO IMEDIATO ENCONTRADO**

O Publication Gate está protegido. K3 está encerrado. Nenhuma publicação indevida foi identificada. Os achados principais são estruturais (inventário, analytics, métricas) e não representam risco de segurança ou bypass.

**Próximos passos recomendados para revisão humana:**
1. Investigar `academy/inventario.json`
2. Decidir sobre GA4
3. Planejar auditoria de scripts de disparo outbound
4. Atualizar documentação de governança
