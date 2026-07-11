@echo off
REM verificar-precondicoes-automacao.bat
REM Confere se o ambiente esta pronto para as tarefas comerciais automaticas.
REM Nao altera nada; so reporta.

echo ==== Praia Digital - Verificacao de pre-condicoes ====

set REPO=C:\Users\Carolina\praia-digital
set PYTHON_REQUIRED=3.11

echo.
echo [1/5] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
  echo [ERRO] Python nao encontrado.
  pause
  exit /b 1
)
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version_info.major)"') do set MAJOR=%%i
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version_info.minor)"') do set MINOR=%%i
echo Python detectado: %MAJOR%.%MINOR%
if %MAJOR% LSS 3 (
  echo [ERRO] Python 3.11+ necessario.
  pause
  exit /b 1
)

echo.
echo [2/5] Verificando repo %REPO%...
if not exist "%REPO%" (
  echo [ERRO] Repo nao encontrado.
  pause
  exit /b 1
)

echo.
echo [3/5] Verificando arquivos comerciais...
set FILES=%REPO%\docs\sales\leads-litoral-enriquecido-realista.csv %REPO%\docs\sales\tracking-envios-lote-50-2026-07-12.csv %REPO%\scripts\automation\classificar_respostas_leads.py
for %%f in (%FILES%) do (
  if exist "%%f" (
    echo [OK] %%~nxf
  ) else (
    echo [FALTA] %%~nxf
  )
)

echo.
echo [4/5] Verificando tracker de follow-up...
if exist "%REPO%\docs\sales\followup-registro.md" (
  echo [OK] followup-registro.md
) else (
  echo [FALTA] followup-registro.md
)

echo.
echo [5/5] Verificando saidas geradas...
if exist "%REPO%\outreach\emails-personalizados" (
  echo [OK] emails-personalizados
) else (
  echo [FALTA] emails-personalizados
)
if exist "%REPO%\outreach\emails-followup-classificados" (
  echo [OK] emails-followup-classificados
) else (
  echo [FALTA] emails-followup-classificados
)

echo.
echo Verificacao concluida.
pause
