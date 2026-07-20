#!/usr/bin/env python3
"""
Plano de Assinatura para Profissionais (Proptech).
Gera pagina de planos + CSV de tiers. Reuso das ferramentas ja existentes.
Uso: python scripts/gerar_plano_assinatura.py
"""
import os, json
REPO=r"C:/Users/Carolina/praia-digital"
OUT=os.path.join(REPO,"assets/plano-assinatura.html")
CSV=os.path.join(REPO,"docs/data/planos-assinatura.csv")
TIERS=[
 {"nome":"Starter","preco":49,"publico":"Corretor autônomo","feat":["Busca Inteligente","Calculadora de ROI","Score Hermes","10 descrições/mês"]},
 {"nome":"Pro","preco":149,"publico":"Imobiliária pequena","feat":["Tudo do Starter","Gerador de descrições ilimitado","Recomendação automática","Avaliação de preço IA","White-label básico"]},
 {"nome":"Black","preco":399,"publico":"Imobiliária / rede","feat":["Tudo do Pro","White-label completo (70/30)","Assistente virtual p/ compradores","Boletim diário white-label","API de leads"]},
]
html=f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Planos Pro — Praia Digital</title>
<style>body{{font-family:Arial,sans-serif;max-width:880px;margin:auto;padding:24px;color:#112}}h1{{color:#0a3a6b;text-align:center}}
.grid{{display:flex;gap:12px;flex-wrap:wrap}}.card{{flex:1;min-width:240px;background:#f0f7ff;border:1px solid #cfe3f5;border-radius:12px;padding:1.2rem}}
.card h2{{color:#0a3a6b;margin:.2rem 0}}.preco{{font-size:1.8rem;font-weight:800;color:#0a3a6b}}.feat{{font-size:.88rem;color:#334;line-height:1.7}}
.cta{{display:inline-block;margin-top:.8rem;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.6rem 1.2rem;border-radius:9px;text-decoration:none}}
.banner{{background:linear-gradient(135deg,#1e3a8a,#0a3a6b);color:#fff;text-align:center;padding:1.2rem;border-radius:12px;margin:1.2rem 0}}
small{{color:#667}}</style></head><body>
<h1>🚀 Planos Pro para Profissionais</h1>
<p style="text-align:center;color:#445">A inteligência da Praia Digital trabalhando pela sua imobiliária — por Assinatura.</p>
<div class="grid">"""
for t in TIERS:
    html+=f"""<div class="card"><h2>{t['nome']}</h2><div class="preco">R${t['preco']}<span style="font-size:.8rem">/mês</span></div>
    <p style="color:#0369a1;font-size:.85rem">{t['publico']}</p><div class="feat">{'<br>• '.join(['']+t['feat'])}</div>
    <a class="cta" href="https://praia.digital/assets/painel-ferramentas.html">Começar →</a></div>"""
html+="""</div>
<div class="banner"><b>White-label:</b> sua marca, nossa IA. Revenue share 70% imobiliária / 30% Praia Digital. <a href="https://praia.digital/assets/painel-ferramentas.html" style="color:#4ade80;font-weight:800">Saiba mais →</a></div>
<p style="font-size:.8rem;color:#667">Praia Digital · 1ª Plataforma Brasileira de Inteligência Imobiliária</p></body></html>"""
os.makedirs(os.path.dirname(OUT),exist_ok=True)
open(OUT,"w",encoding="utf-8").write(html)
import csv
open(CSV,"w",encoding="utf-8-sig",newline="").write("plano,preco_mensal,publico\n"+ "\n".join(f"{t['nome']},{t['preco']},{t['publico']}" for t in TIERS))
print(f"Plano assinatura: {OUT} | 3 tiers | CSV: {CSV}")
