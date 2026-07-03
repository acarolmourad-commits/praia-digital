@echo off
setlocal
chcp 65001 >nul
title Praia Digital - SEO Windows Helper
echo ==============================
echo   Praia Digital - SEO Windows
echo ==============================
echo.
echo Olá! Você clicou com carinho, então vamos fazer isso junto :)
echo.
echo 1) Abrir o index do site no navegador
echo 2) Abrir outreach/index.html
echo 3) Mostrar status git curto
echo.
set /p op="Qual passo você quer agora? "
echo.

if "%op%"=="1" goto open_index
if "%op%"=="2" goto open_outreach
if "%op%"=="3" goto git_status
goto help

:open_index
echo ✅ Abrindo o site principal...
start "" "%~dp0..\index.html"
goto done

:open_outreach
echo ✅ Abrindo outreach...
if exist "%~dp0outreach\index.html" ( start "" "%~dp0outreach\index.html" ) else ( echo ❌ outreach/index.html não encontrado. )
goto done

:git_status
echo ✅ Verificando git...
git status -sb || echo ❌ git não encontrado.
goto done

:help
echo Quase! Escolha 1, 2 ou 3, por favor.

:done
echo.
echo Feito! Se precisar, é só rodar de novo. 🚀
pause
