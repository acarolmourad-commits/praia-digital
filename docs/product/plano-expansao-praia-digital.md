# Plano de Expansão — Praia Digital (análise baseada em dados reais)

**Autor:** Estratégia de Expansão (Produto/Mercado) · **Data:** 2026-07-16
**Base:** dados extraídos do repo em 16/07/2026 (sem invenção).

---

## 0. O que os dados REAIS mostram

| Fonte | Dado verificado |
|------|-----------------|
| Outbound proprietários (B2C) | 188 leads, 7 cidades (Santos, Guarujá, Praia Grande, Itanhaém, São Vicente, Peruíbe, Bertioga), funil operando |
| `docs/materiais/leads-litoral-enriquecido.csv` | **600 leads B2B** (imobiliárias/construtoras/gestores/corretores) |
| Status dessa base | 486 contato inicial · **101 parcerias FECHADAS** · 13 interessados |
| Perfil | construtora 158 · imobiliaria 140 · gestor 113 · administradora 74 · corretor 70 · corretor-autonomo 40 |
| Dor principal | leads 98 · conteudo 86 · anuncios 82 · conversao 70 · atendimento 64 |
| Orçamento estimado | mediana ~R$ (soma relevante) — canal com budgeting real |
| Parcerias fechadas por cidade | Santos 24 · Guarujá 14 · Peruíbe 13 · Itanhaém 12 · Praia Grande 11 · São Vicente 11 · Bertioga 8 · Mongaguá 8 |
| Blog SEO | 1.302 artigos; destinos mais citados: Bertioga 466, Santos 404, Guarujá 330, Praia Grande 272, Peruíbe 142, Ubatuba 136, Ilhabela 123, Itanhaém 113, Caraguatatuba 63 |

**Insight central:** a Praia Digital JÁ Opera um **canal B2B (imobiliárias) com 101 parcerias ativas** e 600 leads mapeados — mas o outbound que construímos foca só no **B2C (proprietário autogestor)**. Há um **desalinhamento de ativo vs. esforço**: o dinheiro/comissão recorrente vem das imobiliárias, mas a máquina de outbound está toda no proprietário.

---

## 1. Expansão A — Canal Imobiliárias (B2B) como produto dedicado  ⭐ prioridade 1

**Por que:** 101 parcerias já fechadas provam product-market fit. Orçamento médio dos leads B2B > B2C. Dores (leads, conteúdo, conversão) são exatamente o que nossa stack já resolve (SEO 1.302 artigos, calculadora de yield, simulador).

**Algoritmo conceitual — "Praia Digital Partner Score" (priorização):**
```
PPS = w1·pontuacao_lead + w2·(orcamento_normalizado) + w3·(ja_interagiu? 1:0) - w4·(dias_sem_contato)
pesos sugeridos: w1=0.4, w2=0.3, w3=0.2, w4=0.1
Gatilho: PPS > limiar → entra em follow-up automático (reuso do motor de outbound)
```

**Plano acionável:**
1. Reativar os **486 leads B2B em `contato_inicial_enviado`** (7+ dias sem toque) com sequência própria (copy B2B, não B2C).
2. Criar `docs/sales/csv-lotes-b2b/` com gerador parametrizado (reuso de `gerar_lote_whatsapp.py`).
3. Calcular PPS e priorizar Mongaguá/Bertioga (onde ainda há espaço vs. Santos saturado).
4. Propor pacote "Imobiliária Parceira": repasse de inventário + calculadora de yield white-label.

---

## 2. Expansão B — Norte do Litoral (Ubatuba/Ilhabela/Caraguatatuba)  ⭐ prioridade 2

**Por que:** blog já tem 136+123+63 = **322 menções de SEO** no litoral norte — há demanda de busca, mas ZERO cobertura de outbound e poucas parcerias. Mercado verde.

**Plano:**
- Mapear leads B2B do norte (ainda não estão na base de 600, que é só litoral sul/centro).
- Landing específica + calculadora de yield por CEP dessas cidades.
- Parceria com 1 imobiliária âncora local (entrada B2B).

---

## 3. Expansão C — White-label da Calculadora de Yield por CEP

**Por que:** a calculadora (backend testado + front protótipo) é um **ativo de aquisição B2B**: imobiliárias a usam no próprio site para captar proprietários. Transforma custo de dev em produto recorrente.

**Proposta de parceria real:** oferecer à imobiliária âncora (ex: as 101 já fechadas) a calculadora embedada no site delas, com lead compartilhado. Modelo: revenue share sobre contratos fechados via lead da calculadora.

---

## 4. Próximos passos imediatos (esta semana)

- [ ] Validar com Carolina qual expansão priorizar (A/B/C).
- [ ] Se A: gerar lote B2B de reativação (486 leads) + copiar template WPP para tom B2B.
- [ ] Se B: levantar base B2B litoral norte (scraping de portais ou parceria).
- [ ] Se C: empacotar calculadora como produto (pricing + termo de parceria).

---

## Aviso de dado
- `leads-litoral-enriquecido.csv` NÃO está no path que `automacao_diaria.py` lê (script aponta para arquivo fora do repo). O relatório "587 follow-ups" veio de base externa. A base REAL versionada está em `docs/materiais/leads-litoral-enriquecido.csv` (600 leads). **Recomenda-se ajustar o caminho do script para o arquivo versionado** ou versionar o externo.
