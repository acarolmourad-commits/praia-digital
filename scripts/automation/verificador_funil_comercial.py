
from pathlib import Path
from datetime import datetime

BASE = Path('C:/Users/Carolina/praia-digital')
CHECKLIST = BASE / 'docs' / 'sales' / 'checklist-verificacao-funil-comercial-praia-digital.md'
TRACKER = BASE / 'docs' / 'sales' / 'followup-registro.md'
CAPTURADOS = BASE / 'docs' / 'sales' / 'parcerias-leads-capturados.csv'
BACKUP_MANIFEST = BASE / 'docs' / 'sales' / 'backups' / 'manifest_backups.json'
BACKUP_DIR = BASE / 'docs' / 'sales' / 'backups'

hoje = datetime.now().strftime('%Y-%m-%d')

# 1. Leads capturados hoje
leads_hoje = 0
capturados_txt = ''
if CAPTURADOS.exists():
    capturados_txt = CAPTURADOS.read_text(encoding='utf-8')
    leads_hoje = capturados_txt.count(hoje)

# 2. Follow-ups pendentes hoje
followups_hoje = 0
if TRACKER.exists():
    txt = TRACKER.read_text(encoding='utf-8')
    followups_hoje = txt.count(hoje) + txt.lower().count('pendente_envio')

# 3. Backup do dia
backup_ok = False
if BACKUP_MANIFEST.exists():
    try:
        import json
        manifest = json.loads(BACKUP_MANIFEST.read_text(encoding='utf-8'))
        for rel, info in manifest.items():
            if info.get('ultimo_backup') == hoje:
                backup_ok = True
                break
    except Exception:
        pass

# 4. Pasta de backup do dia existe?
backup_pasta = BACKUP_DIR / f'backup-{hoje}'
backup_existe = backup_pasta.exists()

# 5. Gera checklist de verificação
linhas = []
linhas.append(f'# Verificação do Funil Comercial — {hoje}')
linhas.append('')
linhas.append(f'- Leads capturados hoje: {leads_hoje}')
linhas.append(f'- Follow-ups pendentes hoje: {followups_hoje}')
linhas.append(f'- Backup executado hoje: {"SIM" if backup_ok else "NÃO"}')
linhas.append(f'- Pasta de backup existe: {"SIM" if backup_existe else "NÃO"}')
linhas.append('')
if leads_hoje == 0:
    linhas.append('- [ ] Nenhum lead novo capturado hoje. Verificar formulário do site.')
else:
    linhas.append(f'- [ ] {leads_hoje} lead(s) capturado(s) hoje. Processar com `python scripts/automation/processar_novos_leads_site.py`')
if followups_hoje == 0:
    linhas.append('- [ ] Nenhum follow-up pendente para hoje. Verificar tracker.')
else:
    linhas.append(f'- [ ] {followups_hoje} follow-up(s) pendente(s) para hoje.')
if not backup_ok:
    linhas.append('- [ ] Backup não executado hoje. Rodar `python scripts/automation/backup_incremental_dados_comerciais.py`')
else:
    linhas.append('- [ ] Backup do dia OK.')
linhas.append('')
linhas.append('## Ações corretivas')
linhas.append('- Se leads capturados > 0: gerar follow-ups e atualizar briefing.')
linhas.append('- Se followups pendentes > 0: enviar e-mails/WhatsApp e registrar no tracker.')
linhas.append('- Se backup não OK: executar backup antes de qualquer envio.')
linhas.append('')
linhas.append(f'Gerado em: {datetime.now().isoformat()}')

CHECKLIST.write_text('\n'.join(linhas), encoding='utf-8')
print('\n'.join(linhas))
