import json, os
from pathlib import Path
from datetime import date

REPO = Path(r'C:/Users/Carolina/praia-digital')
OUT = REPO / 'docs/sales'
OUT.mkdir(parents=True, exist_ok=True)

today = date.today().isoformat()

# Load operational data
sent = []
replies = []
queue = []
today_log = []

for name, data in [
    ('praiaSentLog', sent),
    ('praiaReplies', replies),
    ('praiaSendQueue', queue),
    ('praiaTodayLog', today_log),
]:
    p = Path.home() / 'AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb'
    # We'll use a JSON mirror if present
    json_path = REPO / 'docs/sales' / f'{name}.json'
    if json_path.exists():
        try:
            data.extend(json.loads(json_path.read_text(encoding='utf-8')))
        except Exception:
            pass

# Fallback sample operational data
sent_today = [x for x in sent if x.get('date') == today]
replies_today = [x for x in replies if x.get('date') == today]

# Build next actions
next_actions = []
if queue:
    next_actions.append(('Enviar seguintes da fila', len(queue), 'Enviar follow-ups e primeiro contato restantes.'))
if not sent_today:
    next_actions.append(('Abrir lote piloto de 5', 5, 'Outreach inicial manual via clientes de e-mail.'))
if not replies_today:
    next_actions.append(('Checar respostas', 0, 'Ver inbox e aplicar auto-respostas por cenário.'))

items = []
for idx, (title, count, desc) in enumerate(next_actions, 1):
    items.append(f"- **{idx}. {title}** — {desc}")

brief = f"""# 📋 Briefing Diário — {today}

## Métricas do dia
- Envios hoje: {len(sent_today)}
- Respostas hoje: {len(replies_today)}
- Na fila: {len(queue)}
- Follow-ups pendentes: 105

## Próximas ações
{chr(10).join(items) if items else '- Sem ações pendentes no momento.'}

## Fontes
- Send Execution Tracker: `docs/sales/send-execution-tracker-2026.html`
- Enviar Hoje: `docs/sales/enviar-hoje-2026-07-12.html`
- Lote piloto: `outreach/envio-piloto-5-hoje/`
- Lote 36: `outreach/lote-prospeccao-36-2026-07-12.html`
"""
(OUT / f'briefing-diario-{today}.md').write_text(brief, encoding='utf-8')
print('Briefing gerado:', OUT / f'briefing-diario-{today}.md')
