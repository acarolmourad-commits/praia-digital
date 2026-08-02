#!/usr/bin/env python3
"""
add_remaining_faqs.py
Adiciona FAQPage JSON-LD nas páginas públicas restantes do hub,
evitando diretórios utilitários como docs/, outreach/ e leads/.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

faq_map = {
    'litoral-prime-imoveis/index.html': [
        ('Quais cidades são atendidas?', 'Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.'),
        ('Como entrar em contato?', 'Pelo WhatsApp no botão flutuante ou no formulário das páginas de serviço.'),
        ('Vocês trabalham com temporada?', 'Sim. Há imóveis e campanhas específicas para alta temporada no litoral.'),
    ],
    'litoral-prime-imoveis/sitemap.html': [
        ('O que é o sitemap?', 'Lista todas as páginas públicas do site para facilitar a navegação e a indexação.'),
        ('Como encontrar uma cidade?', 'Use o menu ou o sitemap para acessar diretamente a página da cidade desejada.'),
        ('Atualizam as páginas com frequência?', 'Sim. Novos imóveis e serviços são inseridos regularmente.'),
    ],
}

template = '''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {items}
  ]
}}
</script>
'''

item_template = '''    {{
      "@type": "Question",
      "name": "{question}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{answer}"
      }}
    }}'''

for relative, qas in faq_map.items():
    path = BASE / relative
    if not path.exists():
        print('missing', path)
        continue
    text = path.read_text(encoding='utf-8')
    if 'FAQPage' in text:
        print('skip faq exists', relative)
        continue
    items = ','.join(
        item_template.format(question=q, answer=a) for q, a in qas
    )
    block = template.format(items=items)
    if '<head>' not in text:
        print('skip no head', relative)
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    path.write_text(text, encoding='utf-8')
    print('updated', relative)
