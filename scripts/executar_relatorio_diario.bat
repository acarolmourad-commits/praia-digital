@echo off
cd /d "%~dp0.."
python scripts/automation/gerar_relatorio_diario_outbound.py
pause
