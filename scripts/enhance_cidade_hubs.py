import re
from pathlib import Path

cities = {
    'bertioga': 'Bertioga',
    'itanhaem': 'Itanhaém',
    'mongagua': 'Mongaguá',
    'sao-vicente': 'São Vicente',
    'peruibe': 'Peruíbe',
}

extra_section = '''
      <h2>Dados locais que importam</h2>
      <div class="card">
        <ul class="ticks">
          <li>Perfil de temporada consistente com picos em feriados.</li>
          <li>Valorização alinhada ao fluxo de acesso e oferta local.</li>
          <li>Oferta variada de apartamentos e casas.</li>
          <li>Comprador que valoriza liquidez, serviços e proximidade da capital.</li>
        </ul>
      </div>
'''

for slug, name in cities.items():
    p = Path(f'cidades/{slug}.html')
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if 'Dados locais que importam' in txt:
        continue
    # insert before last </main> or before footer
    if '</main>' in txt:
        txt = txt.replace('</main>', extra_section + '    </main>', 1)
    else:
        txt = txt.replace('  </div>\n</body>', extra_section + '  </div>\n</body>', 1)
    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
