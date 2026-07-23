#!/usr/bin/env python3
"""
gerador_posts_sociais.py
Gera posts automáticos para Instagram/TikTok/Facebook baseados no portfólio.
Uso: python litoral-prime-imoveis/automation/gerador_posts_sociais.py
"""
import json
import random
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
PORTFOLIO = BASE / 'imoveis/portfolio.json'
OUTPUT_DIR = BASE / 'docs/posts'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES = [
    "🏖️ {titulo} por {preco} em {cidade}/{bairro}.\n\nLocalização privilegiada, acabamento de alto padrão. Agende sua visita!\n\n📞 WhatsApp: (11) 95434-6288\n🌐 Site: litoralprime.com.br\n\n#LitoralPrime #ImoveisLitoralSP #Santos #Guaruja #PraiaGrande #Bertioga #Itanhaem #Mongagua #SaoVicente #Peruibe",
    "🔥 Oportunidade única! {titulo}\n📍 {cidade}/{bairro}\n💰 {preco}\n\nPerfeito para quem busca qualidade e localização. Clique no link da bio para agendar!\n\n#Imoveis #LitoralSP #Investimento #Praia",
    "🏠 Novo imóvel disponível! {titulo}\n📍 {cidade}/{bairro}\n💲 {preco}\n\nAgende uma visita virtual ou presencial. Vamos realizar seu sonho!\n\n📲 (11) 95434-6288\n\n#ImovelNovo #LitoralPrime #SaoPaulo",
    "🌊 Viva no litoral de SP! {titulo}\n📍 {cidade}/{bairro}\n💼 {preco}\n\nCondições especiais de lançamento. Consulte-nos!\n\n#Litoral #Imoveis #Praia #Investimento #SaoPaulo",
]

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_post(imovel):
    template = random.choice(TEMPLATES)
    titulo = imovel.get("titulo", "Imóvel")
    preco = formatar_moeda(imovel.get("preco", 0))
    cidade = imovel.get("cidade", "")
    bairro = imovel.get("bairro", "")
    return template.format(titulo=titulo, preco=preco, cidade=cidade, bairro=bairro)

def main():
    if not PORTFOLIO.exists():
        print("[Litoral Prime] Portfólio não encontrado.")
        return
    
    with PORTFOLIO.open(encoding='utf-8') as f:
        imoveis = json.load(f)
    
    hoje = datetime.now().strftime('%Y-%m-%d')
    posts_gerados = []
    
    for imovel in imoveis:
        post = gerar_post(imovel)
        posts_gerados.append(post)
    
    # Salvar posts do dia
    output_file = OUTPUT_DIR / f"posts-{hoje}.txt"
    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"Posts gerados em {hoje}\n")
        f.write("="*60 + "\n\n")
        for i, post in enumerate(posts_gerados, 1):
            f.write(f"Post {i}:\n{post}\n\n")
            f.write("-"*60 + "\n\n")
    
    print(f"[Litoral Prime] {len(posts_gerados)} posts gerados para {hoje}")
    print(f"Arquivo: {output_file}")
    return posts_gerados

if __name__ == '__main__':
    main()
