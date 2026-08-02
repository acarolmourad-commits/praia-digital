from pathlib import Path
import re

root = Path('imoveis')

targets = [
    'apartamento-vista-mar-santos.html',
    'imoveis/1-quarto-s.html',
    'imoveis/35m2-sem-vaga.html',
]

# Simple generic recommended section for property pages
section = '''
<section class="recommended">
  <h2>Imóveis recomendados no litoral</h2>
  <ul>
    <li><a href="../imoveis.html">Ver todos os imóveis</a></li>
    <li><a href="../blog/index.html">Conteúdos sobre imóveis no litoral</a></li>
    <li><a href="../servicos.html">Serviços imobiliários</a></li>
  </ul>
</section>
'''

updated = 0
for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'recommended' in text:
        continue
    # insert before footer if present
    if '<footer' in text:
        new_text = text.replace('<footer', section + '<footer', 1)
    else:
        new_text = text + section
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print('updated', path.relative_to(root))
        updated += 1

print('updated', updated, 'pages')
