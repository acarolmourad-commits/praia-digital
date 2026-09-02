# CJ / Booking.com Affiliate Setup

## Status
Aguardando AID/Publisher ID do Booking.com via Commission Junction (CJ).

## Passo a passo para captura do AID
1. Acesse `https://members.cj.com/member/7746180/publisher/links/search/` com a conta da Praia Digital.
2. Busque por `Booking.com`.
3. Copie o `AID` ou `Publisher ID` do link/formulário de Booking.

## Ativação
1. Abra `partials/booking-banner.html`.
2. Substitua `BOOKING_AID_PLACEHOLDER` pelo AID final.
3. Commit e push.
4. Valide HTTP 200 nas páginas com banner.

## Notas
- O placeholder atual é: `BOOKING_AID_PLACEHOLDER`
- Documentação complementar: `docs/monetization/MULTI_AFFILIATE_NETWORKS.md`
