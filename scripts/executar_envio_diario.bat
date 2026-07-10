@echo off
chcp 65001 >nul
echo ==========================================
echo Praia Digital — Executar envio diario
echo ==========================================
echo.

REM Caminho do repositorio
set REPO=C:\Users\Carolina\praia-digital

REM Executa script de preparacao do lote
echo [1/3] Preparando lote diario...
python "%REPO%\scripts\preparar_envio_diario.py"
if %ERRORLEVEL% neq 0 (
    echo ERRO ao preparar lote diario.
    pause
    exit /b 1
)

set CSV=%REPO%\csv-lotes-email\lote-diario-%date:~0,4%-%date:~5,2%-%date:~8,2%.csv

REM Abre o CSV
echo.
echo [2/3] Abrindo CSV...
start "" "%CSV%"

REM Abre pagina de envio Brevo
echo.
echo [3/3] Abrindo pagina de envio Brevo...
start "" "https://www.brevo.com/pt-BR/"

echo.
echo ==========================================
echo Lote diario pronto.
echo - CSV aberto para importacao
echo - Brevo aberto para envio
echo - Apos envio, atualize o tracker:
echo   docs\sales\tracker-envios-unificado-2026-07-10.md
echo ==========================================
pause
