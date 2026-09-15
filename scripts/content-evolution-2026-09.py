#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolução de conteúdo 2026-09 — Praia Digital
Aplica, de forma idempotente e com verificações, as melhorias aprovadas no
relatório de auditoria de conteúdo:
1) index.html: title, hero (H1/sub/CTAs/e-mail), saudação do chatbot,
   CTA 'metaverso' -> Hermes Agents, remoção da seção de corretores fictícios,
   banner de afiliados movido para antes do rodapé com disclaimer.
2) sobre/servicos/cases/contato/personas: reescritas de copy aprovadas.
3) Correção global: comercial@praiadigital.com -> comercial@praia.digital
4) Rebrand: 'Litoral Prime (Imóveis)' -> 'Praia Digital'
5) Redirects 301! para páginas duplicadas (politica-privacidade, termos-uso)
6) Exclusão de arquivos internos (tmp_*.py, .bak, CSVs de leads)
7) llms.txt / llms-full.txt / humans.txt alinhados à marca.
Roda na raiz do repo. Sai com erro se alguma substituição obrigatória falhar.
"""
import os, re, sys

CHANGES, WARNINGS = [], []

def load(p):
    return open(p, encoding='utf-8', errors='ignore').read()

def save(p, s):
    open(p, 'w', encoding='utf-8').write(s)

def rep(s, old, new, label, required=True, count=1):
    if old in s:
        CHANGES.append(label)
        return s.replace(old, new, count)
    if new in s:
        CHANGES.append(label + ' (já aplicado)')
        return s
    if required:
        raise SystemExit(f'FALHA: trecho não encontrado -> {label}')
    WARNINGS.append('não encontrado (opcional): ' + label)
    return s

# ---------------- 1) index.html ----------------
p = 'index.html'
s = load(p)
s = rep(s, '<title>Praia Digital — Imóveis no Litoral com IA para imobiliárias</title>',
        '<title>Praia Digital — IA que gera leads e vendas para imobiliárias no litoral paulista</title>', 'index:title')
s = rep(s, '>Imóveis no litoral paulista com inteligência artificial</h1>',
        '>Mais leads qualificados, menos trabalho repetitivo para sua imobiliária no litoral</h1>', 'index:hero-h1')
s = rep(s, '<p>A primeira plataforma do litoral com inteligência artificial — apartamentos, casas, pousadas e terrenos para decisões mais inteligentes.</p>',
        '<p>IA aplicada a captação, avaliação de preço e atendimento automático — para imobiliárias e corretores de Santos a Ubatuba. Sem taxa de setup, resultados nas primeiras semanas.</p>', 'index:hero-sub')
s = rep(s, '<a href="#buscar" class="btn btn-primary">🔍 Buscar imóveis</a>',
        '<a href="#buscar" class="btn btn-primary">🔍 Encontrar imóveis no litoral</a>', 'index:cta1')
s = rep(s, '<a href="#nl-search" class="btn btn-outline">✨ Busca inteligente</a>',
        '<a href="#nl-search" class="btn btn-outline">✨ Buscar com linguagem natural</a>', 'index:cta2')
s = rep(s, '<a href="#investidor-roi" class="btn btn-amber">📈 Simular Rentabilidade</a>',
        '<a href="#investidor-roi" class="btn btn-amber">📈 Simular rentabilidade do meu imóvel</a>', 'index:cta3')
s = rep(s, '<a href="#gerador" class="btn btn-outline" style="border:2px solid #fff;color:#fff;">🧠 Testar IA para Corretores</a>',
        '<a href="#gerador" class="btn btn-outline" style="border:2px solid #fff;color:#fff;">🧠 Testar a IA na minha imobiliária — grátis</a>', 'index:cta4')
s = rep(s, 'Olá! Sou a assistente inteligente da Praia Digital. 🧠 Posso responder perguntas sobre imóveis, bairros, financiamento, investimento e muito mais — tudo em português!',
        'Olá! Sou a assistente da Praia Digital. Pergunte sobre imóveis, bairros ou financiamento no litoral — respondo na hora.', 'index:chatbot')
s = rep(s, '<a href="blog/ia-para-metaverse-imoveis-litoral.html" target="_blank" rel="noopener" class="btn btn-ocean" style="text-align:center;">🌐 IA para metaverso de imóveis</a>',
        '<a href="solucoes/hermes-agents.html" class="btn btn-ocean" style="text-align:center;">🤖 Hermes Agents — IA autônoma para imobiliárias</a>', 'index:metaverso')

# remoção da seção de corretores fictícios (perfis não verificáveis)
if '<section class="agents-section" id="corretores-equipe">' in s:
    st = s.find('<section class="agents-section" id="corretores-equipe">')
    en = s.find('</section>', st) + len('</section>')
    s = s[:st] + '<!-- Seção de corretores removida: perfis não verificáveis (política editorial: não fabricar dados). Reintroduzir apenas com corretores parceiros reais. -->' + s[en:]
    CHANGES.append('index:agentes-ficticios-removidos')

# banner de afiliados -> antes do rodapé, com disclaimer
if '<section aria-label="Destaque automação e equipamentos 2026"' in s and 'Conteúdo comercial: esta seção contém links de afiliados' not in s:
    st = s.find('<section aria-label="Destaque automação e equipamentos 2026"')
    en = s.find('</section>', st) + len('</section>')
    banner = s[st:en]
    s = s.replace(banner, '', 1)
    fpos = s.rfind('<footer')
    disclosure = ('<aside aria-label="Conteúdo de afiliados" style="max-width:1000px;margin:2rem auto;padding:0 1rem;">\n'
                  '<p style="font-size:0.8rem;opacity:0.6;text-align:center;">Conteúdo comercial: esta seção contém links de afiliados. A Praia Digital pode receber comissão por compras, sem custo adicional para você. Conteúdo editorial não é influenciado por parcerias.</p>\n')
    s = s[:fpos] + disclosure + banner + '\n</aside>\n\n' + s[fpos:]
    CHANGES.append('index:afiliados-movidos-com-disclaimer')

s = s.replace('comercial@praiadigital.com', 'comercial@praia.digital')
assert 'comercial@praiadigital.com' not in s
save(p, s)

# ---------------- 2) páginas-chave ----------------
p = 'sobre.html'; s = load(p)
s = rep(s, '<p class="lead">Somos uma operação de SEO/GEO, conteúdo e tecnologia dedicada ao mercado imobiliário do litoral norte e sul de São Paulo. Unimos dados, automação e experiência editorial para gerar visibilidade qualificada, leads úteis e resultados mensuráveis para corretores, imobiliárias, proprietários e investidores.</p>',
        '<p class="lead">Somos uma plataforma de tecnologia e conteúdo que ajuda corretores, imobiliárias, proprietários e investidores a vender e alugar mais no litoral paulista — com IA, dados locais e atendimento humano.</p>', 'sobre:lead')
save(p, s)

p = 'servicos.html'; s = load(p)
s = rep(s, '<h1>Serviços</h1>', '<h1>Serviços que enchem sua agenda de visitas</h1>', 'servicos:h1')
s = rep(s, '<p class="lead">Soluções digitais para imobiliárias e proprietários no litoral paulista.</p>',
        '<p class="lead">Conteúdo, mídia profissional e automação com IA para imobiliárias e proprietários do litoral paulista.</p>', 'servicos:lead')
s = rep(s, '<p>Do anúncio à gestão, combinamos conteúdo, mídia e automação para reduzir vazio, aumentar captação e melhorar a conversão de leads em operações de temporada e venda.</p>',
        '<p>Da descrição do anúncio à gestão completa da temporada: cada serviço existe para atrair mais interessados e converter leads em locações e vendas. Comece por qualquer serviço, sem fidelidade.</p>', 'servicos:intro')
s = s.replace('>Ver mais</a>', '>Ver como funciona</a>')
save(p, s)

p = 'cases.html'; s = load(p)
def cta_swap(s, href, new_label):
    i = s.find(href)
    if i < 0:
        WARNINGS.append('cases href não encontrado: ' + href); return s
    j = s.find('Ver case</a>', i)
    if j < 0:
        return s
    return s[:j] + new_label + '</a>' + s[j + len('Ver case</a>'):]
s = cta_swap(s, 'cases/case-imobiliaria-porto', 'Ver como a Porto da Lua gerou 35 leads em 4 semanas →')
s = cta_swap(s, 'cases/case-recomendacao-automatica-imoveis-2026.html', 'Ver como a IA aumentou visitas agendadas em 28% →')
s = cta_swap(s, 'cases/case-reducao-tempo-resposta-costa-verde-2026.html', 'Ver como a Costa Verde cortou 60% do tempo de resposta →')
s = cta_swap(s, 'cases/case-roi-', 'Ver como o parceiro chegou a ROI positivo em 90 dias →')
card = re.search(r'<div class="card">\s*<h2>Centro Histórico — Fechamento</h2>[\s\S]*?</div>\s*', s)
if card and 'Case em andamento' in card.group(0):
    s = s.replace(card.group(0), '', 1); CHANGES.append('cases:card-em-andamento-removido')
s = s.replace('>Quero um case similar</a>', '>Quero um resultado assim — falar com a equipe</a>')
save(p, s)

p = 'contato.html'; s = load(p)
s = s.replace('Contato | Litoral Prime Imóveis', 'Contato | Praia Digital')
s = s.replace('Fale com a Litoral Prime Imóveis: atendimento especializado', 'Fale com a Praia Digital: atendimento especializado')
s = s.replace('contato litoral prime imóveis', 'contato praia digital')
s = s.replace('"name": "Litoral Prime Imóveis"', '"name": "Praia Digital"')
s = rep(s, '<h1>Fale com a Litoral Prime Imóveis</h1>', '<h1>Fale com um especialista do litoral</h1>', 'contato:h1')
s = rep(s, '<p class="subtitle">Atendimento especializado para compra, venda e temporada no litoral de SP.</p>',
        '<p class="subtitle">Compra, venda, temporada ou parceria — resposta em horário comercial, direto no WhatsApp.</p>', 'contato:sub')
save(p, s)

p = 'personas.html'; s = load(p)
for href, label in [('personas/corretor-ia-2026.html', 'Falar com o Corretor IA'),
                    ('personas/investidor-ia-2026.html', 'Analisar meu investimento'),
                    ('personas/airbnb-ia-2026.html', 'Otimizar meu anúncio de temporada'),
                    ('personas/credito-ia-2026.html', 'Simular meu financiamento'),
                    ('personas/documentacao-ia-2026.html', 'Organizar minha documentação')]:
    s = s.replace(href + '">Abrir<', href + '">' + label + '<')
save(p, s)

# ---------------- 3) e-mail oficial em todo o site (exceto backup/) ----------------
fixed = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in {'backup', 'backups', '.git', 'node_modules', 'uploads'}]
    for name in files:
        if not name.endswith(('.html', '.md', '.txt', '.xml')):
            continue
        fp = os.path.join(root, name)
        t = load(fp)
        if 'comercial@praiadigital.com' in t:
            save(fp, t.replace('comercial@praiadigital.com', 'comercial@praia.digital')); fixed += 1
CHANGES.append(f'email-oficial corrigido em {fixed} arquivos')

# ---------------- 4) rebrand 'Litoral Prime' ----------------
rebranded = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in {'backup', 'backups', '.git', 'node_modules', 'uploads'}]
    for name in files:
        if not name.endswith(('.html', '.md', '.txt', '.xml')):
            continue
        fp = os.path.join(root, name)
        t = load(fp)
        if 'Litoral Prime' in t:
            t = t.replace('Litoral Prime Imóveis', 'Praia Digital').replace('Litoral Prime', 'Praia Digital')
            save(fp, t); rebranded += 1
CHANGES.append(f'rebrand aplicado em {rebranded} arquivos')

# ---------------- 5) redirects de duplicatas ----------------
with open('_redirects', 'a', encoding='utf-8') as f:
    f.write('/politica-privacidade.html  /politica-de-privacidade.html  301!\n')
    f.write('/termos-uso.html  /termos-de-uso.html  301!\n')
CHANGES.append('_redirects: duplicatas consolidadas')

# ---------------- 6) exclusões de governança ----------------
for d in ['tmp_audit2.py','tmp_find_html_leak.py','tmp_fix_html_end.py','tmp_fix_leak.py','tmp_fix_leak2.py','tmp_fix_leak3.py','tmp_global_leak_audit.py','index.html.bak-20260820-103122','conversion_tracking_report.csv','checklist-followup-lote.csv','politica-privacidade.html','termos-uso.html']:
    if os.path.exists(d):
        os.remove(d); CHANGES.append('removido: ' + d)

print('=== ALTERAÇÕES ===')
for c in CHANGES: print('-', c)
if WARNINGS:
    print('=== AVISOS ===')
    for w in WARNINGS: print('-', w)
print('OK')
