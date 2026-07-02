@echo off
chcp 65001 >nul
echo Agendador de follow-ups B2B - Praia Digital
echo.
setlocal enabledelayedexpansion

:: CONFIG
set BATCH_SIZE=5
set DELAY_SECONDS=30
set MAILTO_BATCH=https://praia.digital/outreach/enviar-emails-batch.html

echo Abrindo página de envio em lote...
start "" "%MAILTO_BATCH%"

echo.
echo Instrucoes:
echo 1. A pagina de envio foi aberta no navegador.
echo 2. Clique em cada botao "Enviar e-mail" para abrir o cliente de e-mail.
echo 3. Envie os e-mails manualmente.
echo.
echo follow-ups preparados em: docs/sales/follow-up-1-3dias.md, follow-up-2-7dias.md, follow-up-3-fechamento.md
echo.
pause
