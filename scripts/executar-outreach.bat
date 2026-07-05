@echo off
chcp 65001 >nul
title Praia Digital - Execucao Outreach
echo ==============================
echo   Praia Digital - Execucao
echo ==============================
echo.
echo Hoje: enviar 5 e-mails iniciais
echo 72h: follow-up automatico
echo 7d: follow-up avancado
echo 12d: fechamento
echo.
echo 1) Abrir roteiro de envio hoje
echo 2) Abrir follow-up 72h
echo 3) Abrir deep dives dos top 5
echo 4) Abrir batch de e-mails
echo 5) Abrir registro de respostas
echo 6) Abrir site Praia Digital
echo.
set /p opcao="Escolha uma opcao (1-6): "

if "%opcao%"=="1" start "" "docs/sales/roteiro-envio-top5-hoje.md"
if "%opcao%"=="2" start "" "docs/sales/follow-up-1-3dias.md"
if "%opcao%"=="3" start "" "docs/sales/lead-deepdive"
if "%opcao%"=="4" start "" "outreach/enviar-emails-batch.html"
if "%opcao%"=="5" start "" "docs/sales/followup-registro.md"
if "%opcao%"=="6" start "" "https://acarolmourad-commits.github.io/praia-digital/"

echo.
echo Execucao concluida.
pause
