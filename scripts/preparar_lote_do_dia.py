import shutil, os
from datetime import datetime

base = r'C:\Users\Carolina\praia-digital'
plano_path = os.path.join(base, 'docs', 'sales', 'plano-envio-prioritario.md')
csv_dir = os.path.join(base, 'csv-lotes-email')

hoje = datetime.now().strftime('%Y%m%d')
dia_semana = datetime.now().weekday()  # 0=segunda ... 6=domingo
mapa_dia = {0:'Hoje',1:'Dia 2',2:'Dia 3-4',3:'Dia 3-4',4:'Dia 5-6',5:'Dia 5-6',6:'Dia 7'}
dia_nome = mapa_dia.get(dia_semana, 'Hoje')

# Parse best-effort do plano: encontrar linhas de CSV no dia correspondente
linhas_csv = []
capture = False
with open(plano_path, 'r', encoding='utf-8') as f:
for line in f:
if dia_nome in line:
capture = True
elif any(d in line for d in ['Hoje','Dia 2','Dia 3-4','Dia 5-6','Dia 7']):
capture = False
if capture and '.csv' in line:
linhas_csv.append(line.strip().split('`')[1])

emails = []
for rel in linhas_csv:
src = os.path.join(base, rel)
if os.path.exists(src):
with open(src, 'r', encoding='utf-8') as f:
emails.extend(f.read().strip().splitlines()[1:])  # skip header

out_csv = os.path.join(csv_dir, f'lote-hoje-{hoje}.csv')
with open(out_csv, 'w', encoding='utf-8') as f:
f.write('Linhas\n')
for e in emails:
f.write(e + '\n')

print('Dia da semana:', dia_nome)
print('CSV de hoje:', out_csv)
print('Linhas:', len(emails))
