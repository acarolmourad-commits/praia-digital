import csv
from pathlib import Path

REPO = Path(r'C:/Users/Carolina/praia-digital')
SRC = REPO / 'docs/sales/leads-litoral-enriquecido.csv'
OUT = REPO / 'docs/sales/leads-importacao-brevo-2026-07-14.csv'

rows = []
with open(SRC, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome = (row.get('pessoa_de_contato') or '').strip() or (row.get('nome') or '').strip()
        email = (row.get('email') or '').strip()
        telefone = (row.get('whatsapp') or row.get('telefone') or '').strip()
        cidade = (row.get('cidade') or '').strip().title()
        estado = (row.get('estado') or row.get('state') or '').strip().upper() or 'SP'
        imobiliaria = (row.get('nome_da_imobiliaria') or '').title()
        origem = (row.get('fonte') or 'outreach').strip()
        status = (row.get('status') or 'novo').strip()
        if email:
            rows.append({
                'NOME': nome or 'Contato',
                'EMAIL': email,
                'TELEFONE': telefone,
                'CIDADE': cidade,
                'ESTADO': estado,
                'IMOBILIARIA': imobiliaria,
                'ORIGEM': origem,
                'STATUS': status,
                'LISTA': 'Leads Litoral SP'
            })

with open(OUT, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['NOME','EMAIL','TELEFONE','CIDADE','ESTADO','IMOBILIARIA','ORIGEM','STATUS','LISTA'])
    writer.writeheader()
    writer.writerows(rows)

print(f'Exportado {len(rows)} leads para {OUT}')
