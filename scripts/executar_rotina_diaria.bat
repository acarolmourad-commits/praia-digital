@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital

echo === Rotina Diaria Automatica — Praia Digital ===
echo.

echo [1/5] Validando lote de prospecção...
python scripts/automation/validar_lote_prospeccao_diaria.py
if %errorlevel% neq 0 (
    echo [AVISO] Validação apresentou avisos. Verifique o relatório.
)

echo.
echo [2/5] Gerando onboardings de parceiros...
python scripts/automation/gerar_onboarding_parceiro.py
if %errorlevel% neq 0 (
    echo [AVISO] Onboarding gerado com ressalvas.
)

echo.
echo [3/5] Gerando relatório diário de outbound...
python scripts/automation/gerar_relatorio_diario_outbound.py
if %errorlevel% neq 0 (
    echo [AVISO] Relatório diário não foi gerado.
)

echo.
echo [4/5] Rodando roteiro diário de outreach WhatsApp...
python scripts/automation/roteiro_diario_outreach_auto.py
if %errorlevel% neq 0 (
    echo [AVISO] Roteiro diário de outreach não foi gerado.
)

echo.
echo [5/5] Bloqueando reenvio para leads já contactados...
python scripts/automation/bloquear_reenvio_whatsapp.py
if %errorlevel% neq 0 (
    echo [AVISO] Bloqueio de reenvio não foi gerado.
)

echo.
echo Rotina diária concluída.
pause
