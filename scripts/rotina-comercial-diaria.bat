@echo off
title Praia Digital - Rotina Comercial Diaria
echo.
echo ==============================
echo   ROTINA COMERCIAL DIARIA
echo ==============================
echo.
echo [1/3] Backup incremental...
python scripts/automation/backup_incremental_dados_comerciais.py > nul 2>&1
echo.
echo [2/3] Processar novos leads do site...
python scripts/automation/processar_novos_leads_site.py
echo.
echo [3/3] Gerar briefing matinal...
python scripts/automation/gerar_briefing_dinamico.py
echo.
echo ==============================
echo   ROTINA CONCLUIDA
echo ==============================
echo.
echo Proximo: abrir docs/sales/briefing-matinal-comercial-praia-digital.html
echo.
pause
