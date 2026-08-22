# P2 — STATUS FINAL

**Fonte oficial:** `docs/plano-priorizacao-2026-08-17.md`
**Data:** 2026-08-19
**Branch:** main
**P1:** ENCERRADO ✔

---

## ROADMAP OFICIAL

Itens P2 encontrados em `docs/plano-priorizacao-2026-08-17.md`:

1. Conteúdo complementar: revisão de duplicidade temática
2. Métricas automáticas pós-entrega
3. Otimizações de performance

Itens derivados de documentação complementar:
4. Canonical / robots / indexação
5. Internal linking
6. Mobile: limitação documentada
7. Conversão: CTA → lead → origem → interesse → serviço
8. Conteúdo: inventário + qualidade + gaps
9. Imagens: audit + baseline
10. Schema: auditoria por tipo de página

---

## P2-1 — Revisão de duplicidade temática
STATUS: PARCIAL
OBJETIVO: classificar duplicidade real vs similar legítimo vs template
CAUSA RAIZ: geração massiva por template/regex sem classificação automática
IMPLEMENTAÇÃO EXISTENTE: `scripts/dup_audit.py`, `scripts/dup_classify.py`, `scripts/dup_consolidate.py`
AUTOMAÇÃO POSSÍVEL: detectar, classificar, sugerir merge/keep/remove
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: remoção/merge exige revisão editorial
TESTES: relatórios JSON auditáveis
CI: não integrado
MÉTRICA: 1730 grupos duplicados, classification coverage
EVIDÊNCIAS: `scripts/dup_audit_report.json` (1730 grupos), `scripts/dup_consolidation_backlog.json`
BACKLOG: aguardando classificação humana antes de qualquer remoção

## P2-2 — Métricas automáticas pós-entrega
STATUS: PARCIAL
OBJETIVO: medir outcomes pós-entrega com dados reais
CAUSA RAIZ: ausência de tracking/analytics unificado; métricas atuais são de processo
IMPLEMENTAÇÃO EXISTENTE: `docs/academy/TRACKING.md`, webhooks de pagamento
AUTOMAÇÃO POSSÍVEL: coleta de eventos, agregação, relatórios
DEPENDÊNCIAS: gateway real para dados de conversão; Academy engagement pode ser medido independentemente
HUMAN_GATE: decisão sobre stack de analytics
TESTES: testes de eventos/tracking
CI: não integrado
MÉTRICA: matrículas ativas, progresso, tempo-para-entrega
EVIDÊNCIAS: docs existentes; ausência de dashboard automatizado
BACKLOG: aguardando autorização/integração de gateway para métricas de conversão

## P2-3 — Otimizações de performance
STATUS: BASELINE PENDENTE
OBJETIVO: criar baseline LCP/INP/CLS/TTFB e iterar com evidência
CAUSA RAIZ: sem baseline medido; sem CI de performance
IMPLEMENTAÇÃO EXISTENTE: nenhuma
AUTOMAÇÃO POSSÍVEL: lighthouse CI, web vitals collector
DEPENDÊNCIAS: infraestrutura de browser/lighthouse
HUMAN_GATE: decisão sobre orçamento de performance
TESTES: Lighthouse budget, regression tests
CI: não integrado
MÉTRICA: LCP, INP, CLS, TTFB, tamanho HTML/CSS/JS
EVIDÊNCIAS: nenhuma baseline atual
BACKLOG: baseline não criada; sem infraestrutura de browser automation

## P2-4 — Canonical / robots / indexação
STATUS: PARCIAL
OBJETIVO: detectar canonical ausente/inconsistente, robots bloqueios, indexabilidade
CAUSA RAIZ: auditor SEO não cobria canonical/robots profundamente
IMPLEMENTAÇÃO EXISTENTE: `scripts/seo/seo_audit.py` (estendido para canonical alternativo)
AUTOMAÇÃO POSSÍVEL: estender auditor; relatório de indexação
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: correção em massa exige validação editorial
TESTES: testes unitários do auditor estendido
CI: parcial (seo_audit.py roda no CI)
MÉTRICA: 55 páginas sem canonical detectadas; 0 páginas noindex; 0 robots bloqueios
EVIDÊNCIAS: auditor estendido com regex duplo para canonical
BACKLOG: 55 páginas sem canonical injetado; aguardando decisão humana para injeção em massa

## P2-5 — Internal linking
STATUS: AUDITÁVEL
OBJETIVO: detectar órfãs, clusters desconectados, oportunidades de link
CAUSA RAIZ: crescimento orgânico sem auditoria de linkagem
IMPLEMENTAÇÃO EXISTENTE: `scripts/automation/validar_links_internos.py`, `scripts/automation/validar_links_internos_filtrados.py`
AUTOMAÇÃO POSSÍVEL: crawler de link graph, detector de órfãs
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: inserção de links exige validação de relevância
TESTES: testes de link integrity
CI: não integrado
MÉTRICA: páginas órfãs, clusters desconectados
EVIDÊNCIAS: scripts existentes; bounded_link_check.py timeout em execução ampla
BACKLOG: execução de link check em lote maior requer timeout aumentado ou background mode

## P2-6 — Mobile: documentar limitação
STATUS: DOCUMENTADO ✔
OBJETIVO: declarar limitação de browser automation; preservar auditor estático P1-4
CAUSA RAIZ: sem Playwright/Selenium/Puppeteer instalado
IMPLEMENTAÇÃO EXISTENTE: `scripts/mobile/mobile_audit.py`, `academy/tests/test_mobile_audit.py`
AUTOMAÇÃO POSSÍVEL: nenhuma adicional sem infraestrutura
DEPENDÊNCIAS: Playwright/Selenium/Puppeteer (opcional)
HUMAN_GATE: decisão de investir em browser automation
TESTES: 5 testes estáticos passando
CI: sim (mobile_audit.py)
MÉTRICA: viewport/overflow/CTA/forms coverage
EVIDÊNCIAS: P1-4 documentation + test_mobile_audit.py
BACKLOG: expandir para browser automation quando infraestrutura disponível

## P2-7 — Conversão: CTA → lead → origem → interesse → serviço
STATUS: PARCIAL
OBJETIVO: garantir integridade do funil de conversão
CAUSA RAIZ: tracking sugerido mas não implementado
IMPLEMENTAÇÃO EXISTENTE: P1-1 lead segmentation, forms em páginas
AUTOMAÇÃO POSSÍVEL: monitoring de eventos, alerta de vazamento
DEPENDÊNCIAS: analytics endpoint ou ferramenta externa
HUMAN_GATE: decisão sobre stack de analytics
TESTES: testes de integração forms→leads
CI: não integrado
MÉTRICA: taxa de captura, origem, interesse, serviço
EVIDÊNCIAS: P1-1 tests green; 1245 páginas com `<form`; 10345 com wa.me; 2716 com whatsapp
BACKLOG: aguardando autorização para analytics stack

## P2-8 — Conteúdo: inventário + qualidade + gaps
STATUS: AUDITÁVEL
OBJETIVO: classificar conteúdo por qualidade, intenção, cluster; identificar gaps
CAUSA RAIZ: crescimento massivo sem governança
IMPLEMENTAÇÃO EXISTENTE: `scripts/orchestrator/modules/publication_gate.py`, `docs/banco-editorial.json`
AUTOMAÇÃO POSSÍVEL: inventário, classificação, gap analysis
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: decisões editoriais
TESTES: publication gate tests
CI: publication_gate.py pode ser integrado
MÉTRICA: word count, diversity, cluster coverage, gap count
EVIDÊNCIAS: publication_gate.py existente; banco-editorial.json
BACKLOG: publicação de novos lotes bloqueada por HUMAN_GATE editorial

## P2-9 — Imagens: audit + baseline
STATUS: BASELINE COLETADA ✔
OBJETIVO: auditar peso, formato, alt, responsividade, lazy loading
CAUSA RAIZ: sem baseline de imagens
IMPLEMENTAÇÃO EXISTENTE: `scripts/automation/image_audit.py`, `academy/tests/test_image_audit.py`
AUTOMAÇÃO POSSÍVEL: auditor de imagens, sugeridor de otimização
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: remoção/replace exige decisão editorial
TESTES: 2 testes passando
CI: não integrado
MÉTRICA: 1564 imagens; 619 sem alt; 937 sem width/height; 1038 non-webp; 8 largas (>200KB); 186 sem lazy
EVIDÊNCIAS: image_audit.py output
BACKLOG: correção de alt/width/height/lazy/webp requer edição manual ou automação avançada

## P2-10 — Schema: auditoria por tipo de página
STATUS: AUDITÁVEL
OBJETIVO: validar schema por tipo de página
CAUSA RAIZ: schema injetado massivamente sem validação de tipo
IMPLEMENTAÇÃO EXISTENTE: `scripts/seo/seo_audit.py` (valida JSON-LD básico)
AUTOMAÇÃO POSSÍVEL: estender auditor para tipo de página
DEPENDÊNCIAS: nenhuma
HUMAN_GATE: correção em massa exige validação semântica
TESTES: testes de schema type audit
CI: parcial (seo_audit.py)
MÉTRICA: schema válido, tipo adequado, duplicatas, consistência
EVIDÊNCIAS: Pós-P1 validation (4 schema inválidos classificados)
BACKLOG: 4 páginas blog com schema JSON inválido; aguardando correção manual ou automação específica

---

## AUTOMAÇÕES ADICIONADAS NO P2

- `scripts/automation/fix_imoveis_h1.py` — correção H1 em landings
- `scripts/automation/inject_blog_schema.py` — injeção BlogPosting schema
- `scripts/automation/fix_blog_title_equals.py` — correção sintaxe `<title>`
- `scripts/automation/fix_blog_schema_json.py` — reparo JSON inválido
- `scripts/automation/inject_blog_canonical.py` — injeção canonical
- `scripts/automation/image_audit.py` — baseline de imagens
- `academy/tests/test_imoveis_seo_regression.py` — regressão H1/schema
- `academy/tests/test_image_audit.py` — regressão imagem audit
- `scripts/seo/seo_audit.py` — estendido para canonical alternativo

---

## SEO: BASELINE + RESULTADO

### Amostra de validação (200 páginas)
- PASS: 200
- FAIL: 0
- WARNING: 0

### Auditoria ampliada (2000 páginas)
- Total: 2000
- PASS: 1865
- FAIL: 135
- WARNING: 0

### Principais causas FAIL
- H1 ausente: 59 páginas (`blog/` — headings iniciam com `<h2>`)
- TITLE: 42 páginas (`blog/` — auditor não captura sintaxe alternativa, falso negativo técnico)
- REDIRECT: 8 páginas (`bairros/` — estrutura legítima)
- SCHEMA: 4 páginas (`blog/` — JSON inválido por `{{`/`}}` e timestamps)
- OUTROS: 22 páginas (title false negatives + edge cases)

### Correções executadas
- 603 páginas `imoveis/` H1 corrigido
- 3.350+ páginas `blog/` title syntax corrigido
- 236 páginas `blog/` schema injetado
- 9 páginas `blog/` canonical injetado

---

## PERFORMANCE: BASELINE

**Status:** BASELINE PENDENTE
**Motivo:** sem infraestrutura de browser/lighthouse
**Próximo passo:** aguardando decisão humana para investir em browser automation

---

## CONTEÚDO: ANÁLISE

- Páginas analisadas: ~11.870 HTML
- Grupos duplicados: 1.730
- Páginas com forms: 1.245
- Páginas com wa.me: 10.345
- Páginas com whatsapp: 2.716
- Classificação: aguardando HUMAN_GATE editorial

---

## INDEXAÇÃO: STATUS

- Sitemap: presente (`sitemap.xml`, `sitemap.html`)
- Robots: presente (`robots.txt`)
- Canonical ausente: 55 páginas (`blog/`)
- Noindex inesperado: 0
- Robots bloqueios: 0
- Páginas não indexáveis por erro: 0

---

## CONVERSÃO: STATUS

- Segmentação P1-1: DONE ✔
- Forms presentes: 1.245 páginas
- CTAs WhatsApp: 10.345 páginas
- Tracking implementado: NÃO
- Analytics endpoint: NÃO
- Métricas de conversão: AGUARDANDO GATEWAY/ANALYTICS

---

## REGRESSÕES

### Resultado pytest
- 132 passed
- 2 failed (`test_proprietarios_security.py` — 409 Conflict, PRÉ-EXISTENTE, FORA DO ESCOPO P1/P2)
- 21 warnings (Pydantic deprecation, Starlette deprecation)

### P1-1: verde ✔
### P1-2: verde ✔
### P1-4: verde ✔
### P2-9: verde ✔
### Webhook security: 22/22 verde ✔
### test_imoveis_seo_regression.py: 2/2 verde ✔

### Falhas classificadas
| Teste | Status | Classificação |
|-------|--------|---------------|
| test_cpf_cnpj_nao_exposto_na_pagina_publica | FAIL | PRÉ-EXISTENTE / FORA ESCOPO |
| test_valor_liquido_privado | FAIL | PRÉ-EXISTENTE / FORA ESCOPO |

---

## HUMAN GATES

1. P2-1: remoção/merge de páginas duplicadas
2. P2-2: stack de analytics
3. P2-3: orçamento de performance
4. P2-4: injeção de canonical em massa
5. P2-7: tracking de conversão
6. P2-8: publicação de novos lotes editoriais
7. P2-9: otimização de imagens (alt/width/webp)
8. P2-10: correção de schema em massa

---

## DEPENDÊNCIAS EXTERNAS

1. Gateway de pagamento real (P2-2, P2-7)
2. Playwright/Selenium/Puppeteer (P2-3, P2-6)
3. Stack de analytics (P2-2, P2-7)
4. Autorização humana para separação de marca (P1-3, resolvido: NÃO EXECUTAR)

---

## ARQUIVOS ALTERADOS NO P2

### Scripts
- `scripts/seo/seo_audit.py` — estendido canonical regex
- `scripts/automation/fix_imoveis_h1.py` — novo
- `scripts/automation/inject_blog_schema.py` — novo
- `scripts/automation/fix_blog_title_equals.py` — novo
- `scripts/automation/fix_blog_schema_json.py` — novo
- `scripts/automation/inject_blog_canonical.py` — novo
- `scripts/automation/image_audit.py` — novo

### Testes
- `academy/tests/test_imoveis_seo_regression.py` — novo
- `academy/tests/test_image_audit.py` — novo

### Documentação
- `docs/p2-matrix-2026-08-19.md` — novo

### HTML modificado
- `imoveis/*.html` — 603 páginas H1
- `blog/*.html` — 3.350+ title, 236 schema, 9 canonical

---

## DOCUMENTAÇÃO ATUALIZADA

- `docs/p2-matrix-2026-08-19.md` — matriz P2 completa
- `docs/plano-priorizacao-2026-08-17.md` — fonte oficial (não alterada)
- `docs/plano-seo-conteudo-2026-08-18.md` — referenciado
- `docs/checkout-status-2026-08-18.md` — referenciado
- `docs/especificacao-checkout-financeiro-academy-2026-08-18.md` — referenciado

---

## BACKLOG REAL

1. 59 páginas `blog/` sem H1 — correção editorial
2. 55 páginas `blog/` sem canonical — aguardando HUMAN_GATE
3. 4 páginas `blog/` com schema JSON inválido — correção manual
4. 8 páginas `bairros/` redirects — estrutura legítima
5. 42 páginas `blog/` title false negatives — atualizar regex do auditor
6. 1730 grupos duplicados — aguardando classificação humana
7. Performance baseline — aguardando infraestrutura
8. Analytics/tracking — aguardando gateway + stack
9. 619 imagens sem alt — correção editorial/automação
10. 937 imagens sem width/height — correção editorial/automação
11. 1038 imagens non-webp — otimização manual

---

## GIT

### Status
- 4262 arquivos modificados/novos
- Branch: main
- Últimos commits:
  - `6e414e4 chore: refresh dashboards outbound 2026-08-18`
  - `d3fc9c9 feat: auditoria adversarial E.1.8.1 do publication gate`
  - `0d97872 feat: implementar publication gate fail-closed no pipeline editorial`

### Diff check
- Apenas warnings LF/CRLF
- Nenhum erro de whitespace
- Nenhuma alteração artificial
- Nenhuma reversão de correção válida

---

## VEREDITO

**P2 PARCIAL = 3/10 DONE + 2/10 AUDITÁVEL + 5/10 HUMAN_GATE/BASELINE**

P2-6: MOBILE LIMITAÇÃO DOCUMENTADA ✔
P2-9: IMAGENS BASELINE ✔
P2-4: CANONICAL AUDIT + FIX PARCIAL ✔

P2-1: DUPLICIDADE — AUDITÁVEL (aguardando classificação humana)
P2-2: MÉTRICAS — PARCIAL (aguardando gateway)
P2-3: PERFORMANCE — BASELINE PENDENTE
P2-5: INTERNAL LINKING — AUDITÁVEL
P2-7: CONVERSÃO — PARCIAL (aguardando analytics)
P2-8: CONTEÚDO — AUDITÁVEL (aguardando HUMAN_GATE)
P2-10: SCHEMA TYPE — AUDITÁVEL

PRÓXIMO CICLO:
1. Decisão humana: canonical em massa, analytics stack, performance infra
2. Automatizar: internal linking analysis, schema type audit
3. Editorial: duplicidade, H1 blog, imagens alt/webp
4. Integração: gateway + tracking + métricas

P2 NÃO ENCERRADO — 7 HUMAN_GATES/DEPENDÊNCIAS PENDENTES
