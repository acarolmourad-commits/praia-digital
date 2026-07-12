
import json, datetime
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
OUT = BASE / 'docs' / 'sales' / 'status-funil-comercial-2026-07-12.html'
TRACKER = BASE / 'docs' / 'sales' / 'followup-registro.md'
CAPTURADOS = BASE / 'docs' / 'sales' / 'parcerias-leads-capturados.csv'
BACKUP_MANIFEST = BASE / 'docs' / 'sales' / 'backups' / 'manifest_backups.json'
BACKUP_DIR = BASE / 'docs' / 'sales' / 'backups'

hoje = datetime.datetime.now().strftime('%Y-%m-%d')
agora = datetime.datetime.now().isoformat()

# 1. leads capturados hoje
leads_count = 0
if CAPTURADOS.exists():
    with CAPTURADOS.open('r', encoding='utf-8') as f:
        sample = f.read()
        leads_count = sample.count(hoje)

# 2. follow-ups pendentes hoje
followups_count = 0
if TRACKER.exists():
    txt = TRACKER.read_text(encoding='utf-8')
    followups_count = txt.count(hoje) + txt.lower().count('pendente_envio')

# 3. backup status
backup_ok = False
backup_path = ''
if BACKUP_MANIFEST.exists():
    try:
        manifest = json.loads(BACKUP_MANIFEST.read_text(encoding='utf-8'))
        for rel, info in manifest.items():
            if info.get('ultimo_backup') == hoje:
                backup_ok = True
                backup_path = info.get('backup_path', f"backup-{hoje}")
                break
    except Exception:
        pass

# 4. enriched leads exists
enriched = (BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-enriquecido-2026-07-12.csv').exists()

# 5. onboarding packages
onboarding = len([p for p in (BASE / 'docs' / 'sales' / 'onboarding-parceiros').glob('parceiro-*') if p.is_dir()]) if (BASE / 'docs' / 'sales' / 'onboarding-parceiros').exists() else 0

# status class helper
def status_class(ok):
    return 'ok' if ok else 'danger'

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Status do Funil Comercial — Praia Digital</title>
<style>
  :root{{--bg:#f4f6f8;--card:#fff;--ink:#0f172a;--muted:#64748b;--accent:#0b4f6c;--ok:#14532d;--warn:#713f12;--danger:#7f1d1d;--radius:12px}}
  * {{ box-sizing: border-box }}
  body {{ font-family: Arial,Helvetica,sans-serif; background: var(--bg); color: var(--ink); margin: 0; padding: 22px }}
  .container {{ max-width: 980px; margin: 0 auto }}
  header {{ background: linear-gradient(135deg,#0b4f6c,#1570a1); color: #fff; padding: 22px; border-radius: var(--radius); margin-bottom: 18px }}
  header h1 {{ margin: 0 0 6px; font-size: 20px }}
  header p {{ margin: 0; opacity: .9 }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px }}
  .card {{ background: var(--card); padding: 16px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,.04) }}
  .card h2 {{ margin: 0 0 10px; color: #154c79; font-size: 15px }}
  .metric {{ font-size: 32px; font-weight: 700; color: var(--accent) }}
  .metric.ok {{ color: #14532d }}
  .metric.danger {{ color: #7f1d1d }}
  .badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700 }}
  .badge.ok {{ background: #dcfce7; color: var(--ok) }}
  .badge.danger {{ background: #fee2e2; color: var(--danger) }}
  .actions {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px }}
  .btn {{ display: inline-block; padding: 10px 14px; background: var(--accent); color: #fff; text-decoration: none; border-radius: 10px; font-size: 13px; font-weight: 700 }}
  .btn.secondary {{ background: #e2e8f0; color: #0f172a }}
  .footer {{ text-align: center; margin-top: 18px; color: var(--muted); font-size: 12px }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>Status do Funil Comercial</h1>
    <p>Atualizado em {agora}</p>
  </header>

  <div class="grid">
    <div class="card">
      <h2>Leads capturados hoje</h2>
      <div class="metric {status_class(leads_count > 0)}">{leads_count}</div>
      <div class="actions">
        <a class="btn secondary" href="docs/sales/parcerias-leads-capturados.csv">Base capturada</a>
      </div>
    </div>
    <div class="card">
      <h2>Follow-ups pendentes</h2>
      <div class="metric {status_class(followups_count == 0)}">{followups_count}</div>
      <div class="actions">
        <a class="btn secondary" href="outreach/followups-pendentes">Follow-ups</a>
      </div>
    </div>
    <div class="card">
      <h2>Backup do dia</h2>
      <div class="metric {status_class(backup_ok)}">{'OK' if backup_ok else 'Pendente'}</div>
      <div class="actions">
        <a class="btn secondary" href="docs/sales/backups/">Backups</a>
      </div>
    </div>
    <div class="card">
      <h2>Enriquecimento de leads</h2>
      <div class="metric ok">{'SIM' if enriched else 'NÃO'}</div>
    </div>
    <div class="card">
      <h2>Onboarding parceiros</h2>
      <div class="metric">{onboarding}</div>
      <div class="actions">
        <a class="btn secondary" href="docs/sales/onboarding-parceiros">Onboarding</a>
      </div>
    </div>
    <div class="card">
      <h2>Ações rápidas</h2>
      <div class="actions">
        <a class="btn" href="scripts/automation/verificador_funil_comercial.py">Rodar verificação</a>
        <a class="btn secondary" href="docs/sales/GUIA-ATIVACAO-ENVIO-AUTOMATICO-SEGURO.md">Guia SMTP</a>
      </div>
    </div>
  </div>

  <div class="footer">
    Praia Digital — Site: <a href="https://acarolmourad-commits.github.io/praia-digital/">Praia Digital</a> | Ferramentas: <a href="https://praia.digital">praia.digital</a>
  </div>
</div>
</body>
</html>
"""

OUT.write_text(html, encoding='utf-8')
print(f"Status page gerada em {OUT}")
print(f"leads={leads_count}, followups={followups_count}, backup={'OK' if backup_ok else 'PENDENTE'}, enriched={enriched}, onboarding={onboarding}")
