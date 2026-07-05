#!/usr/bin/env python3
"""Gerador automático de sequência de e-mails personalizados para top leads."""
import csv
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'
OUT = BASE / 'docs/sales/sequencia-email-personalizada.md'

BASE_TEMPLATE = """Assunto: Parceria zero-custo para {nome}: receita recorrente nova, sem investimento em tecnologia

Abertura: {abertura}

Corpo:
Não é mais uma oferta de ferramenta. É um modelo de aliança ganha-ganha para aumentar a receita de ambos sem custo inicial.

Eu sou Carolina Mourad, CEO da Praia Digital. Ajudo imobiliárias e construtoras do litoral paulista a captar mais leads qualificados e converter mais vendas — sem mexer no site atual e com investimento inicial zero.

O que eu proponho:
• Nós entregamos: captação digital automatizada + DL Deep com nutrição automática + conteúdo SEO por cidade e bairro.
• Vocês fornecem: o BDR MLP e o conteúdo humano final.
• Resultado esperado: +agendamentos, +negócios fechados e, em até 30 dias, um case conjunto.

Preciso de 3 informações:
1) Vídeo curto BTS/raio-BTS do time de vendas;
2) 30min em vídeo na semana que vem;
3) Site atual + 1 coordenador(a).

Links:
• Site: https://acarolmourad-commits.github.io/praia-digital/
• Ferramentas gratuitas: https://praia.digital

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288
comercial@praia.digital
https://praia.digital"""

FOLLOWUP_TEMPLATE = """Assunto: Follow-up: proposta de parceria com IA — sem custo inicial

Opa, só passando rapidinho para não sumir.

A ideia continua a mesma: um piloto sem investimento inicial focado em resultado seu. Se fizer sentido, eu sigo com o Deep Dive e confirmamos 30min em vídeo.

Links:
• Site: https://acarolmourad-commits.github.io/praia-digital/
• Ferramentas gratuitas: https://praia.digital

Se quiser, eu posso enviar 1 case curto agora e você já vê o formato.

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288
comercial@praia.digital"""

ADVANCE_TEMPLATE = """Assunto: Re: Parceria zero-custo — próximo passo: Deep Dive + call de 30min

Perfeito, vamos consolidar o avanço.

Próximos passos:
1) Eu envio o Deep Dive até {data} com números do mercado e exemplo de caso.
2) Confirmamos a call de 30min na semana que vem.
3) Na call, apresento o plano de 7 a 14 dias sem investimento.

Links:
• Site: https://acarolmourad-commits.github.io/praia-digital/
• Ferramentas gratuitas: https://praia.digital

Atenciosamente,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288
comercial@praia.digital
https://praia.digital"""

def main():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        leads = list(csv.DictReader(f))
    top = sorted(leads, key=lambda x: int(x.get('_score', '0')), reverse=True)[:5]
    
    lines = []
    lines.append("# Sequência de e-mails personalizada — Top 5 leads")
    lines.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    lines.append("")
    
    for i, lead in enumerate(top, 1):
        nome = lead['nome_da_imobiliaria']
        cidade = lead['cidade']
        dor = lead.get('dor_principal', '')
        dif = lead.get('diferencial', '')
        score = lead.get('_score', '?')
        
        abertura = f"Em {cidade}, o maior gargalo costuma ser {dor}. A Praia Digital preparou um piloto de 7 a 14 dias sem custo inicial para resolver isso em {nome}."
        
        lines.append(f"## Lead {i}: {nome} ({cidade}) — Score {score}")
        lines.append("")
        
        # Dia 0
        lines.append("### Dia 0 — E-mail inicial")
        lines.append(BASE_TEMPLATE.format(nome=nome, abertura=abertura))
        lines.append("")
        
        # Dia 3
        lines.append(f"### Dia 3 — Follow-up ({(datetime.now() + timedelta(days=3)).strftime('%d/%m/%Y')})")
        lines.append(FOLLOWUP_TEMPLATE)
        lines.append("")
        
        # Dia 7
        lines.append(f"### Dia 7 — Avanço para call ({(datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')})")
        lines.append(ADVANCE_TEMPLATE.format(data=(datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')))
        lines.append("")
        
        lines.append("---")
        lines.append("")
    
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'CREATED {OUT}')
    print(f'Leads: {len(top)}')

if __name__ == '__main__':
    main()
