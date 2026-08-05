@echo off
setlocal

set "MP_TOKEN=%MERCADOPAGO_TOKEN%"
set "MP_PUBLIC=%MERCADOPAGO_PUBLIC_KEY%"
set "BASE_URL=%BASE_URL%"

if "%MP_TOKEN%"=="" (
  echo [ERRO] MERCADOPAGO_TOKEN nao definido.
  pause
  exit /b 1
)

echo === Teste Mercado Pago - preferencia ===
curl -s -X POST https://api.mercadopago.com/v1/checkout/preferences ^
  -H "Authorization: Bearer %MP_TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"title\":\"Teste\",\"quantity\":1,\"unit_price\":10,\"currency_id\":\"BRL\"}],\"back_urls\":{\"success\":\"%BASE_URL%/education/checkout.html?status=approved\",\"failure\":\"%BASE_URL%/education/checkout.html?status=rejected\",\"pending\":\"%BASE_URL%/education/checkout.html?status=pending\"},\"auto_return\":\"approved\"}"

echo.
echo === Teste concluido ===
pause
