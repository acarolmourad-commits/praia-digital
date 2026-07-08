
import os, re, csv
from pathlib import Path

BATCH_DIR=Path('outreach/batch-semanal')
OUT_CSV=Path('outreach/lote-hoje-executavel.csv')

def extract_text(html):
    text=re.sub(r'<[^>]+>','',html)
    text=text.replace('\n',' ')
    text=re.sub(r'\s+',' ',text).strip()
    return text

items={
    'day1': sorted((BATCH_DIR/'day1').glob('*.html')) if (BATCH_DIR/'day1').exists() else [],
    'day2': sorted((BATCH_DIR/'day2').glob('*.html')) if (BATCH_DIR/'day2').exists() else [],
    'day3': sorted((BATCH_DIR/'day3').glob('*.html')) if (BATCH_DIR/'day3').exists() else [],
}
rows=[]
for day,files in items.items():
    for path in files:
        html=path.read_text(encoding='utf-8', errors='ignore')
        title=re.search(r'<title>([^<]+)</title>', html)
        email=re.search(r'mailto:([^?]+)', html)
        subject=title.group(1) if title else path.stem
        to=email.group(1) if email else ''
        body=extract_text(html)
        rows.append({'day':day,'file':path.name,'to':to,'subject':subject,'body':body[:240]})
with OUT_CSV.open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f, fieldnames=['day','file','to','subject','body'])
    writer.writeheader()
    writer.writerows(rows)
print('exported', len(rows), 'rows to', OUT_CSV)
