import json, csv, os
from pathlib import Path
from datetime import date, timedelta

REPO = Path(r'C:/Users/Carolina/praia-digital')
QUIZ_JSON = REPO / 'outreach' / 'leads-site-capturados' / 'quiz-leads.json'
NURTURING_DIR = REPO / 'outreach' / 'nurturing'
NURTURING_DIR.mkdir(parents=True, exist_ok=True)
TODAY = date.today()

# Load leads
leads = []
if QUIZ_JSON.exists():
    try:
        leads = json.loads(QUIZ_JSON.read_text(encoding='utf-8'))
    except Exception:
        leads = []

# Perfil -> recommended tool
tool_map = {
    'captacao': 'Captura de leads por cidade',
    'atendimento': 'Assistente virtual 24/7',
    'fechamento': 'Avaliação de preço automática',
    'organizacao': 'Modelo de proposta de parceria'
}

# City -> SEO article
city_article_map = {
    'santos': 'santos-orla-gastronomia-passeios-2026-sp-2026-07-14.html',
    'guaruja': 'guaruja-ilha-panqueca-fim-semana-2026-sp-2026-07-14.html',
    'praia-grande': 'guia-completo-praia-grande-familia-2026-sp-2026-07-14.html',
    'ubatuba': 'ubatuba-trilhas-praias-guia-2026-sp-2026-07-14.html',
    'peruibe': 'peruibe-centro-historico-praias-2026-sp-2026-07-14.html',
    'sao vicente': 'sao-vicente-historico-monumentos-2026-sp-2026-07-14.html',
    'bertioga': 'bertioga-riviera-sao-francisco-guia-2026-sp-2026-07-14.html',
    'itanhaem': 'itanhaem-centro-antigo-lagoa-2026-sp-2026-07-14.html',
    'mongagua': 'mongagua-praias-familiares-2026-sp-2026-07-14.html',
    'cabo frio': 'cabo-frio-roteiro-casais-2026-sp-2026-07-14.html',
    'buzios': 'buzios-praias-famosas-guia-2026-sp-2026-07-14.html',
    'paraty': 'paraty-historico-ilhas-2026-rj-2026-07-14.html',
    'florianopolis': 'florianopolis-praias-guia-2026-sc-2026-07-14.html',
    'balneario camboriu': 'balneario-camboriu-compras-praia-2026-sc-2026-07-14.html',
    'outro': 'blog/seo-local-imobiliaria-litoral-paulista-2026.html'
}

# Sequence templates
templates = {
    0: {
        'subject': 'Seu diagnóstico Praia Digital está pronto',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nParabéns por completar o Diagnóstico Gratuito da Praia Digital!\n\nAnalisei suas respostas e preparei um plano personalizado para {l.get('cidade','sua cidade')}.\n\n👉 Ferramenta recomendada: {tool_map.get(l.get('q1',''), 'Ferramentas gratuitas')}\n👉 Artigo estratégico: {city_article_map.get(l.get('q3',''), 'blog/seo-local-imobiliaria-litoral-paulista-2026.html')}\n\nAcesse gratuitamente: https://praia.digital\n\nAbraço,\nCarolina Mourad\nCEO · Praia Digital"
    },
    2: {
        'subject': 'Artigo exclusivo para {cidade}',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nEm {l.get('cidade','sua cidade')}, imobiliárias que usam IA estão captando mais leads qualificados.\n\nArtigo recomendado: {city_article_map.get(l.get('q3',''), 'blog/seo-local-imobiliaria-litoral-paulista-2026.html')}\n\nQuer testar as ferramentas gratuitas? https://praia.digital\n\nCarolina\nPraia Digital"
    },
    4: {
        'subject': 'Case real: +40% leads em 30 dias',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nQuero compartilhar um case real: Barra Norte Imóveis (Guarujá)\n• +40% leads qualificados\n• -60% tempo de atendimento\n• 3x mais agendamentos\n\n👉 Ver case: https://acarolmourad-commits.github.io/praia-digital/blog/case-sucesso-barra-norte-imoveis-guaruja-2026.html\n\nResponda QUERO para aplicar o mesmo modelo.\n\nCarolina Mourad\nCEO · Praia Digital"
    },
    7: {
        'subject': 'Ferramenta gratuita recomendada para você',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nHoje quero dar acesso a uma ferramenta gratuita que pode transformar sua operação:\n\n🎯 {tool_map.get(l.get('q1',''), 'Ferramentas gratuitas')}\n\n👉 Acesse: https://praia.digital\n\nAbraço,\nCarolina\nPraia Digital"
    },
    14: {
        'subject': 'Proposta personalizada para sua imobiliária',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nDepois de 2 semanas compartilhando conteúdo, preparei uma proposta personalizada:\n\n🎯 Objetivo: {l.get('q5','')}\n📍 Cidade: {l.get('cidade','')}\n💰 30 dias grátis, depois R$ 297/mês\n\nResultado esperado: +40% leads qualificados.\n\nQuer agendar uma call de 15 minutos?\n(11) 95434-6288\n\nCarolina Mourad\nCEO · Praia Digital"
    },
    21: {
        'subject': 'Última chance: 30 dias grátis',
        'body': lambda l: f"Olá, {l.get('nome','')}!\n\nEsta é minha última tentativa. Não quero ser insistente.\n\nOferta especial válida até {(TODAY + timedelta(days=7)).strftime('%d/%m/%Y')}:\n✅ 30 dias grátis do plano Professional\n✅ Onboarding personalizado\n✅ Suporte prioritário\n\n👉 Responda SIM que eu ativo agora\n\nSe não for agora, sem problemas. Ferramentas gratuitas em https://praia.digital\n\nSucesso em {l.get('cidade','')}! 🏖️\n\nCarolina Mourad\nCEO · Praia Digital"
    }
}

created = []
for lead in leads:
    nome = lead.get('nome', '')
    email = lead.get('email', '')
    if not nome or not email:
        continue
    
    # Parse registration date
    reg_date = None
    raw_date = lead.get('data', '')
    if raw_date:
        try:
            reg_date = date.fromisoformat(raw_date.split('T')[0])
        except Exception:
            reg_date = TODAY
    
    for day_offset, template in templates.items():
        send_date = reg_date + timedelta(days=day_offset) if reg_date else TODAY
        if send_date > TODAY + timedelta(days=7):
            continue
        subject = template['subject'].replace('{cidade}', lead.get('cidade', 'sua cidade'))
        body = template['body'](lead)
        
        path = NURTURING_DIR / f"{email.replace('@','_').replace('.','_')}_day{day_offset}_{send_date}.txt"
        if path.exists():
            continue
        path.write_text(f"Subject: {subject}\nTo: {email}\nDate: {send_date.isoformat()}\n\n{body}", encoding='utf-8')
        created.append(str(path))

print(f"Criados {len(created)} e-mails de nurturing")
for p in created[:10]:
    print("-", Path(p).name)
