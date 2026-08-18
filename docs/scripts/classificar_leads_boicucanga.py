#!/usr/bin/env python3
"""
Classificação e deduplicação de leads — Frente Boiçucanga
Uso: preparar leads priorizados sem disparar contato.
"""
import csv, re, hashlib
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent.parent.parent / 'docs' / 'comercial'
LEADS_PATH = BASE / 'leads_boicucanga.csv'
OUT_PATH = BASE / 'leads_boicucanga_classificados.csv'

SCORE_RULES = {
    'proximidade_praia': 2,
    'piscina': 2,
    'ar_condicionado': 1,
    'estacionamento': 1,
    'capacidade_grupos': 1,
    'area_externa': 1,
    'anuncio_baixa_qualidade': 2,
    'anunciante_identificavel': 1,
    'contato_comercial_publico': 1,
    'potencial_temporada': 2,
}
REDUCOES = {
    'imovel_inadequado_temporada': 3,
    'localizacao_pouco_interessante': 2,
    'anuncio_otimizado': 2,
    'sem_canal_legitimo': 3,
    'informacoes_insuficientes': 2,
}

SEGMENTOS = [
    'A. Proprietário/anunciante do imóvel',
    'B. Corretor responsável',
    'C. Imobiliária com estoque',
    'D. Proprietário que já possui Airbnb',
    'E. Oportunidade de edição de anúncio',
    'F. Oportunidade de administração completa',
]

OFERTAS = [
    'Administração de temporada',
    'Edição/otimização de anúncio Airbnb',
    'Edição de anúncio',
    'Monitoramento',
]


def score_leads(leads_path: Path):
    rows = []
    if not leads_path.exists():
        print(f'Arquivo não encontrado: {leads_path}')
        return []
    with leads_path.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)

    # Ensure columns
    for col in ['score', 'classificacao', 'segmento', 'oferta_recomendada', 'duplicado', 'hash_url']:
        if col not in fieldnames:
            fieldnames.append(col)

    seen = set()
    out = []
    for r in rows:
        url = r.get('url', '').strip()
        parsed = urlparse(url)
        url_hash = hashlib.md5((parsed.netloc + parsed.path).encode('utf-8')).hexdigest()[:10]
        r['hash_url'] = url_hash
        r['duplicado'] = 'sim' if url_hash in seen else 'nao'
        seen.add(url_hash)

        texto = f"{r.get('titulo','')} {r.get('caracteristicas','')} {r.get('justificativa','')} {url}".lower()
        score = 0
        if any(x in texto for x in ['piscina', 'piscinas']): score += SCORE_RULES['piscina']
        if any(x in texto for x in ['ar-condicionado', 'ar condicionado']): score += SCORE_RULES['ar_condicionado']
        if any(x in texto for x in ['vaga', 'garagem', 'estacionamento']): score += SCORE_RULES['estacionamento']
        if any(x in texto for x in ['quarto', 'quartos', 'suíte', 'suites', 'família', 'grupo']): score += SCORE_RULES['capacidade_grupos']
        if any(x in texto for x in ['varanda', 'área externa', 'area externa', 'jardim']): score += SCORE_RULES['area_externa']
        if any(x in texto for x in ['baixa qualidade', 'antigo', 'desatualizado', 'foto ruim']): score += SCORE_RULES['anuncio_baixa_qualidade']
        if any(x in texto for x in ['imobiliaria', 'corretor', 'anunciante']): score += SCORE_RULES['anunciante_identificavel']
        if any(x in texto for x in ['contatar', 'whatsapp', 'telefone', 'e-mail', 'email']): score += SCORE_RULES['contato_comercial_publico']
        if any(x in texto for x in ['temporada', 'locação', 'aluguel']): score += SCORE_RULES['potencial_temporada']
        if any(x in texto for x in ['comercial', 'sala', 'loja']): score += REDUCOES['imovel_inadequado_temporada']
        if any(x in texto for x in ['interior', 'rural', 'fazenda']): score += REDUCOES['localizacao_pouco_interessante']
        if any(x in texto for x in ['novo', 'recente', 'reformado']): score += REDUCOES['anuncio_otimizado']
        if not any(x in texto for x in ['contatar', 'whatsapp', 'telefone', 'e-mail', 'email', 'imobiliaria', 'anunciante']): score += REDUCOES['sem_canal_legitimo']

        r['score'] = str(score)
        r['classificacao'] = 'A' if score >= 8 else 'B' if score >= 5 else 'C'
        if 'airbnb' in url or 'airbnb' in texto:
            r['segmento'] = 'D. Proprietário que já possui Airbnb'
            r['oferta_recomendada'] = 'Edição/otimização de anúncio Airbnb'
        elif any(x in texto for x in ['temporada', 'locação', 'aluguel']):
            r['segmento'] = 'F. Oportunidade de administração completa'
            r['oferta_recomendada'] = 'Administração de temporada'
        else:
            r['segmento'] = 'A. Proprietário/anunciante do imóvel'
            r['oferta_recomendada'] = 'Administração de temporada'
        out.append(r)

    out.sort(key=lambda r: (-int(r['score']), r.get('hash_url', '')))
    with OUT_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out)
    print(f'Classificados: {len(out)} leads -> {OUT_PATH}')
    return out


if __name__ == '__main__':
    score_leads(LEADS_PATH)
