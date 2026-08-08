#!/usr/bin/env python3
import glob, os, re, json, hashlib
from collections import defaultdict, Counter
from urllib.parse import urlparse
from difflib import SequenceMatcher

BASE = "."
BLOG_DIR = os.path.join(BASE, "blog")
OUT_PATH = os.path.join(BASE, "docs", "banco-editorial.json")

KEYWORDS_CITY = [
    "santos","guaruja","guarujá","praia grande","bertioga","itanhaem","itanhaém",
    "mongagua","mongaguá","sao vicente","são vicente","peruibe","peruíbe",
    "caraguatatuba","ilhabela","sao sebastiao","são sebastião","ubatuba",
    "maresias","riviera","litoral norte","litoral sul","litoral paulista","litoral de sp"
]
CITY_NORM = {
    "guarujá":"guaruja","guaruja":"guaruja","santos":"santos","praia grande":"praia_grande",
    "bertioga":"bertioga","itanhaém":"itanhaem","itanhaem":"itanhaem",
    "mongaguá":"mongagua","mongagua":"mongagua","são vicente":"sao_vicente","sao vicente":"sao_vicente",
    "peruíbe":"peruibe","peruibe":"peruibe","caraguatatuba":"caraguatatuba","ilhabela":"ilhabela",
    "são sebastião":"sao_sebastiao","sao sebastiao":"sao_sebastiao","maresias":"maresias",
    "riviera":"riviera","ubatuba":"ubatuba","litoral norte":"litoral_norte","litoral sul":"litoral_sul",
    "litoral paulista":"litoral_paulista","litoral de sp":"litoral_sp"
}
ARTICLE_TYPES = {
    "A": "Artigo SEO gratuito",
    "B": "Artigo de conversao",
    "C": "Artigo-ponte",
    "D": "Artigo de autoridade",
    "E": "Artigo comercial",
}
PRODUCTS = [
    {
        "id": "curso-gestao-temporada",
        "nome": "Curso de Gestão de Imóveis de Temporada",
        "descricao": "Formação completa para proprietários e gestores que querem profissionalizar aluguéis de temporada no litoral.",
        "publico": "Proprietários, gestores e corretores que querem atuar com temporada.",
        "problema": "Falta de método, precificação e operação para aluguéis de temporada.",
        "transformacao": "Processo estruturado de gestão, precificação, reservas, estadia e pós-estadia.",
        "categoria": "curso",
        "nivel": "intermediario",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/curso-gestao-temporada",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["aluguel temporada", "gestao locacao", "temporada litoral", "rentabilidade", "ocupacao"],
        "cta_recomendado": "Quer aprender a profissionalizar seu imóvel de temporada? Veja o treinamento completo."
    },
    {
        "id": "curso-comprar-imovel-praia-sem-golpes",
        "nome": "Curso: Comprar Imóvel na Praia Sem Golpes",
        "descricao": "Checklist, documentação e estratégias para comprar imóvel no litoral com segurança.",
        "publico": "Compradores de primeira viagem e investidores iniciantes no litoral.",
        "problema": "Falta de clareza sobre documentação, riscos e como escolher imóvel com segurança.",
        "transformacao": "Capacidade de avaliar imóveis, validar documentação e fechar compra com menor risco.",
        "categoria": "curso",
        "nivel": "iniciante",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/comprar-imovel-praia-sem-golpes",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["comprar imovel", "documentacao imovel", "segurança compra", "primeiro imovel", "escritura"],
        "cta_recomendado": "Quer comprar com segurança? Conheça o curso completo para compradores no litoral."
    },
    {
        "id": "ebook-rentabilidade-temporada",
        "nome": "E-book: Rentabilidade de Temporada no Litoral",
        "descricao": "Guia prático para calcular retorno, definir preço e analisar viabilidade de imóveis de temporada.",
        "publico": "Proprietários e investidores que avaliam temporada como oportunidade.",
        "problema": "Dificuldade para calcular rentabilidade real e tomar decisão de investimento.",
        "transformacao": "Planilha e critérios claros para avaliar retorno e comparar oportunidades.",
        "categoria": "ebook",
        "nivel": "iniciante",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/ebook-rentabilidade-temporada",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["rentabilidade", "retorno investimento", "temporada", "aluguel temporada", "investimento imovel"],
        "cta_recomendado": "Quer calcular a viabilidade do seu imóvel? Baixe o guia completo de rentabilidade."
    },
    {
        "id": "checklist-captacao-imoveis",
        "nome": "Checklist: Captação de Imóveis para Corretores",
        "descricao": "Material pronto para estruturar a captação de imóveis no litoral sem depender de anúncios.",
        "publico": "Corretores e pequenas imobiliárias do litoral.",
        "problema": "Falta de processo de captação consistente e previsível.",
        "transformacao": "Rotina de prospecção, scripts e pontos de contato para captar imóveis regularmente.",
        "categoria": "checklist",
        "nivel": "iniciante",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/checklist-captacao-imoveis",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["captacao imoveis", "prospeccao", "corretor litoral", "proprietario", "captar imoveis"],
        "cta_recomendado": "Quer captar mais imóveis sem anúncios? Use o checklist pronto para corretores."
    },
    {
        "id": "curso-marketing-digital-imobiliaria",
        "nome": "Curso de Marketing Digital para Imobiliárias",
        "descricao": "Treinamento de SEO local, Google Business Profile, conteúdo e anúncios para imobiliárias do litoral.",
        "publico": "Imobiliárias e corretores que querem atrair leads qualificados.",
        "problema": "Falta de presença digital, conteúdo fraco e leads inconsistentes.",
        "transformacao": "Estrutura de marketing local, calendário de conteúdo, modelo de anúncios e métricas.",
        "categoria": "curso",
        "nivel": "intermediario",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/marketing-digital-imobiliaria",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["marketing digital", "seo local", "google business", "leads", "anuncios imoveis"],
        "cta_recomendado": "Quer atrair leads qualificados todos os dias? Veja o curso de marketing digital para imobiliárias."
    },
    {
        "id": "minicurso-automacao-imobiliaria",
        "nome": "Mini Curso: Automação para Imobiliárias",
        "descricao": "Introdução prática a automações, CRM leve e atendimento digital para imobiliárias pequenas.",
        "publico": "Pequenas imobiliárias e corretores sem equipe de tecnologia.",
        "problema": "Atendimento lento, follow-up fraco e processos repetitivos manuais.",
        "transformacao": "Automações simples de atendimento, follow-up e organização de leads.",
        "categoria": "mini-curso",
        "nivel": "iniciante",
        "link_hotmart": "https://www.hotmart.com/pt-br/producto/minicurso-automacao-imobiliaria",
        "artigos_relacionados": [],
        "keywords_relacionadas": ["automacao imobiliaria", "chatbot", "atendimento digital", "crm", "follow-up"],
        "cta_recomendado": "Quer reduzir o tempo de resposta e organizar o atendimento? Comece pelo mini curso de automação."
    }
]

def detect_city(text):
    lower = text.lower()
    best = None
    for c in KEYWORDS_CITY:
        if c in lower:
            if best is None or len(c) > len(best):
                best = c
    return CITY_NORM.get(best)

def extract_meta(content, pattern):
    m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return (m.group(1).strip() if m else None)

def extract_h1(content):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1))
        return re.sub(r'\s+', ' ', text).strip()
    return None

def extract_h2s(content, limit=20):
    return re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)[:limit]

def slug_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]

def canonical_ok(content, path):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content, re.IGNORECASE)
    expected_slug = slug_from_path(path)
    c = m.group(1) if m else None
    if not c:
        return None
    parsed = urlparse(c)
    expected_path = f"/blog/{expected_slug}.html"
    if parsed.path.endswith(expected_path):
        return True
    if parsed.path.endswith(f"/blog{expected_slug}.html"):
        return False
    return None

def classify_funnel(title):
    t = title.lower()
    if any(x in t for x in ["guia","primeira compra","primeiro imovel","como escolher","como comprar","quando comprar","quando vender","quanto custa","morar","seguranca","documentacao","financiamento","impostos","checklist"]):
        return "Topo"
    if any(x in t for x in ["avaliacao","avaliar","preco","preço","valor","rentabilidade","investir","comparar","mercado","analise","análise","roi","tendencias","tendência"]):
        return "Meio"
    if any(x in t for x in ["captacao","captar","leads","vendas","fechar","parceria","automacao","automação","whatsapp","visita","proposta","fechamento","case","resultado","reducao","redução","conversao","conversão","funil","nurturing"]):
        return "Fundo"
    return "Meio"

def cluster_from_slug(title, slug, city):
    t = (title + " " + slug).lower()
    if any(x in t for x in ["aluguel","temporada","airbnb","booking","taxa ocupacao","ocupacao","alta temporada","baixa temporada","gestao locacao"]):
        return "locacao_temporada"
    if any(x in t for x in ["venda","vender","vendas","fechamento","fechar","compra","comprar"]):
        return "compra_venda"
    if any(x in t for x in ["investimento","investir","rentabilidade","roi","retorno","valorizacao","valorização","lucro"]):
        return "investimento"
    if any(x in t for x in ["bairro","bairros","centro","ponta","gonzaga","embare","jose menino","vila nova","boa viagem","santos","guaruja","guarujá","praia grande","bertioga","itanhaem","mongagua","sao vicente","peruibe","caraguatatuba","ilhabela","sao sebastiao","maresias","ubatuba"]):
        return "bairros_cidades"
    if any(x in t for x in ["seo local","google business","maps","perfil google","backlinks","autoridade local"]):
        return "seo_local"
    if any(x in t for x in ["marketing digital","redes sociais","instagram","facebook","reels","tiktok","video","conteudo"]):
        return "marketing_digital"
    if any(x in t for x in ["automacao","automação","ia","inteligencia artificial","chatbot","assistente virtual","ferramentas"]):
        return "automacao_ia"
    if any(x in t for x in ["parceria","construtoras","indicação","ganho compartilhado","white label"]):
        return "parcerias"
    if any(x in t for x in ["juridico","documentacao","escritura","iptu","usucapiao","lei","inadimplencia","seguro"]):
        return "juridico"
    if any(x in t for x in ["financiamento","consorcio","fgts","entrada","parcelamento"]):
        return "financiamento"
    if any(x in t for x in ["case","caso","resultado","antes e depois","depoimento"]):
        return "cases"
    return "editorial"

def intent_from_title(title):
    t = title.lower()
    if any(x in t for x in ["como","quando","quanto","qual","onde","por que","porque","dicas","guia","checklist","passo a passo"]):
        return "informacional"
    if any(x in t for x in ["comprar","vender","investir","alugar","captar","leads","vendas","fechar","anunciar"]):
        return "comercial"
    if any(x in t for x in ["case","resultado","depoimento","analise","análise","comparar","melhor"]):
        return "navegacional_comparativo"
    return "informacional"

def article_type_from_title(title, slug):
    t = title.lower()
    s = slug.lower()
    if any(x in t for x in ["curso","treinamento","aula","modulo","certificado"]):
        return "B"
    if any(x in t for x in ["checklist","planilha","template","modelo","guia completo","passo a passo"]):
        return "C"
    if any(x in t for x in ["case","resultado","depoimento","antes e depois"]):
        return "D"
    if any(x in t for x in ["comprar","vender","investir","alugar","captar","leads","vendas","fechar","anunciar"]):
        return "E"
    return "A"

def recommend_product(title, slug, city):
    t = (title + " " + slug).lower()
    candidates = []
    for p in PRODUCTS:
        score = 0
        for kw in p["keywords_relacionadas"]:
            if kw in t:
                score += 1
        candidates.append((score, p))
    candidates.sort(key=lambda x: (-x[0], x[1]["id"]))
    best_score, best = candidates[0]
    if best_score >= 1:
        return best["id"], best_score
    return None, 0

def cta_text_for_product(prod_id):
    for p in PRODUCTS:
        if p["id"] == prod_id:
            return p["cta_recomendado"], p["link_hotmart"]
    return None, None

records = []
missing_canonical = []
city_counts = Counter()
cluster_counts = Counter()
funnel_counts = Counter()
intent_counts = Counter()
type_counts = Counter()

for path in sorted(glob.glob(os.path.join(BLOG_DIR, "*.html"))):
    slug = slug_from_path(path)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
    except Exception:
        continue
    title = extract_meta(content, r'<title[^>]*>(.*?)</title>')
    if not title:
        continue
    title = re.split(r'\s*[|\-\u2013\u2014]\s*', title)[0].strip()
    desc = extract_meta(content, r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']')
    kw = extract_meta(content, r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\']([^"\']+)["\']')
    keywords = [k.strip() for k in kw.split(',')] if kw else []
    city = detect_city(title + " " + (desc or "") + " " + slug)
    h1 = extract_h1(content)
    h2s = extract_h2s(content)
    canon = canonical_ok(content, path)
    if canon is False:
        missing_canonical.append(path)
    city_counts[city or "geral"] += 1
    cluster = cluster_from_slug(title, slug, city)
    cluster_counts[cluster] += 1
    funnel = classify_funnel(title)
    funnel_counts[funnel] += 1
    intent = intent_from_title(title)
    intent_counts[intent] += 1
    article_type = article_type_from_title(title, slug)
    type_counts[article_type] += 1
    prod_id, prod_score = recommend_product(title, slug, city)
    cta_text, hotmart_link = cta_text_for_product(prod_id) if prod_id else (None, None)
    records.append({
        "id": hashlib.md5(slug.encode('utf-8')).hexdigest()[:10],
        "slug": slug,
        "path": os.path.relpath(path, BASE),
        "title": title,
        "h1": h1,
        "h2_count": len(h2s),
        "meta_description": desc,
        "keywords": keywords[:8],
        "primary_keyword": keywords[0] if keywords else None,
        "city": city,
        "funnel": funnel,
        "intent": intent,
        "cluster": cluster,
        "canonical_ok": canon,
        "status": "publicado",
        "article_type": article_type,
        "article_type_label": ARTICLE_TYPES[article_type],
        "product_related_id": prod_id,
        "product_relation_score": prod_score,
        "hotmart_link": hotmart_link,
        "recommended_cta": cta_text,
        "conversion_potential": "alta" if prod_score >= 2 else "media" if prod_score == 1 else "baixa",
        "commercial_cluster": cluster,
        "cta_intensity": "forte" if article_type == "B" else "media" if article_type in ("C","E") else "suave"
    })

dup_signals = []
n = len(records)
for i in range(n):
    for j in range(i+1, n):
        a, b = records[i], records[j]
        if a['city'] and b['city'] and a['city'] != b['city']:
            continue
        if a['intent'] != b['intent']:
            continue
        if a['cluster'] != b['cluster']:
            continue
        ratio = SequenceMatcher(None, a['title'].lower(), b['title'].lower()).ratio()
        if ratio >= 0.85:
            dup_signals.append({
                "type": "possible_duplicate",
                "score": round(ratio, 2),
                "a": a['path'],
                "b": b['path'],
                "reason": "Títulos muito similares com mesma intenção, cluster e cidade"
            })

city_cluster = defaultdict(Counter)
for r in records:
    city_cluster[r['city'] or 'geral'][r['cluster']] += 1

priority_scores = {
    "locacao_temporada": 3,
    "compra_venda": 3,
    "investimento": 3,
    "bairros_cidades": 2,
    "seo_local": 3,
    "marketing_digital": 2,
    "automacao_ia": 2,
    "parcerias": 1,
    "juridico": 2,
    "financiamento": 2,
    "cases": 1,
    "editorial": 1,
}
next_queue = []
for city, clusters in city_cluster.items():
    for cluster, count in clusters.items():
        score = priority_scores.get(cluster, 1)
        if count < 4:
            next_queue.append((cluster, city, count, score))
seen = set()
unique_queue = []
for cluster, city, count, score in next_queue:
    key = (cluster, city)
    if key in seen:
        continue
    seen.add(key)
    unique_queue.append({"cluster": cluster, "city": city, "count": count, "priority_score": score, "priority": "alta" if score >= 3 else "media" if score == 2 else "baixa"})
unique_queue.sort(key=lambda x: (-x['priority_score'], x['count'], x['city'], x['cluster']))
unique_queue = unique_queue[:20]
top10 = unique_queue[:10]

update_candidates = [r['path'] for r in records if r['canonical_ok'] is False or r.get('internal_links') == []][:40]

product_mapping = defaultdict(list)
for r in records:
    if r['product_related_id']:
        product_mapping[r['product_related_id']].append({
            "path": r['path'],
            "title": r['title'],
            "type": r['article_type_label'],
            "cta": r['recommended_cta'],
            "conversion_potential": r['conversion_potential']
        })

report = {
    "meta": {
        "total_articles": len(records),
        "domain": "praia.digital",
        "blog_path": BLOG_DIR,
        "scope": "controle editorial contínuo + integracao hotmart"
    },
    "products": PRODUCTS,
    "article_types": ARTICLE_TYPES,
    "status_counts": dict(Counter(r['status'] for r in records)),
    "article_type_counts": dict(type_counts),
    "funnel_counts": dict(funnel_counts),
    "intent_counts": dict(intent_counts),
    "city_counts": dict(city_counts),
    "cluster_counts": dict(cluster_counts),
    "canonical_issues": missing_canonical[:20],
    "duplicate_signals": dup_signals[:100],
    "update_candidates": update_candidates[:40],
    "next_queue": top10,
    "coverage_by_city_cluster": {c: dict(clusters) for c, clusters in city_cluster.items()},
    "product_mapping": product_mapping,
    "articles": records,
}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as fh:
    json.dump(report, fh, ensure_ascii=False, indent=2)

print('wrote', OUT_PATH)
print('total', len(records), 'articles')
print('article types:', dict(type_counts))
print('product mapping entries:', len(product_mapping))
for pid, items in product_mapping.items():
    print(' -', pid, ':', len(items))
print('duplicate signals:', len(dup_signals))
print('canonical issues:', len(missing_canonical))
print('top10 next queue:')
for item in top10:
    print(item)
