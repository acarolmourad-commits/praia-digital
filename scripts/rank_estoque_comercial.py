# Preparar estoque comercial — 10 Motor A + 30 Motor B + 586 B2B

import csv
from pathlib import Path

root=Path('C:/Users/Carolina/praia-digital')

motor_a=root/'docs'/'comercial'/'motor_a_novo_estoque_2026-08-16.csv'
motor_b=root/'docs'/'comercial'/'leads_sao_sebastiao_bertioga.csv'

out=root/'docs'/'comercial'/'fila_comercial_rankeada_2026-08-16.md'

def parse_score(v):
    try: return float(v)
    except: return 0

def score_lead(score, tipo, servico):
    s=parse_score(score)
    t=(tipo or '').lower()
    if any(x in t for x in ['proprietário','proprietario','anfitriao','anfitrião']): adj=5
    elif 'imobiliaria' in t: adj=0
    else: adj=2
    final=s+adj
    if 'administração' in (servico or '').lower() or 'administracao' in (servico or '').lower(): final+=5
    if 'seo' in (servico or '').lower(): final+=3
    return min(final,100)

rows=[]
for src in [motor_a, motor_b]:
    if not src.exists(): continue
    with src.open('r', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        for row in reader:
            rows.append({
                'lead_id': row.get('lead_id',''),
                'score_ajustado': score_lead(row.get('score',''), row.get('tipo_cliente',''), row.get('servico_potencial','')),
                'score_bruto': parse_score(row.get('score','')),
                'nome': row.get('nome_empresa',''),
                'cidade': row.get('city',''),
                'tipo': row.get('tipo_cliente',''),
                'servico': row.get('servico_potencial',''),
                'score_raw': row.get('score',''),
                'status': row.get('status',''),
                'url': row.get('url',''),
                'canal': row.get('canal_contato',''),
            })

rows_sorted=sorted(rows, key=lambda x: x['score_ajustado'], reverse=True)
top=sorted(rows_sorted, key=lambda x: x['score_ajustado'], reverse=True)[:20]

lines=['# Fila comercial ranqueada — 2026-08-16\n','Ranked por score ajustado: score bruto + ajuste por tipo e serviço.\n']
for i,r in enumerate(top,1):
    lines.append(f"{i}. {r['lead_id']} | {r['nome']} | {r['cidade']} | {r['servico']} | score_ajustado={r['score_ajustado']} | raw={r['score_raw']}")
lines.append('\nUso: priorizar contato pelo maior score ajustado; para D2 pós-análise, usar como fila pós-aprendizado.')
out.write_text('\n'.join(lines), encoding='utf-8')
print(f'fila_comercial_rankeada_2026-08-16.md criada com {len(top)} leads no topo')
