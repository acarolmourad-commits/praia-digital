#!/usr/bin/env python3
"""Gerador de roteiro de envio de e-mails para hoje."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'docs/sales/leads-litoral-enriquecido.csv'
OUT = BASE / 'docs/sales/roteiro-envio-hoje.md'

def main():
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        leads = list(csv.DictReader(f))
    top = sorted(leads, key=lambda x: int(x.get('_score', '0')), reverse=True)[:5]
    
    lines = []
    lines.append("# Roteiro de envio de e-mails — Hoje")
    lines.append(f"Data: {datetime.now().strftime('%d/%m/%Y')}")
    lines.append(f"Leads selecionados: {len(top)}")
    lines.append("")
    lines.append("## Instruções")
    lines.append("1. Abra `outreach/enviar-emails-batch.html`")
    lines.append("2. Para cada lead abaixo, clique em 'Abrir e-mail'")
    lines.append("3. Cole o texto personalizado no corpo do e-mail")
    lines.append("4. Envie e marque como enviado")
    lines.append("")
    lines.append("## Modelo de e-mail")
    lines.append("Assunto: Parceria zero-custo para [Nome da Empresa]: receita recorrente nova, sem investir em tecnologia")
    lines.append("")
    lines.append("Corpo:")
    lines.append("Não é mais uma oferta de ferramenta. É um modelo de aliança ganha-ganha para aumentar a receita de ambos sem custo inicial.")
    lines.append("")
    lines.append("Eu sou Carolina Mourad, CEO da Praia Digital. Ajudo imobiliárias e construtoras do litoral paulista a captar mais leads qualificados e converter mais vendas — sem mexer no site atual e com investimento inicial zero.")
    lines.append("")
    lines.append("O que eu proponho:")
    lines.append("• Nós entregamos: captação digital automatizada + DL Deep + nutrição automática + conteúdo SEO por cidade e bairro.")
    lines.append("• Vocês fornecem: o BDR MLP e o conteúdo humano final.")
    lines.append("• Resultado esperado: +agendamentos, +negócios fechados e, em até 30 dias, um case conjunto.")
    lines.append("")
    lines.append("Preciso de 3 informações:")
    lines.append("1) Vídeo curto BTS/raio-BTS do time de vendas;")
    lines.append("2) 30min em vídeo na semana que vem;")
    lines.append("3) Site atual + 1 coordenador(a).")
    lines.append("")
    lines.append("Links:")
    lines.append("- Site: https://acarolmourad-commits.github.io/praia-digital/")
    lines.append("- Ferramentas gratuitas: https://praia.digital")
    lines.append("")
    lines.append("Atenciosamente,")
    lines.append("Carolina Mourad")
    lines.append("CEO — Praia Digital")
    lines.append("(11) 95434-6288")
    lines.append("comercial@praia.digital")
    lines.append("https://praia.digital")
    lines.append("")
    lines.append("## Leads para envio hoje")
    lines.append("")
    
    for i, lead in enumerate(top, 1):
        nome = lead['nome_da_imobiliaria']
        cidade = lead['cidade']
        email = lead['email']
        score = lead.get('_score', 'N/A')
        dor = lead.get('dor_principal', '')
        
        lines.append(f"### {i}. {nome} ({cidade})")
        lines.append(f"- **E-mail:** {email}")
        lines.append(f"- **Score:** {score}")
        lines.append(f"- **Dor principal:** {dor}")
        lines.append(f"- **Copy personalizada:**")
        lines.append(f"  > 'Em {cidade}, o maior gargalo costuma ser {dor}. A Praia Digital preparou um piloto de 7 a 14 dias sem custo inicial para resolver isso em {nome}.'")
        lines.append(f"- **Horário sugerido:** 10h ou 15h")
        lines.append(f"- **Follow-up:** 72h após este envio")
        lines.append("")
    
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'CREATED {OUT}')
    print(f'Leads selecionados: {len(top)}')

if __name__ == '__main__':
    main()
