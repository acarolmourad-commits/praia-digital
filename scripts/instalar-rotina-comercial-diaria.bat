@echo off
REM Instalador da Rotina Comercial Diaria - Praia Digital
REM Cria uma tarefa no Agendador do Windows para executar diariamente as 09:00

setlocal enabledelayedexpansion

echo ==========================================
echo  Instalacao da Rotina Comercial Diaria
echo ==========================================
echo.
echo Verificando permissoes...

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo AVISO: Execute este script como Administrador para criar a tarefa agendada.
    echo Clique com o botao direito no arquivo e selecione "Executar como administrador".
    echo.
    pause
    exit /b 1
)

set REPO=C:\Users\Carolina\praia-digital
set TASK_NAME=PraiaDigital_RotinaDiaria
set PYTHON=C:\Users\Carolina\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPT=%REPO%\scripts\automation\orquestrador_rotina_comercial.py

echo.
echo Repositorio: %REPO%
echo Script: %SCRIPT%
echo Horario: Todos os dias as 09:00
echo.

REM Verificar se o Python existe
if not exist "%PYTHON%" (
    echo Procurando python no PATH...
    where python >nul 2>&1
    if %errorLevel% equ 0 (
        set PYTHON=python
        echo Python encontrado no PATH
    ) else (
        echo.
        echo ERRO: Python nao encontrado. Instale Python 3.8+ em python.org
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Criando tarefa agendada...
echo.

REM Remover tarefa existente se houver
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if %errorLevel% equ 0 (
    echo Removendo tarefa anterior...
    schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
)

REM Criar nova tarefa
echo Criando tarefa agenda: %TASK_NAME%
schtasks /create ^
  /tn "%TASK_NAME%" ^
  /tr "cmd /c cd /d %REPO% && %PYTHON% %SCRIPT%" ^
  /sc daily ^
  /st 09:00 ^
  /ru "%USERNAME%" ^
  /f >nul

if %errorLevel% equ 0 (
    echo.
    echo ==========================================
    echo   SUCESSO: Rotina instalada com sucesso!
    echo ==========================================
    echo.
    echo A rotina executara automaticamente todos os dias as 09:00.
    echo.
    echo Para executar agora, use:
    echo   scripts\rotina-mestre-praia-digital.bat
    echo.
    echo Para ver a tarefa:
    echo   schtasks /query /tn %TASK_NAME%
    echo.
    echo Para remover:
    echo   schtasks /delete /tn %TASK_NAME% /f
    echo.
) else (
    echo.
    echo ERRO: Nao foi possivel criar a tarefa agendada.
    echo.
    echo Tente executar este script como Administrador.
    echo.
    echo Ou use o metodo manual:
    echo   1. Abra o Agendador de Tarefas do Windows
    echo   2. Criar Tarefa Basica
    echo   3. Executar: cd /d %REPO% ^&^& %PYTHON% %SCRIPT%
    echo   4. Agendar: diariamente, 09:00
    echo.
)

pause
