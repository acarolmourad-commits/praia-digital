
import csv, os, re
from datetime import date, timedelta
from pathlib import Path

LEADS_CSV = 'docs/sales/leads-litoral-enriquecido.csv'
TRACKER = 'docs/sales/followup-registro.md'
OUT_DIR = Path('outreach')
BATCH_DIR = Path('outreach/batch-hoje')

def load_leads():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def load_tracker():
    if not os.path.exists(TRACKER):
        return []
    text = open(TRACKER, 'r', encoding='utf-8').read()
    entries=[]
    for line in text.splitlines():
        parts=[p.strip() for p in line.strip().split('|')]
        if len(parts)>5 and parts[0].isdigit():
            entries.append({'id':parts[0],'imobiliaria':parts[1],'envio':parts[2],'f3':parts[3],'f7':parts[4],'status':parts[5]})
    return entries

def assemble_batch(leads, tracker, day=1):
    BATCH_DIR.mkdir(exist_ok=True)
    batch=[]
    for entry in tracker:
        lid = entry.get('id')
        asset_map = {'envio': entry.get('envio'), 'f3': entry.get('f3'), 'f7': entry.get('f7')}
        for stage, path in asset_map.items():
            if not path or not os.path.exists(path):
                continue
            if day == 1 and stage != 'envio':
                continue
            if day == 2 and stage != 'f3':
                continue
            if day == 3 and stage != 'f7':
                continue
            lead = next((l for l in leads if l.get('id')==lid), None)
            if not lead:
                continue
            dest = BATCH_DIR / f"day{day}-lead{lid}-{stage}.html"
            html = open(path, 'r', encoding='utf-8').read()
            dest.write_text(html, encoding='utf-8')
            batch.append({'lead_id': lid, 'stage': stage, 'file': str(dest), 'email': lead.get('email','')})
    return batch

if __name__ == '__main__':
    leads = load_leads()
    tracker = load_tracker()
    for day in [1,2,3]:
        batch = assemble_batch(leads, tracker, day)
        print(f'Dia {day}: {len(batch)} assets preparados')
        for b in batch[:5]:
            print(' ', b['lead_id'], b['stage'], b['file'])
