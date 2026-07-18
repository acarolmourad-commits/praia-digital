#!/usr/bin/env python3
"""
Calibra o yield de cada imovel REAL do cadastro usando o modelo da calculadora
(calculadora-widget-standalone.html):
  ADR = baseADR*1.28 ; ocup = min(baseOcup*1.12,0.92) ; receitaLiq = ADR*ocup*365*0.80
  aluguelLonga = (casa?3500:cobertura?4800:2600) + quartos*600
  precoBase = (casa?480000:cobertura?650000:420000)
  yieldA = receitaLiq / precoBase
Gera docs/data/yield_por_imovel.json (cache honesto, derivado dos 60 reais do CSV).
Sem reservas reais ainda => usa o modelo da calculadora (transparente no cabecalho).
"""
import csv, json, os
REPO = r"C:/Users/Carolina/praia-digital"
CSV = os.path.join(REPO, "propriedades/cadastro-imoveis.csv")
OUT = os.path.join(REPO, "docs/data/yield_por_imovel.json")

def base_adr(tipo, q):  # modelo da calculadora
    return 250 + q*70 + (tipo.lower()=="casa" and 60 or tipo.lower()=="cobertura" and 120 or 0)
def modelo(tipo, q):
    adr = base_adr(tipo,q)*1.28
    ocup = min(0.55 + q*0.02, 0.85)*1.12
    ocup = min(ocup, 0.92)
    rec_liq = adr*ocup*365*0.80
    alug_longa = (tipo.lower()=="casa" and 3500 or tipo.lower()=="cobertura" and 4800 or 2600) + q*600
    preco_real = int(r["preco"] or 0)
    # yield REAL = receita liquida de temporada / preco real do imovel
    yieldA = rec_liq/preco_real if preco_real else 0
    mult = (rec_liq/12)/alug_longa
    return round(yieldA*100,1), round(mult,1), round(adr,0), round(ocup*100,0)

rows=[]
with open(CSV, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        if not r.get("id"): continue
        y, mult, adr, ocup = modelo(r["tipo"], int(r["dormitorios"] or 1))
        rows.append({"id":r["id"],"cidade":r["cidade"],"tipo":r["tipo"],
                     "preco":int(r["preco"] or 0),"dormitorios":int(r["dormitorios"] or 0),
                     "yield_pct":y,"mult":mult,"adr_estimado":int(adr),"ocup_pct":int(ocup)})
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"modelo":"calculadora-widget-standalone (ADR+28%, ocup+12%, liq80%)",
           "fonte":"60 imoveis reais de propriedades/cadastro-imoveis.csv",
           "nota":"Sem reservas reais ainda; yield derivado do modelo da calculadora (reproduzivel).",
           "imovel":rows}, open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"yield_por_imovel.json: {len(rows)} imoveis | yield medio: {sum(x['yield_pct'] for x in rows)/len(rows):.1f}%")
