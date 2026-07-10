#!/usr/bin/env python3
"""Gera CSV personalizado para Brevo com tokens de mesclagem e variacoes de template."""
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
LEADS_CSV = BASE / 'csv-lotes-email' / 'lote-mestre-unificado-2026-07-10.csv'
OUT_DIR = BASE / 'csv-lotes-email'
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES = {
    'A_seo_local': 'Parceria sem custo para {imobiliaria}: mais procura local sem mexer no site atual',
    'B_anuncios': '{imobiliaria}: avaliacao gratuita de anuncios + captacao sem custo inicial',
    'C_assistente_whatsapp': '{imobiliaria}: assistente no WhatsApp para reduzir tempo de resposta',
    'D_cases': '{imobiliaria}: case de +35 leads qualificados no litoral',
    'E_curta': 'Parceria sem custo para {imobiliaria}',
}

BODY_TEMPLATE = """Olá, {nome_contato},

Sou Carolina Mourad, CEO da Praia Digital. Ajudo imobiliárias e construtoras do litoral paulista a captar mais proprietários e compradores qualificados, com SEO local, conteúdo por bairro e automação leve — sem pedir investimento inicial no piloto.

Em vez de mais uma ferramenta, proponho um modelo de crescimento compartilhado: nós entregamos direcionamento de captação e conteúdo; vocês fornecem o time comercial e experiência local. Em até 30 dias, podemos ter um case conjunto.

Quero só 3 informações para iniciar:
1) Coordenador(a) do piloto
2) Site atual
3) 30min na semana que vem para alinhar

Links:
Site: https://acarolmourad-commits.github.io/praia-digital/
Ferramentas: https://praia.digital
WhatsApp: https://wa.me/5511954346288

Até breve,
Carolina Mourad
CEO — Praia Digital
(11) 95434-6288
https://praia.digital"""


def main():
    if not LEADS_CSV.exists():
        print(f'CSV not found: {LEADS_CSV}')
        return
    with open(LEADS_CSV, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    saida = []
    for i, r in enumerate(rows, 1):
        template_key = list(TEMPLATES.keys())[(i - 1) % len(TEMPLATES)]
        assunto = TEMPLATES[template_key]
        imobiliaria = r.get('nome', '').strip() or 'Parceiro'
        cidade = r.get('cidade', '').strip() or 'litoral'
        nome_contato = r.get('nome', '').strip() or 'Equipe'
        corpo = BODY_TEMPLATE.format(
            nome_contato=nome_contato,
            imobiliaria=imobiliaria,
        )
        saida.append({
            'email': r.get('email', '').strip(),
            'nome': nome_contato,
            'imobiliaria': imobiliaria,
            'cidade': cidade,
            'template': template_key,
            'assunto': assunto,
            'corpo': corpo,
        })
    out_path = OUT_DIR / f'lote-brevo-personalizado-{datetime.now().strftime("%Y-%m-%d")}.csv'
    fieldnames = ['email', 'nome', 'imobiliaria', 'cidade', 'template', 'assunto', 'corpo']
    with open(out_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(saida)
    print(f'GENERATED {len(saida)} personalized rows -> {out_path}')


if __name__ == '__main__':
    main()
