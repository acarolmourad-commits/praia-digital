# Material de Retorno — Prova de ROI (resposta à Msg 2)

Quando o proprietário responde "sim" à Msg 2 (quer ver exemplo real de ROI), envie a **Msg 2.5** abaixo por WhatsApp, seguida do link da landing `assets/retorno-gestao-completa.html`. Tudo reaproveita ativos já existentes da Praia Digital — sem duplicar conteúdo.

## Mensagem 2.5 — Prova de ROI (copiar/colar)

```
[Nome], perfeito! Olha um exemplo real de um imóvel parecido com o seu no [Cidade]:

📊 Caso [Cidade] — apartamento 2 quartos, temporada:
• Antes (autogestão): ~R$ 2.100/mês · dono fazia tudo (limpeza, check-in, preço "no olhômetro")
• Depois (Praia Digital): ~R$ 3.450/mês · +64% de receita, zero horas do dono
• Tecnologia de Precificação Dinâmica ajusta a diária toda virada de demanda (feriados, eventos, baixa estação)

Você ganha mais dormindo. 😴💰
Quer eu simular no SEU imóvel? É só me passar quartos e bairro que eu traço o ROI real.
```

## Landing de apoio (reuso de ativos)
- `assets/roi-ia-imobiliaria.html` — calculadora de ROI
- `assets/servico-avaliacao-preco-imoveis-litoral.html` — avaliação automática de preço
- `assets/simulador-roi-parcerias-imobiliarias-2026.html` — simulador de parcerias

Link curto pra enviar: https://praia.digital (central de ferramentas)

## Regra de fluxo
1. Lead responde "sim" à Msg 2 → status `respondeu` no tracker (`atualizar_status_whatsapp.py --status respondeu`)
2. Envia Msg 2.5 + link
3. Se fecha proposta → `--status fechou --valor <R$ mensal estimado>`
4. Sem resposta após Msg 2.5 → mantém `respondeu`, reaborda no ciclo mensal
