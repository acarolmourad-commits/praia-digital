# Eventos de abandono — Diagnóstico do Anúncio de Temporada 2026
Data: 2026-08-15
Tipo: instrumentação / analytics
Camada: DIAGNÓSTICO → LEAD

---

## Definição de abandono

Abandono = usuário que inicia uma etapa e não avança para a próxima dentro de um intervalo razoável.

Intervalos:
- Diagnóstico iniciado → conclusão: 30 minutos
- Conclusão → CTA clicado: 15 minutos
- CTA clicado → lead criado: 30 minutos

## Pontos de medição

1. Visita → início
2. Início → item 3
3. Item 3 → item 5
4. Item 5 → item 10
5. Item 10 → conclusão
6. Conclusão → CTA
7. CTA → lead
8. Lead → D0 enviado
9. D0 → D2
10. D2 → D5
11. D5 → D10
12. D10 → resposta

## Dados a registrar

- ID da sessão
- Timestamp de entrada
- Timestamp de saída
- Última etapa concluída
- Último item respondido
- Dispositivo
- Fonte de tráfego
- Score obtido
- Classificação
- Caminho sugerido
- CTA clicado (sim/não)
- Lead criado (sim/não)
- Tempo total no diagnóstico

## Ações de otimização

- Se taxa de abandono em visita → início for alta: simplificar chamada para iniciar
- Se taxa de abandono entre itens 3-5 for alta: reduzir complexidade dos itens iniciais
- Se taxa de abandono entre itens 5-10 for alta: agrupar itens menos relevantes
- Se taxa de abandono entre item 10 e conclusão for alta: encurtar segunda metade
- Se taxa de abandono entre conclusão e CTA for alta: revisar texto do CTA
- Se taxa de abandono entre CTA e lead for alta: reduzir friction na coleta de dados

## Regra

Não modificar o diagnóstico enquanto houver poucos dados.
Esperar pelo menos 20 conclusões antes de tomar decisões de alteração.
