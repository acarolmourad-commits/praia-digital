
import os, csv, re
from datetime import datetime

BATCH_DIR='outreach/batch-hoje'
SENT_LOG='docs/sales/batch-sent-log.csv'

def run_batch():
    files=sorted([f for f in os.listdir(BATCH_DIR) if f.endswith('.html')])
    if not files:
        print('batch vazio')
        return
    rows=[]
    for f in files:
        path=os.path.join(BATCH_DIR,f)
        text=open(path,'r',encoding='utf-8').read()
        # extrair lead id e estágio pelo nome do arquivo dayX-type-leadY.html
        m=re.search(r'lead-(\d+)|lead(\d+)', f)
        lead=m.group(1) if m else 'unknown'
        stage='envio' if 'envio' in f else 'followup'
        rows.append({'lead_id':lead,'stage':stage,'file':path,'sent_at':datetime.now().isoformat()})
    # salvar log
    with open(SENT_LOG,'a',encoding='utf-8',newline='') as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=['lead_id','stage','file','sent_at'])
        writer.writerows(rows)
    print('batch executado:', len(rows), 'arquivos')

if __name__=='__main__':
    run_batch()
