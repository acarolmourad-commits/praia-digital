# Matriz de resposta comercial — Motor A + Motor B
Data: 2026-08-15
Tipo: regra de classificação
Objetivo: evitar tratamento igual para leads diferentes

## Matriz

| RESPOSTA | INTENÇÃO | OBJEÇÃO | PRÓXIMA AÇÃO | RESULTADO |
|----------|----------|---------|--------------|-----------|
| Tenho interesse | ALTA | nenhuma | enviar detalhes | aguardando |
| Pediu preço | ALTA | preço | responder com preço aprovado | aguardando resposta |
| Pediu prazo | ALTA | prazo | alinhar disponibilidade | aguardando resposta |
| Pediu informações | MÉDIA | dúvida | responder com dados específicos | aguardando resposta |
| Não respondeu | BAIXA | silêncio | seguir D2/D5/D10 | aguardando |
| Recusou | NENHUMA | recusa | encerrar follow-up | encerrado |
| Pediu para parar | NENHUMA | bloqueio | bloquear lead | bloqueado |
| Demonstrou interesse com condição | MÉDIA/ALTA | condição | alinhar condição com oferta | aguardando |
| Objeção: já tenho gestor | BAIXA | concorrência | nutrir / reativar após 30 dias | aguardando |
| Objeção: eu mesmo faço | BAIXA | autonomia | educar / diagnóstico | aguardando |
| Objeção: não quero gastar | BAIXA | orçamento | educar / ROI | aguardando |
| Objeção: já tenho boas fotos | BAIXA | percepção | educar / comparação | aguardando |
| Objeção: meu anúncio já funciona | BAIXA | conformismo | diagnóstico | aguardando |
| Objeção: não preciso mexer agora | BAIXA | timing | nutrir / reativar | aguardando |
| Objeção: só quero aumentar reservas | MÉDIA | resultado | alinhar expectativa | aguardando |
| Objeção: não quero alterar preço | MÉDIA | preço | explicar estratégia | aguardando |
| Objeção: vou pensar | BAIXA | indecisão | follow-up D5/D10 | aguardando |
| Objeção: vou esperar a temporada | BAIXA | timing | nutrir / reativar antes da temporada | aguardando |

## Regras

- Classificar individualmente
- Registrar data e canal de cada resposta
- Atualizar status no CRM após classificação
- Não enviar nova mensagem antes do próximo follow-up programado, exceto quando a resposta exigir ação humana
