# Checklist: Backup Incremental Antes do Envio
Praia Digital — Comercial e Parcerias

Objetivo: evitar perda de dados comerciais e garantir rastreabilidade antes de qualquer envio em massa.

## Passo único recomendado
- [ ] Executar `docs/sales/executar-backup-incremental-comercial.bat` ou `python scripts/automation/backup_incremental_dados_comerciais.py`
- [ ] Confirmar que o resumo JSON mostra `total_atualizados >= 1` ou, se `total_atualizados = 0`, confirmar `total_ignorados` coerente
- [ ] Anotar a pasta do backup em `docs/sales/backups/backup-YYYY-MM-DD/`

## Apenas após backup OK
- [ ] Abrir `docs/sales/pacote-execucao-final-2026-07-12.html`
- [ ] Rodar validação: `python scripts/automation/validar_lote_prospeccao_diaria.py` quando aplicável
- [ ] Disparar envio: Brevo import CSV ou `docs/sales/csv-lotes-email/lote-smtp-50-oficial-2026-07-12.csv`
- [ ] Registrar no tracker: `docs/sales/tracking-envios-lote-50-2026-07-12.csv`

## Bloqueio
- Se backup falhar ou a pasta não existir, não enviar.
- Nunca commitar `.env`.
