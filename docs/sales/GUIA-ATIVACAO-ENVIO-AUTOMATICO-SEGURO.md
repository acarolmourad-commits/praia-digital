# Guia: Ativar envio automatico seguro
Praia Digital — Comercial e Parcerias

Objetivo: habilitar o envio de e-mails em massa atraves do Brevo/SMTP sem expor credenciais.

## Passo 1 — Configurar .env (local, nao commitado)
Criar/editar `.env` na raiz do repositorio com:

```ini
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=seu-usuario-brevo
SMTP_PASSWORD=sua-senha-brevo
SMTP_FROM_NAME=Praia Digital
SMTP_FROM_EMAIL=comercial@praia.digital
```

## Passo 2 — Validar credenciais
Rodar: `python scripts/automation/validar_smtp.py`
Esperado: `SMTP_OK`.

## Passo 3 — Sanitizar CSV de envio
Rodar: `python scripts/automation/validar_base_leads.py docs/sales/csv-lotes-email/lote-brevo-50-realistas-2026-07-12.csv`
Esperado: `OK`.

## Passo 4 — Fazer backup obrigatorio
Rodar: `python scripts/automation/backup_incremental_dados_comerciais.py`
Confirmar saida `total_atualizados >= 1` ou `total_ignorados coerente`.

## Passo 5 — Enviar lote
Rodar: `python scripts/automation/enviar_lote_smtp_validado.py`
Esperado: `Envio concluido: X/Y`.

## Checklist seguranca
- [ ] `.env` esta no `.gitignore`
- [ ] Nenhuma credencial foi commitada
- [ ] CSV de envio nao contem dados pessoais reais
- [ ] Teste enviado para proprio e-mail antes do lote

## Se algo falhar
- Verificar logs do script de envio
- Checar quota do Brevo
- Confirmar dominio/SPF/DKIM se necessario
