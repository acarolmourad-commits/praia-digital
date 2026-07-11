@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital
echo Gerando sitemap...
python scripts/automation/gerar_sitemap_auto.py
echo Concluido.
