@echo off
setlocal
set "URL=https://academy.praia.digital"

echo === Sanity check pos-deploy ===
echo URL: %URL%
echo.

echo [1/4] Health check
powershell -Command "try { $r = Invoke-WebRequest -Uri '%URL%/health' -UseBasicParsing; Write-Host ('Status: ' + $r.StatusCode); Write-Host $r.Content } catch { Write-Host 'FALHOU'; Write-Host $_.Exception.Message }"

echo.
echo [2/4] Monitoring status
powershell -Command "try { $r = Invoke-WebRequest -Uri '%URL%/monitoring/status' -UseBasicParsing; Write-Host ('Status: ' + $r.StatusCode); Write-Host $r.Content } catch { Write-Host 'FALHOU'; Write-Host $_.Exception.Message }"

echo.
echo [3/4] Frontend health
python scripts/frontend_health_check.py --base https://praia.digital --wait 0

echo.
echo [4/4] Sitemap validation
powershell -Command "try { $r = Invoke-WebRequest -Uri 'https://praia.digital/sitemap.xml' -UseBasicParsing; Write-Host ('Status: ' + $r.StatusCode); Write-Host ('Tamanho: ' + $r.Content.Length + ' chars') } catch { Write-Host 'FALHOU'; Write-Host $_.Exception.Message }"

echo.
echo === Concluido ===
pause
