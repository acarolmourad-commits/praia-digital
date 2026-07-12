import json, csv
from pathlib import Path
from datetime import date

REPO = Path(r'C:/Users/Carolina/praia-digital')
LEADS_JSON = REPO / 'outreach' / 'leads-site-capturados' / 'leads-capturados.json'
LEADS_CSV = REPO / 'docs/sales/novos-leads-site-2026-07-12.csv'
BASE_LEADS = REPO / 'docs/sales/leads-litoral-enriquecido.csv'

LEADS_JSON.parent.mkdir(parents=True, exist_ok=True)

if LEADS_JSON.exists():
    try:
        leads = json.loads(LEADS_JSON.read_text(encoding='utf-8'))
    except Exception:
        leads = []
else:
    leads = []

today = date.today().isoformat()
new_leads = [l for l in leads if l.get('data', '').startswith(today)]

print(f'Leads capturados hoje: {len(new_leads)}')

if new_leads:
    with open(LEADS_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['nome','email','whatsapp','cidade','imobiliaria','interesse','data','origem'])
        for l in new_leads:
            writer.writerow([
                l.get('nome',''),
                l.get('email',''),
                l.get('whatsapp',''),
                l.get('cidade',''),
                l.get('imobiliaria',''),
                l.get('interesse',''),
                l.get('data',''),
                l.get('origem','formulario-site-praia-digital')
            ])
    print('Exportado:', LEADS_CSV)
else:
    print('Sem leads novos no JSON; mantendo CSV existente.')

print('Rotina de captura de leads do site pronta para uso.')
