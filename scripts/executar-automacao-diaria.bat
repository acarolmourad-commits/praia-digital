@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital
echo Executando automacao da Praia Digital...
echo Data: %date% %time%
python scripts/batch_imoveis.py
echo Imoveis atualizados.
echo.
echo Automacao concluida.
pause
