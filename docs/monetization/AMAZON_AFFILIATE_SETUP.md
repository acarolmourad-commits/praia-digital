# Amazon Associates — Guia de Injeção de Tag

## Status
- StoreID oficial aplicada em produção: `praiadigital-20`

## Ponto único de injeção
- Componente central: `partials/affiliate-products.html`
- Artigos injetados:
  - `blog/como-preparar-imovel-para-aluguel-temporada-riviera-2026.html`
  - `blog/guia-de-servicos-e-conveniencia-riviera-de-sao-lourenco-2026.html`
  - `blog/esportes-e-lazer-na-riviera-de-sao-lourenco-2026.html`
  - `blog/guia-pet-friendly-riviera-de-sao-lourenco-bertioga-2026.html`

## Formato aplicado
- Links com parâmetro `tag=praiadigital-20` em todas as seções de produtos recomendados.
- Exemplo: `https://www.amazon.com/s?k=smart+lock&tag=praiadigital-20`

## Instruções rápidas
1. Abra `partials/affiliate-products.html` ou os artigos acima.
2. Localize os links de cada card.
3. Para alterar a tag, substitua `praiadigital-20` pelo novo ID em todos os arquivos.
4. Salve e faça commit.

## Observações
- Mantenha o mesmo destino por categoria para facilitar a troca futura.
- Não exponha chaves secretas; apenas o `tag` público do programa.
- Valide HTTP 200 após alterações.
