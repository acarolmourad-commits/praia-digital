@echo off
title Praia Digital - Regenerar onboarding
cd /d C:\Users\Carolina\praia-digital
python scripts/automation/gerar_onboarding_parceiro.py
python scripts/automation/gerar_status_funil.py
echo.
echo Concluido. Abra docs/sales/onboarding-parceiros/index.html para continuar.
pause
