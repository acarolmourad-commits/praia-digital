# Relatório Editorial Semanal — Praia Digital

**Data:** 16 de novembro de 2026
**Script:** `docs/scripts/build_banco_editorial.py` (executado em 16/11/2026, exit 0)

## Visão geral

- **Total de artigos no banco editorial:** 4.159
- **Distribuição por tipo:** A=2.952 (SEO gratuito), C=413 (artigo-ponte), E=374 (comercial), D=210 (autoridade), B=210 (conversão)
- **Sinais de duplicidade detectados:** 7.145 (JSON de saída limitado aos 100 primeiros; total completo no log da execução)
- **Problemas de canonical:** 0
- **Artigos que precisam de atualização:** 0

## Distribuição por cluster

| Cluster | Quantidade |
|---|---|
| automacao_ia | 1.110 |
| bairros_cidades | 843 |
| locacao_temporada | 607 |
| editorial | 505 |
| compra_venda | 490 |
| investimento | 332 |
| marketing_digital | 155 |
| seo_local | 50 |
| juridico | 33 |
| cases | 16 |
| financiamento | 11 |
| parcerias | 7 |

## Top 5 próximos temas prioritários

1. **Cluster:** investimento | **Cidade:** Ilhabela | **Prioridade:** alta
2. **Cluster:** locação_temporada | **Cidade:** Itanhaém | **Prioridade:** alta
3. **Cluster:** investimento | **Cidade:** litoral_sp | **Prioridade:** alta
4. **Cluster:** compra/venda | **Cidade:** litoral_sul | **Prioridade:** alta
5. **Cluster:** investimento | **Cidade:** Maresias | **Prioridade:** alta

## Observações

- A base cresceu de 4.108 para 4.159 artigos (+51).
- Os sinais de duplicidade subiram de 6.892 para 7.145 (+253) — títulos muito similares com mesma intenção, cluster e cidade. Concentrados em clusters de temporada (ex.: variações de "cancelamento flexível", "checkout atrasado", "reserva para grupo grande"), indicando necessidade de revisão/merge de conteúdo semelhante.
- Nenhum artigo foi sinalizado como candidato a atualização nesta rodada (0 canonical issues, 0 update candidates). Há 96 artigos sem link canonical (ausência, não erro de canonicalização).
- Os próximos temas prioritários concentram-se em investimento, locação temporária e compra/venda, com foco em cidades estratégicas do litoral de SP (Ilhabela, Itanhaém, Maresias, Peruíbe, Riviera, litoral sul).

---
*Relatório gerado automaticamente pelo script `docs/scripts/build_banco_editorial.py`.*
