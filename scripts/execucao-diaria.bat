@echo off
echo ==========================================
echo Praia Digital - Execucao Diaria
echo ==========================================
echo.

echo [1/4] Backup incremental...
cd /d C:\Users\Carolina\praia-digital
python scripts/automation/gerar_lotes_e_followups.py
echo.

echo [2/4] Atualizando tracker...
if not exist docs\sales\tracker_envios.csv (
    echo nome,email,cidade,imovel_url,fonte,data_captura,status,ultimo_contato,proxima_acao,observacoes > docs\sales\tracker_envios.csv
)
echo.

echo [3/4] Abrindo execucao diaria...
start docs/sales/execucao-diaria-praia-digital-2026.html
echo.

echo [4/4] Links uteis:
echo - CRM Visual: docs/sales/crm-visual-2026.html
echo - Follow-ups JSON: docs/sales/followups_gerados.json
echo - Tracker CSV: docs/sales/tracker_envios.csv
echo.
echo Checklist rapido:
echo - [ ] Enviar 1 proposta do lote 35 ou 36
echo - [ ] Registrar envio no tracker
echo - [ ] Responder follow-up pendente
echo - [ ] Publicar 1 artigo/conteudo SEO
echo.
pause
