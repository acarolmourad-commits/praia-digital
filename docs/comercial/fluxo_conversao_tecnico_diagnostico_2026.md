# Fluxo de conversão técnico — Diagnóstico do Anúncio de Temporada 2026
Data: 2026-08-15
Tipo: especificação técnica
Camada: DIAGNÓSTICO → LEAD → OFERTA DE EDIÇÃO

---

## Estágios do funil

1. Visita ao diagnóstico
2. Início do diagnóstico
3. Item 1
4. Item 2
5. Item 3
6. Item 4
7. Item 5
8. Item 6
9. Item 7
10. Item 8
11. Item 9
12. Item 10
13. Item 11
14. Item 12
15. Item 13
16. Item 14
17. Item 15
18. Conclusão do diagnóstico
19. CTA clicado
20. Lead criado no CRM
21. D0 enviado
22. D2 enviado
23. D5 enviado
24. D10 enviado
25. Resposta recebida
26. Handoff humano
27. Edição solicitada
28. Venda concluída

## Regras de automação

- D0 enviado automaticamente quando lead é criado
- D2 enviado automaticamente 2 dias após D0 sem resposta
- D5 enviado automaticamente 3 dias após D2 sem resposta
- D10 enviado automaticamente 5 dias após D5 sem resposta
- Resposta positiva → HANDOFF automático
- Resposta negativa → ENCERRAR automático
- Pedido de preço → responder com preço automático
- Pedido de agendamento → HANDOFF automático

## Dependências manuais mínimas

- Acesso ao anúncio deve ser autorizado pelo proprietário
- Proposta personalizada deve ser revisada por humano antes do envio
- Edição deve ser executada por humano
- Venda deve ser confirmada por humano

Tudo o que for possível de ser automatizado antes da autorização humana deve ser automatizado.

## Campos obrigatórios do lead

- Nome
- Canal de contato
- Cidade/bairro do imóvel
- Tipo de imóvel
- Score do diagnóstico
- Classificação
- Caminho sugerido
- Fonte do tráfego
- Data de criação
- Status no funil
