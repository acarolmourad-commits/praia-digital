# E.1.8 — IMPLEMENTAÇÃO DO PUBLICATION GATE

Data: 2026-08-18
Fase: Correção da causa-raiz (pipeline seguro)
Base: diagnóstico E.1.7 (`310ac50`) + evidências de repositório

## 1. Objetivo

Impedir que páginas com placeholder mínimo, conteúdo insuficiente ou estrutura incompleta cheguem ao commit/publicação em `blog/`, sem recuperar ou alterar o estoque existente.

## 2. Escopo

NÃO executado nesta etapa:
- recuperação das 966 páginas;
- enriquecimento em massa;
- alteração de páginas antigas;
- publicação de novos artigos.

Executado nesta etapa:
- criação de `scripts/orchestrator/modules/publication_gate.py`;
- integração fail-closed em `scripts/orchestrator/modules/article_generator.py`;
- integração fail-closed em `scripts/orchestrator/modules/editorial_batch.py`;
- integração fail-closed em `scripts/orchestrator/orchestrator_24h.py`.

## 3. Arquivos alterados

- `scripts/orchestrator/modules/publication_gate.py` (novo)
- `scripts/orchestrator/modules/article_generator.py`
- `scripts/orchestrator/modules/editorial_batch.py`
- `scripts/orchestrator/orchestrator_24h.py`

## 4. Ponto exato do pipeline onde o gate foi inserido

### 4.1 article_generator.py
`write_article()` agora chama `validate_generated_article()` **antes** de escrever o arquivo.
Qualquer violação retorna `PublicationGateError` e impede o `WRITE`.

### 4.2 editorial_batch.py
`generate_batch()` captura `PublicationGateError` e registra em `skipped`.
Se o gate bloquear, o artigo não é escrito nem registrado no sitemap/banco.

### 4.3 orchestrator_24h.py
Após `review()` e antes de `publish()`, o módulo `publication_gate` é carregado dinamicamente.
Caminhos de HTML dos itens revisados são validados; itens bloqueados têm `qa.passed=False`,
recebem `publication_error='publication_gate_blocked'` e não são publicados.

## 5. Regras implementadas no gate

- `placeholder_detected`: bloqueia se houver qualquer marcador de placeholder mínimo.
- `generic_repetition`: bloqueia se 3+ padrões genéricos mínimos coincidirem.
- `min_words`: bloqueia se `< 120` palavras.
- `min_content_size`: bloqueia se `< 800` bytes.
- `min_h2`: bloqueia se `< 2` H2.
- `missing_title`: bloqueia se `<title>` ausente.
- `missing_meta_description`: bloqueia se meta description ausente.
- `missing_canonical`: bloqueia se canonical ausente.
- `missing_h1`: bloqueia se H1 ausente.
- `min_internal_links`: bloqueia se `< 1` link interno.

## 6. Enriquecimento obrigatório

`article_generator.py` agora valida o HTML gerado antes da escrita.
Se o template mínimo for usado sem enriquecimento suficiente, o gate retorna `BLOCK_PUBLICATION`.
Não há fallback silencioso.

## 7. Testes executados

### 7.1 Casos que devem ser bloqueados (E.1.6 degraded)
- `blog/mongagua-curso-locacao-temporada-imoveis-2026.html` -> BLOCK
- `blog/guaruja-case-sucesso-financiamento-imoveis-2026.html` -> BLOCK
- `blog/itanhaem-curso-juridico-imoveis-2026.html` -> BLOCK
- `blog/case-sucesso-automacao-imoveis-sao-sebastiao-2026.html` -> BLOCK
- `blog/imovel-litoral-investimento-imovel-usado-2026.html` -> BLOCK
- `blog/imovel-litoral-averbacao-imovel-prazo-2026.html` -> BLOCK
- `blog/imovel-litoral-custo-obra-reforma-2026.html` -> BLOCK
- `blog/sao-sebastiao-oeste-bairros-imoveis-2026.html` -> BLOCK

Resultado: 8/8 bloqueados corretamente.

### 7.2 Casos que devem ser aprovados (E.1.6 stable)
- `blog/acelerar-fechamento-vendas-litoral-paulista-2026.html` -> PASS
- `blog/case-de-sucesso-proprietario-guaruja-temporada-2026.html` -> PASS

Resultado: 2/2 aprovados.

### 7.3 Observação de regressão
- `blog/geracao-descricoes-anuncios-ia.html` -> BLOCK por `min_h2=1`.
  Esta página é um ativo estático de ferramenta, não um artigo de blog tradicional.
  Não foi alterada. Se necessário, pode receber isenção explícita em regra futura,
  mas não representa um problema causado pelo gate novo.

## 8. Confirmações obrigatórias

- Nenhuma página do estoque das 966 foi alterada.
- Nenhuma recuperação em massa foi executada.
- O bloqueio ocorre **antes** do commit/publicação.

## 9. Próxima ação recomendada

Aplicar o gate como pré-condição obrigatória em TODO ponto que escreva em `blog/`,
incluindo scripts manuais de criação, e revisar exceções legítimas como páginas de
ferramenta/ativos estáticos antes de expandir o gate para outras seções.
