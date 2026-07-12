@echo off
echo ==========================================
echo Praia Digital - Rotina Mestre Unificada
echo ==========================================
echo.

echo [1/5] Backup incremental...
cd /d C:\Users\Carolina\praia-digital
python scripts/automation/backup_incremental_comercial.py
echo.

echo [2/5] Gerando briefing dinamico...
python scripts/automation/gerar_briefing_dinamico.py
echo.

echo [3/5] Atualizando tracker...
if not exist docs\sales\tracker_envios.csv (
    echo nome,email,cidade,imovel_url,fonte,data_captura,status,ultimo_contato,proxima_acao,observacoes > docs\sales\tracker_envios.csv
)
echo.

echo [4/5] Abrindo arquivos...
start docs/sales/central-comando-praia-digital.html
start docs/sales/briefing-comercial-diario.md
start docs/sales/tracker_envios.csv
echo.

echo [5/5] Checklist do dia:
echo - [ ] Enviar 1 proposta do lote atual
echo - [ ] Registrar envio no tracker
echo - [ ] Responder follow-ups pendentes
echo - [ ] Publicar 1 artigo/conteudo SEO
echo.
echo Rotina concluida.
pause
