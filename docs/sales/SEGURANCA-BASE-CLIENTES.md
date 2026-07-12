# Guia: impedir commit acidental de dados comerciais reais
Praia Digital — Segurança e Privacidade

## Regra principal
- Nunca commitar e-mails, WhatsApps, nomes ou dados pessoais de imobiliárias parceiras.
- Seguir sempre o guia de troca da base real: `docs/sales/GUIA-TROCA-BASE-LEADS-REAIS.md`

## Comando útil
Depois de colocar a base real localmente, execute:
```powershell
cd C:\Users\Carolina\praia-digital
git update-index --skip-worktree docs/sales/leads-litoral-enriquecido.csv
git update-index --skip-worktree docs/sales/parcerias-leads-capturados.csv
git update-index --skip-worktree docs/sales/csv-lotes-email/lote-brevo-50-realistas-2026-07-12.csv
```
Isso permite manter dados locais sem sobrescrevê-los com futuros pulls.

## Checklist rápido
- [ ] Não compartilhar prints da base real
- [ ] Manter `.env` e `.gitignore` atualizados
- [ ] Usar formulário seguro para novos leads: `assets/ferramentas/captura-manual-leads-imobiliarias-2026.html`
