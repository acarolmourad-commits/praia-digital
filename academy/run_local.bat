@echo off
echo ===== Deploy Local - Praia Digital Academy =====
echo.
echo ATENCAO: configure academy/.env antes de continuar.
pause

echo.
echo Instalando dependencias...
cd academy
pip install -r requirements.txt

echo.
echo Iniciando servidor local em http://127.0.0.1:8000
uvicorn main:app --host 127.0.0.1 --port 8000
pause
