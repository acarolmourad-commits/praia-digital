@echo off
setlocal
set "REPO=https://github.com/acarolmourad-commits/praia-digital.git"
set "BRANCH=main"
set "VALIDATE_URL=https://academy.praia.digital"

echo ============================================
echo   Praia Digital Academy - Deploy no Render
echo ============================================
echo.
echo PASSO 1: Abra o Render
echo   https://dashboard.render.com/
echo.
echo PASSO 2: Crie um Web Service
echo   - Repositorio: acarolmourad-commits/praia-digital
echo   - Branch: main
echo   - Regiao: Virginia (EUA) ou SP (Brasil)
echo   - Runtime: Docker ou Python
echo.
echo PASSO 3: Configure variaveis de ambiente
echo   - DATABASE_URL: postgresql://academy:senha@host:5432/academy
echo   - SECRET_KEY: gere uma chave forte
echo   - SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
echo   - ALLOWED_ORIGINS: https://praia.digital,https://www.praia.digital,https://academy.praia.digital
echo   - MERCADOPAGO_TOKEN: access token do Mercado Pago
echo   - MERCADOPAGO_PUBLIC_KEY: public key do Mercado Pago
echo   - BASE_URL: https://academy.praia.digital
echo   - WHATSAPP_API_URL: https://graph.facebook.com/v19.0
echo   - WHATSAPP_TOKEN: token da API WhatsApp
echo   - WHATSAPP_PHONE_ID: phone ID
echo   - WHATSAPP_TO_NUMBER: numero destino
echo.
echo PASSO 4: Apos deploy, valide
echo   python scripts/check_academy_deploy.py --url %VALIDATE_URL% --wait 30
echo   python scripts/frontend_health_check.py --base https://praia.digital --wait 30
echo.
echo PASSO 5: Configure DNS
echo   - academy.praia.digital ^> Web Service URL
echo.
echo ============================================
echo.
pause
