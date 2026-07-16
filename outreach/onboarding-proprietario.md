# Onboarding Proprietário — Gestão Completa (pós-fechou)

Quando o lead vira `fechou` no tracker, inicie o onboarding abaixo. Reaproveita a estrutura de `docs/sales/onboarding/onboarding-*.html` mas com passos de ativação de imóvel (não de parceria).

## Mensagem de boas-vindas (WhatsApp — copiar/colar)

```
[Nome], seja muito bem-vindo(a) à Praia Digital! 🎉 Seu imóvel em [Cidade] agora roda no piloto de Gestão Completa.
Resumo do que acontece a partir de agora:
1️⃣ Contrato e acesso — te mando o link pra assinar e liberar o calendário do Airbnb/Booking pra gente.
2️⃣ Ficha do imóvel — me manda fotos, regras e o que não pode faltar pro hóspede.
3️⃣ Precificação Dinâmica ON — a gente calibra o preço ideal por dia. Você não toca em nada.
4️⃣ Primeira reserva — você recebe o relatório semanal de faturamento no WhatsApp.

Você ganha mais trabalhando zero horas. Qualquer dúvida, estou aqui. Vamos nessa! 💪
```

## Checklist de ativação (terra no prazo de 5 dias)
- [ ] Contrato assinado (link enviado)
- [ ] Acesso de coanfitrião liberado (Airbnb + Booking)
- [ ] Fotos e descrição recebidas
- [ ] Regras da casa e check-in definidas
- [ ] Precificação Dinâmica ativada
- [ ] Primeira diária publicada
- [ ] Relatório semanal agendado

## Landing de apoio
- `assets/onboarding-proprietario.html` — página de boas-vindas + checklist visual

## Regra
- Após `fechou`: `atualizar_status_whatsapp.py --status fechou --valor <R$ mensal>`
- Envia Msg boas-vindas + link da landing
- Marca checklist no registro do lote (`outreach/followup-registro-<LOTE>.md`)
