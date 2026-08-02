#!/usr/bin/env python3
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
faqs = {
    'blog/propriedade-para-expatriados-litoral-2026.html': [
        ('Expatriados podem comprar no litoral?', 'Sim. Há suporte jurídico e consultoria para compra por estrangeiros.'),
        ('Quais documentos são necessários?', 'Passaporte, visto, comprovante de renda e endereço no exterior; orientamos o processo.'),
        ('Atendem financiamento internacional?', 'Não diretamente, mas indicamos parceiros para financiamento e câmbio.'),
    ],
    'marketing/roteiro-video-curto-60s-parcerias-2026-07-12.html': [
        ('Como usar vídeo curto para parcerias?', 'Reels/Shorts com cases, tours e chamadas para demo aumentam o alcance.'),
        ('Qual o formato ideal?', '60s, roteiro simples, legenda e CTA para WhatsApp ou demo.'),
        ('Funciona para imobiliárias pequenas?', 'Sim. Mesmo com produção simples, vídeos curtos aumentam a visibilidade local.'),
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
for rel, qas in faqs.items():
    p = BASE / rel
    if not p.exists():
        print('missing', p)
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'FAQPage' in text:
        print('skip', rel)
        continue
    items = ','.join(item_template.format(question=q, answer=a) for q, a in qas)
    block = template.format(items=items)
    if '<head>' not in text:
        print('skip no head', rel)
        continue
    text = text.replace('<head>', '<head>\n' + block, 1)
    p.write_text(text, encoding='utf-8')
    print('updated', rel)

# remove empty file if present
empty = BASE / 'blog' / ' Automacao-imoveis-alta-temporada-litoral-2026.html'
if empty.exists():
    try:
        empty.unlink()
        print('removed empty', empty)
    except Exception as e:
        print('remove error', e)
