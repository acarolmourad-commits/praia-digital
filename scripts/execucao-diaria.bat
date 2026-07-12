@echo off
echo ==========================================
echo Praia Digital - Execucao Diaria
echo ==========================================
echo.

cd /d C:\Users\Carolina\praia-digital

echo [1/5] Backup incremental...
if exist scripts\automation\backup_incremental_comercial.py (
    python scripts\automation\backup_incremental_comercial.py
) else (
    echo backup_incremental_comercial.py nao encontrado, pulando.
)
echo.

echo [2/5] Gerando follow-ups...
python scripts\automation\gerar_lotes_e_followups.py
echo.

echo [3/5] Simulando envio de e-mails...
python scripts\automation\simular_envio_lote.py --lote 35 --dry-run
echo.

echo [4/5] Atualizando tracker...
if not exist docs\sales\tracker_envios.csv (
    echo nome,email,cidade,imovel_url,fonte,data_captura,status,ultimo_contato,proxima_acao,observacoes > docs\sales\tracker_envios.csv
)
echo.

echo [5/5] Abrindo execucao diaria...
start docs/sales/execucao-diaria-praia-digital-2026.html
echo.

echo Checklist rapido:
echo - [ ] Enviar 1 proposta real do lote 35 ou 36
echo - [ ] Registrar envio manual no tracker
echo - [ ] Responder follow-up pendente
echo - [ ] Publicar 1 artigo/conteudo SEO
echo.
pause
