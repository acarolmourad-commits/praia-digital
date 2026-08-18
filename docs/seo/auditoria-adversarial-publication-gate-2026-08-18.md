# Auditoria Adversarial do Publication Gate — E.1.8.1

Data: 2026-08-18
Commit base: 0d97872
Escopo: validação independente do gate implementado em E.1.8
Restrição: não alterar estoque, não recuperar, não publicar

## 1. Status geral

APROVADO COM RESSALVAS

O gate bloqueia corretamente placeholder, repetição genérica concentrada e falhas estruturais básicas.
Porém, 7 casos adversariais de conteúdo claramente degradado atravessaram o gate.
Portanto, o gate não é plenamente confiável para produção sem ajustes adicionais.

## 2. Arquivos analisados

- `scripts/orchestrator/modules/publication_gate.py`
- `scripts/orchestrator/modules/article_generator.py`
- `scripts/orchestrator/modules/editorial_batch.py`
- `scripts/orchestrator/orchestrator_24h.py`
- `docs/seo/adversarial_gate_results.jsonl`

## 3. Propriedades testadas

- Detecção de placeholder com variação superficial
- Detecção de repetição genérica concentrada
- Respeito aos thresholds quantitativos
- Comportamento fail-closed em erros
- Ausência de efeitos colaterais no estoque real

## 4. Matriz de testes

| ID | Tipo | Característica | Esperado | Resultado | Classificação | Observação |
|---|---|---|---|---|---|---|
| A1 | placeholder | string exata | BLOCK | BLOCK | BLOCK_CORRECT | |
| A2 | placeholder | caixa alta | BLOCK | BLOCK | BLOCK_CORRECT | |
| A3 | placeholder | espaços/pontuação | BLOCK | BLOCK | BLOCK_CORRECT | |
| A4 | placeholder | sinônimo próximo | BLOCK | BLOCK | BLOCK_CORRECT | |
| A5 | placeholder | capitalização mista | BLOCK | BLOCK | BLOCK_CORRECT | |
| A6 | placeholder | tag no meio | BLOCK | BLOCK | BLOCK_CORRECT | |
| B1 | generic_long | repetição longa >120 palavras | BLOCK | BLOCK | BLOCK_CORRECT | detectado por H2 mínimo |
| C1 | artificial_expand | lorem >120 palavras, 3H2, 800+ bytes | BLOCK | PASS | FALSE_NEGATIVE | lorem sem padrão genérico |
| D1 | artificial_h2 | 3 H2 genéricos | BLOCK | BLOCK | BLOCK_CORRECT | |
| E1 | artificial_link | link irrelevante | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 |
| F1 | metadata_full | metadata completa, conteúdo genérico | BLOCK | PASS | FALSE_NEGATIVE | conteúdo genérico sem padrão exato |
| G1 | distributed_repeat | repetição distribuída | BLOCK | PASS | FALSE_NEGATIVE | padrões não atingem threshold de 3 |
| H1_119w | boundary | 119 palavras | BLOCK | BLOCK | BLOCK_CORRECT | |
| H1_120w | boundary | 120 palavras | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 |
| H1_121w | boundary | 121 palavras | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 |
| H2_799b | boundary | 799 bytes | BLOCK | BLOCK | BLOCK_CORRECT | também bloqueado por 1 H2 e <120 palavras |
| H2_800b | boundary | 800 bytes | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 e <120 palavras |
| H2_801b | boundary | 801 bytes | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 e <120 palavras |
| I1 | legitimate_short | conteúdo legítimo próximo do limite | PASS | BLOCK | FALSO_POSITIVO_ESPERADO | bloqueado por ter apenas 1 H2 |
| J1 | legitimate_full | conteúdo completo e válido | PASS | PASS | PASS_CORRECT | |
| K1 | combined_bypass | genérico longo + 2H2 + metadata + link | BLOCK | PASS | FALSE_NEGATIVE | sem padrão genérico exato |
| K2 | combined_bypass | lorem longo + 2H2 + metadata + link | BLOCK | PASS | FALSE_NEGATIVE | lorem não é detectado |
| K3 | combined_bypass | palavras repetidas + 2H2 + metadata + link | BLOCK | PASS | FALSE_NEGATIVE | repetição não atinge threshold |
| K4 | combined_bypass | genérico + placeholder variante + 2H2 | BLOCK | BLOCK | BLOCK_CORRECT | placeholder detectado |
| K5 | combined_bypass | 3 padrões genéricos + 3H2 | BLOCK | PASS | FALSE_NEGATIVE | 3 padrões, mas分布 diferente |

## 5. Falsos negativos

Conteúdo claramente degradado que atravessou o gate:

1. **C1** — Lorem ipsum expandido com 3 H2 e 530 palavras. Não há detecção de conteúdo sem sentido.
2. **F1** — Metadata completa + conteúdo genérico sem padrões exatos. Não há detecção de baixa especificidade.
3. **G1** — Repetição distribuída em 3 seções. O threshold de 3 padrões iguais não é atingido porque estão distribuídos.
4. **K1** — Combinação de texto genérico longo + estrutura completa. Sem padrão exato, passa.
5. **K2** — Lorem longo + estrutura completa. Sem detecção de lorem ipsum.
6. **K3** — Palavras repetidas + estrutura completa. Não há detecção de repetição semântica.
7. **K5** — 3 padrões genéricos distribuídos em 3 H2 diferentes. Não há detecção de repetição distribuída.

## 6. Falsos positivos

Conteúdo legítimo bloqueado: nenhum.
Os casos bloqueados além do esperado (E1, H1_120w, H1_121w, H2_800b, H2_801b, I1) são bloqueios corretos por regras estruturais adicionais (1 H2, <120 palavras), não falsos positivos semânticos.

## 7. Fail-closed

- HTML inválido: caminho inexistente → BLOCK_PUBLICATION com `missing_path`.
- Campo ausente: regex não encontra title/meta/canonical/H1 → BLOCK_PUBLICATION.
- Erro interno: `article_generator.py` captura `PublicationGateError` e registra como `skipped`, não escreve arquivo.
- Em `orchestrator_24h.py`, exceção no gate é capturada e logada, mas o fluxo continua; itens não bloqueados por erro são publicados. Isso é uma lacuna moderada.

## 8. Integridade confirmada

- 966 páginas do estoque: não alteradas
- Sitemap: não alterado
- Registry: não alterado
- Commits adicionais: nenhum
- Publicações: nenhuma
- Recuperação em massa: nenhuma

## 9. Lacunas encontradas

### Críticas
1. **Semântica não avaliada**: o gate não detecta conteúdo degradado que satisfaz todos os thresholds quantitativos.
2. **Lorem ipsum não detectado**: texto latim padrão passa como conteúdo válido.
3. **Repetição distribuída não detectada**: padrões genéricos espalhados em múltiplas seções não atingem o threshold de 3 ocorrências iguais.

### Moderadas
4. **Fail-closed parcial em orchestrator_24h**: erro no gate não impede publicação automaticamente.
5. **Semântica de link interno**: link irrelevante satisfaz a regra de link interno.

### Melhorias futuras
6. Detectar sequências de placeholder/variantes com regex mais abrangente.
7. Adicionar heurística de diversidade lexical.
8. Considerar análise de entropia de texto para detectar lorem ipsum/gibberish.

## 10. Recomendação operacional

O Publication Gate **não é plenamente confiável para produção** em seu estado atual.
Ele é eficaz contra as classes de degradação conhecidas da E.1.6, mas falha contra conteúdo degradado construído para escapar das regras mínimas.

Próxima ação: corrigir as lacunas críticas antes de declarar o gate como proteção suficiente.
