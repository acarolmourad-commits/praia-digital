# Relatório Editorial Semanal — Praia Digital

**Data:** 24 de agosto de 2026  
**Script:** `docs/scripts/build_banco_editorial.py`  
**Arquivo gerado:** `docs/banco-editorial.json`

---

## Resumo

| Métrica | Valor |
|---|---|
| Total de artigos no banco editorial | 3.653 |
| Sinais de duplicidade detectados | 857.290 |
| Artigos que precisam atualização | 0 |
| Problemas de canonical tag | 0 |

---

## Análise rápida

- **Total de artigos:** 3.653 artigos processados do diretório `blog/`.
- **Duplicidade:** 857.290 sinais de possível duplicidade foram encontrados. Esse número é elevado porque o algoritmo compara pares de títulos por similaridade (>= 0,85) e o corpus contém muitas palavras comuns como "litoral", "imóveis" e "imobiliárias". Não significa que há centenas de milhares de artigos duplicados; a maioria dos pares deve ser legítima. Recomenda-se revisão manual por amostragem ou ajuste do limiar.
- **Atualizações necessárias:** Nenhum artigo apresentou problema de canonical tag, então não há candidatos imediatos a atualização técnica.
- **Tipos de artigo:** Predominam artigos SEO gratuitos (tipo A: 3.616), seguidos por artigos-ponte (tipo C: 18), artigos de conversão (tipo E: 16), artigos comerciais (tipo B: 1) e artigos de autoridade (tipo D: 2).

---

## 5 próximos temas prioritários

Com base na cobertura atual por cluster e cidade, os próximos temas prioritários (alta prioridade, score 3) são:

1. **Investimento em Caraguatatuba** — cluster: `investimento`
2. **Compra e venda em Ilhabela** — cluster: `compra_venda`
3. **Investimento em Ilhabela** — cluster: `investimento`
4. **Investimento em Itanhaém** — cluster: `investimento`
5. **Locação de temporada em Itanhaém** — cluster: `locacao_temporada`

---

## Observações

- O mapeamento de produtos foi aplicado a **6 categorias** de produtos, com destaque para `ebook-rentabilidade-temporada` (473 artigos vinculados) e `curso-marketing-digital-imobiliaria` (102 artigos vinculados).
- Não foram registrados problemas de canonical tag no escaneamento atual.
- Recomenda-se, na próxima semana, uma amostragem manual dos sinais de duplicidade ou ajuste do algoritmo para reduzir falsos positivos.
