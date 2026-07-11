@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital

echo === Deploy SEO Diario — Praia Digital ===
echo.

echo [1/3] Atualizando sitemap...
python scripts/automation/gerar_sitemap_auto.py
if %errorlevel% neq 0 (
    echo Erro ao gerar sitemap. Abortando.
    pause
    exit /b 1
)

echo.
echo [2/3] Gerando relatorio diario de outbound...
python scripts/automation/gerar_relatorio_diario_outbound.py

echo.
echo [3/3] Abrindo paineis...
start "" "docs/sales/painel-diario-unificado-praia-digital-2026.html"
start "" "docs/materiais/painel-indexacao-seo-praia-digital-2026.html"
start "" "docs/sales/checklist-diaria-execucao-praia-digital-2026.html"

echo.
echo Deploy SEO diario concluido.
pause
