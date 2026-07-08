import os, re, shutil, csv
from datetime import date, timedelta
from pathlib import Path

TRACKER='docs/sales/followup-registro.md'
BATCH_ROOT=Path('outreach/batch-semanal')
BATCH_ROOT.mkdir(exist_ok=True)

def load_leads():
    with open('docs/sales/leads-litoral-enriquecido.csv','r',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def build_week():
    leads=load_leads()
    # pick 30 leads with outreach assets, cycle day1 envio + day2 followups + day3 closing
    count=0
    for r in leads:
        lid=r.get('id')
        envio=f'outreach/envio-auto-{lid}.html'
        if not os.path.exists(envio):
            continue
        day1=BATCH_ROOT / 'day1' / f'envio-{lid}.html'
        day1.parent.mkdir(exist_ok=True)
        shutil.copy(envio, day1)
        # day2: 3dias followup if exists
        fu3=f'outreach/followup-3dias-lead-{lid}.html'
        if os.path.exists(fu3):
            shutil.copy(fu3, BATCH_ROOT/'day2'/f'followup3-{lid}.html')
        # day3: 7dias followup or call
        fu7=f'outreach/followup-7dias-lead-{lid}.html'
        if os.path.exists(fu7):
            shutil.copy(fu7, BATCH_ROOT/'day3'/f'followup7-{lid}.html')
        call=f'outreach/call-lead-{lid}.html'
        if os.path.exists(call):
            shutil.copy(call, BATCH_ROOT/'day3'/f'call-{lid}.html')
        count+=1
        if count>=30:
            break
    print('weekly batch built for', count, 'leads')

if __name__=='__main__':
    build_week()
