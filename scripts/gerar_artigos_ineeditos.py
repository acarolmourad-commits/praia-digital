#!/usr/bin/env python3
"""
Artigos SEO INEDITOS (sem duplicar os 1300 ja publicados).
Verifica titulos existentes e gera apenas os ausentes. Angulos novos:
comparativo 2026-2027, IR, sucessao, nomadismo, multi-proprietario, etc.
Uso: python scripts/gerar_artigos_ineeditos.py [--dry]
"""
import os, glob, re
REPO=r"C:/Users/Carolina/praia-digital"
BLOG=os.path.join(REPO,"blog")
EXIST=set()
for f in glob.glob(os.path.join(BLOG,"*.html")):
    EXIST.add(os.path.basename(f).replace('.html','').lower())
ARTIGOS=[
 ("imposto-de-renda-aluguel-temporada-2026-guia", "Imposto de Renda no Aluguel por Temporada 2026: guia do proprietário","Receita de Airbnb/Booking entra no IRPF. Veja carnê-leão, deduzões e como a Precificação Dinâmica impacta o lucro líquido declarável."),
 ("comprar-imovel-praia-2026-vs-2027", "Comprar imóvel na praia em 2026 ou esperar 2027?","Análise de juros, valorização e janela de entrada. Use a Calculadora de Rentabilidade para projetar os dois cenários."),
 ("multi-proprietario-gestao-temporada", "Como dividir a gestão de imóvel na praia entre irmãos/sócios","Governança, contrato e Gestão Completa para evitar conflito. Score Hermes ajuda a decidir se vale o ativo."),
 ("nomadismo-digital-morar-litoral-sp", "Nomadismo digital no litoral de SP: onde ficar e por que","Conectividade, custo de vida e ROI de curto prazo em Santos, Ubatuba e Caraguatuba."),
 ("reforma-pequena-retorno-temporada", "Reforma de R$ 5 mil que aumenta 20% o yield do seu imóvel","Antes/depois: iluminação, cama e fotos. Geração automática de descrições valoriza o anúncio."),
 ("quando-vender-imovel-temporada-lucro", "Quando vender seu imóvel de temporada pelo maior lucro","Sazonalidade, sinal de saturação e comparativo com manter na Gestão Completa."),
 ("inadimplencia-temporada-como-evitar", "Inadimplência no aluguel por temporada: como eliminar","Caução, seguro e triagem. Assistente virtual qualifica o hóspede antes da reserva."),
 ("investidor-fora-sp-comprar-litoral", "Investidor de fora de SP: guia para comprar no litoral paulista","Remoto, PGTO internacional, gestão zero horas. Busca Inteligente filtra por cidade e preço."),
 ("condominio-alto-padrao-yield", "Condomínio de alto padrão vale a pena para renda?","Compare yield bruto vs taxa de condomínio. Comparador Inteligente decide."),
 ("airbnb-vs-booking-litoral-sp", "Airbnb ou Booking no litoral SP: onde seu imóvel vende mais","Comissões, perfil de hóspede e ocupação. Recomendação automática cruza os dois."),
 ("primeira-renda-temporada-passos", "Primeira renda com temporada em 30 dias: passo a passo","Do cadastro à primeira reserva. Avaliação de preço IA define a diária inicial."),
 ("mercado-inverno-litoral-oportunidade", "Inverno no litoral: a oportunidade de compra escondida","Baixa temporada = preço de imóvel menor. Simulador projeta payback com ocupação anual."),
]
def slugify(s): return s
def gerar(dry=False):
    n=0
    for slug,titulo,resumo in ARTIGOS:
        if slug.lower() in EXIST:
            continue
        if dry: print(f"[DRY] {slug}"); n+=1; continue
        html=f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo} — Praia Digital</title><meta name="description" content="{resumo}">
<style>body{{font-family:Arial,sans-serif;max-width:720px;margin:auto;padding:22px;color:#112}}h1{{color:#0a3a6b}}
p{{line-height:1.7;color:#223}}.cta{{display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.6rem 1.2rem;border-radius:9px;text-decoration:none;margin-top:1rem}}small{{color:#667}}</style></head><body>
<h1>{titulo}</h1><p>{resumo}</p>
<p>Este é um artigo otimizado da Praia Digital, parte da série "Diário do Hermes". Para decisão completa, use nossas ferramentas de inteligência imobiliária.</p>
<p style="text-align:center"><a class="cta" href="https://praia.digital/assets/painel-ferramentas.html">Abrir Painel de Ferramentas →</a></p>
<p style="font-size:.8rem;color:#667">Praia Digital · 1ª Plataforma Brasileira de Inteligência Imobiliária</p></body></html>"""
        open(os.path.join(BLOG,f"{slug}.html"),"w",encoding="utf-8").write(html)
        n+=1
    print(f"{'DRY: ' if dry else ''}{n} artigos ineditos criados")
if __name__=="__main__":
    import sys; gerar(dry="--dry" in sys.argv)
