@echo off
echo Executando Health Check...
cd C:\Users\Carolina\praia-digital
python scripts/automation/health_check_site.py > docs/sales/health-check-latest.txt 2>&1
echo.
type docs/sales/health-check-latest.txt
echo.
pause
