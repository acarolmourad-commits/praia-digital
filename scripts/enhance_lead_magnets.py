from pathlib import Path

lead_base = Path('lead')
content_map = {
    'santos': {
        'title': 'Guia de Imóveis em Santos — Orla, Gonzaga e Embaré',
        'description': 'Guia local de Santos: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Santos.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Valorização histórica consistente com liquidez elevada.',
            'Alta temporada e demanda por moradia o ano todo.',
            'Orla como diferencial de preço e velocidade de venda.',
            'Perfil de comprador que valoriza serviços, acesso e renda por locação.',
        ],
    },
    'guaruja': {
        'title': 'Guia de Imóveis no Guarujá — Pitangueiras, Astúrias e Enseada',
        'description': 'Guia local do Guarujá: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo no Guarujá.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Mercado maduro com fluxo de caixa previsível.',
            'Oferta variada de apartamentos e casas.',
            'Acesso rápido a São Paulo pela Imigrantes.',
            'Perfil de comprador que valoriza liquidez, serviços e orla.',
        ],
    },
    'praia-grande': {
        'title': 'Guia de Imóveis em Praia Grande — Guilhermina, Ocian e Tupi',
        'description': 'Guia local de Praia Grande: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Praia Grande.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Entrada competitiva e liquidez crescente.',
            'Oferta ampla para diferentes perfis de comprador.',
            'Acesso direto pela via Imigrantes/Anchieta.',
            'Perfil de comprador que valoriza custo-benefício e potencial de valorização.',
        ],
    },
    'bertioga': {
        'title': 'Guia de Imóveis em Bertioga — Riviera e Centro',
        'description': 'Guia local de Bertioga: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Bertioga.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Exclusividade com liquidez na Riviera de São Lourenço.',
            'Natureza preservada e temporada relevante.',
            'Oferta direcionada a perfis de alto padrão.',
            'Perfil de comprador que valoriza privacidade, acesso e experiência de orla.',
        ],
    },
    'itanhaem': {
        'title': 'Guia de Imóveis em Itanhaém — Centro, Cibratel e Jardim São Fernando',
        'description': 'Guia local de Itanhaém: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Itanhaém.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Custo-benefício atrativo no Litoral Sul.',
            'Documentação regular e ocupação crescente.',
            'Oferta variada para famílias e investidores.',
            'Perfil de comprador que valoriza estabilidade, serviços e acesso.',
        ],
    },
    'mongagua': {
        'title': 'Guia de Imóveis em Mongaguá — Jardim São Paulo, Balneário e Centro',
        'description': 'Guia local de Mongaguá: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Mongaguá.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Custo de entrada competitivo e liquidez em alta.',
            'Oferta acessível para primeiro imóvel.',
            'Acesso fácil pela rodovia e proximidade com Santos.',
            'Perfil de comprador que valoriza custo-benefício, calmaria e potencial.',
        ],
    },
    'sao-sebastiao': {
        'title': 'Guia de Imóveis em São Sebastião — Centro Histórico, Juquehy e Maresias',
        'description': 'Guia local de São Sebastião: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em São Sebastião.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Temporada forte e procura internacional.',
            'Oferta que vai do padrão médio ao alto.',
            'Acesso combinado entre rodovia e marina.',
            'Perfil de comprador que valoriza exclusividade, natureza e rentabilidade.',
        ],
    },
    'ubatuba': {
        'title': 'Guia de Imóveis em Ubatuba — Centro, Itaguá e São Lourenço',
        'description': 'Guia local de Ubatuba: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Ubatuba.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Natureza preservada e temporada relevante.',
            'Oferta variada com potencial de valorização.',
            'Acesso por via Anchieta/Imigrantes + rodovias estaduais.',
            'Perfil de comprador que valoriza experiência, privacidade e retorno.',
        ],
    },
    'ilhabela': {
        'title': 'Guia de Imóveis em Ilhabela — Vila, Pernambuco e Bonete',
        'description': 'Guia local de Ilhabela: imóveis, investimentos, temporada, valorização e serviços.',
        'topics': [
            ('Avaliação local', 'Comparáveis e preço justo em Ilhabela.'),
            ('Temporada', 'Ocupação, preço e operação na orla.'),
            ('Investimento', 'ROI, custos e documentação.'),
        ],
        'highlights': [
            'Exclusividade e procura por temporada alta.',
            'Oferta voltada a perfis de alto padrão.',
            'Acesso por ferry-boat + São Sebastião.',
            'Perfil de comprador que valoriza privacidade, mar intacto e retorno.',
        ],
    },
}

for folder, data in content_map.items():
    p = lead_base / folder / 'index.html'
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    slug = folder
    wa_text = f"Ol%C3%A1%2C%20quero%20o%20guia%20de%20{data['title'].split('—')[0].strip().replace(' ', '%20')}"
    # rebuild body main
    topics_html = ''.join([
        f'<div class="card"><strong>{t[0]}</strong><p style="opacity:.75; margin-top:6px;">{t[1]}</p></div>'
        for t in data['topics']
    ])
    highlights_html = ''.join([f'<li>{h}</li>' for h in data['highlights']])
    main = f'''    <main id="main">
      <h1>{data['title']}</h1>
      <p class="lead">{data['description']}</p>

      <a class="cta" href="https://wa.me/5511954346288?text={wa_text}">Falar com especialista</a>
      <a class="cta" href="/education/cursos/index.html" style="background:#ff8c00">Ver cursos</a>

      <div class="card" style="margin-top:1.2rem">
        <h2>Baixar guia gratuito</h2>
        <form id="leadForm" class="form">
          <input type="text" id="name" placeholder="Nome" required>
          <input type="email" id="email" placeholder="E-mail" required>
          <input type="tel" id="phone" placeholder="Telefone/WhatsApp" required>
          <select id="city">
            <option value="">Cidade de interesse</option>
            <option value="caraguatatuba">Caraguatatuba</option>
            <option value="ubatuba">Ubatuba</option>
            <option value="ilhabela">Ilhabela</option>
            <option value="santos">Santos</option>
            <option value="guaruja">Guarujá</option>
            <option value="bertioga">Bertioga</option>
            <option value="sao-sebastiao">São Sebastião</option>
            <option value="praia-grande">Praia Grande</option>
          </select>
          <button type="submit">Quero receber o guia</button>
        </form>
        <p id="formMessage" style="margin-top:10px;opacity:.85;"></p>
      </div>

      <h2>Tópicos do guia</h2>
      <div class="grid grid-3">
        {topics_html}
      </div>

      <h2>Dados locais que importam</h2>
      <div class="card">
        <ul class="ticks">
          {highlights_html}
        </ul>
      </div>
    </main>'''
    if '<main id="main">' in txt and '</main>' in txt:
        txt = txt.split('<main id="main">', 1)[0] + main + '\n  </main>\n</body>\n</html>'.join(txt.split('</main>', 1)[1:])
    else:
        txt = txt.replace('</body>', main + '\n</body>')
    p.write_text(txt, encoding='utf-8')
    print(f'updated {p}')

print('done')
