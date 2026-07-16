# Expansão B — Litoral Norte (Ubatuba / Ilhabela / Caraguatatuba / São Sebastião)

**Status:** mercado verde — 322 menções de SEO no blog (Ubatuba 136, Ilhabela 123, Caraguatatuba 63) e **ZERO leads B2B** na base (que cobre só sul/centro). O tráfego de busca existe; falta converter em parceria.

## Plano de aquisição (executável)

1. **Landings de parceria norte** (geradas em `parcerias-norte/parceria-*.html`) — convertem o tráfego de SEO em lead de imobiliária.
   - Gerador: `scripts/gerar_landing_parceria_norte.py`
   - Ações: linkar essas landings nos artigos de norte do blog (call-to-action "Seja parceira em {cidade}") e indexar no sitemap.
2. **Imobiliária âncora local** — fechar 1 parceira em cada cidade para validar o modelo norte (entrada B2B, igual às 101 já fechadas no sul).
3. **Lote B2B norte** — quando as landings trouxerem leads, gerar CSV com `gerar_lote_b2b.py` (já parametrizável por cidade/filtro) e seguir o mesmo funil.

## Template de abordagem B2B — Norte (3 mensagens)

> Variáveis: `[Cidade]` = Ubatuba/Ilhabela/Caraguatatuba · `[Contato]` = pessoa · `[Imob]` = imobiliária

**Msg1 — Quebra-gelo (âncora local)**
> Olá [Contato]! Tudo bem? Sou da Praia Digital. Acompanho a [Imob] em [Cidade] e sei que, na alta temporada, o desafio é manter o calendário cheio fora dos feriados — e sem depender só de anúncio pago. A gente resolve: levamos proprietários qualificados pra você e cuidamos da gestão completa de temporada. Você foca em fechar, não em check-in.

**Msg2 — Solução + prova social**
> [Contato], pra ser direto: já fechamos 101 parcerias com imobiliárias no litoral de SP (Santos, Guarujá, Praia Grande…) e o modelo sobe a ocupação da carteira com nossa Precificação Dinâmica. No [Cidade] ainda não temos parceira — queria que a [Imob] fosse a primeira a surfar esse fluxo de proprietários que o nosso blog já atrai (1.300+ artigos de SEO, incluindo vários de [Cidade]).

**Msg3 — Encerramento cordial**
> [Contato], sem compromisso: posso te mandar 1 case real de imobiliária parceira nossa que dobrou a ocupação em 90 dias? Leva 2 min e mostra o retorno no seu bolso. Se fizer sentido pra [Imob], a gente estrutura a parceria em [Cidade].

## Próximos passos
- [ ] Linkar landings nos artigos de norte do blog + sitemap
- [ ] Rodar `gerar_lote_b2b.py` quando houver leads norte
- [ ] Fechar âncora em Ubatuba (maior volume de SEO)
