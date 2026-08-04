#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona FAQPage JSON-LD em páginas que ainda não possuem.
Aplicável a imoveis/ e personas/ com perguntas contextualizadas.
"""
import os, re
from pathlib import Path

REPO = Path('.').resolve()

IMOVEIS_FAQ = [
    ("Quais as formas de visitação?", "Visitas presenciais e virtuais por videoconferência. Agende pelo WhatsApp."),
    ("Quais as formas de pagamento?", "Financiamento, parcelamento direto ou à vista, conforme o imóvel."),
    ("O imóvel aceita permuta?", "Avaliamos permuta conforme o perfil do imóvel e da negociação."),
    ("Como funciona a assessoria?", "Acompanhamento completo: busca, visita, proposta e escritura."),
    ("Quais os custos adicionais?", "ITBI, escritura e taxa de registro. Simulamos junto ao financiamento."),
]

PERSONAS_FAQ = {
    'investidor': [
        ("Qual o retorno esperado?", "Varia por cidade e tipo, mas historicamente acima da poupança."),
        ("Como funciona a gestão de temporada?", "Cuidamos de anúncios, check-in, limpeza e suporte."),
        ("Quais cidades têm melhor retorno?", "Santos, Guarujá e Praia Grande concentram liquidez e rentabilidade."),
        ("Preciso de experiência?", "Não. Nós orientamos todo o processo do início ao fechamento."),
    ],
    'familia': [
        ("Quais bairros são mais seguros?", "Condomínios fechados e bairros com infraestrutura completa."),
        ("O imóvel tem lazer?", "Muitos incluem piscina, playground e área verde."),
        ("Como é a proximidade de escolas?", "Priorizamos imóveis próximos de escolas e serviços essenciais."),
        ("Tem opção de financiamento?", "Sim, trabalhamos com os principais bancos e construtoras."),
    ],
    'temporada': [
        ("Como funciona o aluguel de temporada?", "Contrato simples, entrada caução e taxa de limpeza."),
        ("Quais os períodos mais procurados?", "Verão, feriados prolongados e alta temporada."),
        ("Preciso de uma administradora?", "Recomendamos para maior segurança e rentabilidade."),
        ("Como fica a manutenção?", "Incluímos suporte básico e indicação de parceiros locais."),
    ],
    'primeiro-imovel': [
        ("Por onde começo?", "Defina orçamento, cidade e tipo de imóvel. Nós ajudamos no restante."),
        ("Quanto preciso de entrada?", "Varia de 20% a 40%, conforme o financiamento."),
        ("O financiamento é complicado?", "Não. Orientamos toda a documentação e simulação."),
        ("Quais custos devo prever?", "Entrada, ITBI, escritura e eventuais reformas."),
    ],
}

def faq_json(questions):
    items = []
    for q, a in questions:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }

def patch_imovel(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'FAQPage' in txt:
        return False
    slug = path.stem
    title_m = re.search(r'<title>\s*(.+?)\s*</title>', txt, re.I|re.S)
    title = title_m.group(1) if title_m else slug.replace('-', ' ').title()
    questions = IMOVEIS_FAQ + [(f"O que é um {title.split(' | ')[0].strip()}?", f"Imóvel do tipo {title.split(' | ')[0].strip()} oferecido pela Litoral Prime com assessoria completa.")]
    data = faq_json(questions)
    import json
    script = f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>\n'
    txt = txt.replace('</head>', script + '</head>', 1)
    path.write_text(txt, encoding='utf-8')
    return True

def patch_persona(path: Path):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    if 'FAQPage' in txt:
        return False
    slug = path.stem
    questions = PERSONAS_FAQ.get(slug, [])
    if not questions:
        return False
    import json
    data = faq_json(questions)
    script = f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>\n'
    txt = txt.replace('</head>', script + '</head>', 1)
    path.write_text(txt, encoding='utf-8')
    return True

def main():
    imoveis = [p for p in (REPO / 'imoveis').glob('*.html') if p.name != 'template-landing.html']
    personas = list((REPO / 'personas').glob('*.html'))
    patched = 0
    for p in imoveis:
        if patch_imovel(p):
            patched += 1
    for p in personas:
        if patch_persona(p):
            patched += 1
    print('FAQ_ADDED', patched)

if __name__ == '__main__':
    main()
