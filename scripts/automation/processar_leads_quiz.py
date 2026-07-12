import json, csv
from pathlib import Path
from datetime import date

REPO = Path(r'C:/Users/Carolina/praia-digital')
QUIZ_JSON = REPO / 'outreach' / 'leads-site-capturados' / 'quiz-leads.json'
LEADS_CSV = REPO / 'docs/sales' / 'novos-leads-quiz-2026-07-12.csv'

QUIZ_JSON.parent.mkdir(parents=True, exist_ok=True)

if QUIZ_JSON.exists():
    try:
        data = json.loads(QUIZ_JSON.read_text(encoding='utf-8'))
    except Exception:
        data = []
else:
    data = []

if data:
    with open(LEADS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['nome','email','whatsapp','cidade','imobiliaria','desafio','porte','objetivo','origem','data'])
        for item in data:
            writer.writerow([
                item.get('nome',''),
                item.get('email',''),
                item.get('whatsapp',''),
                item.get('cidade',''),
                item.get('imobiliaria',''),
                item.get('q1',''),
                item.get('q2',''),
                item.get('q5',''),
                'quiz-diagnostico-gratuito',
                item.get('data','')
            ])
    print('Exportado:', LEADS_CSV)
else:
    print('Sem leads no quiz ainda; CSV mantido.')

print('Processador de leads do quiz pronto.')
