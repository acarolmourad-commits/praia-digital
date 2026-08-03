import os, re, json, html
from pathlib import Path

base = Path('C:/Users/Carolina/praia-digital/imoveis')
files = sorted(base.rglob('*.html'))

sample = []
for f in files:
    if 'imovel-' in f.name and f.parent == base / 'imoveis' and len(sample) < 15:
        sample.append(f)
for f in files:
    if f.parent == base and len(sample) < 20:
        sample.append(f)
if len(sample) < 20:
    for f in files:
        if f.parent == base / 'imoveis' and f not in sample and len(sample) < 20:
            sample.append(f)

def strip_html(html_text):
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', html_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

results = []

for path in sample:
    raw = path.read_text(encoding='utf-8', errors='ignore')
    text = strip_html(raw)
    title_m = re.search(r'<title[^>]*>(.*?)</title>', raw, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_m.group(1)) if title_m else ''
    desc_m = re.search(r'<meta[^>]*name\s*=\s*["\']description["\'][^>]*content\s*=\s*["\']([^"\']*)["\']', raw, re.IGNORECASE)
    description = html.unescape(desc_m.group(1)) if desc_m else ''
    
    # (a) schema completo RealEstateListing + Offer.price + priceCurrency
    has_full_schema = False
    json_ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.DOTALL | re.IGNORECASE)
    for block in json_ld_blocks:
        try:
            data = json.loads(block)
            candidates = []
            if isinstance(data, dict):
                if '@graph' in data and isinstance(data['@graph'], list):
                    candidates.extend(data['@graph'])
                else:
                    candidates.append(data)
            elif isinstance(data, list):
                candidates.extend(data)
            for item in candidates:
                if isinstance(item, dict):
                    t = item.get('@type', [])
                    is_listing = (t == 'RealEstateListing') or (isinstance(t, list) and 'RealEstateListing' in t)
                    if not is_listing:
                        continue
                    offers = item.get('offers', {})
                    if isinstance(offers, dict) and offers.get('price') and offers.get('priceCurrency'):
                        has_full_schema = True
        except Exception:
            pass
    
    # (b) Offer.price e priceCurrency
    has_price = False
    has_currency = False
    for block in json_ld_blocks:
        try:
            data = json.loads(block)
            candidates = []
            if isinstance(data, dict):
                candidates = data.get('@graph', [data]) if '@graph' in data else [data]
            elif isinstance(data, list):
                candidates = data
            for item in candidates:
                if isinstance(item, dict):
                    offers = item.get('offers', {})
                    if isinstance(offers, dict):
                        if offers.get('price'):
                            has_price = True
                        if offers.get('priceCurrency'):
                            has_currency = True
        except Exception:
            pass
    if not has_price:
        has_price = bool(re.search(r'"price"\s*:\s*\d', raw))
    if not has_currency:
        has_currency = bool(re.search(r'"priceCurrency"\s*:\s*"[A-Z]{3}"', raw))
    
    # (c) imagem duplicada/quebrada
    imgs = re.findall(r'<img[^>]*>', raw, re.IGNORECASE)
    broken = 0
    seen = []
    for tag in imgs:
        src_m = re.search(r'src\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
        src = src_m.group(1).strip() if src_m else ''
        if not src:
            broken += 1
        elif src in seen:
            broken += 1
        seen.append(src)
    consecutive = len(re.findall(r'<img[^>]*>\s*<img[^>]*>', raw, re.IGNORECASE))
    malformed = len(re.findall(r'<img[^>]*<img', raw, re.IGNORECASE))
    has_broken_img = (broken > 0) or (consecutive > 0) or (malformed > 0)
    broken_count = broken + consecutive + malformed
    
    # (d) termos de liquidez
    terms = ['lance', 'oportunidade', 'desconto']
    text_lower = text.lower()
    found_terms = [t for t in terms if t in text_lower]
    
    # (e) apelo de venda
    appeal_keywords = {
        'venda': 3, 'vende-se': 3, 'à venda': 3, 'comprar': 2, 'investimento': 3,
        'exclusivo': 4, 'único': 2, 'lançamento': 3, 'preço': 2, 'condição': 1,
        'imperdível': 4, 'promoção': 3, 'financiamento': 3, 'entrada': 2,
        'desconto': 3, 'oportunidade': 3, 'lance': 2, 'médio padrão': 1,
        'alto padrão': 2, 'lazer': 1, 'vista mar': 2, 'varanda': 1,
        'condomínio': 1, 'academia': 1, 'piscina': 1, 'churrasqueira': 1,
        'orla': 2, 'praia': 2, 'lazer completo': 2, 'gourmet': 1, 'duplex': 2,
        'cobertura': 2, 'terreno': 1, 'casa': 1, 'apartamento': 1,
        'área': 1, 'quartos': 1, 'vaga': 1, 'pet': 1, 'whatsapp': 1,
        'visitar': 2, 'agendar': 2, 'detalhes': 1, 'contato': 1,
        'alto': 1, 'luxo': 3, 'premium': 3, 'novo': 1, 'reformado': 2,
        'pronto': 1, 'entrega': 1, 'documentação': 1, 'financiar': 2
    }
    appeal_score = 0
    for kw, weight in appeal_keywords.items():
        appeal_score += text_lower.count(kw) * weight
    if has_full_schema:
        appeal_score += 2
    if found_terms:
        appeal_score += 3
    if len(description) > 80:
        appeal_score += 2
    
    results.append({
        'file': path.name,
        'path': str(path),
        'title': title[:120],
        'description': description[:200],
        'has_full_schema': has_full_schema,
        'has_price': has_price,
        'has_currency': has_currency,
        'broken_count': broken_count,
        'has_broken_img': has_broken_img,
        'liquidity_terms': found_terms,
        'appeal_score': appeal_score,
        'text_snippet': text[:500].replace('\n', ' ')
    })

total = len(results)
pct_a = sum(1 for r in results if r['has_full_schema']) / total * 100
pct_b_price = sum(1 for r in results if r['has_price']) / total * 100
pct_b_currency = sum(1 for r in results if r['has_currency']) / total * 100
pct_c = sum(1 for r in results if r['has_broken_img']) / total * 100
pct_d = sum(1 for r in results if r['liquidity_terms']) / total * 100

ranked = sorted(results, key=lambda x: x['appeal_score'], reverse=True)[:5]

report = {
    'sample_size': total,
    'stats': {
        'a_schema_completo_pct': round(pct_a, 1),
        'b_offer_price_pct': round(pct_b_price, 1),
        'b_price_currency_pct': round(pct_b_currency, 1),
        'c_img_quebrada_pct': round(pct_c, 1),
        'd_termos_liquidez_pct': round(pct_d, 1)
    },
    'top5': []
}
for r in ranked:
    report['top5'].append({
        'file': r['file'],
        'title': r['title'],
        'description': r['description'],
        'appeal_score': r['appeal_score'],
        'liquidity_terms': r['liquidity_terms'],
        'snippet': r['text_snippet'][:300]
    })

out_path = Path('C:/Users/Carolina/praia-digital/relatorio_auditoria_imoveis.json')
out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

print('=== ESTATÍSTICAS DA AMOSTRA (20 páginas) ===')
print(f'(a) RealEstateListing schema completo: {pct_a:.0f}%')
print(f'(b) Offer.price: {pct_b_price:.0f}% | priceCurrency: {pct_b_currency:.0f}%')
print(f'(c) Imagem duplicada/quebrada: {pct_c:.0f}%')
print(f'(d) Termos de liquidez: {pct_d:.0f}%')
print()
print('=== TOP 5 OPORTUNIDADES DE VENDA ===')
for i, r in enumerate(ranked, 1):
    print(f'{i}. {r["file"]}')
    print(f'   Título: {r["title"]}')
    print(f'   Descrição: {r["description"]}')
    print(f'   Score apelo: {r["appeal_score"]} | liquidez: {r["liquidity_terms"]}')
    print(f'   Trecho: {r["text_snippet"][:300]}')
    print()
print(f'Relatório salvo em: {out_path}')
