from pathlib import Path

repo = Path('.')
out_dir = repo/'cidades-expansao'
out_dir.mkdir(exist_ok=True)

base = 'https://acarolmourad-commits.github.io/praia-digital'

cities = {
    'balneario-camboriu.html': {
        'city': 'Balneário Camboriú',
        'state': 'SC',
        'phase': 'Fase 2 — SC',
        'perfil': [
            ('Famílias classe média/alta (nacional)', '55–60%', 'Estadia 7–14 dias, lazer e proximidade à orla.'),
            ('Jovens/grupos de amigos', '20–25%', '3–7 dias, badalação e vista mar.'),
            ('Internacional (AR/UY/BR)', '15–20%', '10–21 dias, luxo e privacidade.'),
        ],
        'sazonalidade': [
            ('Dez–jan (alta)', '85–95%', 'R$ 900–1.400'),
            ('Feriados prolongados', '75–85%', 'R$ 750–1.100'),
            ('Fev–mar (pós-alta)', '45–55%', 'R$ 450–650'),
            ('Jun–ago (ocioso)', '30–40%', 'R$ 380–580'),
        ],
        'diaria': [
            ('Centro / Av. Atlântica', 'R$ 1.100–1.600', 'R$ 550–750'),
            ('Barra Sul / Barra Norte', 'R$ 1.300–1.800', 'R$ 650–850'),
            ('Praia Central', 'R$ 950–1.400', 'R$ 480–680'),
            ('Zonas afastadas (10–15 min)', 'R$ 700–1.000', 'R$ 380–550'),
        ],
        'concorrencia': [
            ('Imobiliárias tradicionais', 'Manual, fotos amadoras', 'IA + SEO por bairro + preço dinâmico.'),
            ('Airbnb/Booking', 'Taxa 14–22%, sem curadoria', 'Conteúdo proprietário + ranking local.'),
            ('Startups regionais', 'Limitadas a 1 cidade', 'Plataforma multi-cidade + dashboard.'),
        ],
    },
    'florianopolis.html': {
        'city': 'Florianópolis',
        'state': 'SC',
        'phase': 'Fase 2 — SC',
        'perfil': [
            ('Famílias e surfistas (nacional)', '50–55%', 'Estadia 7–14 dias, praias e natureza.'),
            ('Jovens/estrangeiros (workation)', '25–30%', '15–30 dias, digital nomads.'),
            ('Internacional (EU/AR/BR)', '18–22%', '10–21 dias, ilhas e trilhas.'),
        ],
        'sazonalidade': [
            ('Dez–jan (alta)', '85–95%', 'R$ 700–1.200'),
            ('Feriados prolongados', '75–85%', 'R$ 600–1.000'),
            ('Fev–mar (pós-alta)', '50–60%', 'R$ 400–650'),
            ('Jun–ago (ocioso)', '35–45%', 'R$ 320–500'),
        ],
        'diaria': [
            ('Centro / Beira-mar', 'R$ 800–1.300', 'R$ 450–700'),
            ('Jurerê Internacional', 'R$ 1.000–1.800', 'R$ 600–900'),
            ('Campeche / Barra', 'R$ 600–1.000', 'R$ 350–600'),
            ('Lagoa da Conceição', 'R$ 700–1.200', 'R$ 400–650'),
        ],
        'concorrencia': [
            ('Imobiliárias tradicionais', 'Manual, baixa conversão', 'IA + follow-up automático.'),
            ('Airbnb/Booking', 'Taxa alta, genérico', 'Curadoria por perfil + preço dinâmico.'),
            ('Gestoras locais', 'Caras p/ pequeno', 'Plano Starter acessível.'),
        ],
    },
    'porto-de-galinhas.html': {
        'city': 'Porto de Galinhas',
        'state': 'PE',
        'phase': 'Fase 3 — Nordeste',
        'perfil': [
            ('Famílias (nacional + argentinos)', '45–50%', 'Estadia 7–14 dias, piscinas naturais.'),
            ('Casal premium/internacional', '30–35%', '10–21 dias, resorts e luxo.'),
            ('Internacional (EU/EU/AR)', '30–40%', 'Alta diária, estadias longas.'),
        ],
        'sazonalidade': [
            ('Jul–ago (alta nordestina)', '85–95%', 'R$ 800–1.500'),
            ('Dez–jan (alta nacional)', '80–90%', 'R$ 700–1.300'),
            ('Set–nov (pré-alta)', '55–65%', 'R$ 450–750'),
            ('Mar–mai (baixa)', '40–50%', 'R$ 350–600'),
        ],
        'diaria': [
            ('Centro / Praia principal', 'R$ 900–1.500', 'R$ 500–800'),
            ('Muro Alto / Cupe', 'R$ 1.000–1.800', 'R$ 600–900'),
            ('Pontal de Maceió', 'R$ 800–1.400', 'R$ 450–750'),
            ('Zonas afastadas', 'R$ 600–1.000', 'R$ 350–600'),
        ],
        'concorrencia': [
            ('Resorts tradicionais', 'Pacotes fechados, pouco flexíveis', 'Short-term flexível + IA.'),
            ('Airbnb/Booking', 'Taxa alta, sem curadoria', 'Conteúdo local + ranking.'),
            ('Imobiliárias locais', 'Manual, lento', 'SEO por bairro + automação.'),
        ],
    },
    'maceio.html': {
        'city': 'Maceió',
        'state': 'AL',
        'phase': 'Fase 3 — Nordeste',
        'perfil': [
            ('Famílias (nacional)', '50–55%', 'Estadia 7–14 dias, mar azul.'),
            ('Casal premium/internacional', '25–30%', '10–21 dias, resorts.'),
            ('Internacional (EU/PT/AR)', '25–30%', 'Alta diária, estadias longas.'),
        ],
        'sazonalidade': [
            ('Jul–ago (alta nordestina)', '80–90%', 'R$ 600–1.100'),
            ('Dez–jan (alta nacional)', '75–85%', 'R$ 550–1.000'),
            ('Set–nov (pré-alta)', '50–60%', 'R$ 350–650'),
            ('Mar–mai (baixa)', '35–45%', 'R$ 300–500'),
        ],
        'diaria': [
            ('Pajuçara / Ponta Verde', 'R$ 700–1.200', 'R$ 400–700'),
            ('Jatiúca', 'R$ 800–1.400', 'R$ 450–800'),
            ('Ipioca', 'R$ 500–900', 'R$ 300–550'),
            ('Zonas afastadas', 'R$ 400–700', 'R$ 250–450'),
        ],
        'concorrencia': [
            ('Resorts all-inclusive', 'Pouco flexíveis', 'Short-term flexível + IA.'),
            ('Airbnb/Booking', 'Taxa alta, genérico', 'Curadoria + preço dinâmico.'),
            ('Imobiliárias locais', 'Manual', 'Automação + SEO.'),
        ],
    },
    'buzios.html': {
        'city': 'Búzios',
        'state': 'RJ',
        'phase': 'Fase 4 — RJ',
        'perfil': [
            ('Casal premium (nacional/RJ)', '45–50%', 'Estadia 5–10 dias, luxo.'),
            ('Internacional (EU/AR/BR)', '25–30%', '10–21 dias, alta diária.'),
            ('Jovens/grupos', '20–25%', '3–7 dias, badalação.'),
        ],
        'sazonalidade': [
            ('Dez–jan (alta)', '85–95%', 'R$ 1.000–2.000'),
            ('Feriados prolongados', '75–85%', 'R$ 800–1.500'),
            ('Fev–mar (pós-alta)', '50–60%', 'R$ 500–900'),
            ('Jun–ago (ocioso)', '35–45%', 'R$ 400–700'),
        ],
        'diaria': [
            ('Centro / Orla Bardot', 'R$ 1.200–2.000', 'R$ 600–1.000'),
            ('João Fernandes', 'R$ 1.500–2.500', 'R$ 800–1.200'),
            ('Geribá', 'R$ 900–1.600', 'R$ 500–900'),
            ('Zonas afastadas', 'R$ 700–1.200', 'R$ 400–700'),
        ],
        'concorrencia': [
            ('Pousadas tradicionais', 'Manual, baixa conversão', 'IA + follow-up.'),
            ('Airbnb/Booking', 'Taxa alta, sem curadoria', 'Conteúdo + ranking.'),
            ('Gestoras RJ', 'Caras p/ pequeno', 'Plano Starter.'),
        ],
    },
    'angra-dos-reis.html': {
        'city': 'Angra dos Reis',
        'state': 'RJ',
        'phase': 'Fase 4 — RJ',
        'perfil': [
            ('Famílias (RJ/SP)', '50–55%', 'Estadia 5–10 dias, ilhas.'),
            ('Casal premium', '20–25%', '10–21 dias, mansões.'),
            ('Internacional (EU/AR)', '15–20%', 'Alta diária, estadias longas.'),
        ],
        'sazonalidade': [
            ('Dez–jan (alta)', '80–90%', 'R$ 800–1.600'),
            ('Feriados prolongados', '70–80%', 'R$ 650–1.200'),
            ('Fev–mar (pós-alta)', '45–55%', 'R$ 400–800'),
            ('Jun–ago (ocioso)', '30–40%', 'R$ 350–600'),
        ],
        'diaria': [
            ('Centro / Orla', 'R$ 900–1.500', 'R$ 500–800'),
            ('Frade / Condomínios', 'R$ 1.000–2.000', 'R$ 600–1.000'),
            ('Ilha Grande (Abraão)', 'R$ 500–1.000', 'R$ 300–600'),
            ('Zonas afastadas', 'R$ 400–800', 'R$ 250–500'),
        ],
        'concorrencia': [
            ('Imobiliárias tradicionais', 'Manual, lento', 'IA + SEO.'),
            ('Airbnb/Booking', 'Taxa alta, genérico', 'Curadoria + preço dinâmico.'),
            ('Operadoras de ilha', 'Pouco flexíveis', 'Short-term flexível.'),
        ],
    },
    'cabo-frio.html': {
        'city': 'Cabo Frio',
        'state': 'RJ',
        'phase': 'Fase 4 — RJ',
        'perfil': [
            ('Famílias (RJ/SP)', '55–60%', 'Estadia 5–10 dias, praias.'),
            ('Jovens/grupos', '20–25%', '3–7 dias, badalação.'),
            ('Internacional (AR/BR)', '10–15%', 'Estadias médias.'),
        ],
        'sazonalidade': [
            ('Dez–jan (alta)', '85–95%', 'R$ 600–1.200'),
            ('Feriados prolongados', '75–85%', 'R$ 500–900'),
            ('Fev–mar (pós-alta)', '50–60%', 'R$ 350–650'),
            ('Jun–ago (ocioso)', '35–45%', 'R$ 300–500'),
        ],
        'diaria': [
            ('Passagem / Centro', 'R$ 700–1.200', 'R$ 400–700'),
            ('Praia do Forte', 'R$ 800–1.400', 'R$ 450–800'),
            ('Foguete', 'R$ 600–1.000', 'R$ 350–600'),
            ('Zonas afastadas', 'R$ 400–800', 'R$ 250–450'),
        ],
        'concorrencia': [
            ('Imobiliárias tradicionais', 'Manual, baixa conversão', 'IA + follow-up.'),
            ('Airbnb/Booking', 'Taxa alta, sem curadoria', 'Conteúdo + ranking.'),
            ('Gestoras locais', 'Caras p/ pequeno', 'Plano Starter.'),
        ],
    },
}

def rows(data, headers):
    h = ''.join(f'<th>{x}</th>' for x in headers)
    body = ''
    for r in data:
        body += '<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>'
    return f'<table><tr>{h}</tr>{body}</table>'

def render(c, key):
    d = cities[key]
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{d['city']} — Análise de Expansão | Praia Digital</title>
<meta name="description" content="Análise de viabilidade de locação de temporada em {d['city']}/{d['state']}: perfil do turista, sazonalidade, diárias e concorrência.">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1f2937;line-height:1.6;padding:2rem}}
.container{{max-width:1000px;margin:0 auto;background:#fff;padding:2.5rem;border-radius:20px;box-shadow:0 12px 40px rgba(0,0,0,.06)}}
h1{{font-size:2rem;color:#0a1628;margin-bottom:.4rem}}
.phase{{display:inline-block;background:#eef2ff;color:#2563eb;padding:.3rem .9rem;border-radius:999px;font-weight:700;font-size:.85rem;margin-bottom:1rem}}
h2{{color:#0a1628;margin:1.8rem 0 .8rem;border-bottom:2px solid #e5e7eb;padding-bottom:.3rem}}
table{{width:100%;border-collapse:collapse;margin:.8rem 0;font-size:.95rem}}
th,td{{border:1px solid #e5e7eb;padding:.65rem .85rem;text-align:left}}
th{{background:#0a1628;color:#fff}}
tr:nth-child(even){{background:#f8fafc}}
.cta{{display:inline-block;margin-top:1.4rem;padding:.75rem 1.25rem;background:#0a1628;color:#fff;border-radius:12px;font-weight:700;text-decoration:none}}
.links{{display:flex;flex-wrap:wrap;gap:10px;margin-top:1rem}}
.chip{{background:#eef2ff;color:#2563eb;padding:8px 12px;border-radius:999px;font-size:13px;font-weight:600;text-decoration:none}}
.footer{{margin-top:2rem;font-size:.85rem;color:#6b7280;text-align:center}}
</style>
</head>
<body>
<div class="container">
<span class="phase">{d['phase']}</span>
<h1>Análise de Expansão — {d['city']}/{d['state']}</h1>
<p>Inteligência Praia Digital | Parte do roadmap nacional iniciado no litoral paulista.</p>

<h2>1) Perfil do turista</h2>
{rows(d['perfil'], ['Segmento','Participação','Característica'])}

<h2>2) Sazonalidade real</h2>
{rows(d['sazonalidade'], ['Período','Ocupação','Diária média'])}
<p>Implicação: preço dinâmico automatizado e pacotes de baixa temporada são essenciais para sustentar receita.</p>

<h2>3) Diária média — apto 2 quartos bem localizado</h2>
{rows(d['diaria'], ['Localização','Alta temporada','Baixa temporada'])}

<h2>4) Concorrência e pontos fracos</h2>
{rows(d['concorrencia'], ['Concorrente','Ponto fraco','Como a PD ganha'])}

<div class="links">
<a class="chip" href="expansao-nacional-litoral-paulista.html">Relatório de Expansão</a>
<a class="chip" href="mapa-inteligente.html">Mapa Inteligente</a>
<a class="chip" href="planos-assinatura.html">Planos</a>
<a class="chip" href="dashboard-prospeccao.html">Painel de Prospecção</a>
</div>

<a class="cta" href="index.html">Voltar para o site</a>
<div class="footer">CEO Carolina Moura | Praia Digital | 2026</div>
</div>
</body>
</html>
'''

sitemap_items = []
for key, d in cities.items():
    path = out_dir/key
    path.write_text(render(d, key), encoding='utf-8')
    sitemap_items.append(f'{base}/cidades-expansao/{key}')

print('criadas', len(sitemap_items), 'paginas de cidade')
for i in sitemap_items:
    print(i)
