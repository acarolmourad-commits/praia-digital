import csv, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEADS_CSV = os.path.join(BASE, 'docs', 'sales', 'leads-litoral-enriquecido.csv')
OUTPUT_DIR = os.path.join(BASE, 'outreach', 'followups-gerados')
os.makedirs(OUTPUT_DIR, exist_ok=True)

oferta = sys.argv[1] if len(sys.argv) > 1 else 'consultoria imobiliária gratuita'
cidades = ['Santos', 'Guarujá', 'Praia Grande', 'Bertioga', 'Itanhaém', 'Peruíbe', 'São Vicente', 'Mongaguá', 'Ubatuba', 'Ilhabela']

leads = []
with open(LEADS_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        leads.append(dict(row))

selecionados = [l for l in leads if l.get('cidade', '').strip() in cidades and l.get('status', '').strip().lower() == 'contato_inicial_enviado']
selecionados.sort(key=lambda x: int(x.get('_score', x.get('score', 0)) or 0), reverse=True)
selecionados = selecionados[:12]

print(f'Leads selecionados: {len(selecionados)}')
for l in selecionados:
    print(f"- {l['id']} | {l['nome_da_imobiliaria']} | {l['cidade']} | score {l.get('_score', l.get('score','?'))}")

for l in selecionados:
    texto = f"""Olá, {l['pessoa_de_contato']}!

Sou Carolina Moura, CEO da Praia Digital.

Notei que {l['nome_da_imobiliaria']} ({l['cidade']}) pode melhorar resultados com {oferta}.

Resumo:
- Diagnóstico/entrega rápido
- Acesso gratuito a ferramentas profissionais
- Plano de ação personalizado

Responda este e-mail ou fale no WhatsApp: (11) 95434-6288

Att,
Carolina Moura
"""
    path = os.path.join(OUTPUT_DIR, f'followup-{l["id"]}.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(texto)

print('Follow-ups salvos em:', OUTPUT_DIR)
