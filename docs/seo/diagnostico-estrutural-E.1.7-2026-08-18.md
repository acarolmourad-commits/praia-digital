# E.1.7 — DIAGNÓSTICO ESTRUTURAL

Data: 2026-08-18
Fase: Diagnóstico de causa-raiz (somente investigação)
Base: amostra E.1.6 + histórico E.1.2/E.1.4/E.1.5 + evidências de repositório

## 1. Resumo executivo

As páginas degradadas da amostra E.1.6 não foram corrompidas após a publicação. Elas nasceram já degradadas no momento do commit de publicação. Os commits de criação contêm HTML mínimo ou placeholder diretamente, sem conteúdo substantivo. Isso muda a classificação da causa: não é um problema de pipeline pós-publicação, nem de template que falhou depois — é um problema de **processo de publicação** que permitiu o commit de HTML mínimo/placeholder sem exigir enriquecimento nem validação de conteúdo mínimo.

## 2. Famílias investigadas

- A — CURSO/CITY-CURSO
- B — CASE DE SUCESSO GENÉRICO
- C — ARTIGO OPERACIONAL THIN
- D — BAIRRO/GUIA REGIONAL
- E — OPERAÇÃO DE TEMPORADA

## 3. Origem de cada família

### A — Curso/city-curso
- Páginas: `blog/mongagua-curso-locacao-temporada-imoveis-2026.html`, `blog/itanhaem-curso-juridico-imoveis-2026.html`
- Commit de criação: `058769c` (Batch 95) e `9d18aa7` (Batch 130)
- Forma de criação: HTML de ~61 linhas criado diretamente em `blog/` via commit manual/assistido.
- Conteúdo na criação: já continha "Conteúdo completo em breve. Para decisões rápidas, use nossas ferramentas de inteligência imobiliária." e CTA para `assets/painel-ferramentas.html`.

### B — Case de sucesso genérico
- Páginas: `blog/guaruja-case-sucesso-financiamento-imoveis-2026.html`, `blog/case-sucesso-automacao-imoveis-sao-sebastiao-2026.html`
- Commit de criação: `77376ea` (chore financeiro) e `5e6fc34` (Batch 82)
- Forma de criação: HTML de ~61 linhas criado diretamente em `blog/`.
- Conteúdo na criação: placeholder idêntico + CTA idêntico, sem dados factuais verificáveis.

### C — Artigo operacional thin
- Páginas: `blog/imovel-litoral-investimento-imovel-usado-2026.html`, `blog/imovel-litoral-averbacao-imovel-prazo-2026.html`, `blog/imovel-litoral-custo-obra-reforma-2026.html`
- Commit de criação: `7fad60d` (Batch 54 lote 1), `d2729ad` (Batch 64 lote 2), `2f102d0` (Batch 57 lote 1)
- Forma de criação: HTML de ~25 linhas criado diretamente em `blog/`.
- Conteúdo na criação: 1 parágrafo introdutório + 3 H2 com 1 frase cada + "Próximo passo: veja..." link.

### D — Bairro/guia regional
- Página: `blog/sao-sebastiao-oeste-bairros-imoveis-2026.html`
- Commit de criação: `1fe11aa` (Batch 181)
- Forma de criação: HTML de ~88 linhas criado diretamente em `blog/`.
- Conteúdo na criação: mistura de seção real + placeholder final + CTA painel.

### E — Operação de temporada
- Página: `blog/case-de-sucesso-proprietario-guaruja-temporada-2026.html`
- Commit de criação: `b00777f` (batch 2026-08-14)
- Destaque: esta página foi criada com conteúdo real (77 linhas), e na amostra E.1.6 foi classificada como ESTÁVEL. Portanto, a família “operação de temporada” na amostra não apresentou degradação; a degradação está concentrada em A/B/C/D.

## 4. Templates identificados

- `partials/article-template.html` — template canônico com placeholder `Conteúdo em desenvolvimento: {{PRIMARY_KEYWORD}}.`, CTA, hotmart_link e SEO. É referenciado por `scripts/orchestrator/modules/article_generator.py`.
- Nenhum template específico de “case”, “curso” ou “bairro” foi encontrado; essas famílias usam HTML handwritten direto no commit, não o template acima.

## 5. Prompts identificados

- Nenhum prompt de IA foi encontrado como causa direta das páginas degradadas. O arquivo `scripts/orchestrator/modules/content_enrichment.py` contém templates de parágrafos por cluster e fallbacks, mas essas páginas **não passaram por esse enriquecedor** antes do commit.

## 6. Scripts/processos identificados

- `scripts/orchestrator/modules/article_generator.py` — gera artigos a partir de `partials/article-template.html`, mas **não foi usado** para as páginas degradadas da amostra.
- `scripts/orchestrator/modules/content_enrichment.py` — expansão de placeholder para conteúdo real; não executado nessas páginas.
- `scripts/orchestrator/modules/editorial_batch.py` — chama `article_generator.generate_article`; não é o responsável pelas páginas em questão.
- Processo real identificado: commits manuais/assistidos que escrevem HTML pequeno diretamente em `blog/` e atualizam `docs/editorial/REGISTRO_EDITORIAL.json` + `sitemap.xml`.

## 7. Componentes compartilhados

- Placeholder compartilhado (texto idêntico):
  `Conteúdo completo em breve. Para decisões rápidas, use nossas ferramentas de inteligência imobiliária.`
  Ocorrências em `blog/`: 966 arquivos.

- CTA painel compartilhado:
  `<a class="cta" href="https://praia.digital/assets/painel-ferramentas.html">Abrir Painel de Ferramentas →</a>`
  Presente nas famílias A e B, inserido manualmente nos commits.

## 8. Rastreamento do placeholder

- Texto: `Conteúdo completo em breve. Para decisões rápidas, use nossas ferramentas de inteligência imobiliária.`
- Origem: inserido diretamente nos commits de criação, não herdado de template após geração.
- Escopo: 966 páginas em `blog/` (confirmado por grep).
- Famílias afetadas na amostra E.1.6: A e B.
- Não existe condição de bloqueio no momento da criação/publicação.

## 9. Rastreamento do CTA

- CTA: `Abrir Painel de Ferramentas →` para `assets/painel-ferramentas.html`.
- Origem: inserção manual/assistida no HTML no momento da criação.
- Mesmo componente reaproveitado por múltiplas famílias (A e B).
- Não é injetado automaticamente por template; está hardcoded nos commits.

## 10. Rastreamento da duplicação

- Páginas com placeholder repetem o mesmo parágrafo introdutório e o mesmo bloco final.
- Páginas thin repetem estrutura mínima e link "Próximo passo: veja...".
- Causa: não é loop nem fallback de enriquecimento; é cópia de estrutura mínima criada manualmente/assistida.

## 11. Causa do artigo mínimo

- As páginas thin foram criadas como HTML mínimo no commit original (ex.: 25 linhas, 3 H2, 1 frase por H2).
- Nenhuma etapa subsequente expandiu o conteúdo.
- Portanto, a causa é a publicação de HTML mínimo sem exigência de conteúdo mínimo.

## 12. Gate de publicação

- GATE_EXISTENTE: parcial.
  - Existem skills e regras editoriais que pedem validação SEO, conteúdo mínimo, ausência de placeholder, CTA coerente.
  - Porém essas regras não são aplicadas como um bloqueio técnico automático antes do commit.
- SEM_GATE para:
  - placeholder explícito;
  - “conteúdo completo em breve”;
  - conteúdo muito curto;
  - H2 sem desenvolvimento;
  - CTA repetido sem variação;
  - seção incompleta.

## 13. Validadores existentes

- `scripts/orchestrator/modules/article_generator.py` — valida existência de template e gera SEO básico; não valida conteúdo mínimo.
- `scripts/orchestrator/modules/content_enrichment.py` — enriquece placeholder, mas não é invocado como gate.
- `docs/editorial/REGISTRO_EDITORIAL.json` — registra status; não impede publicação.
- `scripts/automation/seo_audit.py` — auditoria SEO, não bloqueia publicação automaticamente.
- Nenhum validador de “conteúdo mínimo/placeholder/parágrafo duplicado” é executado como pré-condição de commit.

## 14. Comparação estável × degradada

| Elemento | Estável | Degradada | Evidência |
|---|---|---|---|
| Tamanho na criação | 77+ linhas | 25–61 linhas | git show diff das páginas na criação |
| Placeholder na criação | Não | Sim | commits originais contêm placeholder |
| CTA painel | Não | Sim | commits originais com CTA idêntico |
| H2/parágrafo mínimo | Não | Sim | artigos thin nascem com 3 H2 e 1 frase |
| Expansão posterior | Não | Não | páginas não passaram por enriquecimento |
| Schema/SEO técnico | Presente | Presente | ambas têm BlogPosting/canonical/meta |

Primeiro ponto de divergência: **criação do HTML** — páginas degradadas já nascem com conteúdo mínimo/placeholder.

## 15. Mapa completo do pipeline

- ENTRADA: definição manual/assistida de título, cidade, cluster.
- SELEÇÃO: banco editorial/registro; sem bloqueio de qualidade mínima.
- GERAÇÃO: criação manual/assistida de HTML pequeno em `blog/`; sem uso obrigatório de template ou gerador estruturado.
- ENRIQUECIMENTO: existe (`content_enrichment.py`), mas **não foi executado** para essas páginas.
- VALIDAÇÃO EDITORIAL: regras em skills, mas **não aplicadas automaticamente** como gate.
- VALIDAÇÃO SEO: parcial (`seo_audit.py`), mas não bloqueia publicação.
- PUBLICAÇÃO: commit direto sem impedimento de placeholder/conteúdo mínimo.
- SITEMAP/ESTOQUE: URLs entram no sitemap porque são commitadas.

## 16. Hipóteses

| Hipótese | Evidência | Arquivo/Origem | Confiança |
|---|---|---|---|
| Template defeituoso | Template `partials/article-template.html` gera placeholder, mas não é a origem dessas páginas | partials/article-template.html | BAIXA |
| Prompt defeituoso | Nenhum prompt usado na criação dessas páginas | — | NÃO CONFIRMADA |
| Dados incompletos | Páginas thin foram criadas com dados mínimos intencionais | commits de batch | MÉDIA |
| Falha de enriquecimento | Enriquecimento existe, mas não foi executado | content_enrichment.py | ALTA |
| Fallback permissivo | N/A | — | NÃO CONFIRMADA |
| Falha de validação | Nenhum gate técnico impede publicação de placeholder/conteúdo mínimo | scripts/orchestrator/modules/* | ALTA |
| Processo editorial | Processo atual permite commit de HTML mínimo/placeholder diretamente | commits e docs/editorial | ALTA |
| Publicação sem gate | Não há bloqueio técnico antes do commit | pipeline atual | ALTA |

## 17. Causa-raiz

Classificação: **CAUSA_PROCESSO** (primária) + **CAUSA_VALIDACAO** (secundária)

- Primária: o processo editorial atual permite criar/publicar HTML mínimo/placeholder em `blog/` sem passar por enriquecimento ou validação de qualidade mínima.
- Secundária: os validadores existentes são recomendados/auditórios, não são gates automáticos antes do commit.

## 18. Famílias potencialmente afetadas

- A — CURSO/CITY-CURSO
- B — CASE DE SUCESSO GENÉRICO
- C — ARTIGO OPERACIONAL THIN
- D — BAIRRO/GUIA REGIONAL

EVIDÊNCIA FORTE: 966 páginas com placeholder idêntico em `blog/`, indicando que o problema é sistêmico nessas famílias.

## 19. Confiança do diagnóstico

ALTA

Justificativa: evidências diretas do repositório (commits, diffs, conteúdo na criação) confirmam que as páginas degradadas nasceram já degradadas.

## 20. Recomendação

CORRIGIR_CAUSA_RAIZ

## 21. Próxima ação

Criar gate técnico obrigatório no processo de publicação que bloqueie commits de páginas em `blog/` quando contiverem placeholder mínimo, conteúdo inferior a limite mínimo de palavras, ou ausência de seções desenvolvidas; habilitar o enriquecimento obrigatório para páginas criadas via template mínimo.
