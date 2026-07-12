@echo off
title Praia Digital - Rotina Comercial Diaria
echo.
echo ==============================
echo   ROTINA COMERCIAL DIARIA
echo ==============================
echo.
echo [1/4] Backup incremental...
python scripts/automation/backup_incremental_dados_comerciais.py > nul 2>&1
echo.
echo [2/4] Processar novos leads do site...
python scripts/automation/processar_novos_leads_site.py
echo.
echo [3/4] Gerar briefing matinal...
python scripts/automation/gerar_briefing_dinamico.py
echo.
echo [4/4] Gerar central de comando dinamica...
python scripts/automation/gerar_central_dinamica.py
echo.
echo ==============================
echo   ROTINA CONCLUIDA
echo ==============================
echo.
echo Proximo: abrir central-comando-praia-digital.html
echo.
