@echo off
echo ==========================================
echo Praia Digital - Envio Manual do Dia
echo ==========================================
echo.

cd /d C:\Users\Carolina\praia-digital

echo [1/3] Abrindo hub de prospecção personalizada...
start outreach/hub-prospeccao-personalizada.html
echo.

echo [2/3] Abrindo dashboard de prospecção...
start docs/sales/dashboard-prospeccao-2026.html
echo.

echo [3/3] Abrindo tracker para registro...
start docs/sales/tracker_envios.csv
echo.

echo Ação recomendada:
echo - Abra a página do lead no hub
echo - Clique em "Responder" para abrir o e-mail
echo - Envie a proposta
echo - Marque no tracker como enviado
echo.
pause
