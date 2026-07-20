#!/usr/bin/env python3
"""
Newsletter Semanal automatica (Proptech).
Compila: top3 cidades do boletim + 1 imovel em destaque (cadastro real) + 1 dica.
Reusa sinais reais. Gera assets/newsletter-semanal.html + arquivo.
Uso: python scripts/gerar_newsletter_semanal.py
"""
import os, glob, csv, json
from collections import Counter
from datetime import date, timedelta
REPO=r"C:/Users/Carolina/praia-digital"
BLOG=os.path.join(REPO,"blog");OUT=os.path.join(REPO,"assets/newsletter-semanal.html")
LIT=["Bertioga","Guarujá","Santos","Praia Grande","São Vicente","Mongaguá","Itanhaém","Peruíbe","Ilhabela","São Sebastião","Caraguatatuba","Ubatuba","Riviera de São Lourenço"]
def top_cidades():
    c=Counter()
    for f in glob.glob(os.path.join(BLOG,"*.html")):
        t=open(f,encoding="utf-8",errors="ignore").read().lower()
        for cid in LIT:
            if cid.lower() in t: c[cid]+=1
    return c.most_common(3)
def destaque():
    p=os.path.join(REPO,"propriedades/cadastro-imoveis.csv")
    if not os.path.exists(p): return None
    r=list(csv.DictReader(open(p,encoding="utf-8-sig")))
    return r[0] if r else None
def gerar():
    hoje=date.today(); sem=hoje-timedelta(days=7)
    top=top_cidades(); d=destaque()
    top_html="".join(f"<li><b>{c}</b> — {v} menções no blog (atenção de mercado)</li>" for c,v in top)
    dest=f"<li><b>{d['titulo']}</b> — {d['cidade']}, R${int(d['preco']):,}, {d['dormitorios']}q. <a href='https://praia.digital/assets/busca-inteligente.html'>Ver na Busca →</a></li>" if d else "<li>Em breve.</li>"
    html=f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Newsletter Semanal — Praia Digital</title><style>body{{font-family:Arial,sans-serif;max-width:620px;margin:auto;padding:20px;color:#112}}h1{{color:#0a3a6b}}
.card{{background:#f0f7ff;border:1px solid #cfe3f5;border-radius:12px;padding:1rem;margin:.8rem 0;line-height:1.7}}li{{margin:.3rem 0;color:#334}}
.cta{{display:inline-block;background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:800;padding:.6rem 1.2rem;border-radius:9px;text-decoration:none}}small{{color:#667}}</style></head><body>
<h1>📬 Newsletter Semanal — Praia Digital</h1>
<p><span style="background:linear-gradient(90deg,#22d3ee,#4ade80);color:#04141f;font-weight:700;padding:.2rem .7rem;border-radius:999px;font-size:.75rem">{hoje:%d/%m/%Y}</span> Resumo de {sem:%d/%m} a {hoje:%d/%m}.</p>
<div class="card"><b>🔥 Cidades em alta esta semana</b><ul>{top_html}</ul></div>
<div class="card"><b>🏠 Imóvel em destaque</b><ul>{dest}</ul></div>
<div class="card"><b>💡 Dica do Hermes</b> Compare sempre o yield de temporada com o aluguel longo antes de comprar — use a Calculadora de Rentabilidade.</div>
<p style="text-align:center"><a class="cta" href="https://praia.digital/assets/painel-ferramentas.html">Abrir Painel de Ferramentas →</a></p>
<p style="font-size:.8rem;color:#667">Praia Digital · 1ª Plataforma Brasileira de Inteligência Imobiliária</p></body></html>"""
    open(OUT,"w",encoding="utf-8").write(html)
    print(f"Newsletter: {OUT} | Top: {top}")
if __name__=="__main__": gerar()
