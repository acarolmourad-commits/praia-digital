@echo off
REM Script executado pelo Agendador do Windows
REM Abre os 3 sistemas operacionais da Praia Digital

echo ==========================================
echo  Praia Digital - Rotina Diaria Automatica
echo  %date% %time%
echo ==========================================
echo.

cd /d C:\Users\Carolina\praia-digital

echo [1/3] Abrindo Central de Comando...
start "" "central-comando-praia-digital.html"

echo [2/3] Abrindo Send Execution Tracker...
start "" "docs/sales/send-execution-tracker-2026.html"

echo [3/3] Abrindo CRM Visual...
start "" "docs/sales/crm-visual-2026.html"

echo.
echo ==========================================
echo  Sistemas abertos com sucesso!
echo ==========================================
echo.
echo Proximos passos:
echo   1. Verifique o backlog de vendas
echo   2. Envie os lotes de prospeccao
echo   3. Registre no tracker
echo   4. Verifique respostas
echo.
echo Arquivos uteis:
echo   - docs/sales/enviar-hoje-2026-07-12.html
echo   - outreach/envio-piloto-5-hoje/
echo   - outreach/lote-prospeccao-36-2026-07-12.html
echo.
timeout /t 10 >nul
