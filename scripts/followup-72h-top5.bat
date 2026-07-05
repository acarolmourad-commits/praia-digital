@echo off
chcp 65001 >nul
title Praia Digital - Follow-up 72h Top 5
echo ==============================
echo   Follow-up 72h — Top 5 leads
echo ==============================
echo.
echo 1) Abrir roteiro de envio hoje
echo 2) Abrir follow-up 72h
echo 3) Abrir registro de respostas
echo 4) Abrir site Praia Digital
echo.
set /p opcao="Escolha uma opcao (1-4): "

if "%opcao%"=="1" start "" "docs/sales/roteiro-envio-top5-hoje.md"
if "%opcao%"=="2" start "" "docs/sales/follow-up-1-3dias.md"
if "%opcao%"=="3" start "" "docs/sales/followup-registro.md"
if "%opcao%"=="4" start "" "https://acarolmourad-commits.github.io/praia-digital/"

echo.
echo Concluido.
pause
