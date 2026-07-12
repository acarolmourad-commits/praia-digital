# Guia: trocar base de leads de exemplo para dados reais
Praia Digital — Comercial e Parcerias

Objetivo: substituir `docs/sales/leads-litoral-enriquecido.csv` por uma base real **sem quebrar** as automações instaladas.

## Regras
- Mantenha exatamente as colunas do CSV atual.
- Nunca commitar dados sensíveis no repositório.
- Após importar, atualizar apenas o arquivo CSV local; scripts continuam funcionando.

## Colunas obrigatórias
NOME, EMAIL, WHATSAPP, CIDADE, EMPRESA, ASSUNTO, LINK_EMAIL_PERSONALIZADO, ORIGEM, INTERESSE, STATUS, PRIORIDADE, SCORE

## Passo a passo
1. Fazer backup do CSV atual: `python scripts/automation/backup_incremental_dados_comerciais.py`
2. Abrir `docs/sales/leads-litoral-enriquecido-template.csv`
3. Preencher com dados reais em editor seguro (Excel, Google Sheets, Notepad).
4. Salvar como `docs/sales/leads-litoral-enriquecido.csv` **sem alterar nome**.
5. Rodar validador: `python scripts/automation/validar_base_leads.py`
6. Conferir saida do validador: deve informar `OK` por coluna e total de registros.
7. Atualizar manualmente no tracker `docs/sales/followup-registro.md` apenas se quiser inscrever os novos leads em follow-ups D3/D7/D14.
8. Nao commitar dados pessoais se a base contiver informacoes reais. Use `.gitignore` se necessario para o arquivo e commitar apenas o template.

## Checklist
- [ ] Backup executado
- [ ] CSV real salvo com o mesmo nome
- [ ] Validador OK
- [ ] Estrutura de colunas preservada
- [ ] Scripts testados com o novo CSV
- [ ] Dados sensiveis protegidos/ignorados pelo git
