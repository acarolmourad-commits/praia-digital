@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital

echo === Rotina Diaria Automatica — Praia Digital ===
echo.

echo [1/3] Validando lote de prospecção...
python scripts/automation/validar_lote_prospeccao_diaria.py
if %errorlevel% neq 0 (
    echo [AVISO] Validação apresentou avisos. Verifique o relatório.
)

echo.
echo [2/3] Gerando onboardings de parceiros...
python scripts/automation/gerar_onboarding_parceiro.py
if %errorlevel% neq 0 (
    echo [AVISO] Onboarding gerado com ressalvas.
)

echo.
echo [3/3] Gerando relatório diário de outbound...
python scripts/automation/gerar_relatorio_diario_outbound.py
if %errorlevel% neq 0 (
    echo [AVISO] Relatório diário não foi gerado.
)

echo.
echo Rotina diária concluída.
pause
