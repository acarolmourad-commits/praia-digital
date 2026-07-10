#!/usr/bin/env python3
"""Gerador de follow-up por cidade para outreach B2B."""
import csv
from pathlib import Path

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'

cities = ["Praia Grande","Santos","Guarujá","São Vicente","Peruíbe","Bertioga","Mongaguá","Itanhaém"]

def generate_followups():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        leads = list(csv.DictReader(f))
    
    # Group by city
    by_city = {}
    for lead in leads:
        city = lead.get('cidade_ref', lead.get('cidade', ''))
        by_city.setdefault(city, []).append(lead)
    
    # Generate follow-up for each city
    for city in cities:
        city_leads = by_city.get(city, [])
        if not city_leads:
            continue
        
        # Take top 5 by score
        top = sorted(city_leads, key=lambda x: int(x.get('_score', '0')), reverse=True)[:5]
        
        followup = f"""# Follow-up — {city}
Data: {datetime.now().strftime('%Y-%m-%d')}

Modelo para reenvio:
Assunto: Follow-up: proposta de parceria com IA — sem custo inicial

Opa, só passando rapidinho para não sumir.

A ideia continua a mesma: um piloto sem investimento inicial focado em resultado seu. Se fizer sentido, eu sigo com o Deep Dive e confirmamos 30min em vídeo.

Links:
• Site: https://acarolmourad-commits.github.io/praia-digital/
• Ferramentas gratuitas: https://praia.digital

Se quiser, eu posso enviar um caso curto agora.

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288
comercial@praia.digital

## Leads para follow-up em {city}:
"""
        for i, lead in enumerate(top, 1):
            followup += f"{i}. {lead['nome_da_imobiliaria']} — {lead['email']} — Score: {lead.get('_score', 'N/A')}\n"
        
        (BASE / f'docs/sales/followup-{city.lower().replace(" ","-")}.md').write_text(followup, encoding='utf-8')
        print(f'CREATED docs/sales/followup-{city.lower().replace(" ","-")}.md')

if __name__ == '__main__':
    generate_followups()
