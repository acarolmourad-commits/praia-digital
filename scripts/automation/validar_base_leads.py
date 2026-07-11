import csv, sys
from pathlib import Path
REQUIRED = [
    'lead_id','nome_imobiliaria','cidade','uf','nome_contato','email','whatsapp','site','origem','notas','prioridade'
]
def main():
    p = Path('docs/sales/leads-litoral-enriquecido.csv')
    if not p.exists():
        print('Arquivo nao encontrado: docs/sales/leads-litoral-enriquecido.csv')
        sys.exit(1)
    with p.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        headers = reader.fieldnames or []
        missing = [h for h in REQUIRED if h not in headers]
        if missing:
            print('Faltam colunas:', missing)
            sys.exit(1)
        rows = list(reader)
    print('Colunas OK:', headers)
    print('Total leads:', len(rows))
    vazios = [k for k in REQUIRED if all((r.get(k) or '').strip()=='' for r in rows)]
    print('Campos 100% vazios:', vazios)
    sem_email = [r for r in rows if not (r.get('email') or '').strip()]
    print('Sem email:', len(sem_email))
    sys.exit(0)
if __name__=='__main__':
    main()
