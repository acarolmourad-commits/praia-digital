@echo off
setlocal
echo === Praia Digital Academy - Deploy Helper ===
echo.
echo 1. Abra o Render: https://dashboard.render.com/
echo 2. Crie um Web Service com:
echo    - Repositorio: acarolmourad-commits/praia-digital
echo    - Branch: main
echo    - Regiao: Virginia (EUA) ou SP (Brasil)
echo 3. Configure as variaveis de ambiente (veja docs/deploy-summary.md)
echo 4. Apos deploy, valide com:
echo    python scripts/check_academy_deploy.py --url https://academy.praia.digital --wait 30
echo.
pause
