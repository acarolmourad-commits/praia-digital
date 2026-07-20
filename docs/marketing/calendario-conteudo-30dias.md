# Calendário de Marketing & Redes Sociais — Praia Digital (30 dias)

Parte da estrutura proptech. Conteúdo 100% inédito, ancorado nos 14 roteiros e 12 artigos já publicados (sem duplicar os 1.300 do blog).

## Pilar de conteúdo
- **Diário (vídeo):** 1 Reels/TikTok/Short por dia, da série "Diário do Hermes" (14 roteiros prontos em `docs/content/roteiros-video-diario.json`).
- **Semanal (newsletter):** toda 2ª, resumo do boletim + imóvel em destaque (`assets/newsletter-semanal.html`).
- **Quinzenal (artigo SEO):** 2 artigos inéditos/mês (`blog/` — 12 já publicados, +12 por gerador).
- **Mensal (parceiros):** 1 case white-label para LinkedIn/B2B.

## Calendário Dia a Dia (exemplo recorrente)
| Dia | Rede | Formato | Tema (roteiro #) |
|----|------|---------|-----------------|
| 1 | IG/TikTok | Short | #1 Santos lidera yield |
| 2 | IG/TikTok | Short | #2 Airbnb ou anual |
| 3 | IG/TikTok | Short | #3 Erro de precificação |
| 4 | IG/TikTok | Short | #4 Score Hermes 10s |
| 5 | IG/TikTok | Short | #5 Cidades subvalorizadas |
| 6 | LinkedIn | Post B2B | Case white-label |
| 7 | IG/TikTok | Short | #6 Financiar praia |
| 8 | Newsletter | E-mail | Edição semanal |
| 9 | IG/TikTok | Short | #7 Kitnet maior mult. |
| 10 | IG/TikTok | Short | #8 Comparador |
| 11 | IG/TikTok | Short | #9 Gestão zero horas |
| 12 | IG/TikTok | Short | #10 Avaliação IA |
| 13 | IG/TikTok | Short | #11 Assistente virtual |
| 14 | IG/TikTok | Short | #12 Gerador descrições |
| 15 | LinkedIn | Artigo | "Por que proptech no litoral" |
| 16 | IG/TikTok | Short | #13 Recomendação auto |
| 17 | IG/TikTok | Short | #14 Boletim diário |
| 18 | IG/TikTok | Short | Repete #1 (sazonado) |
| 19 | Newsletter | E-mail | Edição semanal |
| 20 | IG/TikTok | Short | Artigo #1 Imposto renda |
| 21 | IG/TikTok | Short | Artigo #2 2026 vs 2027 |
| 22 | LinkedIn | Post B2B | Plano de assinatura Pro |
| 23 | IG/TikTok | Short | Artigo #5 Reforma 5k |
| 24 | IG/TikTok | Short | Artigo #8 Airbnb vs Booking |
| 25 | IG/TikTok | Short | Artigo #11 1ª renda 30d |
| 26 | Newsletter | E-mail | Edição semanal |
| 27 | IG/TikTok | Short | Artigo #12 Mercado inverno |
| 28 | IG/TikTok | Short | Repete #4 Score |
| 29 | LinkedIn | Case | Parceira fechada |
| 30 | IG/TikTok | Short | Resumo do mês |

## KPIs
- Alcance: 50k/mês em 90 dias.
- Lead qualificado: 200/mês via ferramentas.
- Conversão assinatura: 5%/mês dos leads Pro.
- Imóveis cadastrados: +500 no trimestre.
- Parceiras white-label: 20 no trimestre.

## Automação
- Cron `boletim-diario-inteligencia` (07h): gera boletim.
- Cron `newsletter-semanal-praia` (2ª 08h): gera newsletter + avisa.
- Cron `video-ideia-diaria` (08h): envia roteiro do dia no Telegram.
