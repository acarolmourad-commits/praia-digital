@echo off
REM instalador-tarefas-comerciais.bat
REM Cria tarefas agendadas no Windows para automação comercial da Praia Digital
REM Requer execucao como Administrador

echo Instalando tarefas comerciais automaticas...

echo ==== Verificando executavel python ====
python --version >nul 2>&1
if %errorlevel% neq 0 (
  echo Python nao encontrado. Instale o Python 3.11+ primeiro.
  pause
  exit /b 1
)

echo ==== Verificando repo praia-digital ====
cd C:\Users\Carolina\praia-digital
if not exist "scripts\automation\agendar_followup_tracker_auto.py" (
  echo Repo nao encontrado em C:\Users\Carolina\praia-digital
  pause
  exit /b 1
)

echo ==== Criando tarefa: envio diario de leads 09:00 ====
schtasks /create /tn "PraiaDigital-Envio-Diario-09h" /tr "python C:\Users\Carolina\praia-digital\scripts\automation\envio_diario_lote.py" /sc daily /st 09:00 /f >nul 2>&1

echo ==== Criando tarefa: follow-up tracker 09h30 ====
schtasks /create /tn "PraiaDigital-Followup-Tracker-09h30" /tr "python C:\Users\Carolina\praia-digital\scripts\automation\agendar_followup_tracker_auto.py" /sc daily /st 09:30 /f >nul 2>&1

echo ==== Criando tarefa: newsletter semanal segunda 10h ====
schtasks /create /tn "PraiaDigital-Newsletter-Segunda-10h" /tr "python C:\Users\Carolina\praia-digital\scripts\automation\enviar_newsletter_semanal.py" /sc weekly /d MON /st 10:00 /f >nul 2>&1

echo.
echo Tarefas instaladas.
echo Abra o Agendador de Tarefas para verificar.
echo Quando configurar o SMTP no .env, os envios comecam automaticamente.
pause
