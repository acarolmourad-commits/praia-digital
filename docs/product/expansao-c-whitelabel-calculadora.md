# Expansão C — White-label da Calculadora de Yield por CEP (Produto B2B)

**Status:** ativo técnico 100% construído e testado (`scripts/app_yield_cep.py` + `/estimate` + `/lead/capture`; `assets/calculadora-yield-cep.html`). Falta o **embalamento comercial**: transformar esse ativo de dev em produto recorrente embedado no site das 101 imobiliárias parceiras.

## Por que white-label (e não só nossa)

A calculadora é um **magnet de leads proprietário**: o dono entra, simula o yield, e vira lead. Hoje esse lead fica só na Praia Digital. Se embedarmos a calculadora **no site da imobiliária parceira** (com a marca dela), ela capta o proprietário no próprio canal — e divide a gestão conosco. Ganha-ganha:
- Imobiliária: captação de proprietários sem anúncio pago (a dor #1 das 101: `leads 98, anuncios 82`).
- Praia Digital: inventário de gestão sem custo de aquisição + revenue share.

## Modelo de negócio (sugestão)

| Item | Proposta |
|------|----------|
| Produto | Calculadora de Yield por CEP embedada (iframe) no site da parceira, com logo da parceira |
| Setup | Gratuito p/ as 101 já parceiras (ativo de retenção) |
| Lead | 100% da imobiliária (dono do canal) |
| Conversão em gestão | Revenue share 70% imobiliária / 30% Praia Digital sobre a comissão de gestão do contrato fechado via calculadora |
| SLA | Suporte + atualização de dados (histórico interno) trimestral |
| Exclusividade | 1 parceira por micro-região (âncora) |

## Proposta de parceria (texto para envio — 101 parceiras)

> Olá [Contato], tudo bem? Sou da Praia Digital. Como sua imobiliária já é nossa parceira em [Cidade], temos um ativo pronto pra te ajudar a captar mais proprietários sem gastar com anúncio pago: uma **Calculadora de Yield por CEP** que embedamos no seu site (com a sua marca). O dono simula quanto o imóvel rende em temporada e vira seu lead — e quando fechamos a gestão, dividimos a comissão (70% pra você / 30% Praia Digital). Setup grátis pra parceiro. Quer ver um protótipo funcionando?

## Algoritmo de priorização de rollout (Partner Score já definido na Expansão A)

```
Rollout_ordenado = parceiras_fechadas ordenadas por (ja_parceira=1) + pontuacao_lead desc
Prioridade top: Santos(24), Guarujá(14), Peruíbe(13), Itanhaém(12) -> lançar primeiro
```

## Entregáveis técnicos para o dev (já 90% pronto)

1. Parametrizar a calculadora por `tenant` (logo + cor da parceira) — variável de ambiente/query param.
2. Rota `/api/v1/lead/capture` já grava `origem=calc-cep`; adicionar `parceiro_id` para atribuir o lead.
3. Dashboard de leads por parceiro (reuso de `gerar_dashboard_outbound.py`).
4. Termo de parceria (PDF) — anexo comercial.

## Próximos passos
- [ ] Aprovar modelo de revenue share com Carolina
- [ ] Parametrizar tenant na calculadora (feature branch)
- [ ] Disparar proposta paras 101 parceiras (reuso do `gerar_lote_b2b.py` filtrando `status=parceria_fechada`)
- [ ] Fechar 1 âncora (Santos) como case white-label
