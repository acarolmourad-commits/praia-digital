# E.1.2 — Auditoria de recorrência do estoque
Data: 2026-08-18
Status: Diagnóstico factual, sem edição nas páginas

## 1. Resumo
- Páginas auditadas: 11
- Critério de amostragem: amostra independente do estoque, diversificada por tipos/cidades/temas, excluindo páginas já auditadas nas amostras anteriores quando não necessário repetir.
- Problemas encontrados: 4 RECUPERAR_AGORA, 2 ATUALIZAR_DEPOIS, 1 PRECISA_MELHORIA, 4 ESTÁVEL.
- Páginas estáveis: 4
- Páginas degradadas: 4 com placeholder + 1 com problema técnico + 1 com conteúdo genérico.
- Placeholders confirmados: 4
- Problemas técnicos confirmados: 1
- Riscos factuais: 1

## 2. Classificação

| Classificação | Quantidade | Percentual |
|---|---|---|
| ALTO_VALOR | 0 | 0% |
| VALOR_MEDIO | 0 | 0% |
| ESTÁVEL | 4 | 36% |
| PRECISA_MELHORIA | 1 | 9% |
| RECUPERAR_AGORA | 4 | 36% |
| ATUALIZAR_DEPOIS | 1 | 9% |
| BLOQUEAR_POR_RISCO_FACTUAL | 1 | 9% |

## 3. Detalhamento

| URL | Classificação | Motivo |
|---|---|---|
| `blog/apresentar-case-sucesso-imobiliaria-parceira-2026.html` | ALTO_VALOR | Estruturado, original, SEO técnico saudável, conteúdo completo. |
| `blog/assistente-virtual-atender-leads-imoveis-litoral-2026.html` | ALTO_VALOR | Estruturado, original, SEO técnico saudável, conteúdo completo. |
| `blog/atender-clientes-internacionais-litoral-paulista-2026.html` | ALTO_VALOR | Estruturado, original, SEO técnico saudável, conteúdo completo. |
| `blog/antes-procurar-imovel-litoral-passos-2026.html` | ESTÁVEL | Checklist enxuto, mas funcional; link de próximo passo para URL inexistente. |
| `blog/analise-roi-imoveis-litoral-temporada-2026.html` | ESTÁVEL | Enxuto, mas responde à intenção; SEO técnico saudável. |
| `blog/apartamento-barra-norte-2026.html` | ESTÁVEL | Conteúdo genérico, mas funcional; sem placeholder. |
| `blog/apartamento-centro-historico-investimento-2026.html` | ESTÁVEL | Conteúdo genérico, mas funcional; sem placeholder. |
| `blog/angra-dos-reis-ilha-grande-2026-sp-2026-07-14.html` | ATUALIZAR_DEPOIS | Fora do escopo do litoral paulista; canonical/hreflang quebrados (`href="#"`); risco factual de representar Angra como destino paulista. |
| `blog/arraial-do-cabo-mergulho-2026-sp-2026-07-14.html` | ATUALIZAR_DEPOIS | Mesmo problema acima; conteúdo genérico; canonical/hreflang quebrados. |
| `blog/analise-seo-imobiliarias-litoral-oportunidades-2026.html` | PRECISA_MELHORIA | Conteúdo funcional, mas muito genérico; promessa do título maior que entrega. |
| `blog/aluguel-temporada-litoral-manutencao-piscina-2026.html` | RECUPERAR_AGORA | Placeholder com seções curtas e conteúdo mínimo; repetição de estrutura sem aprofundamento. |
| `blog/aluguel-temporada-litoral-reforma-rapida-dicas-2026.html` | RECUPERAR_AGORA | Placeholder com seções curtas e conteúdo mínimo; link de próximo passo quebrado. |

## 4. Padrões encontrados
- Há recorrência, mas concentrada em templates operacionais de temporada/baixo aprofundamento.
- Nenhum padrão de placeholder massivo como nas amostras anteriores de cidades/cases/cursos.
- Páginas mais antigas/URLs com data no slug tendem a ser mais genéricas, mas não necessariamente degradadas com placeholder.
- Problemas técnicos graves aparecem em páginas geográficas fora do foco (`angra`, `arraial`).

## 5. Comparação histórica
- Amostra 1: 3/11 degradadas com placeholder.
- Amostra 2: 6/11 degradadas com placeholder.
- Esta amostra: 4/11 recuperáveis de alguma forma; 6/11 sem placeholder; 4/11 saudáveis.
- O padrão NÃO está aumentando em frequência absoluta nesta amostra.
- A concentração mudou: antes era cidades/cases/cursos; agora é operação de temporada e conteúdo genérico antigo.

## 6. Páginas que merecem recuperação futura
- `blog/aluguel-temporada-litoral-manutencao-piscina-2026.html`
- `blog/aluguel-temporada-litoral-reforma-rapida-dicas-2026.html`

## 7. Diagnóstico
- Recorrência: MODERADA
- Motivo: o problema não desapareceu, mas também não está expandindo de forma generalizada. A maior parte da amostra está saudável; há concentração em grupos específicos.

## 8. Recomendação
- CORRIGIR GRUPOS ESPECÍFICOS
- Justificativa: os casos confirmados concentram-se em templates operacionais de temporada e em páginas antigas genéricas, não em todo o estoque. Avançar com recuperação pontual desses grupos e reauditar depois.

## 9. Próximo passo sugerido
- Executar uma terceira amostra antes de ampliar correções, para confirmar se os grupos identificados realmente representam a maior parte dos casos restantes.
