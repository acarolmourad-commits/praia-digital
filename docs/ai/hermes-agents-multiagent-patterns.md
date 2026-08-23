# Padrões Multi-Agente — Hermes Agents

> Arquiteturas para múltiplos agentes colaborando.

## Padrão 1: Supervisor + Workers
- 1 agente supervisor recebe tarefas complexas
- Delega para workers especializados
- Consolida resposta final

## Padrão 2: Pipeline Sequencial
- Agente 1: coleta dados
- Agente 2: processa/analisa
- Agente 3: gera resposta
- Cada um passa output para o próximo

## Padrão 3: Roteamento por Intenção
- Classificador de intenção
- Roteia para agente especializado
- Fallback para humano se nenhum match

## Padrão 4: Consenso Multi-Agente
- 3 agentes opinam independentemente
- Votação ou sintese de respostas
- Aumenta acurácia em decisões críticas
