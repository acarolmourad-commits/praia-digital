import csv
from pathlib import Path
from datetime import date, datetime

root = Path("C:/Users/Carolina/praia-digital")
today = date.today().isoformat()

# Helper to safely read file
def safe_read(path_str):
    p = root / path_str
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")

# 1. Follow-ups pendentes
tracker = safe_read("docs/sales/followup-registro.md")
followups = [l for l in tracker.splitlines() if today in l and "follow-up" in l.lower()]

# 2. Leads capturados
leads_text = safe_read("docs/sales/parcerias-leads-capturados.csv")
leads_lines = leads_text.splitlines()
leads_count = max(0, len(leads_lines) - 1)  # exclude header

# 3. Follow-ups gerados
followup_dir = root / "outreach/followups-pendentes"
followup_files = list(followup_dir.glob("*.html")) if followup_dir.exists() else []
followup_count = len(followup_files)

# 4. Backup status
backup_root = root / "backups"
backup_count = len(list(backup_root.iterdir())) if backup_root.exists() else 0

# Build briefing
briefing = f"""# Briefing Comercial — {today}

## 📊 Indicadores rápidos
- Leads capturados: {leads_count}
- Follow-ups pendentes hoje: {len(followups)}
- Follow-ups gerados: {followup_count}
- Backups disponíveis: {backup_count}

## 📅 Follow-ups do dia
"""
if followups:
    for i, line in enumerate(followups, 1):
        briefing += f"{i}. {line.strip()}\n"
else:
    briefing += "Nenhum follow-up pendente para hoje.\n"

briefing += f"""
## 🎯 Ações sugeridas
1. Revisar Formspree e adicionar novos leads no tracker.
2. Disparar follow-ups pendentes pelo WhatsApp ou e-mail.
3. Atualizar status dos leads após contato.
4. Executar backup antes de fechar o dia: `python scripts/automation/backup_dados_prospeccao.py`

## 🔗 Links úteis
- Tracker: docs/sales/followup-registro.md
- Leads: docs/sales/parcerias-leads-capturados.csv
- Cases: cases-rapidos-parcerias.html
- Ferramentas: https://praia.digital

---
Gerado automaticamente por Praia Digital em {datetime.now().strftime('%H:%M:%S')}
"""

out_path = root / "docs/sales/briefing-comercial-diario.md"
out_path.write_text(briefing, encoding="utf-8")
print(f"Briefing gerado em: {out_path}")
print(f"Resumo: {len(followups)} follow-ups, {leads_count} leads, {followup_count} follow-ups gerados")
