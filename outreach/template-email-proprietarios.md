# Template — Outbound Email (Proprietários Autogestores)

**Público-alvo:** proprietários que anunciam sozinhos no Airbnb/Booking em `[Região]`.
**Canal:** e-mail (Brevo/Gmail/Outlook manual — SMTP não configurado).
**Dores:** perda de tempo com limpeza, check-in e precificação errada.
**Solução:** Gestão Completa + Tecnologia de Precificação Dinâmica → ganhar mais trabalhando zero horas.
**Tom:** profissional, cordial, foco em ROI.

> Substituir `[Nome]` e `[Cidade]` antes do envio. Sequência: email 1 hoje, email 2 em +2 dias, email 3 em +5 dias.

---

## Email 1 — Abordagem (quebra-gelo)

```
Assunto: [Nome], seu imóvel em [Cidade] pode estar rendendo mais (sem seu trabalho)

Olá, [Nome].

Sou da Praia Digital e vi que seu imóvel em [Cidade] está anunciado direto no Airbnb/Booking.

Sem compromisso: muitos proprietários que cuidam sozinhos perdem horas com limpeza, check-in e uma precificação que não acompanha a demanda — e deixam dinheiro na mesa sem perceber.

Você sente isso aí também?

Um abraço,
Equipe Praia Digital
```

## Email 2 — Solução (follow-up +2 dias)

```
Assunto: Re: seu imóvel em [Cidade] — ganhar mais trabalhando zero horas

[Nome], complementando:

A Praia Digital oferece Gestão Completa + Tecnologia de Precificação Dinâmica. Assumimos limpeza, check-in e o preço certo em cada dia — e você ganha mais trabalhando zero horas.

Exemplo real (imóvel parecido em [Cidade]): ~R$ 2.100/mês autogestão → ~R$ 3.450/mês conosco (+64%), zero horas do dono.

Quer que eu simule o ROI no SEU imóvel? É só responder com quartos e bairro.

Equipe Praia Digital
```

## Email 3 — Encerramento cordial (follow-up +5 dias)

```
Assunto: Última mensagem sobre seu imóvel em [Cidade]

[Nome], não vou insistir — só não queria que esse tempo perdido com limpeza e preço errado continuasse custando seu lucro.

Se um dia quiser ganhar mais sem levantar um dedo, a Praia Digital resolve. Fico à disposição quando fizer sentido.

Um abraço e bom proveito do seu imóvel!

Equipe Praia Digital
```

---

## Variáveis
- `[Nome]` — nome do proprietário.
- `[Cidade]` — cidade do imóvel.

## Notas de operação
- Envio manual via Brevo/Gmail/Outlook (SMTP não configurado).
- Importar o CSV `lote-email-proprietarios-<LOTE>-<DATA>.csv` no Brevo ou copiar/colar.
- Marcar status no tracker (`atualizar_status_email.py`): enviado_email1/2/3, respondeu, fechou, sem_interesse.
