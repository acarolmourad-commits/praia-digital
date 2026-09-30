import re, glob, os

DIR = 'servicos/cidade-servico'
CITIES = {
 'santos':'Santos','guaruja':'Guarujá','praia-grande':'Praia Grande','sao-vicente':'São Vicente',
 'mongagua':'Mongaguá','itanhaem':'Itanhaém','peruibe':'Peruíbe','bertioga':'Bertioga'}
SERVICES = {
 'avaliacao':'Avaliação de Imóveis','captacao':'Captação de Imóveis','automacao':'Automação Imobiliária',
 'consultoria':'Consultoria Imobiliária','descricao-ia':'Descrição com IA','venda-imovel':'Venda de Imóveis'}

# ---- 1) Fix 48 existing cidade-servico pages (issue #31) ----
for f in glob.glob(f'{DIR}/*.html'):
    base = os.path.basename(f)[:-5]
    if base.endswith('venda-imovel'): city_slug, svc_slug = base[:-len('-venda-imovel')], 'venda-imovel'
    elif base.endswith('descricao-ia'): city_slug, svc_slug = base[:-len('-descricao-ia')], 'descricao-ia'
    else: city_slug, svc_slug = base.rsplit('-', 1)
    city, svc = CITIES[city_slug], SERVICES[svc_slug]
    s = open(f, encoding='utf-8').read()
    orig = s
    s = re.sub(r'(?m)^  (\{"@context": "https://schema\.org", "@type": "Organization".*\})$',
               '  <script type="application/ld+json">\n  \\1\n  </script>', s)
    s = s.replace('\n style="margin-top:18px">\n      <h2>Quero receber mais informações</h2>',
                  '\n    <div class="lead-form" style="margin-top:18px">\n      <h2>Quero receber mais informações</h2>')
    s = s.replace('Atendimento especializado em Guarujá', f'Atendimento especializado em {city}')
    s = s.replace('<a href="../../cidades/guaruja.html">Hub Guarujá</a>',
                  f'<a href="../../cidades/{city_slug}.html">Hub {city}</a>')
    s = re.sub(r'("@type": "RealEstateListing",\s*\n\s*)"name": "[^"]*",',
               lambda m: m.group(1) + f'"name": "{svc} em {city}",', s)
    s = re.sub(r'"description": "Serviço de [^"]*: atendimento especializado pela Praia Digital\."',
               f'"description": "{svc} em {city}: atendimento especializado pela Praia Digital."', s)
    s = re.sub(r'("areaServed": \{\s*\n\s*"@type": "City",\s*\n\s*)"name": "[^"]*"',
               lambda m: m.group(1) + f'"name": "{city}"', s)
    if svc_slug != 'automacao':
        s = re.sub(r'<script type="application/ld\+json">\s*\n\{"@context": "https://schema\.org", "@type": "FAQPage".*?\n</script>\n', '', s, flags=re.S)
    if city_slug in ('praia-grande','sao-vicente'):
        s = re.sub(r'<p>[^<]*profissional para o mercado imobiliário de [^<]*\.[^<]*</p>',
                   f'<p>{svc} profissional para o mercado imobiliário de {city}. Atendimento rápido e especializado pela Praia Digital.</p>', s)
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)

# slug bug extra: meta keywords/twitter/hero in praia-grande/sao-vicente
SVC_BROKEN = {
 'avaliacao':('Avaliacao','Avaliação de Imóveis'),'captacao':('Captacao','Captação de Imóveis'),
 'automacao':('Automacao','Automação Imobiliária'),'consultoria':('Consultoria','Consultoria Imobiliária'),
 'descricao-ia':('Descricao Ia','Descrição com IA'),'venda-imovel':('Venda Imovel','Venda de Imóveis')}
for cslug,(last,first,full) in {'praia-grande':('Grande','Praia','Praia Grande'),'sao-vicente':('Vicente','Sao','São Vicente')}.items():
    for sslug,(broken,svc) in SVC_BROKEN.items():
        f=f'{DIR}/{cslug}-{sslug}.html'
        s=open(f,encoding='utf-8').read(); o=s
        s=s.replace(f'{last} {broken} em {first}', f'{svc} em {full}')
        s=s.replace(f'{last} {broken} profissional para o mercado imobiliário de {first}',
                    f'{svc} profissional para o mercado imobiliário de {full}')
        if s!=o: open(f,'w',encoding='utf-8').write(s)
print('step1 ok')

# ---- 2) Generate 36 new pages (issue #31, part 2) ----
CITIES_12 = [
 ('santos','Santos'),('guaruja','Guarujá'),('praia-grande','Praia Grande'),('sao-vicente','São Vicente'),
 ('mongagua','Mongaguá'),('itanhaem','Itanhaém'),('peruibe','Peruíbe'),('bertioga','Bertioga'),
 ('ilhabela','Ilhabela'),('caraguatatuba','Caraguatatuba'),('sao-sebastiao','São Sebastião'),('ubatuba','Ubatuba')]
SERVICES_L = list(SERVICES.items()) + [('midia-profissional','Mídia Profissional')]
NEW_CITIES = {
 'ilhabela': ('Ilhabela','Ilhabela combina arquipélago preservado, marinas e condomínios de alto padrão com forte demanda de temporada e náutica.',
   ['Temporada náutica com alta demanda em feriados e regatas.','Condomínios de alto padrão com valorização consistente.','Acesso por ferry-boat a partir de São Sebastião.','Praias preservadas valorizam imóveis com vista mar.']),
 'caraguatatuba': ('Caraguatatuba','Caraguatatuba é o principal polo urbano da Costa Norte, com comércio completo e praias como Martim de Sá e Tabatinga.',
   ['Maior população da Costa Norte, com demanda o ano todo.','Praia Martim de Sá com forte apelo de temporada.','Acesso rápido pela Tamoios e Rio-Santos.','Mercado aquecido para moradia e investimento.']),
 'sao-sebastiao': ('São Sebastião','São Sebastião une centro histórico, Maresias e Camburi, com perfil de surf, temporada e alto padrão.',
   ['Maresias e Camburi com liquidez alta na temporada.','Centro histórico com charme, gastronomia e serviços.','Ferry-boat para Ilhabela movimenta toda a região.','Alta procura por casas em condomínio e pé na areia.']),
 'ubatuba': ('Ubatuba','Ubatuba reúne mais de 100 praias, como Itamambuca e Praia Grande, e forte mercado de temporada e esportes náuticos.',
   ['Mais de 100 praias com perfis variados de público.','Itamambuca e Praia Grande como destaques de demanda.','Temporada forte e demanda crescente de moradia fixa.','Acesso pela Rio-Santos e Oswaldo Cruz.'])}
MIDIA = {
 'intro': 'Fotografia profissional, vídeo, drone e tour virtual 360° para destacar seu imóvel nos portais e nas redes sociais.',
 'ganha': ['Fotos profissionais com tratamento de imagem.','Vídeo e imagens de drone homologado.','Tour virtual 360° para visitação remota.','Entrega otimizada para portais, redes e WhatsApp.'],
 'paraquem': 'Proprietários e corretores que querem anúncios com destaque real e mais visitas qualificadas.',
 'faq': [('O que está incluído no pacote de mídia?','Fotos profissionais, vídeo curto, imagens de drone e tour virtual 360°, conforme o perfil do imóvel.'),
         ('Quanto tempo leva a produção?','A captura é feita em uma visita e a entrega editada em até 5 dias úteis.'),
         ('Funciona para imóveis de temporada?','Sim, material profissional aumenta reservas e permite cobrar diárias melhores.'),
         ('Vocês cuidam da publicação?','Podemos integrar a mídia aos seus anúncios e à descrição gerada por IA.')]}

def build_midia_template():
    t = open(f'{DIR}/santos-avaliacao.html', encoding='utf-8').read()
    t = t.replace('Avaliação de Imóveis', 'Mídia Profissional')
    t = t.replace('santos-avaliacao', 'santos-midia-profissional')
    t = t.replace('Mídia Profissional profissional para o mercado imobiliário de Santos. Atendimento rápido e especializado pela Praia Digital.',
                  'Fotografia, vídeo, drone e tour virtual para valorizar imóveis em Santos. Atendimento rápido e especializado pela Praia Digital.')
    t = t.replace('"description": "Mídia Profissional em Santos: atendimento especializado pela Praia Digital."',
                  '"description": "Mídia profissional para imóveis em Santos: fotos, vídeo, drone e tour virtual pela Praia Digital."')
    t = re.sub(r'(?<=<h2>Sobre este serviço em Santos</h2>\n)<p>.*?</p>', f'<p>{MIDIA["intro"]}</p>', t)
    ganha = '\n'.join(f'<li>{i}</li>' for i in MIDIA['ganha'])
    t = re.sub(r'(?<=<h2>O que você ganha</h2>\n<ul>\n).*?(?=</ul>)', ganha + '\n', t, flags=re.S)
    t = re.sub(r'(?<=<h2>Para quem é</h2>\n)<p>.*?</p>', f'<p>{MIDIA["paraquem"]}</p>', t)
    faq = '\n'.join(f'        <li><strong>{q}</strong><br>{a}</li>' for q,a in MIDIA['faq'])
    t = re.sub(r'(?<=<h2>Perguntas frequentes</h2>\n      <ul>\n).*?(?=      </ul>)', faq + '\n', t, flags=re.S)
    return t

nav12 = '\n'.join(f'        <li><a href="../../cidades/{s}.html">{n}</a></li>' for s,n in CITIES_12)

def transform(tpl_text, tpl_city_slug, tpl_city_name, tpl_svc_slug, city_slug, city_name, svc_slug, intro_p, dados_list):
    t = tpl_text
    t = t.replace(f'{tpl_city_slug}-{tpl_svc_slug}.html', f'{city_slug}-{svc_slug}.html')
    t = t.replace(tpl_city_name, city_name)
    t = t.replace(f'cidades/{tpl_city_slug}.html', f'cidades/{city_slug}.html')
    t = t.replace(f'bairros/{tpl_city_slug}/', f'bairros/{city_slug}/')
    t = re.sub(r'img/[a-z0-9-]+\.(webp|jpg)', 'img/default-home.jpg', t)
    t = re.sub(r'(?<=<h2>Dados locais que importam</h2>\n)<p>.*?</p>', f'<p>{intro_p}</p>', t, count=1)
    items = '\n'.join(f'        <li>{i}</li>' for i in dados_list)
    t = re.sub(r'(<h2>Dados locais que importam</h2>\n      <ul>\n).*?(      </ul>)', lambda m: m.group(1)+items+'\n'+m.group(2), t, flags=re.S)
    t = re.sub(r'(<h2>Por cidade</h2>\n      <ul class="nav-menu">\n).*?(      </ul>)', lambda m: m.group(1)+nav12+'\n'+m.group(2), t, flags=re.S)
    rel = [f'        <li><a href="/cidades/{city_slug}.html">Todos os imóveis em {city_name}</a></li>',
           f'        <li><a href="/bairros/{city_slug}/index.html">Bairros em {city_name}</a></li>']
    for s,n in SERVICES_L:
        if s != svc_slug:
            rel.append(f'        <li><a href="/servicos/cidade-servico/{city_slug}-{s}.html">{n} em {city_name}</a></li>')
    t = re.sub(r'(<section id="related-links">\n      <h2>Conteúdo relacionado</h2>\n      <ul>\n).*?(      </ul>)',
               lambda m: m.group(1)+'\n'.join(rel)+'\n'+m.group(2), t, flags=re.S)
    return t

created = []
for slug,(name,intro,lista) in NEW_CITIES.items():
    for svc_slug, svc_name in SERVICES.items():
        tpl = open(f'{DIR}/santos-{svc_slug}.html', encoding='utf-8').read()
        out = transform(tpl, 'santos', 'Santos', svc_slug, slug, name, svc_slug, intro, lista)
        open(f'{DIR}/{slug}-{svc_slug}.html','w',encoding='utf-8').write(out)
        created.append(f'{slug}-{svc_slug}')

midia_tpl = build_midia_template()
BAIXADA_INTRO = {
 'santos':'Santos combina orla histórica, Gonzaga, Embaré e Boqueirão com fluxo turístico o ano todo.',
 'guaruja':'Guarujá une praias urbanas, condomínios de alto padrão e forte demanda de temporada.',
 'praia-grande':'Praia Grande oferece diversidade de bairros, infraestrutura urbana e demanda por temporada.',
 'sao-vicente':'São Vicente combina centro histórico, orla e acesso rápido a Santos.',
 'mongagua':'Mongaguá tem perfil familiar, preços acessíveis e demanda de temporada crescente.',
 'itanhaem':'Itanhaém une praias tranquilas, centro histórico e boa relação preço/valor.',
 'peruibe':'Peruíbe mistura natureza, praias extensas e oportunidades de investimento.',
 'bertioga':'Bertioga une Riviera de São Lourenço, Guaratuba e Centro com alto padrão e refúgio na Mata Atlântica.'}
DADOS_GENERICOS = ['Mercado local com demanda de moradia e temporada.','Acesso facilitado pelas principais rodovias do litoral.','Orla e bairros com perfis variados de imóveis.','Oportunidades para moradia e investimento.']
for slug,name in CITIES_12:
    intro = BAIXADA_INTRO.get(slug) or NEW_CITIES[slug][1]
    lista = NEW_CITIES.get(slug, (None,None,DADOS_GENERICOS))[2]
    out = transform(midia_tpl, 'santos', 'Santos', 'midia-profissional', slug, name, 'midia-profissional', intro, lista)
    open(f'{DIR}/{slug}-midia-profissional.html','w',encoding='utf-8').write(out)
    created.append(f'{slug}-midia-profissional')

s = open('sitemap.xml', encoding='utf-8').read()
block = ''.join(f'<url><loc>https://praia.digital/servicos/cidade-servico/{u}.html</loc><lastmod>2026-09-30</lastmod><changefreq>weekly</changefreq><priority>0.6</priority></url>\n' for u in created)
s = s.replace('</urlset>', block + '</urlset>')
open('sitemap.xml','w',encoding='utf-8').write(s)
print('step2 ok', len(created))

# ---- 3) Menu completo nas 4 paginas da Baixada (issue #22) ----
for f in ['cidades/santos.html','cidades/guaruja.html','cidades/praia-grande.html','cidades/bertioga.html']:
    s = open(f, encoding='utf-8').read()
    s = s.replace('<body>\n<header class="pd">', '<body>\n<meta name="pd-shared-nav">\n<header class="pd">', 1)
    s = re.sub(r'<footer class="pd">.*?</footer>', '<meta name="pd-shared-footer">', s, flags=re.S)
    open(f,'w',encoding='utf-8').write(s)
print('step3 ok')

# ---- 4) Ancoras vazias no menu compartilhado (issue #21) ----
f='partials/header.html'
s=open(f,encoding='utf-8').read()
s=s.replace('<a href="#" class="pd-nav-label" role="button" aria-expanded="false">\n        Sou Corretor / Imobiliária',
            '<a href="/corretores/cadastrar-imovel.html" class="pd-nav-label" role="button" aria-expanded="false">\n        Sou Corretor / Imobiliária')
s=s.replace('<a href="#" class="pd-nav-label" role="button" aria-expanded="false">\n        Ferramentas IA &amp; Estudos',
            '<a href="/apps/" class="pd-nav-label" role="button" aria-expanded="false">\n        Ferramentas IA &amp; Estudos')
s=s.replace('<a href="https://praia.digital/#rental" class="pd-nav-label"','<a href="/apps/simulador-roi-temporada/" class="pd-nav-label"')
s=s.replace('<a href="https://praia.digital/#rental">Simulador de ROI</a>','<a href="/apps/simulador-roi-temporada/">Simulador de ROI</a>')
s=s.replace('<a href="https://praia.digital/#buscar" class="pd-nav-label"','<a href="/encontrar-imovel.html" class="pd-nav-label"')
s=s.replace('<a href="https://praia.digital/#buscar">Busca de Imóveis</a>','<a href="/encontrar-imovel.html">Busca de Imóveis</a>')
open(f,'w',encoding='utf-8').write(s)
print('step4 ok')

# ---- 5) Bairros Jaragua/Massaguacu slug sem acento (issue #24) ----
import shutil
os.rename('bairros/caraguatatuba/jaraguá.html', 'bairros/caraguatatuba/jaragua.html')
os.rename('bairros/caraguatatuba/massaguaçu.html', 'bairros/caraguatatuba/massaguacu.html')
for f in glob.glob('**/*.html', recursive=True):
    s=open(f,encoding='utf-8').read(); o=s
    s=s.replace('jaraguá.html','jaragua.html').replace('massaguaçu.html','massaguacu.html')
    if s!=o: open(f,'w',encoding='utf-8').write(s)
print('step5 ok')

# ---- 6) Hub /cidades/index.html com as 12 cidades (issue #25) ----
CITY_CARDS = [
 ('santos','Santos','Gonzaga, Boqueirão e Ponta da Praia — liquidez e valorização.','Gonzaga|Boqueirão|Ponta da Praia'),
 ('guaruja','Guarujá','Enseada, Pitangueiras e Astúrias — mercado maduro com fluxo previsível.','Enseada|Pitangueiras|Astúrias'),
 ('praia-grande','Praia Grande','Ocian, Guilhermina e Vila Caiçara — entrada competitiva e liquidez crescente.','Ocian|Guilhermina|Vila Caiçara'),
 ('sao-vicente','São Vicente','Gonzaguinha e centro — preço de entrada com potencial de valorização.','Gonzaguinha|Centro|Itararé'),
 ('mongagua','Mongaguá','Centro e balneários — custo de entrada competitivo e liquidez em alta.','Centro|Jardim São Paulo|Balneário'),
 ('itanhaem','Itanhaém','Centro, Cibratel e arredores — documentação regular e ocupação crescente.','Centro|Cibratel|Jardim São Fernando'),
 ('peruibe','Peruíbe','Centro e orla extensa — estratégico no encontro do litoral sul.','Centro|Jardim São Miguel|Parque Turístico'),
 ('bertioga','Bertioga','Riviera de São Lourenço, Centro e Boracéia — exclusividade com liquidez.','Riviera|Centro|Boracéia'),
 ('ilhabela','Ilhabela','Vila, Perequê e praias preservadas — temporada náutica e alto padrão.','Vila|Perequê|Bonete'),
 ('caraguatatuba','Caraguatatuba','Martim de Sá e Tabatinga — principal polo urbano da Costa Norte.','Martim de Sá|Tabatinga|Massaguaçu'),
 ('sao-sebastiao','São Sebastião','Maresias, Camburi e centro histórico — surf, temporada e ferry para Ilhabela.','Maresias|Camburi|Centro Histórico'),
 ('ubatuba','Ubatuba','Mais de 100 praias, Itamambuca e Praia Grande — temporada e náutica.','Itamambuca|Praia Grande|Centro')]
cards = []
for slug, name, desc, tags in CITY_CARDS:
    tag_html = ''.join(f'<span class="tag">{t}</span>' for t in tags.split('|'))
    cards.append(f'''      <article class="card">
        <h2>{name}</h2>
        <p>{desc}</p>
        <div class="actions">
          <a class="btn" href="/cidades/{slug}.html">Ver guia da cidade</a>
          <a class="btn" href="/bairros/{slug}/index.html" style="background:#fff;color:#1F2937">Bairros</a>
        </div>
        <div style="margin-top:10px">{tag_html}</div>
      </article>''')
f = 'cidades/index.html'
s = open(f, encoding='utf-8').read()
s = re.sub(r'(?s)<div class="grid">.*?</div>\s*\n\s*<meta name="pd-shared-footer">',
           '<div class="grid">\n' + '\n'.join(cards) + '\n    </div>\n\n    <meta name="pd-shared-footer">', s)
s = s.replace('Pacotes SEO/GEO, artigos e roteiros por cidade do litoral paulista.',
              'Guias completos das 12 cidades do litoral paulista: bairros, temporada, valorização, balsas, gastronomia e eventos.')
s = s.replace('<p class="lead">Pacotes SEO/GEO, artigos, roteiros e materiais de conversão por cidade do litoral paulista.</p>',
              '<p class="lead">Guias completos das 12 cidades do litoral paulista: bairros, temporada, valorização, balsas, gastronomia premiada e eventos. Escolha a cidade:</p>')
s = s.replace('Conteúdo por cidade', 'Cidades do Litoral Paulista')
open(f,'w',encoding='utf-8').write(s)
print('step6 ok')
