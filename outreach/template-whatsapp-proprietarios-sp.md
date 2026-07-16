# Template WhatsApp — Proprietários Autogestores (São Paulo / CAPITAL)

Sequência de 3 mensagens curtas de abordagem para o WhatsApp.
Público: proprietários que anunciam sozinhos no Airbnb/Booking na **capital paulista**.
Dor central: perda de tempo com limpeza, check-in e precificação errada.
Solução: Gestão Completa + Tecnologia de Precificação Dinâmica → "ganhe mais, trabalhando zero horas".
Tom: profissional, cordial, foco em ROI.

> Variável: `[Nome]` = proprietário. Região fixa: **São Paulo**.

## MSG 1 — Quebra-gelo (valida a dor sem vender)
> Olá, [Nome]! Tudo bem? Sou da Praia Digital. Vi que você anuncia seu imóvel no Airbnb/Booking em São Paulo. Imagino a rotina: coordenar a limpeza, correr pro check-in entre um compromisso e outro, e ainda tentar acertar o preço todo dia numa cidade onde a demanda muda a cada evento e feriado. É trabalho demais pra quem queria só ver o aluguel cair na conta, né?

## MSG 2 — Solução + ROI (o "zero horas")
> Por isso criamos a **Gestão Completa**: cuidamos de limpeza, check-in e, o principal, aplicamos nossa **Tecnologia de Precificação Dinâmica** — que ajusta o valor diário conforme a procura em São Paulo e eleva sua ocupação. Resultado: você **ganha mais, trabalhando zero horas**. Sem dor de cabeça, sem correria.

## MSG 3 — Encerramento cordial (CTA leve, sem pressão)
> [Nome], sem nenhum compromisso: posso te mostrar uma simulação rápida de quanto seu imóvel pode render com a gente? Leva 2 minutinhos e pode abrir seus olhos pro retorno real. O que acha?

## Notas de copy (capital vs. litoral)
- Em SP capital o dono quase nunca mora perto do apto → o check-in é o maior atrito (trânsito/imprevisibilidade). A Msg1 foca nisso.
- A precificação dinâmica brilha em cidade com eventos/feriados/congressos espalhados → Msg2 ressalta "cada evento e feriado".
- Não cite praia/mar (é capital urbana). Foque em "retorno", "ocupação", "zero horas".

## Como gerar lote CSV
O funil atual (`scripts/gerar_lote_whatsapp.py`) cobre o **litoral de SP** (Santos, Guarujá, Praia Grande, Itanhaém, São Vicente, Peruíbe, Bertioga). Para usar esta variante capital:
1. Precisa de uma base de leads da **capital** (CPF/CNPJ, nome, telefone, bairro).
2. Estender `gerar_lote_whatsapp.py` para aceitar um arquivo de entrada de SP-capital e usar este template (colunas Mensagem_1_QuebraGelo / Mensagem_2_Solucao / Mensagem_3_Encerramento).
3. Ou tratar as 7 cidades atuais como "Grande SP/litoral" e aplicar este mesmo copy (trocar só a variável de região por bairro).
