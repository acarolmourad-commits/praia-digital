import csv, time, urllib.parse
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital/docs/sales')
BASE.mkdir(parents=True, exist_ok=True)
LEADS_PATH = BASE / 'lead-list.json'
DONE_PATH = BASE / 'prospeccao-done.csv'

DONE_PATH.write_text('fonte,query,dominio,email,status\n', encoding='utf-8')
LEADS_PATH.write_text('[]', encoding='utf-8')

QUERIES = [
  'imobiliaria santos site:.br email contato',
  'imobiliaria guarujá site:.br email contato',
  'imobiliaria bertioga site:.br email contato',
  'imobiliaria sao vicente site:.br email contato',
  'imobiliaria praia grande site:.br email contato',
  'imobiliaria mongaguá site:.br email contato',
  'imobiliaria itanhaem site:.br email contato',
  'imobiliaria peruibe site:.br email contato',
]

print('Script de prospecção manual pronto.')
print('Depois você pode rodar manualmente cada busca em motor público e copiar apenas domínios/emails verificados para cá.')
