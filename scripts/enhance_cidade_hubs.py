import re
from pathlib import Path

cities = {
    'santos': {
        'name': 'Santos',
        'highlights': [
            'Valorização histórica consistente com liquidez elevada.',
            'Alta temporada e demanda por moradia o ano todo.',
            'Orla como diferencial de preço e velocidade de venda.',
            'Perfil de comprador que valoriza serviços, acesso e renda por locação.',
        ],
    },
    'guaruja': {
        'name': 'Guarujá',
        'highlights': [
            'Mercado maduro com fluxo de caixa previsível.',
            'Oferta variada de apartamentos e casas.',
            'Acesso rápido a São Paulo pela Imigrantes/ferry-boat.',
            'Perfil de comprador que valoriza liquidez, serviços e orla.',
        ],
    },
    'praia-grande': {
        'name': 'Praia Grande',
        'highlights': [
            'Entrada competitiva e liquidez crescente.',
            'Oferta ampla para diferentes perfis de comprador.',
            'Acesso direto pela via Imigrantes/Anchieta.',
            'Perfil de comprador que valoriza custo-benefício e potencial de valorização.',
        ],
    },
    'bertioga': {
        'name': 'Bertioga',
        'highlights': [
            'Exclusividade com liquidez na Riviera de São Lourenço.',
            'Natureza preservada e temporada relevante.',
            'Oferta direcionada a perfis de alto padrão.',
            'Perfil de comprador que valoriza privacidade, acesso e experiência de orla.',
        ],
    },
    'itanhaem': {
        'name': 'Itanhaém',
        'highlights': [
            'Custo-benefício atrativo no Litoral Sul.',
            'Documentação regular e ocupação crescente.',
            'Oferta variada para famílias e investidores.',
            'Perfil de comprador que valoriza estabilidade, serviços e acesso.',
        ],
    },
    'mongagua': {
        'name': 'Mongaguá',
        'highlights': [
            'Custo de entrada competitivo e liquidez em alta.',
            'Oferta acessível para primeiro imóvel.',
            'Acesso fácil pela rodovia e proximidade com Santos.',
            'Perfil de comprador que valoriza custo-benefício, calmaria e potencial.',
        ],
    },
    'sao-vicente': {
        'name': 'São Vicente',
        'highlights': [
            'Acesso rápido e estrutura consolidada.',
            'Temporada forte com fluxo de segunda residência.',
            'Oferta diversificada entre orla e bairros internos.',
            'Perfil de comprador que valoriza liquidez, serviços e custo-benefício.',
        ],
    },
    'peruibe': {
        'name': 'Peruíbe',
        'highlights': [
            'Natureza preservada e temporada relevante.',
            'Oferta com potencial de valorização.',
            'Acesso pelo Litoral Sul e proximidade com Iguape.',
            'Perfil de comprador que valoriza experiência, privacidade e retorno.',
        ],
    },
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

for slug, data in cities.items():
    p = Path(f'cidades/{slug}.html')
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if 'Dados locais que importam' in txt:
        continue
    highlights_html = ''.join([f'<li>{h}</li>' for h in data['highlights']])
    extra_section = f'''
      <h2>Dados locais que importam</h2>
      <div class="card">
        <ul class="ticks">
          {highlights_html}
        </ul>
      </div>
'''
    if '</main>' in txt:
        txt = txt.replace('</main>', extra_section + '    </main>', 1)
    else:
        txt = txt.replace('  </div>\n</body>', extra_section + '  </div>\n</body>', 1)
    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
