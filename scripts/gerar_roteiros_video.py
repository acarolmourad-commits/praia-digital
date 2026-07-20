#!/usr/bin/env python3
"""
Roteiros de Video Diario (Proptech) — serie "Diario do Hermes".
Gera 14 roteiros INEDITOS (titulos nao existem no blog). Cada um: hook, pontos, CTA.
Uso: python scripts/gerar_roteiros_video.py
"""
import os, json
REPO=r"C:/Users/Carolina/praia-digital"
OUT=os.path.join(REPO,"docs/content/roteiros-video-diario.json")
ROTEIROS=[
 ("Por que Santos lidera o yield de temporada em 2026","Santos tem 103 artigos de mercado e yield medio forte. Mostro 3 bairros com melhor ROI.","Busca Inteligente"),
 ("Airbnb ou aluguel anual? A matematica que decide","Compare receita de temporada vs longo usando a Calculadora de Rentabilidade.","Calculadora de Rentabilidade"),
 ("O erro de precificacao que custa 30% da sua receita","Donos autogestos erram a diaria. Precificacao dinamica resolve.","Score Hermes"),
 ("Como o Score Hermes avalia seu imovel em 10 segundos","ROI 40%, Yield 30%, Demanda 20%, bonus 10%.","Score Hermes"),
 ("3 cidades do litoral SP subvalorizadas agora","Riviera, Caraguatuba e Mongagua com atencao alta e preco still baixo.","Busca Inteligente"),
 ("Financiar o imovel de praia: a parcela come o aluguel?","Simulador mostra quando o ROI cobre a prestacao.","Simulador de Financiamento"),
 ("Kitnet na praia: o menor investimento com maior multiplicador","Multiplicador 1.7-2.3x sobre aluguel longo.","Calculadora de Rentabilidade"),
 ("Comparador Inteligente: qual imovel escolher?","3 opcoes lado a lado por ROI e payback.","Comparador Inteligente"),
 ("Gestao Completa: voce ganha sem trabalhar 1 hora","Limpeza, check-in e precificacao por IA.","Painel de Ferramentas"),
 ("Avaliacao de preco por IA vs avaliador humano","Diferencas e quando usar cada um.","Avaliacao de Preco"),
 ("Assistente virtual para compradores: como funciona","Triagem 24/7 qualificando leads.","Painel de Ferramentas"),
 ("Gerador de descricoes: anuncio que vende em 1 clique","Copy convertido por IA, pronto para Airbnb.","Gerador de Descricoes"),
 ("Recomendacao automatica de imoveis para o cliente","Match por perfil e orcamento.","Recomendacao Automatica"),
 ("Boletim diario: sua vantagem competitiva","Toda manha: ranking de cidades e oportunidades.","Boletim Diario"),
]
def gerar():
    itens=[]
    for i,(titulo,corpo,ferramenta) in enumerate(ROTEIROS,1):
        itens.append({"dia":i,"titulo":titulo,"hook":f"{titulo.split('?')[0] if '?' not in titulo else titulo[:30]}...",
                      "roteiro":[f"Hook (0-3s): {titulo}",f"Conteudo (3-40s): {corpo}",
                      f"Prova: abra a {ferramenta} ao vivo","CTA (40-60s): 'Link na bio — simule o seu.'"],
                      "ferramenta":ferramenta})
    os.makedirs(os.path.dirname(OUT),exist_ok=True)
    json.dump({"serie":"Diario do Hermes","total":len(itens),"roteiros":itens},open(OUT,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
    print(f"Roteiros video: {OUT} | {len(itens)} ineditos")
if __name__=="__main__": gerar()
