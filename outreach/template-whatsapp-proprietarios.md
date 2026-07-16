# Template — Outreach WhatsApp (Proprietários Autogestores)

**Público-alvo:** proprietários que anunciam sozinhos no Airbnb/Booking em `[Região]`.
**Dores:** perda de tempo com limpeza, check-in e precificação errada.
**Solução:** Gestão Completa + Tecnologia de Precificação Dinâmica → ganhar mais trabalhando zero horas.
**Tom:** profissional, cordial, foco em ROI.

> Substituir `[Nome]` e `[Região]` antes do envio. Sequência: msg 1 hoje, msg 2 em +1 a 2 dias, msg 3 em +3 a 4 dias.

---

## Mensagem 1 — Abordagem (quebra-gelo)

```
Olá, [Nome]! Tudo bem? Sou da Praia Digital e vi que o seu imóvel em [Região] está anunciado direto no Airbnb/Booking. 👋

Sem compromisso nenhum: muitos proprietários que cuidam sozinhos acabam perdendo horas com limpeza, check-in e uma precificação que não acompanha a demanda — e deixam dinheiro na mesa sem perceber. Você sente isso aí também?
```

## Mensagem 2 — Solução (follow-up +1 a 2 dias)

```
[Nome], só pra complementar: a Praia Digital oferece Gestão Completa + Tecnologia de Precificação Dinâmica. A gente assume limpeza, check-in e o preço certo em cada dia — e você ganha mais trabalhando zero horas. 💡

Quem adota o modelo costuma ver o faturamento subir enquanto o trabalho cai a zero. Posso te mandar um exemplo real de ROI de um imóvel parecido com o seu?
```

## Mensagem 3 — Encerramento cordial (follow-up +3 a 4 dias)

```
[Nome], não vou insistir — só não queria que esse tempo perdido com limpeza e preço errado continuasse custando o seu lucro. 🤝

Se um dia quiser ganhar mais sem levantar um dedo, a Praia Digital resolve. Fico à disposição quando fizer sentido. Um abraço e bom proveito do seu imóvel!
```

---

## Variáveis
- `[Nome]` — nome do proprietário (do CSV de prospecção).
- `[Região]` — cidade/região do imóvel (ex.: São Paulo, Santos, Guarujá).

## Notas de operação
- Envio via WhatsApp manual (SMTP não configurado) — copiar/colar por contato.
- Não insista após a msg 3; marque o lead como `sem_interesse` no registro.
- Para lotes grandes, gere CSV com as 3 mensagens pré-preenchidas e importe no WhatsApp Business (etiquetas).

## Arquivos relacionados
- `outreach/template-whatsapp-proprietarios-sp.md` — variante **São Paulo (capital)**: mesmo funil, gatilhos urbanos (check-in distante, eventos/feriados). Use quando o público for a capital paulista em vez do litoral.
