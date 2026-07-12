@echo off
title Praia Digital - Rotina Mestre
cd /d C:\Users\Carolina\praia-digital
python scripts/automation/orquestrador_rotina_comercial.py
echo.
echo Abrindo central de comando...
start "" "central-comando-praia-digital.html"
pause
