# Instalação da Rotina Automática Windows — Fallback Manual

Como o agendamento automático por `schtasks` falhou, use uma das opções abaixo para manter a rotina automática.

## Opção 1 — Agendador do Windows (manual)
1. Abra o Agendador de Tarefas.
2. Criar Tarefa Básica.
3. Nome: `PraiaDigital_AbrirSistemas`.
4. Gatilho: `Diariamente`, `09:00`.
5. Ação: `Iniciar um programa`.
6. Programa/script:
   ```
   C:\Users\Carolina\praia-digital\scripts\abrir-sistemas-diarios.bat
   ```
7. Concluir e aceitar.

## Opção 2 — Execução direta agora
Execute manualmente:
```
scripts\abrir-sistemas-diarios.bat
```

## Opção 3 — Launcher alternativo
```
scripts\rotina-mestre-praia-digital.bat
```

## Opção 4 — VBS (quando políticas bloquearem .bat)
Use o arquivo `scripts/rotina-mestre-praia-digital.vbs` existente.
