@echo off
setlocal
chcp 65001 >nul
title Praia Digital - Outreach Windows
echo ==============================
echo   Praia Digital - Outreach
echo ==============================
echo.
echo 1) Abrir página de negociação
echo 2) Abrir follow-up B2B
echo 3) Abrir batch de e-mails
echo 4) Mostrar leads no CSV
echo.
set /p op="Qual passo você quer agora? "
echo.

if "%op%"=="1" goto open_negotiation
if "%op%"=="2" goto open_followup
if "%op%"=="3" goto open_batch
if "%op%"=="4" goto show_leads
goto help

:open_negotiation
echo ✅ Abrindo negociação...
start "" "%~dp0..\outreach\email-negociacao-parceria-ceo.html"
goto done

:open_followup
echo ✅ Abrindo follow-up...
start "" "%~dp0..\outreach\email-followup-b2b.html"
goto done

:open_batch
echo ✅ Abrindo batch...
start "" "%~dp0..\outreach\enviar-emails-batch.html"
goto done

:show_leads
echo ✅ Mostrando leads...
type "%~dp0..\docs\sales\mail-merge.csv" | more
goto done

:help
echo Quase! Escolha 1, 2, 3 ou 4, por favor.

:done
echo.
echo Feito! Se precisar, é só rodar de novo. 🚀
pause
