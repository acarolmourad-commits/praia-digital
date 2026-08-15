# Resposta → Estágio — regras permanentes
Data: 2026-08-15

## Fluxo de resposta
| Resposta | Ação | Estágio | Próxima ação | Responsável |
|----------|------|---------|--------------|-------------|
| ✅ Positiva | Parar follow-up + HANDOFF | HANDOFF_HUMANO | Humano deve entrar em contato | Humano |
| 💰 Perguntou preço | Responder com preço aprovado + continuar follow-up | RESPONDENDO_PRECO | Aguardar decisão | Humano |
| 📅 Pediu agendamento | Parar follow-up + HANDOFF | AGENDAMENTO_HUMANO | Confirmar disponibilidade | Humano |
| ❌ Não tenho interesse | Encerrar follow-up | ENCERRADO | Nenhuma ação | - |
| 🛑 Não quero receber mensagens | Bloquear futuros contatos | BLOQUEADO | Nenhuma ação | - |
| ⏳ Sem resposta | Continuar sequência D2/D5/D10 | SEGUINDO_SEQUENCIA | Executar próximo follow-up | Automático |

## Formato para resposta positiva
Quando chegar uma resposta positiva, registrar:
- SERVIÇO → VALOR POTENCIAL → ESTÁGIO → PRÓXIMA AÇÃO → RESPONSÁVEL

## Objeções recorrentes
Registrar aqui quando aparecerem:
- Nenhuma até o momento
