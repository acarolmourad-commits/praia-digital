import csv
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
SRC = REPO / 'docs/sales/leads-litoral-enriquecido.csv'
OUT = REPO / 'docs/sales/leads-importacao-brevo-2026-07-14.csv'

rows = []
with open(SRC, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome = (row.get('nome') or '').strip()
        email = (row.get('email') or '').strip()
        telefone = (row.get('telefone') or '').strip()
        cidade = (row.get('cidade') or '').strip()
        origem = (row.get('origem') or row.get('source') or '').strip()
        status = (row.get('status') or row.get('stage') or '').strip()
        if email:
            rows.append({
                'NOME': nome or 'Contato',
                'EMAIL': email,
                'TELEFONE': telefone,
                'CIDADE': cidade,
                'ORIGEM': origem or 'outreach',
                'STATUS': status or 'novo',
                'LISTA': 'Leads Litoral SP'
            })

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['NOME','EMAIL','TELEFONE','CIDADE','ORIGEM','STATUS','LISTA'])
    writer.writeheader()
    writer.writerows(rows)

print(f'Exportado {len(rows)} leads para {OUT}')
