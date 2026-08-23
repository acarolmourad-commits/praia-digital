# Workflows de Automação — Hermes Agents

> Biblioteca de workflows prontos para implementar.

## 1. Qualificação de leads
- Trigger: lead entra no WhatsApp
- Ação: agente coleta nome, e-mail, necessidade
- Condição: score > 70 → cria deal no CRM
- Ação: envia e-mail de boas-vindas

## 2. Suporte pós-venda
- Trigger: cliente envia mensagem
- Ação: agente busca status do pedido
- Condição: problema identificado → cria ticket
- Ação: notifica equipe humana

## 3. Reativação de leads
- Trigger: lead inativo há 30 dias
- Ação: agente envia oferta personalizada
- Condição: resposta positiva → agenda call
- Ação: notifica vendedor

## 4. Pesquisa NPS
- Trigger: 7 dias após compra
- Ação: agente envia pesquisa
- Condição: nota < 6 → follow-up humano
- Ação: registra no CRM
