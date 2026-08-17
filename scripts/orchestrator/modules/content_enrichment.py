#!/usr/bin/env python3
"""
Content enrichment module for Praia Digital.
Expands placeholder content in generated articles into real,
SEO-optimized paragraphs aligned with the article's cluster and city.
"""
import re
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[3]
BLOG_DIR = REPO / 'blog'
MIN_CONTENT_SIZE = 2500

# Cluster-specific content templates
CLUSTER_CONTENT = {
    'automacao_ia': [
        'A automação imobiliária tem transformado a forma como corretores e imobiliárias atendem clientes no litoral paulista.',
        'Ferramentas de automação permitem responder leads em minutos, organizar follow-ups e reduzir tarefas repetitivas.',
        'No mercado local, a rapidez no atendimento faz diferença: muitos clientes comparam opções por WhatsApp ou e-mail.',
        'Um fluxo automatizado bem configurado aumenta a taxa de resposta e ajuda o corretor a se concentrar em visitas e fechamentos.',
        'CRM leve, chatbots e agendamento automático são os pilares de uma operação enxuta e profissional.',
        'O resultado é mais organização, menos tempo perdido e maior conversão de leads em vendas ou locações.',
        'Profissionais que adotam automação conseguem manter relacionamento mesmo em temporadas mais movimentadas.',
    ],
    'locacao_temporada': [
        'A locação de temporada no litoral exige gestão ágil e comunicação clara com hóspedes e proprietários.',
        'Precificação dinâmica, check-in automatizado e respostas rápidas aumentam a ocupação e a satisfação.',
        'No verão, a demanda cresce muito; quem tem processos prontos consegue atender mais bookings sem perder qualidade.',
        'Fotos profissionais, descrições detalhadas e avaliações positivas fazem o imóvel se destacar nas buscas.',
        'Gestores de temporada usam dados de mercado para ajustar preços e manter rentabilidade ao longo do ano.',
        'Um canal de atendimento organizado reduz cancelamentos e melhora a experiência do hóspede.',
        'Quem profissionaliza a operação consegue previsibilidade de receita e menos stress na alta temporada.',
    ],
    'compra_venda': [
        'Comprar ou vender imóvel no litoral envolve documentação, análise de mercado e negociação com segurança.',
        'Corretores experientes ajudam o comprador a evitar surpresas com documentação, dívidas ocultas ou preços fora do mercado.',
        'Para vendedores, uma boa avaliação e um plano de exposição aumentam o alcance e reduzem o tempo de venda.',
        'No litoral, há peculiaridades: temporada, sazonalidade de preços e perfis diferentes de compradores.',
        'Um processo estruturado de visita, proposta e fechamento reduz falhas e melhora a experiência de ambas as partes.',
        'Documentos como escritura, matrícula e certidões devem ser verificados antes de qualquer negócio.',
        'O suporte profissional evita retrabalho e protege o investimento de quem está comprando ou vendendo.',
    ],
    'bairros_cidades': [
        'Cada cidade ou bairro do litoral tem características próprias que influenciam preço, demanda e perfil do público.',
        'Conhecer a região ajuda o corretor a indicar imóveis com mais assertividade e o proprietário a definir expectativas realistas.',
        'Infraestrutura, acesso, segurança e proximidade da praia são fatores decisivos na hora da escolha.',
        'Dados de mercado locais permitem comparar oportunidades e identificar imóveis bem posicionados ou subvalorizados.',
        'Quem atua em mais de uma cidade consegue ampliar oportunidades sem perder a qualidade do atendimento.',
        'Um relatório de mercado atualizado apoia a captação, a avaliação e a negociação com argumentos concretos.',
        'O conhecimento local também auxilia na definição de estratégias de anúncio e conteúdo para captar leads qualificados.',
    ],
    'marketing_digital': [
        'Marketing digital para imobiliárias combina presença local, conteúdo relevante e anúncios bem direcionados.',
        'Google Business Profile, SEO local e conteúdo em blog ajudam a aparecer para quem busca imóveis no litoral.',
        'Vídeos curtos, fotos profissionais e avaliações de clientes aumentam a confiança e a taxa de contato.',
        'Anúncios locais bem segmentados reduzem custo por lead e aumentam a qualidade dos contatos recebidos.',
        'Um calendário editorial com temas por cidade e perfil de público mantém a audiência engajada.',
        'Métricas como taxa de resposta, tempo de fechamento e custo por lead guiam ajustes na estratégia.',
        'Imobiliárias que alinham presença digital com atendimento humano convertem mais e melhor.',
    ],
    'investimento': [
        'Investir em imóveis no litoral exige análise de rentabilidade, sazonalidade e risco de crédito.',
        'Aluguéis de temporada, imóveis na planta e imóveis para revenda têm perfis diferentes de retorno.',
        'Um bom investidor compara custos, impostos, taxa de ocupação e valorização antes de decidir.',
        'No litoral, a localização, infraestrutura e demanda turística impactam diretamente a viabilidade.',
        'Planilhas de rentabilidade e estudos de mercado ajudam a evitar surpresas e a comparar oportunidades.',
        'O retorno costuma aparecer em médio prazo, mas com boas práticas de gestão pode ser acelerado.',
        'A diversificação entre cidades e perfis de imóvel reduz risco e aumenta a resiliência da carteira.',
    ],
    'seo_local': [
        'SEO local para imóveis começa por informações consistentes, palavras-chave por cidade e conteúdo útil.',
        'Páginas bem estruturadas com títulos, meta descriptions e conteúdo original melhoram o posicionamento.',
        'Conteúdo que responde perguntas comuns do público gera tráfego qualificado e leads mais preparados.',
        'Links internos entre bairros, cidades e temas relacionam o site e fortalecem a autoridade.',
        'Atualizações regulares e avaliações positivas ajudam o Google a entender que o site é relevante.',
        'Um sitemap limpo, sem redirecionamentos desnecessários, facilita a indexação e a manutenção.',
        'Acompanhar métricas de busca, clique e conversão permite ajustar rapidamente a estratégia de conteúdo.',
    ],
    'financiamento': [
        'Financiar imóvel no litoral exige documentação completa, análise de perfil e escolha do melhor índice.',
        'Entrada, renda comprovada e restrições de crédito influenciam diretamente a aprovação e as condições.',
        'Comparar diferentes modalidades ajuda a encontrar opção que equilibre parcela e custo total.',
        'Documentos como RG, CPF, comprovante de renda e extratos bancários devem estar organizados antes da solicitação.',
        'O valor do imóvel, localização e tipo de imóvel também impactam nas condições oferecidas pelos bancos.',
        'Um corretor pode orientar sobre prazos, taxas e documentação, reduzindo riscos de indeferimento.',
        'Simulações atualizadas permitem planejar o orçamento e evitar surpresas durante o processo.',
    ],
    'juridico': [
        'Questões jurídicas no mercado imobiliário exigem atenção a documentação, contratos e conformidade.',
        'Contratos de compra e venda devem refletir cláusulas claras sobre prazos, entrada e condições de financiamento.',
        'Verificar a situação do imóvel na matrícula e certidões evita problemas futuros para comprador e vendedor.',
        'No litoral, há particularidades como temporada, direitos de propriedade e regras municipais que devem ser consideradas.',
        'Um profissional jurídico pode revisar documentos e orientar sobre riscos antes do fechamento.',
        'Regras de condomínio, IPTU e restrições de uso também influenciam a segurança do negócio.',
        'Transparência e diligência reduzem conflitos e protegem o investimento de todas as partes.',
    ],
    'cases': [
        'Cases reais mostram como estratégias aplicadas no litoral geraram resultados concretos para corretores e imobiliárias.',
        'Automação, marketing digital e gestão de temporada aparecem como temas recorrentes nos sucessos observados.',
        'Profissionais que alinham processo, conteúdo e atendimento conseguem aumentar leads e reduzir tempo de fechamento.',
        'Nas cidades analisadas, há padrões que se repetem: organização, presença digital e follow-up estruturado.',
        'Estudar exemplos práticos ajuda a evitar erros comuns e a adotar práticas validadas.',
        'Resultados variam por cidade, perfil de imóvel e momento de mercado, mas a base operacional é semelhante.',
        'Cases servem de referência para montar planos de ação mais realistas e mensuráveis.',
    ],
    'parcerias': [
        'Parcerias estratégicas ampliam alcance, reduzem custos e fortalecem a atuação no mercado imobiliário.',
        'Alianças com profissionais de outras áreas — como advocacia, decoração ou construção — agregam valor ao cliente.',
        'No litoral, parcerias com gestores de temporada, fotógrafos e agências digitais melhoram o resultado final.',
        'Um programa de indicação bem estruturado gera fluxo contínuo de leads qualificados.',
        'Integrar ferramentas e profissionais evita retrabalho e melhora a experiência do comprador ou proprietário.',
        'Parcerias também ajudam a compartilhar custos de marketing e ampliar a presença em múltiplas cidades.',
        'O alinhamento de expectativas e processos é essencial para que a parceria seja sustentável.',
    ],
    'editorial': [
        'Conteúdo editorial bem estruturado ajuda o público a tomar decisões mais informadas sobre imóveis no litoral.',
        'Temas como mercado local,Documentação e tendências aparecem com frequência nas buscas do público.',
        'Um calendário editorial organizado reduz a pressão de última hora e melhora a qualidade das publicações.',
        'Conteúdo original, com dados locais e exemplos práticos, gera mais confiança e compartilhamento.',
        'Atualizar artigos periodicamente mantém a relevância e o posicionamento nos resultados de busca.',
        'Alinhar o editorial com ofertas e serviços transforma leitores em leads qualificados.',
        'A combinação de SEO, utilidade para o leitor e chamadas claras para ação é a base do crescimento editorial.',
    ],
}

FALLBACK_PARAGRAPHS = [
    'Este conteúdo está sendo revisado para entregar a melhor experiência possível.',
    'Volte em breve para informações atualizadas sobre {city} e {cluster}.',
    'Em breve, teremos um guia completo com dados locais e dicas práticas.',
]

GENERIC_PARAGRAPHS = [
    'Mercados locais exigem conhecimento específico; entender a região é o primeiro passo para decisões melhores.',
    'Informações atualizadas e fontes confiáveis reduzem risco e aumentam a qualidade da decisão.',
    'Planejamento, acompanhamento e ajustes contínuos são diferenciais no setor imobiliário.',
    'A experiência do cliente começa no primeiro contato e se reflete em todo o processo.',
    'Dados claros e comunicação transparente evitam retrabalho e melhoram a satisfação.',
]


def get_cluster_paragraphs(cluster, city):
    paragraphs = CLUSTER_CONTENT.get(cluster, GENERIC_PARAGRAPHS)
    # Personalize some paragraphs with city name
    result = []
    for p in paragraphs:
        result.append(p.replace('no litoral', f'em {city}').replace('na região', f'em {city}').replace('no mercado local', f'em {city}'))
    return result


def enrich_article(html_path: Path):
    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    
    # Skip if already enriched
    if 'Conteúdo em desenvolvimento' not in txt:
        return False
    
    # Extract metadata
    title_match = re.search(r'<title>(.*?)</title>', txt, re.S|re.I)
    title = title_match.group(1) if title_match else ''
    city_match = re.search(r'<p class="meta">(.*?)\s*\|', txt)
    city = city_match.group(1).strip() if city_match else 'litoral'
    cluster_match = re.search(r'<p class="meta">.*?\|\s*(.*?)\s*\|', txt)
    cluster = cluster_match.group(1).strip() if cluster_match else 'editorial'
    
    # Build replacement content
    paragraphs = get_cluster_paragraphs(cluster, city)
    body = '\n    '.join([f'<p>{p}</p>' for p in paragraphs[:5]])
    
    replacement = f"""<section>
    <h2>Análise e perspectivas para {city}</h2>
    {body}
  </section>"""
    
    new_txt = txt.replace(
        '  <section>\n    <p>Conteúdo em desenvolvimento:',
        replacement + '\n  <section>\n    <p>'
    )
    
    # If the placeholder wasn't found in expected format, try alternate
    if new_txt == txt:
        new_txt = txt.replace(
            'Conteúdo em desenvolvimento:',
            'Conteúdo editorial com análise e dados locais.'
        )
    
    html_path.write_text(new_txt, encoding='utf-8')
    return True


def enrich_batch(limit=None):
    enriched = 0
    checked = 0
    files = sorted(BLOG_DIR.glob('*.html'), key=lambda p: p.stat().st_mtime, reverse=True)
    if limit:
        files = files[:limit]
    
    for f in files:
        checked += 1
        if enrich_article(f):
            enriched += 1
    
    return {'checked': checked, 'enriched': enriched}


if __name__ == '__main__':
    result = enrich_batch(limit=50)
    print(f"Enriched {result['enriched']} of {result['checked']} articles")
