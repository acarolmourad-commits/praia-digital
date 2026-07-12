# Guia: Instalar rotina comercial diária no Windows sem bloqueio
Praia Digital — Operações

## Requisito
- Acesso local a `C:\Users\Carolina\praia-digital`
- PowerShell com permissão para rodar scripts locais

## Opção 1 — Execução manual diária recomendada
- Abrir `scripts/rotina-comercial-diaria.bat` sempre ao iniciar o expediente
- Ele executa: backup incremental → processar leads do site → briefing dinâmico

## Opção 2 — Agendador do Windows
1. Abrir Agendador de Tarefas
2. Criar tarefa básica chamada `PraiaDigital-RotinaComercial-Diaria`
3. Acionador: diariamente às 08:00
4. Ação: iniciar programa `C:\Users\Carolina\praia-digital\scripts\rotina-comercial-diaria.bat`
5. Concluir e aceitar. Se o PowerShell bloquear, usar Opção 1.

## Verificação
- Abrir `docs/sales/briefing-matinal-comercial-praia-digital.html`
- Checar KPIs: leads capturados, follow-ups pendentes, priorizados
