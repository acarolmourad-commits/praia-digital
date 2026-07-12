
import csv, datetime, json
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CHECKLIST = BASE / 'docs' / 'sales' / 'checklist-verificacao-funil-comercial-praia-digital.md'
TRACKER = BASE / 'docs' / 'sales' / 'followup-registro.md'
CAPTURADOS = BASE / 'docs' / 'sales' / 'parcerias-leads-capturados.csv'
BACKUP_MANIFEST = BASE / 'docs' / 'sales' / 'backups' / 'manifest_backups.json'
ENRICHED = BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-enriquecido-2026-07-12.csv'
ONBOARDING_DIR = BASE / 'docs' / 'sales' / 'onboarding-parceiros'

hoje = datetime.datetime.now().strftime('%Y-%m-%d')
agora = datetime.datetime.now().isoformat()

# 1. Leads capturados hoje
leads_count = 0
if CAPTURADOS.exists():
    leads_count = CAPTURADOS.read_text(encoding='utf-8').count(hoje)

# 2. Follow-ups pendentes
followups_count = 0
if TRACKER.exists():
    txt = TRACKER.read_text(encoding='utf-8')
    followups_count = txt.count(hoje) + txt.lower().count('pendente_envio')

# 3. Backup
backup_ok = False
backup_path = ''
if BACKUP_MANIFEST.exists():
    try:
        manifest = json.loads(BACKUP_MANIFEST.read_text(encoding='utf-8'))
        for rel, info in manifest.items():
            if info.get('ultimo_backup') == hoje:
                backup_ok = True
                backup_path = str(BASE / info.get('backup_path', f'docs/sales/backups/backup-{hoje}'))
                break
    except Exception:
        pass

# 4. Enriquecimento
enriched_ok = ENRICHED.exists()

# 5. Onboarding
onboarding_count = len([p for p in ONBOARDING_DIR.glob('parceiro-*') if p.is_dir()]) if ONBOARDING_DIR.exists() else 0


# Sugestões automáticas corretivas
sugestoes = []
if leads_count == 0:
    sugestoes.append('- [ ] Nenhum lead novo capturado hoje. Verificar formulário do site e compartilhar landing `parcerias-litoral-paulista.html`.')
else:
    sugestoes.append(f'- [ ] {leads_count} lead(s) capturado(s) hoje. Processar com `python scripts/automation/processar_novos_leads_site.py`')

if followups_count == 0:
    sugestoes.append('- [ ] Nenhum follow-up pendente hoje. Verificar tracker para garantir que há ações agendadas.')
else:
    sugestoes.append(f'- [ ] {followups_count} follow-up(s) pendente(s) para hoje. Usar templates em `docs/sales/mensagens-abertura-parceria-praia-digital.html`.')

if not backup_ok:
    sugestoes.append('- [ ] Backup não executado hoje. Rodar `python scripts/automation/backup_incremental_dados_comerciais.py` antes de qualquer envio.')
else:
    sugestoes.append(f'- [ ] Backup OK. Pasta: `{backup_path}`.')

if not enriched_ok:
    sugestoes.append('- [ ] Leads não enriquecidos. Rodar `python scripts/automation/enriquecer_leads_parceiros.py`.')
else:
    sugestoes.append('- [ ] Leads enriquecidos: SIM.')

if onboarding_count == 0:
    sugestoes.append('- [ ] Sem onboarding gerado. Rodar `docs/sales/regenerar-onboarding.bat`.')
else:
    sugestoes.append(f'- [ ] Onboarding gerado: {onboarding_count} parceiro(s). Pasta: `docs/sales/onboarding-parceiros/`.')

sugestoes.append('- [ ] Após ações, atualizar `docs/sales/briefing-matinal-comercial-praia-digital.html` e abrir `central-comando-praia-digital.html`.')

# Gera checklist
linhas = []
linhas.append(f'# Verificação do Funil Comercial — {hoje}')
linhas.append('')
linhas.append('## Métricas')
linhas.append(f'- Leads capturados hoje: {leads_count}')
linhas.append(f'- Follow-ups pendentes: {followups_count}')
linhas.append(f"- Backup executado: {'SIM' if backup_ok else 'NÃO'}")
linhas.append(f'- Leads enriquecidos: {"SIM" if enriched_ok else "NÃO"}')
linhas.append(f'- Onboarding parceiros: {onboarding_count}')
linhas.append('')
linhas.append('## Ações corretivas sugeridas')
linhas.extend(sugestoes)
linhas.append('')
linhas.append(f'Gerado em: {agora}')

CHECKLIST.write_text('\n'.join(linhas), encoding='utf-8')
print('\n'.join(linhas))
