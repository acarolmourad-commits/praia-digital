
import re
from datetime import date, timedelta
from pathlib import Path

TRACKER='docs/sales/followup-registro.md'
CSV='docs/sales/leads-litoral-enriquecido.csv'
REPORT='docs/sales/relatorio-executivo-dia.md'

rows=list(__import__('csv').DictReader(open(CSV,'r',encoding='utf-8')))
lead_map={r['id']:r for r in rows}
tracker=open(TRACKER,'r',encoding='utf-8').readlines()
entries=[]
for line in tracker:
    parts=[p.strip() for p in line.strip().split('|')]
    if len(parts)>5 and parts[0].isdigit():
        entries.append({'id':parts[0],'imobiliaria':parts[1],'envio':parts[2],'f3':parts[3],'f7':parts[4],'status':parts[5]})
# prioritize: no send today, positive/hot leads, then neutrals without followup
priority=[]
for entry in entries:
    lid=entry['id']
    if entry.get('status')=='enviado' and entry.get('envio')==date.today().isoformat():
        continue
    if entry.get('status') in ['call-agendada','interessado','positivo','negociacao']:
        priority.append((1, entry))
    elif 'followup' not in entry.get('f3','').lower() and 'followup' not in entry.get('f7','').lower():
        priority.append((2, entry))
    else:
        priority.append((3, entry))
priority=sorted(priority, key=lambda x: x[0])
today=date.today().isoformat()
lines=[f'# Relatório Executivo de Prospecção — {today}\n\n']
lines.append('## Prioridades do dia\n')
for _,entry in priority[:20]:
    r=lead_map.get(entry['id'],{})
    lines.append(f"- Lead {entry['id']} | {entry.get('imobiliaria', r.get('nome','?'))} | {r.get('cidade','?')} | status={entry.get('status','?')} | envio={entry.get('envio','?')}\n")
open(REPORT,'w',encoding='utf-8').writelines(lines)
print('report written', len(lines), 'lines')
