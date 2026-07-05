@echo off
chcp 65001 >nul
title Praia Digital - Executar Outreach Hoje
echo ==============================
echo   Executar Outreach - Hoje
echo ==============================
echo.
echo 1) Abrir batch de e-mails (top 20 leads)
echo 2) Abrir roteiro de envio hoje (top 5)
echo 3) Abrir follow-up 72h
echo 4) Abrir registro de respostas
echo 5) Abrir site Praia Digital
echo.
set /p opcao="Escolha uma opcao (1-5): "

if "%opcao%"=="1" start "" "outreach/enviar-emails-batch.html"
if "%opcao%"=="2" start "" "docs/sales/roteiro-envio-top5-hoje.md"
if "%opcao%"=="3" start "" "docs/sales/followup-top5-72h.md"
if "%opcao%"=="4" start "" "docs/sales/registro-respostas.md"
if "%opcao%"=="5" start "" "https://acarolmourad-commits.github.io/praia-digital/"

echo.
echo Concluido.
pause
