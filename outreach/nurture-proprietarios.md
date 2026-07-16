# Nurture / Win-Back — Proprietários Autogestores

Leads marcados como `sem_interesse` NÃO são perdidos. Re-tocar em ondas para mantê-los quentes.

## Cadência
- **D+30** após "não" → Msg5 (valor sem pressão: dica de mercado / variação de preço na rua)
- **D+60** → Msg5b (prova social: novo caso +64% ou novo recurso)
- **D+90** → Msg5c (última tentativa cordial, porta aberta)

Se o lead responder a qualquer Msg5, volta para o funil ativo (Msg2.5).

## Mensagens (WhatsApp — adaptar nome/cidade)

**Msg5 (D+30) — dica de mercado:**
> Oi [Nome], tudo bem? Não é pra vender nada — só pra te avisar: subiu a procura por [Cidade] nesse período e muita gente autogestora está deixando diária na tabela por não reprecificar. Se quiser, simulo rápido quanto seu imóvel ficaria com precificação dinâmica. Sem compromisso. 😉

**Msg5b (D+60) — prova social:**
> [Nome], lembra que a gente conversou? Um proprietário aqui de [Cidade] que anunciava sozinho passou pra Gestão Completa e subiu 64% a receita trabalhando zero horas. Se um dia o tempo de cuidar do Airbnb pesarr, a gente está aqui. É só me dar um alô.

**Msg5c (D+90) — porta aberta:**
> [Nome], última mensagem mesmo, prometo não incomodar mais. Fica aqui meu contato se surgir interesse em ter a Praia Digital cuidando de tudo (limpeza, check-in, preço). Um abraço e bom proveito do seu imóvel! 🏖️

## E-mail (mesmo gatilho, tom um pouco mais formal)
Usar `assets/retorno-gestao-completa.html` como prova social na Msg5b.

## Regra
- 1 mensagem por onda. Não insistir além de D+90.
- Marcar no tracker: `nutrir` (em nurture) → ao reengajar: `respondeu` / ao fechar: `fechou`.
- O `relatorio_nurture.py` avisa no Telegram quem está na janela D+30/60/90.
