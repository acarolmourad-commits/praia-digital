# Relatório Editorial Semanal — Praia Digital

**Data:** 7 de setembro de 2026  
**Script:** `docs/scripts/build_banco_editorial.py`  
**Domínio:** praia.digital

---

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| **Total de artigos** | 3.878 |
| **Sinais de duplicidade** | 5.502 |
| **Artigos para atualização** | 0 |
| **Problemas de canonical** | 0 |

---

## Detalhamento

### Total de artigos
O banco editorial conta com **3.878 artigos** publicados em `/blog`.

### Sinais de duplicidade
Foram detectados **5.502 sinais** de possível duplicidade (pares de títulos com similaridade ≥ 0.85, mesma intenção, cluster e cidade). A detecção usa `SequenceMatcher` e agrupa por cidade, intenção e cluster editorial para reduzir falsos positivos.

### Artigos que precisam atualização
Nenhum artigo foi sinalizado para atualização técnica imediata. Todos os 3.878 artigos possuem referência canônica correta.

### 5 próximos temas prioritários
Com base na matriz cidade × cluster e pontuação de prioridade, os temas com maior urgência são:

1. **Compra e venda — Ilhabela**
2. **Investimento — Ilhabela**
3. **Investimento — Itanhaém**
4. **Locação temporária — Itanhaém**
5. **Compra e venda — Litoral Norte**

---

## Observações
- O script gerou `docs/banco-editorial.json` com o inventário completo, incluindo mapeamento de produtos, clusters, funil e intenção de busca.
- Nenhum problema crítico de SEO técnico (canonical) foi encontrado.
- A lista de duplicidades deve ser revisada manualmente para consolidar ou diferenciar os pares apontados.
