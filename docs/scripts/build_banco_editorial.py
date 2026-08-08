
import glob, os, re, json, hashlib
from collections import defaultdict, Counter
from urllib.parse import urlparse
from difflib import SequenceMatcher

BASE = "."
BLOG_DIR = os.path.join(BASE, "blog")
OUT_PATH = os.path.join(BASE, "docs", "banco-editorial.json")

KEYWORDS_CITY = [
    "santos","guaruj\u00e1","guaruja","praia grande","bertioga","itanha\u00e9m","itanhaem",
    "mongagu\u00e1","mongagua","s\u00e3o vicente","sao vicente","peru\u00edbe","peruibe",
    "caraguatatuba","ilhabela","s\u00e3o sebasti\u00e3o","sao sebastiao","ubatuba",
    "maresias","riviera","litoral norte","litoral sul","litoral paulista","litoral de sp"
]

CITY_NORM = {
    "guaruj\u00e1":"guaruja","guaruja":"guaruja","santos":"santos","praia grande":"praia_grande",
    "bertioga":"bertioga","itanha\u00e9m":"itanhaem","itanhaem":"itanhaem",
    "mongagu\u00e1":"mongagua","mongagua":"mongagua","s\u00e3o vicente":"sao_vicente","sao vicente":"sao_vicente",
    "peru\u00edbe":"peruibe","peruibe":"peruibe","caraguatatuba":"caraguatatuba","ilhabela":"ilhabela",
    "s\u00e3o sebasti\u00e3o":"sao_sebastiao","sao sebastiao":"sao_sebastiao","maresias":"maresias",
    "riviera":"riviera","ubatuba":"ubatuba","litoral norte":"litoral_norte","litoral sul":"litoral_sul",
    "litoral paulista":"litoral_paulista","litoral de sp":"litoral_sp"
}

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

def internal_blog_links(content):
    return re.findall(r'href=["\'](/blog/[^"\']+)["\']', content)

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
    if any(x in t for x in ["guia","primeira compra","primeiro imovel","como escolher","como comprar","quando comprar","quando vender","quanto custa","morar","seguran\u00e7a","documenta\u00e7\u00e3o","financiamento","impostos","checklist"]):
        return "Topo"
    if any(x in t for x in ["avaliacao","avaliar","preco","pre\u00e7o","valor","rentabilidade","investir","comparar","mercado","analise","an\u00e1lise","roi","tendencias","tend\u00eancia"]):
        return "Meio"
    if any(x in t for x in ["captacao","captar","leads","vendas","fechar","parceria","automacao","automa\u00e7\u00e3o","whatsapp","visita","proposta","fechamento","case","resultado","reducao","redu\u00e7\u00e3o","conversao","convers\u00e3o","funil","nurturing"]):
        return "Fundo"
    return "Meio"

def cluster_from_slug(title, slug, city):
    t = (title + " " + slug).lower()
    if any(x in t for x in ["aluguel","temporada","airbnb","booking","taxa ocupacao","ocupacao","alta temporada","baixa temporada","gestao locacao"]):
        return "locacao_temporada"
    if any(x in t for x in ["venda","vender","vendas","fechamento","fechar","compra","comprar"]):
        return "compra_venda"
    if any(x in t for x in ["investimento","investir","rentabilidade","roi","retorno","valorizacao","valoriza\u00e7\u00e3o","lucro"]):
        return "investimento"
    if any(x in t for x in ["bairro","bairros","centro","ponta","gonzaga","embare","jose menino","vila nova","boa viagem","santos","guaruj\u00e1","guaruja","praia grande","bertioga","itanhaem","mongagua","sao vicente","peruibe","caraguatatuba","ilhabela","sao sebastiao","maresias","ubatuba"]):
        return "bairros_cidades"
    if any(x in t for x in ["seo local","google business","maps","perfil google","backlinks","autoridade local"]):
        return "seo_local"
    if any(x in t for x in ["marketing digital","redes sociais","instagram","facebook","reels","tiktok","video","conteudo"]):
        return "marketing_digital"
    if any(x in t for x in ["automacao","automa\u00e7\u00e3o","ia","inteligencia artificial","chatbot","assistente virtual","ferramentas"]):
        return "automacao_ia"
    if any(x in t for x in ["parceria","construtoras","indica\u00e7\u00e3o","ganho compartilhado","white label"]):
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
    if any(x in t for x in ["case","resultado","depoimento","analise","an\u00e1lise","comparar","melhor"]):
        return "navegacional_comparativo"
    return "informacional"

records = []
missing_canonical = []
city_counts = Counter()
cluster_counts = Counter()
funnel_counts = Counter()
intent_counts = Counter()

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
    internal = internal_blog_links(content)
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
        "internal_links": internal[:20],
        "status": "publicado",
        "lastmod": None,
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
                "reason": "T\u00edtulos muito similares com mesma inten\u00e7\u00e3o, cluster e cidade"
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

update_candidates = [r['path'] for r in records if r['canonical_ok'] is False or r['internal_links'] == []][:40]

report = {
    "meta": {
        "total_articles": len(records),
        "domain": "praia.digital",
        "blog_path": BLOG_DIR,
        "scope": "controle editorial cont\u00ednuo"
    },
    "status_counts": dict(Counter(r['status'] for r in records)),
    "funnel_counts": dict(funnel_counts),
    "intent_counts": dict(intent_counts),
    "city_counts": dict(city_counts),
    "cluster_counts": dict(cluster_counts),
    "canonical_issues": missing_canonical[:20],
    "duplicate_signals": dup_signals[:100],
    "update_candidates": update_candidates[:40],
    "next_queue": top10,
    "coverage_by_city_cluster": {c: dict(clusters) for c, clusters in city_cluster.items()},
    "articles": records,
}

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as fh:
    json.dump(report, fh, ensure_ascii=False, indent=2)

print('wrote', OUT_PATH)
print('total', len(records), 'articles')
print('duplicate signals:', len(dup_signals))
print('canonical issues:', len(missing_canonical))
print('next queue count:', len(top10))
for item in top10:
    print(item)
print('top cities:', city_counts.most_common(10))
print('top clusters:', cluster_counts.most_common(10))
