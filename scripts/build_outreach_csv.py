import json, csv
from pathlib import Path

in_path = Path('C:/Users/Carolina/praia-digital/docs/sales/outreach-gmail.json')
out_path = Path('C:/Users/Carolina/praia-digital/docs/sales/outreach-enviados.csv')
out_path.parent.mkdir(parents=True, exist_ok=True)

rows = json.loads(in_path.read_text(encoding='utf-8'))
fields = ['email_to','empresa','message_id','thread_id','date','status']
with out_path.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows:
        snippet = r.get('snippet', '')
        empresa = ''
        if ' equipe da ' in snippet:
            empresa = snippet.split(' equipe da ')[1].split('.')[0]
        w.writerow({
            'email_to': r.get('to', ''),
            'empresa': empresa,
            'message_id': r.get('id', ''),
            'thread_id': r.get('threadId', ''),
            'date': r.get('date', ''),
            'status': 'sent',
        })
print('WROTE', out_path)
print(out_path.read_text(encoding='utf-8'))
