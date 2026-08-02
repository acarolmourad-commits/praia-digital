#!/usr/bin/env python3
"""
add_faqs_remaining.py
Adiciona FAQPage JSON-LD nas páginas públicas restantes sem FAQ,
por diretórios alvo: raiz, blog/, servicos/ e litoral-prime-imoveis/.
"""
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

root_faqs = {
    'automacao-imobiliarias.html': [
        ('O que é automação imobiliária?', 'Ferramentas digitais para gestão de leads, follow-up automático, agendamento e nutrição de clientes.'),
        ('Como a automação ajuda na venda?', 'Respostas rápidas e follow-up consistente aumentam a conversão em até 3x.'),
        ('Preciso trocar meu CRM atual?', 'Não. Integramos com o que você já usa e unificamos o fluxo.'),
    ],
    'avaliacao-preco-imoveis.html': [
        ('Como funciona a avaliação de imóveis?', 'Análise digital com comparáveis de mercado, avaliação presencial opcional e relatório completo.'),
        ('Quanto tempo demora uma avaliação?', 'Em geral de 24 a 48 horas após a visita ou envio de dados do imóvel.'),
        ('A avaliação é automática?', 'Automática por dados de mercado, com possibilidade de revisão antes de enviar ao proprietário.'),
    ],
    'avaliacao-rapida-imovel.html': [
        ('Como funciona a avaliação rápida?', 'Análise digital com comparáveis locais e relatório em minutos.'),
        ('Quais dados são necessários?', 'Endereço, tipo, área e características principais do imóvel.'),
        ('Serve para temporada?', 'Sim. Ajustamos filtros para perfil de temporada ou moradia.'),
    ],
    'captacao-imoveis-litoral.html': [
        ('Como funciona a captação digital?', 'Divulgamos o imóvel em portais, redes sociais e WhatsApp com alcance qualificado.'),
        ('Quanto tempo para captar interessados?', 'Os primeiros contatos surgem em até 72 horas após a publicação.'),
        ('A captação atende temporada?', 'Sim. Campanhas por cidade e datas aumentam ocupação e antecipam reservas.'),
    ],
    'captura-leads.html': [
        ('Como capturar leads rapidamente?', 'Landing pages + formulário + WhatsApp com filtro de intenção em tempo real.'),
        ('Os leads são qualificados?', 'Sim. O fluxo valida interesse antes de chegar ao time comercial.'),
        ('Quanto tempo para implementar?', 'Setup em até 7 dias com página, integração e primeiro teste.'),
    ],
    'consultoria-transformacao-digital-imobiliarias.html': [
        ('Preciso de um projeto grande?', 'Não. Começamos por diagnóstico e evoluímos em módulos, sem interromper a operação.'),
        ('Quanto tempo leva o diagnóstico?', 'Cerca de 15 minutos de call + 5 dias para o roadmap.'),
        ('Funciona para equipe pequena?', 'Sim. O plano Starter cobre 1 módulo e setup básico para pequenos times.'),
    ],
    'descricao-imoveis-ia.html': [
        ('A descrição fica genérica?', 'Não. Cada texto é adaptado por cidade, perfil e canal, com tom e palavras-chave ajustáveis.'),
        ('Em quanto tempo fica pronto?', 'Segundos. O lote é gerado em massa para portais e redes sem bloqueio criativo.'),
        ('Funciona para temporada?', 'Sim. Templates específicos para alta temporada aumentam ocupação e cliques.'),
    ],
    'encontrar-imovel.html': [
        ('Como funciona a busca de imóveis?', 'Filtros por cidade, tipo, bairro e perfil; atendimento humano pelo WhatsApp.'),
        ('Vocês ajudam na negociação?', 'Sim. A equipe acompanha proposta, contrato e fechamento.'),
        ('Atendem temporada e moradia?', 'Sim. Há imóveis para temporada e para venda/moradia permanente.'),
    ],
    'imoveis.html': [
        ('Quais tipos de imóveis vocês oferecem?', 'Apartamentos, casas, coberturas, studios e terrenos no litoral de SP.'),
        ('Como encontrar um imóvel?', 'Use a busca por cidade ou WhatsApp para um atendimento personalizado.'),
        ('Os imóveis são próprios ou de clientes?', 'Trabalhamos com imóveis próprios, clientes e parceiros do litoral.'),
    ],
    'index.html': [
        ('Quais cidades são atendidas?', 'Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.'),
        ('Como entrar em contato?', 'Pelo WhatsApp no botão flutuante ou no formulário das páginas de serviço.'),
        ('Vocês trabalham com temporada?', 'Sim. Há imóveis e campanhas específicas para alta temporada no litoral.'),
    ],
    'investidores.html': [
        ('Quais oportunidades para investidores?', 'Imóveis com potencial de aluguel temporada, valorização e renda passiva no litoral.'),
        ('Como calcular o retorno?', 'Oferecemos análise de mercado, estimativa de ocupação e projeção de rentabilidade.'),
        ('Atendem investidores estrangeiros?', 'Sim. Há suporte para compra por estrangeiros e consultoria internacional.'),
    ],
    'planos-assinatura.html': [
        ('Posso mudar de plano depois?', 'Sim. Ajuste conforme a imobiliária crescer, sem migração complexa.'),
        ('Tem fidelidade?', 'Não. Mensal, com cancelamento sem multa a partir do 2º mês.'),
        ('O plano inclui implementação?', 'Starter inclui setup básico; Professional e Enterprise incluem onboarding.'),
    ],
    'planos-assinatura-profissionais.html': [
        ('Qual a diferença dos planos profissionais?', 'Maior volume de leads, automações avançadas e suporte prioritário.'),
        ('Posso testar antes?', 'Sim. Oferecemos período de teste e onboarding assistido.'),
        ('Como contratar?', 'Pelo WhatsApp, e-mail ou formulário na página de planos.'),
    ],
    'planos-proptech-2026.html': [
        ('Posso mudar de plano depois?', 'Sim. Ajuste conforme a imobiliária crescer, sem migração complexa.'),
        ('Tem fidelidade?', 'Não. Mensal, com cancelamento sem multa a partir do 2º mês.'),
        ('O plano inclui implementação?', 'Starter inclui setup básico; Professional e Enterprise incluem onboarding.'),
    ],
    'seo-local-bairros-litoral.html': [
        ('Em quanto tempo apareço no Google?', 'De 30 a 60 dias, dependendo da concorrência por cidade e bairro.'),
        ('Preciso de site próprio?', 'Não obrigatoriamente. Usamos páginas otimizadas e Google Business Profile para gerar visibilidade.'),
        ('Como medir o resultado?', 'Por impressões, cliques, posição média e leads vindos de busca local.'),
    ],
    'seo-local-imobiliarias.html': [
        ('Em quanto tempo apareço no Google?', 'De 30 a 60 dias, dependendo da concorrência por cidade e bairro.'),
        ('Preciso de site próprio?', 'Não obrigatoriamente. Usamos páginas otimizadas e Google Business Profile para gerar visibilidade.'),
        ('Como medir o resultado?', 'Por impressões, cliques, posição média e leads vindos de busca local.'),
    ],
    'servicos.html': [
        ('Quais serviços estão disponíveis?', 'Avaliação, captação, descrição com IA, consultoria proptech, automação e venda de imóvel.'),
        ('Posso contratar serviços separados?', 'Sim. Cada serviço pode ser contratado de forma modular.'),
        ('Como solicitar um serviço?', 'Pelo formulário na página ou diretamente no WhatsApp.'),
    ],
}

lp_faqs = {
    'cidades': [
        ('Quais bairros têm mais oferta?', 'Os bairros mais buscados estão destacados na página da cidade com oportunidades ativas.'),
        ('Como visitar imóveis na cidade?', 'Agende pelo WhatsApp com um consultor local para visita guiada.'),
        ('Atendem toda a cidade?', 'Sim. A cobertura inclui centro, orla e bairros residenciais.'),
    ],
    'servicos': [
        ('Como solicitar este serviço?', 'Preencha o formulário na página ou chame no WhatsApp para atendimento rápido.'),
        ('Quais cidades são atendidas?', 'Todo o litoral de SP: Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.'),
        ('Quanto tempo para iniciar?', 'Em até 24h após o contato, com briefing e início do atendimento.'),
    ],
    'docs': [
        ('Onde encontrar os guias?', 'Na seção docs/ com checklists, briefings e guias rápidos para corretores.'),
        ('Como usar o briefing diário?', 'Abra o arquivo docs/briefing-diario.html para ver as ações do dia.'),
        ('Os guias são atualizados?', 'Sim. Semanalmente com novos conteúdos e exemplos do litoral.'),
    ],
    'outreach': [
        ('O que é o outreach?', 'Acompanhamento de prospecção, desempenho e materiais de divulgação.'),
        ('Como ver o desempenho?', 'Acesse outreach/desempenho.html para métricas e tracker.'),
        ('Onde estão os posts?', 'Em outreach/posts-redes-sociais.html com conteúdo pronto para publicação.'),
    ],
    'leads': [
        ('Como capturar leads?', 'Use as páginas de leads com formulário + WhatsApp para qualificar interessados.'),
        ('Os leads são verificados?', 'Sim. O fluxo valida nome, telefone e interesse antes de enviar ao comercial.'),
        ('Quais canais de captura?', 'Site, WhatsApp, landing pages e redes sociais integradas.'),
    ],
    'blog': [
        ('Os artigos são atualizados?', 'Sim. Semanalmente com conteúdo sobre mercado, SEO e vendas no litoral.'),
        ('Como usar o blog?', 'Compartilhe artigos com proprietários e investidores para nutrição de leads.'),
        ('Tem guia de temporada?', 'Sim. Há conteúdo específico para alta temporada e aluguel por temporada.'),
    ],
}

generic = [
    ('Como solicitar mais informações?', 'Pelo WhatsApp ou formulário na página para atendimento rápido.'),
    ('Quais cidades são atendidas?', 'Todo o litoral de SP: Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente e Peruíbe.'),
    ('Quanto tempo para retorno?', 'Em até 24 horas após o contato, com atendimento humanizado.'),
]

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

def pick_faq(rel: Path, name: str):
    if rel.parent == BASE:
        key = name
        return root_faqs.get(key, generic)
    if rel.parts[0] == 'litoral-prime-imoveis':
        for segment in lp_faqs:
            if segment in rel.parts:
                return lp_faqs[segment]
        return generic
    if rel.parts[0] == 'blog':
        return lp_faqs['blog']
    if rel.parts[0] == 'servicos':
        return lp_faqs['servicos']
    return generic

targets = []
targets.append(BASE)
for d in ['blog', 'servicos', 'litoral-prime-imoveis']:
    p = BASE / d
    if p.exists():
        targets.append(p)

updated = 0
skipped = 0
errors = 0
for target in targets:
    for path in sorted(target.rglob('*.html')):
        rel = path.relative_to(BASE)
        name = path.name
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            errors += 1
            continue
        if 'FAQPage' in text:
            skipped += 1
            continue
        qas = pick_faq(rel, name)
        items = ','.join(item_template.format(question=q, answer=a) for q, a in qas)
        block = template.format(items=items)
        if '<head>' not in text:
            print('skip no head', rel)
            continue
        text = text.replace('<head>', '<head>\n' + block, 1)
        try:
            path.write_text(text, encoding='utf-8')
            print('updated', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
