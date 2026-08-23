# Calculadora de Preços — Hermes Agents

## Variáveis de precificação

| Variável | Tipo | Observação |
|---|---|---|
| Volume de mensagens | número | Mensagens totais/mês (inbound + outbound) |
| Número de agentes | número | Agentes autônomos distintos em produção |
| Complexidade | categoria | Básica / Intermediária / Avançada |
| Suporte | categoria | Padrão / Premium / Dedicado |

---

## Tabela base

### Por complexidade

| Complexidade | Preço base/agente | Multiplicador mensagem |
|---|---|---|
| Básica | R$ 1.200/mês | 1,0x |
| Intermediária | R$ 2.400/mês | 1,5x |
| Avançada | R$ 4.500/mês | 2,0x |

### Por suporte

| Suporte | Fator |
|---|---|
| Padrão | +0% |
| Premium | +35% |
| Dedicado | +80% |

### Crédito de mensagem por faixa

| Faixa de mensagens | Crédito incluso |
|---|---|
| Até 5.000/mês | 100% |
| 5.001 a 20.000/mês | 80% |
| 20.001 a 100.000/mês | 60% |
| 100.001+/mês | negociado |

---

## Fórmula

```
Custo base = Soma(preço base por agente por complexidade)
Crédito = Custo base * crédito por faixa
Custo adicional = max(0, mensagens - crédito) * R$ 0,08 * multiplicador
Subtotal = Custo base + Custo adicional
Suporte = Subtotal * fator_suporte
Total = Subtotal + Suporte
```

---

## Exemplo 1 — Clínica (intermediária, 3 agentes, 12k mensagens)
- Agentes: 3 × R$ 2.400 = R$ 7.200
- Crédito: 80% = R$ 5.760
- Adicional: (12.000 − 9.600) × R$ 0,08 × 1,5 = R$ 288
- Subtotal: R$ 5.760 + R$ 288 = R$ 6.048
- Suporte premium (+35%): R$ 2.116,80
- **Total: R$ 8.164,80/mês**

---

## Exemplo 2 — E-commerce (avançada, 5 agentes, 55k mensagens)
- Agentes: 5 × R$ 4.500 = R$ 22.500
- Crédito: 60% = R$ 13.500
- Adicional: (55.000 − 33.000) × R$ 0,08 × 2,0 = R$ 3.520
- Subtotal: R$ 13.500 + R$ 3.520 = R$ 17.020
- Suporte padrão (+0%): R$ 0
- **Total: R$ 17.020/mês**

---

## Simulação rápida

- **Imobiliária:** 2 agentes básicos + 8k mensagens + suporte padrão ≈ R$ 2.800/mês
- **Advocacia:** 3 agentes avançados + 6k mensagens + suporte dedicado ≈ R$ 22.400/mês
- **Startup:** 4 agentes intermediários + 18k mensagens + suporte premium ≈ R$ 16.500/mês

---

## Notas
- Preços base atualizados em 08/2026
- Taxa por mensagem excedente calculada por envio/entrada processada pelo agente
- Descontos anuais disponíveis (10% pagamento anual)
- Customizações: negociar por contrato
