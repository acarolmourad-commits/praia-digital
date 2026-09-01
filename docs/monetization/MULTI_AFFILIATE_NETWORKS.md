# Multi-Affiliate Networks — Guia de Injeção

## Objetivo
Padronizar a injeção de IDs de afiliado em múltiplas plataformas nos componentes existentes do Praia Digital.

## Redes suportadas
- Amazon Associates: já implementado via `tag=praiadigital-20`
- Mercado Livre
- Shopee
- Booking.com

## Pontos de injeção
- Componente central: `partials/affiliate-products.html`
- Blocos inline nos artigos do blog que contêm `.affiliate-card`
- Booking.com: `partials/booking-banner.html`

## Formato por rede
- Amazon: `https://www.amazon.com/s?k=...&tag=praiadigital-20`
- Mercado Livre: `https://www.mercadolivre.com.br/...?id_afiliado=SEU_ID`
- Shopee: `https://shopee.com.br/...?af_id=SEU_ID`
- Booking.com: `https://www.booking.com/searchresults.pt.html?aid=BOOKING_AID_PLACEHOLDER&label=praia-digital`

## Booking.com — Ativação
1. Abra `partials/booking-banner.html`.
2. Substitua `BOOKING_AID_PLACEHOLDER` pelo AID final.
3. Insira o componente nas páginas desejadas via include ou snippet.
4. Valide HTTP 200 após alterações.

## Instruções
1. Abra os arquivos listados em `docs/monetization/PRODUCT_MAPPING_2026.md`.
2. Localize os `href` dos cards de afiliados.
3. Para cada rede, substitua o placeholder pelo link formatado com o ID correspondente.
4. Valide HTTP 200 após alterações.

## Observações
- Mantenha os IDs organizados por categoria para facilitar manutenção.
- Não use placeholders expostos em produção.
- Evite redirecionamentos intermediários sem HTTPS.
