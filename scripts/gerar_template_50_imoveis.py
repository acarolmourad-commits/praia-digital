#!/usr/bin/env python3
"""Gera template de importacao em massa com 50 imoveis (TEMPLATE, nao real).
Ids a partir de 3000 para nao colidir com os 60 reais (1001-1060).
Serve ao foco 'cadastrar muitos imoveis'. Uso: python scripts/gerar_template_50_imoveis.py
"""
import os, csv, random
REPO=r"C:/Users/Carolina/praia-digital"
OUT=os.path.join(REPO,"propriedades/modelo-importacao-50-imoveis.csv")
CITIES=["Santos","Guarujá","Praia Grande","Bertioga","São Vicente","Ubatuba","Ilhabela","Caraguatatuba","Itanhaém","Peruíbe","Mongaguá"]
TIPOS=["apartamento","casa","cobertura","studio","kitnet"]
random.seed(42)
rows=[]
for i in range(50):
    cid=random.choice(CITIES); tp=random.choice(TIPOS); q=random.randint(1,4)
    preco=random.randint(18,220)*10000
    area=30+q*random.randint(12,28)
    rows.append([3000+i, f"{tp.title()} {q}q em {cid}", cid, tp, preco, q, area,
                 f"Oportunidade de {tp} no litoral paulista. {q} dormitórios, {area}m², localização privilegiada em {cid}."])
with open(OUT,"w",encoding="utf-8-sig",newline="") as f:
    w=csv.writer(f); w.writerow(["id","titulo","cidade","tipo","preco","dormitorios","area","descricao"]); w.writerows(rows)
print(f"Template 50 imoveis: {OUT} (TEMPLATE — substitua por dados reais)")
