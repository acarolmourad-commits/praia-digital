@echo off
title Praia Digital - Rotina Comercial Diaria
echo.
echo ==============================
echo   ROTINA COMERCIAL DIARIA
echo ==============================
echo.
echo [1/8] Backup incremental...
python scripts/automation/backup_incremental_dados_comerciais.py > nul 2>&1
echo.
echo [2/8] Processar novos leads do site...
python scripts/automation/processar_novos_leads_site.py
echo.
echo [3/8] Gerar briefing matinal...
python scripts/automation/gerar_briefing_dinamico.py
echo.
echo [4/8] Gerar central de comando dinamica...
python scripts/automation/gerar_central_dinamica.py
echo.
echo [5/8] Verificar funil comercial...
python scripts/automation/verificador_funil_comercial.py
echo.
echo [6/8] Gerar pagina de status do funil...
python scripts/automation/gerar_status_funil.py
echo.
echo [7/8] Atualizar sitemap SEO...
python scripts/automation/gerar_sitemap_seo.py
echo.
echo [8/8] Gerar checklist do dia...
python scripts/automation/verificador_funil_comercial.py
echo.
echo ==============================
echo   ROTINA CONCLUIDA
echo ==============================
echo.
echo Proximo: abrir central-comando-praia-digital.html
echo.
pause
