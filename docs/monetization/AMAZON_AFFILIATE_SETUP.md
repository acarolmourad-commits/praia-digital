# Amazon Associates — Guia de Injeção de Tag

## Objetivo
Centralizar a substituição do ID de afiliado da Amazon nos componentes de recomendação do Praia Digital.

## Ponto único de injeção
Edite `partials/affiliate-products.html` e substitua o parâmetro de tracking pelos valores do seu programa:

- Atual: `href="/afiliados/index.html"`
- Para injeção futura, altere para o modelo de link com tag, ex: `https://www.amazon.com/dp/XXXX?tag=praiadigital-20`

## Instruções rápidas
1. Abra `partials/affiliate-products.html`.
2. Localize os links de cada card.
3. Substitua o `href` pelo link de produto Amazon com o parâmetro `?tag=SEU_TAG` ou `&tag=SEU_TAG`.
4. Salve e faça commit.

## Observações
- Mantenha o mesmo destino por categoria para facilitar a troca futura.
- Não exponha chaves secretas; apenas o `tag` público do programa.
- Valide HTTP 200 após alterações.
