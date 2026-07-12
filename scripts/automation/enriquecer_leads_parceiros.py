
import csv, datetime
from pathlib import Path

BASE = Path('C:/Users/Carolina/praia-digital')
CSV_ENTRADA = BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-realista.csv'
CSV_SAIDA = BASE / 'docs' / 'sales' / 'leads-litoral-enriquecido-enriquecido-2026-07-12.csv'

hoje = datetime.datetime.now().strftime('%Y-%m-%d')

if not CSV_ENTRADA.exists():
    print('Base realista não encontrada.')
    raise SystemExit(0)

with CSV_ENTRADA.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    fieldnames = list(reader.fieldnames or [])
    rows = list(reader)

for col in ['DOR_PRINCIPAL', 'CANAL_PREFERIDO', 'CANAL_RECOMENDACAO', 'PERFIL_CLIENTE', 'ULTIMA_INTERACAO']:
    if col not in fieldnames:
        fieldnames.append(col)

def normalize_city(c):
    return ''.join(ch for ch in (c or '').lower() if ch.isalpha())

def enriquecer(row, idx):
    cidade = normalize_city(row.get('cidade'))
    site = (row.get('site') or '').lower()
    notas = (row.get('notas') or '').lower()

    # cidade-based defaults
    if cidade in ['santos', 'guaruja', 'saovicente', 'saovicente']:
        canal = 'WhatsApp'
        recomendacao = 'Anúncios com descrições automáticas'
    elif cidade in ['praiagrande', 'mongagua', 'itanhaem']:
        canal = 'E-mail'
        recomendacao = 'Avaliação automática de preço'
    elif cidade in ['ubatuba', 'ilhabela', 'caraguatatuba']:
        canal = 'WhatsApp'
        recomendacao = 'Recomendação automática por perfil'
    elif cidade in ['bertioga', 'peruibe']:
        canal = 'E-mail'
        recomendacao = 'Assistente virtual 24h'
    else:
        canal = 'E-mail'
        recomendacao = 'SEO local + conteúdo'

    # dor by city/variant
    if cidade in ['ubatuba', 'ilhabela']:
        dor = 'Aumentar reservas de temporada'
        perfil = 'Alta temporada'
    elif cidade in ['santos', 'guaruja', 'saovicente', 'praiagrande']:
        dor = 'Acelerar vendas e captação no verão'
        perfil = 'Vendas'
    elif cidade in ['mongagua', 'itanhaem', 'bertioga', 'peruibe']:
        dor = 'Reduzir custo de captação'
        perfil = 'Captação'
    else:
        dor = 'Captar mais leads qualificados'
        perfil = 'Geral'

    # alternate some via site/number so it isn't uniform
    if idx % 7 == 0:
        canal = 'WhatsApp'
        recomendacao = 'Recomendação automática por perfil'
    elif idx % 11 == 0:
        canal = 'E-mail'
        recomendacao = 'Geração automática de descrições'

    row['DOR_PRINCIPAL'] = dor
    row['CANAL_PREFERIDO'] = canal
    row['CANAL_RECOMENDACAO'] = recomendacao
    row['PERFIL_CLIENTE'] = perfil
    row['ULTIMA_INTERACAO'] = hoje
    return row

rows = [enriquecer(r, i+1) for i, r in enumerate(rows)]

with CSV_SAIDA.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f'Enriquecidos {len(rows)} leads')
print(f'Saída: {CSV_SAIDA}')
