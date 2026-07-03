@echo off
setlocal
chcp 65001 >nul
title Praia Digital - Follow-up Windows
echo ==============================
echo   Follow-up Windows
echo ==============================
echo.
echo 1) Listar follow-ups
echo 2) Marcar follow-up como enviado
echo.
set /p op="Qual passo você quer agora? "
echo.

if "%op%"=="1" goto list
if "%op%"=="2" goto mark
goto help

:list
echo Follow-ups:
if exist "%~dp0..\docs\sales\followups.txt" (
  type "%~dp0..\docs\sales\followups.txt"
) else (
  echo Nenhum follow-up registrado.
)
goto done

:mark
echo Marcando follow-up como enviado...
echo "%date% %time% follow-up enviado" >> "%~dp0..\docs\sales\followups.txt"
echo ✅ Follow-up registrado.
goto done

:help
echo Quase! Escolha 1 ou 2, por favor.

:done
echo.
echo Feito! Se precisar, é só rodar de novo. 🚀
pause
