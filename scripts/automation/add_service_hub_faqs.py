#!/usr/bin/env python3
"""
add_service_hub_faqs.py
Insere FAQPage JSON-LD nas páginas de serviço/hub que ainda não possuem.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

faq_map = {
    'litoral-prime-imoveis/servicos/automacao.html': [
        ('O que é automação imobiliária?', 'Ferramentas digitais para gestão de leads, follow-up automático, agendamento e nutrição de clientes.'),
        ('Como a automação ajuda na venda?', 'Respostas rápidas e follow-up consistente aumentam a conversão em até 3x.'),
        ('Preciso trocar meu CRM atual?', 'Não. Integramos com o que você já usa e unificamos o fluxo.'),
    ],
    'litoral-prime-imoveis/servicos/avaliacao.html': [
        ('Como funciona a avaliação de imóveis?', 'Análise digital com comparáveis de mercado, avaliação presencial opcional e relatório completo.'),
        ('Quanto tempo demora uma avaliação?', 'Em geral de 24 a 48 horas após a visita ou envio de dados do imóvel.'),
        ('A avaliação é automática?', 'Automática por dados de mercado, com possibilidade de revisão antes de enviar ao proprietário.'),
    ],
    'litoral-prime-imoveis/servicos/captacao.html': [
        ('Como funciona a captação digital?', 'Divulgamos o imóvel em portais, redes sociais e WhatsApp com alcance qualificado.'),
        ('Quanto tempo para captar interessados?', 'Os primeiros contatos surgem em até 72 horas após a publicação.'),
        ('A captação atende temporada?', 'Sim. Campanhas por cidade e datas aumentam ocupação e antecipam reservas.'),
    ],
    'litoral-prime-imoveis/servicos/captura-rapida.html': [
        ('Como capturar leads rapidamente?', 'Landing pages + formulário + WhatsApp com filtro de intenção em tempo real.'),
        ('Os leads são qualificados?', 'Sim. O fluxo valida interesse antes de chegar ao time comercial.'),
        ('Quanto tempo para implementar?', 'Setup em até 7 dias com página, integração e primeiro teste.'),
    ],
    'litoral-prime-imoveis/servicos/checklist-leads.html': [
        ('O que é o checklist de leads?', 'Um guia prático para qualificar, priorizar e converter leads imobiliários sem perder oportunidades.'),
        ('Serve para qualificar leads de temporada?', 'Sim. Inclui filtros por perfil: venda, locação ou temporada.'),
        ('Como usar na prática?', 'Baixe, aplique no atendimento e use como roteiro de follow-up pelo WhatsApp.'),
    ],
    'litoral-prime-imoveis/servicos/consulta-rapida.html': [
        ('Como funciona a consulta rápida?', 'Atendimento direto pelo WhatsApp com respostas em minutos para avaliação, captação ou visita.'),
        ('Quais cidades são atendidas?', 'Todo o litoral de SP: Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.'),
        ('Preciso de cadastro prévio?', 'Não. Basta abrir o atendimento e enviar sua necessidade.'),
    ],
    'litoral-prime-imoveis/servicos/consultoria-proptech.html': [
        ('O que é consultoria proptech?', 'Assessoria em tecnologia imobiliária: automação, CRM, marketing digital e operações.'),
        ('Para quem é a consultoria?', 'Para corretores, imobiliárias e investidores que querem digitalizar operações.'),
        ('Como medir o retorno?', 'Por indicadores: redução de retrabalho, aumento de leads qualificados e conversão.'),
    ],
    'litoral-prime-imoveis/servicos/descricao-ia.html': [
        ('A descrição fica genérica?', 'Não. Cada texto é adaptado por cidade, perfil e canal, com tom e palavras-chave ajustáveis.'),
        ('Em quanto tempo fica pronto?', 'Segundos. O lote é gerado em massa para portais e redes sem bloqueio criativo.'),
        ('Funciona para temporada?', 'Sim. Templates específicos para alta temporada aumentam ocupação e cliques.'),
    ],
    'litoral-prime-imoveis/servicos/quero-vender-imovel-litoral.html': [
        ('Como funciona a venda de imóvel?', 'Avaliação, captação digital, divulgação qualificada, negociação e suporte jurídico.'),
        ('Quanto tempo demora para vender?', 'Varia conforme mercado; com nossa estratégia costuma ser de 30 a 90 dias.'),
        ('Quais cidades são atendidas?', 'Todas as 8 cidades do litoral de SP onde atuamos.'),
    ],
    'litoral-prime-imoveis/servicos/template-cidade-servico.html': [
        ('Este template é uma página final?', 'Não. É base para páginas de serviço por cidade; personalize título, descrição e CTA.'),
        ('Posso usar para outras cidades?', 'Sim. Basta trocar cidade e ajustar links internos.'),
        ('Precisa de script?', 'Não. Funciona como HTML estático com JSON-LD opcional.'),
    ],
    'litoral-prime-imoveis/servicos/venda-imovel.html': [
        ('Quais serviços incluem venda de imóvel?', 'Avaliação, fotografia, divulgação, follow-up e suporte jurídico completo.'),
        ('Como funciona o follow-up?', 'Atendimento pelo WhatsApp com atualizações periódicas até a escritura.'),
        ('Atendem qual região?', 'Todo o litoral de SP: 8 cidades cobertas pela Litoral Prime.'),
    ],
    'litoral-prime-imoveis/imoveis.html': [
        ('Quais tipos de imóveis vocês oferecem?', 'Apartamentos, casas, coberturas, studios e terrenos no litoral de SP.'),
        ('Como encontrar um imóvel?', 'Use a busca por cidade ou WhatsApp para um atendimento personalizado.'),
        ('Os imóveis são próprios ou de clientes?', 'Trabalhamos com imóveis próprios, clientes e parceiros do litoral.'),
    ],
    'litoral-prime-imoveis/servicos.html': [
        ('Quais serviços estão disponíveis?', 'Avaliação, captação, descrição com IA, consultoria proptech, automação e venda de imóvel.'),
        ('Posso contratar serviços separados?', 'Sim. Cada serviço pode ser contratado de forma modular.'),
        ('Como solicitar um serviço?', 'Pelo formulário na página ou diretamente no WhatsApp.'),
    ],
    'litoral-prime-imoveis/encontrar-imovel.html': [
        ('Como funciona a busca de imóveis?', 'Filtros por cidade, tipo, bairro e perfil; atendimento humano pelo WhatsApp.'),
        ('Vocês ajudam na negociação?', 'Sim. A equipe acompanha proposta, contrato e fechamento.'),
        ('Atendem temporada e moradia?', 'Sim. Há imóveis para temporada e para venda/moradia permanente.'),
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
