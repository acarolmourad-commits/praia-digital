@echo off
REM Launcher oficial da Central de Comando - Praia Digital
REM Abre todos os sistemas em um clique

echo ==========================================
echo  Praia Digital - Inicializando...
echo ==========================================
echo.

cd /d C:\Users\Carolina\praia-digital

echo [1/4] Abrindo Central de Comando...
start "" "central-comando-praia-digital.html"
timeout /t 2 >nul

echo [2/4] Abrindo Send Execution Tracker...
start "" "docs/sales/send-execution-tracker-2026.html"
timeout /t 2 >nul

echo [3/4] Abrindo CRM Visual...
start "" "docs/sales/crm-visual-2026.html"
timeout /t 2 >nul

echo [4/4] Abrindo Tracker de Envios...
start "" "docs/sales/tracker_envios.csv"

echo.
echo ==========================================
echo  Sistemas abertos!
echo ==========================================
echo.
echo Acoes rapidas:
echo   1. Enviar lote piloto: outreach\envio-piloto-5-hoje\
echo   2. Lote 36: outreach\lote-prospeccao-36-2026-07-12.html
echo   3. Follow-ups: outreach\followups-leads-reais\
echo   4. Gerar novos artigos: python scripts\automation\gerar_artigos_seo_cidades_2026.py
echo.
pause
