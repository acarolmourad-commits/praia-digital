from pathlib import Path
import re

service_names = {
    'automacao': 'Automação Imobiliária',
    'avaliacao': 'Avaliação de Imóveis',
    'captacao': 'Captação de Imóveis',
    'consultoria': 'Consultoria Imobiliária',
    'descricao-ia': 'Descrição com IA',
    'venda-imovel': 'Venda de Imóveis',
}

base_faq = {
    'automacao': [
        ('A automação imobiliária funciona para temporada?', 'Sim, o fluxo cobre follow-up, agendamento e qualificação tanto para venda quanto para temporada/aluguel.'),
        ('Em quanto tempo fica operacional?', 'Em poucos dias, com configuração de funis, templates e integrações essenciais.'),
        ('Integra com o que já usamos?', 'Avaliamos CRM, canal de atendimento, site e ferramentas de agenda para integrar sem quebrar o fluxo atual.'),
        ('Como acompanhar os resultados?', 'Entregamos painel com métricas de resposta, agendamentos e conversão para ajustar o funil sem achismo.'),
    ],
    'avaliacao': [
        ('A avaliação serve para segunda residência?', 'Sim, usamos referências locais de temporada e permanência para chegar a um valor de mercado mais preciso.'),
        ('Em quanto tempo entrego o laudo?', 'Na maioria dos casos, em até 48h após a visita e o envio da documentação.'),
        ('Vocês atendem imóveis na orla?', 'Sim, e nesses casos consideramos restrições de marinha, condomínio e perfil de andar/vista.'),
        ('Posso usar o laudo para vender ou financiar?', 'Sim, o laudo é estruturado para orientar precificação, negociação e processo bancário.'),
    ],
    'captacao': [
        ('Vocês captam imóveis no Litoral Norte?', 'Sim, atendemos Litoral Norte e Sul com abordagem local e rede de contatos por cidade.'),
        ('Como funciona a exclusividade?', 'Definimos cláusulas claras de atendimento, periodicidade de report e metas de venda/aluguel.'),
        ('Qual o perfil de imóvel com maior saída?', 'Apartamentos vista mar, casas em condomínio e imóveis para temporada costumam ter liquidez maior.'),
        ('Como é feito o contato com o proprietário?', 'Com abordagem transparente, proposta de valor e relatório de mercado antes da visita.'),
    ],
    'consultoria': [
        ('A consultoria inclui estratégia de preço?', 'Sim, definimos faixa de preço, timing de entrada/saída e canais mais eficientes por cidade.'),
        ('Serve para investidores?', 'Sim, mapeamos rentabilidade, temporada, valorização e riscos específicos do Litoral Norte e Sul.'),
        ('Atendem pessoa física e jurídica?', 'Sim, com modelos de análise distintos para PF e PJ.'),
        ('Como medir o sucesso da consultoria?', 'Por métricas claras: tempo de venda, preço alcançado, taxa de ocupação e custo de aquisição.'),
    ],
    'descricao-ia': [
        ('A descrição com IA fica pronta em quanto tempo?', 'Em minutos, após enviarmos as fotos, características e diferenciais do imóvel.'),
        ('Serve para anúncios em marketplace?', 'Sim, geramos textos adaptados para site, marketplace e redes sociais.'),
        ('Consigo aprovar antes de publicar?', 'Sim, todas as descrições passam por revisão humana antes do uso final.'),
        ('Melhora o desempenho dos anúncios?', 'Textos mais claros e estruturados ajudam na retenção, compartilhamento e qualidade dos leads.'),
    ],
    'venda-imovel': [
        ('Vocês vendem imóveis no Litoral Norte?', 'Sim, com atuação em cidades como Caraguatatuba, Ilhabela, São Sebastião e Ubatuba.'),
        ('Como funciona o plano de venda?', 'Fotografia, descrição, canais, follow-up, visitas e negociação até o contrato.'),
        ('Qual a taxa de sucesso?', 'Usamos histórico local, qualidade do anúncio e acurácia de preço como fatores principais.'),
        ('Como acomodar visita à distância?', 'Organizamos visitas por data e, quando necessário, enviamos conteúdo audiovisual do imóvel.'),
    ],
}

city_context = {
    'santos': 'Santos tem orla valorizada, temporada forte e perfil de comprador que exige clareza na documentação e no plano de venda.',
    'guaruja': 'Guarujá combina veraneio, temporada e liquidez concentrada em Pitangueiras, Astúrias e Enseada.',
    'praia-grande': 'Praia Grande oferece oferta diversificada em Guilhermina, Ocian e Tupi, com alta procura por moradia e temporada.',
    'bertioga': 'Bertioga une natureza, alto padrão e acessos diferenciados; atenção a área de marinha e regulamentações locais.',
    'itanhaem': 'Itanhaém cresce em oferta acessível e ambiente familiar, com destaques em Cibratel e Jardim São Fernando.',
    'mongagua': 'Mongaguá cresce como opção acessível e tranquila, com destaque para Centro, Jardim São Paulo e Balneário.',
    'sao-vicente': 'São Vicente combina história, orla e oferta econômica a médio padrão em Centro, Gonzaguinha e Itararé.',
    'peruibe': 'Peruíbe se destaca por tranquilidade, segunda residência e natureza preservada em Centro, Jardim São Paulo e Balneário.',
    'caraguatatuba': 'Caraguatatuba tem temporada forte e diversificação de oferta em Centro, Jaguaribe e Prainha.',
    'ilhabela': 'Ilhabela tem perfil exclusivo e sazonalidade forte, com atenção a área de marinha e acesso por ferry-boat.',
    'sao-sebastiao': 'São Sebastião cresce em alto padrão e temporada, com destaque para Centro Histórico, Juquehy e Maresias.',
    'ubatuba': 'Ubatuba combina natureza e temporada, com oferta em Centro, Itaguá e São Lourenço e atenção a restrições ambientais.',
}

base = Path('servicos/cidade-servico')
updated = 0
for p in sorted(base.glob('*.html')):
    txt = p.read_text(encoding='utf-8', errors='ignore')
    stem = p.stem

    city_slug = None
    service_slug = None
    for c in city_context:
        if stem.startswith(c + '-'):
            city_slug = c
            service_slug = stem[len(c) + 1:]
            break
    if not city_slug or not service_slug:
        continue

    faqs = base_faq.get(service_slug, [])
    if not faqs:
        continue

    faq_md = '{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [\n'
    for i, (q, a) in enumerate(faqs):
        if i > 0:
            faq_md += ',\n'
        faq_md += '    {\n'
        faq_md += '      "@type": "Question",\n'
        faq_md += '      "name": "' + q + '",\n'
        faq_md += '      "acceptedAnswer": {\n'
        faq_md += '        "@type": "Answer",\n'
        faq_md += '        "text": "' + a + '"\n'
        faq_md += '      }\n'
        faq_md += '    }'
    faq_md += '\n  ]\n}'

    city_name = city_slug.replace('-', ' ').title()
    service_name = service_names.get(service_slug, service_slug.replace('-', ' ').title())
    faq_section = '\n    <section>\n      <h2>Perguntas frequentes</h2>\n      <ul>\n'
    for q, a in faqs:
        faq_section += '        <li><strong>' + q + '</strong><br>' + a + '</li>\n'
    faq_section += '      </ul>\n    </section>'

    if '<script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "Service",' in txt:
        insert_marker = '</script>\n\n<a id="skip-link"'
        insert_html = '</script>\n\n<script type="application/ld+json">\n' + faq_md + '\n</script>\n\n<a id="skip-link"'
        txt = txt.replace(insert_marker, insert_html, 1)

    if '<section>\n      <h2>Páginas relacionadas</h2>' in txt:
        related_marker = '<section>\n      <h2>Páginas relacionadas</h2>'
        related_replacement = faq_section + '\n\n    <section>\n      <h2>Páginas relacionadas</h2>'
        txt = txt.replace(related_marker, related_replacement, 1)
    elif '<section>\n      <h2>Por cidade</h2>' in txt:
        related_marker = '<section>\n      <h2>Por cidade</h2>'
        related_replacement = faq_section + '\n\n    <section>\n      <h2>Por cidade</h2>'
        txt = txt.replace(related_marker, related_replacement, 1)
    else:
        related_marker = '<section class="lead-form">'
        related_replacement = faq_section + '\n\n    <section class="lead-form">'
        txt = txt.replace(related_marker, related_replacement, 1)

    p.write_text(txt, encoding='utf-8')
    updated += 1

print('updated ' + str(updated) + ' service pages')
