@echo off
chcp 65001 >nul
cd /d C:\Users\Carolina\praia-digital

echo === Central de Operacoes Diarias — Praia Digital ===
echo.

echo [1/4] Abrindo relatórios...
start "" "docs/sales/relatorio-diario-outbound-2026-07-11.html"
start "" "docs/sales/relatorio-semanal-executivo-praia-digital-2026-07-11.html"
start "" "docs/sales/checklist-diaria-execucao-praia-digital-2026.html"

echo [2/4] Abrindo prospeccao...
start "" "docs/sales/validacao-lote-2026-07-11.html"
start "" "docs/materiais/pagina-execucao-validador-lote-praia-digital-2026.html"
start "" "outreach/emails-diretos-top5-litoral-2026.html"

echo [3/4] Abrindo follow-up e negociacao...
start "" "docs/sales/followup-top5-personalizado-72h.md"
start "" "docs/sales/followup-top5-por-cidade.md"
start "" "outreach/template-negociacao-avancada-parcerias-litoral-2026.html"

echo [4/4] Abrindo onboarding e SEO...
start "" "docs/materiais/kit-onboarding-parceiros-praia-digital-2026.html"
start "" "docs/materiais/hub-conteudo-parceiros-praia-digital-2026.html"
start "" "docs/materiais/painel-indexacao-seo-praia-digital-2026.html"

echo.
echo Central aberta.
pause
