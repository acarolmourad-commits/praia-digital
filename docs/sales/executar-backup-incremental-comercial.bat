@echo off
title Backup Incremental Comercial - Praia Digital
cd /d C:\Users\Carolina\praia-digital
python scripts/automation/backup_incremental_dados_comerciais.py
echo.
echo Verificando backups...
dir "docs\sales\backups" /b
echo.
pause
