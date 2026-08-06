from pathlib import Path

city_bairros = {
    'santos': ['gonzaga', 'embare', 'boqueirao'],
    'guaruja': ['pitangueiras', 'asturias', 'enseada'],
    'praia-grande': ['guilhermina', 'ocian', 'tupi'],
    'bertioga': ['centro', 'riviera', 'guaratuba'],
    'itanhaem': ['centro', 'praia', 'condominios'],
    'mongagua': ['centro', 'praia', 'condominios'],
    'sao-vicente': ['centro', 'praia', 'jardim'],
    'peruibe': ['centro', 'praia', 'condominios'],
    'caraguatatuba': ['centro', 'jaguaribe', 'prainha'],
    'ilhabela': ['vila', 'pernambuco', 'bonete'],
    'sao-sebastiao': ['centro-historico', 'juquehy', 'maresias'],
    'ubatuba': ['centro', 'itagua', 'sao-lourenco'],
}

descriptions = {
    'centro': 'Serviços, comércio e acesso.',
    'praia': 'Temporada e vizinhança.',
    'condominios': 'Perfil residencial.',
    'gonzaga': 'Comércio forte, orla e liquidez.',
    'embare': 'Perfil residencial e acesso rápido.',
    'boqueirao': 'Temporada, famílias e diversidade de oferta.',
    'pitangueiras': 'Vista mar, comércio e temporada.',
    'asturias': 'Oferta madura e proximidade da orla.',
    'enseada': 'Mercado amplo e fluxo de caixa.',
    'guilhermina': 'Temporada e comércio ativo.',
    'ocian': 'Entrada competitiva e liquidez.',
    'tupi': 'Perfil familiar e oferta variada.',
    'riviera': 'Alto padrão, golfe e temporada forte.',
    'guaratuba': 'Perfil familiar e praias arredadas.',
    'jaguaribe': 'Temporada e lazer.',
    'prainha': 'Perfil familiar.',
    'vila': 'Serviços e acesso em Ilhabela.',
    'pernambuco': 'Temporada e natureza.',
    'bonete': 'Exclusividade e mar preservado.',
    'centro-historico': 'História, acesso e serviços.',
    'juquehy': 'Temporada e lazer de alto padrão.',
    'maresias': 'Temporada forte e perfil internacional.',
    'itagua': 'Acesso e temporada.',
    'sao-lourenco': 'Perfil residencial e lazer.',
    'jardim': 'Perfil residencial e valorização.',
}

base = Path('bairros')
for city, bairros in city_bairros.items():
    p = base / city / 'index.html'
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    block = '      <h2>Bairros e praias em destaque</h2>\n      <div class="grid grid-3">\n'
    cards = []
    for b in bairros:
        slug = b
        name = b.replace('-', ' ').title()
        desc = descriptions.get(slug, 'Conteúdo local.')
        cards.append(
            f'        <div class="card"><a href="/bairros/{city}/{slug}.html">{name}</a><p style="opacity:.75; margin-top:6px;">{desc}</p></div>'
        )
    block += '\n'.join(cards) + '\n      </div>'
    old = '      <h2>Bairros e praias em destaque</h2>\n      <div class="grid grid-3">\n'
    if old in txt:
        start = txt.index(old)
        end = txt.index('      </div>', start) + len('      </div>')
        txt = txt[:start] + block + txt[end:]
        p.write_text(txt, encoding='utf-8')
        print(f'updated {p}')
    else:
        print(f'skip {p}')

print('done')
