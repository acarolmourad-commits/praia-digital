#!/usr/bin/env python3
"""Gerador de follow-up personalizado por cidade para top 5 leads."""
import csv, random
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'
OUT = BASE / 'docs/sales/followup-top5-por-cidade.md'

CITY_CONTEXT = {
    'Santos': 'Porto, orla e mercado imobiliário consolidado.',
    'Praia Grande': 'Alta demanda por temporada e investimento.',
    'Guarujá': 'Turismo e verão como pilar.',
    'São Vicente': 'Histórico + expansão imobiliária.',
    'Peruíbe': 'Natureza e crescimento de procura.',
    'Bertioga': 'Condomínios e alta rentabilidade.',
    'Mongaguá': 'Família e temporada.',
    'Itanhaém': 'Surf, verão e novos lançamentos.'
}

def main():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        leads = list(csv.DictReader(f))
    top = sorted(leads, key=lambda x: int(x.get('_score', '0')), reverse=True)[:5]
    
    lines = [
        '# Follow-up 72h personalizado por cidade — Top 5 leads',
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        ''
    ]
    
    for i, lead in enumerate(top, 1):
        nome = lead['nome_da_imobiliaria']
        cidade = lead['cidade']
        email = lead['email']
        dor = lead.get('dor_principal', '')
        dif = lead.get('diferencial', '')
        score = lead.get('_score', '?')
        contexto = CITY_CONTEXT.get(cidade, 'Mercado local em crescimento.')
        
        personalizacao = f" Em {cidade}, {contexto.lower()} Por isso, o foco é {dor} com {dif}."
        
        lines += [
            f"## Lead {i}: {nome} ({cidade})",
            f"- E-mail: {email}",
            f"- Score: {score}",
            f"- Dor: {dor}",
            f"- Diferencial: {dif}",
            f"- Contexto local: {contexto}",
            '',
            'Assunto: Follow-up: proposta de parceria com IA — sem custo inicial',
            '',
            'Corpo:',
            'Opa, só passando rapidinho para não sumir.',
            '',
            f'Abertura personalizada:{personalizacao}',
            '',
            'A ideia continua a mesma: um piloto sem investimento inicial focado em resultado seu. Se fizer sentido, eu sigo com o Deep Dive e confirmamos 30min em vídeo.',
            '',
            'Links:',
            '• Site: https://acarolmourad-commits.github.io/praia-digital/',
            '• Ferramentas gratuitas: https://praia.digital',
            '',
            'Se quiser, eu posso enviar 1 case curto agora e você já vê o formato.',
            '',
            'Atenciosamente,',
            'Carolina Mourad',
            'CEO — Praia Digital',
            '(11) 95434-6288',
            'comercial@praia.digital',
            ''
        ]
    
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print('CREATED', OUT)
    print('Leads: 5')

if __name__ == '__main__':
    main()
