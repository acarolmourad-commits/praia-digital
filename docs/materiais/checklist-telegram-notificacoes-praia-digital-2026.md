# Checklist — Telegram para notificações de follow-up e respostas — Praia Digital

## Objetivo
Receber alertas instantâneos no Telegram quando surgir resposta de lead ou quando um follow-up estiver programado.

## Configuração inicial
- [ ] Criar bot no Telegram via @BotFather
- [ ] Obter token do bot
- [ ] Criar grupo/canal privado para a operação
- [ ] Obter chat_id do grupo/canal
- [ ] Registrar credenciais em local seguro

## Tipos de notificação
- [ ] Resposta recebida de lead (email ou WhatsApp)
- [ ] Follow-up 72h disparado
- [ ] Follow-up 7d disparado
- [ ] Lead classificado como quente
- [ ] Reunião agendada
- [ ] Alerta de erro no envio

## Modelos de mensagem
- [ ] Resposta recebida: lead, canal e resumo
- [ ] Follow-up: lead, canal, template usado
- [ ] Lead quente: nome, cidade e próximo passo
- [ ] Reunião: data, horário e link

## Automação sugerida
- [ ] Script Python para enviar mensagens via API do Telegram
- [ ] Integração com tracker após atualização
- [ ] Teste de envio com mensagem de verificação

## Boas práticas
- [ ] Manter chat privado, não público
- [ ] Evitar dados sensíveis em mensagens
- [ ] Limitar alertas a eventos importantes
