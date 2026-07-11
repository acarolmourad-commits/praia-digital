@echo off
title Praia Digital - Outreach WhatsApp
echo.
echo ========================================
echo   Praia Digital - Outreach WhatsApp
echo ========================================
echo.
echo Abrindo ferramentas...
echo.

cd /d C:\Users\Carolina\praia-digital

start "" "docs\materiais\whatsapp-outreach-playground-praia-digital-2026.html"
start "" "outreach\whatsapp-rastrear-envios-2026-07-11.html"
start "" "docs\sales\dashboard-whatsapp-outreach-praia-digital-2026.html"
start "" "docs\sales\guia-execucao-primeiro-lote-whatsapp-2026-07-11.html"

echo Ferramentas abertas no navegador padrao.
echo.
echo Passo a passo:
echo 1) Abra o playground e filtre por cidade/status.
echo 2) Clique em Gerar lote personalizado.
echo 3) Clique em Abrir conversa e envie as mensagens.
echo 4) Marque Enviado no rastreador e clique em Salvar CSV.
echo 5) Gere o relatorio: python scripts\automation\gerar_relatorio_performance_whatsapp.py
echo.
pause
