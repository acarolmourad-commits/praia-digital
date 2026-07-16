#!/usr/bin/env python3
"""
INGESTÃO DE HISTÓRICO INTERNO — Calculadora de Yield Preditivo por CEP
Pré-requisito do MVP: a calculadora PRECISA de ocupação/ADR reais por micro-região.

Este script é o ESQUELETO de ingestão. Ele define o schema de entrada esperado
(de onde virão os dados reais do PMS / planilha de reservas da Praia Digital) e
gera o cache `historico_interno_cep.json` que o endpoint /api/v1/yield/estimate consome.

FONTE ESPERADA (preencher com dados reais do PMS):
  arquivo CSV em docs/data/reservas-internas.csv com colunas:
    cep, tipo, quartos, adr_medio, ocupacao, n_noites_ano, receita_ano, período_inicio, período_fim
  Exemplo de 1 linha:
    11010-000,apartamento,2,320.50,0.68,182,58331.00,2025-01-01,2025-12-31

Se não houver dados reais ainda, o script gera um CACHE VAZIO e a calculadora
cai no modo "estimativa base" (menor confiança) usando só ViaCEP + feriados.

Uso: python scripts/ingest_historico_interno.py
"""
import csv, json, os
from collections import defaultdict
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
SRC = os.path.join(REPO, "docs/data/reservas-internas.csv")
OUT = os.path.join(REPO, "docs/data/historico_interno_cep.json")

def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cache = defaultdict(list)
    if os.path.exists(SRC):
        with open(SRC, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                cep = r["cep"].strip()
                try:
                    cache[cep].append({
                        "tipo": r["tipo"],
                        "quartos": int(r["quartos"]),
                        "adr_medio": float(r["adr_medio"]),
                        "ocupacao": float(r["ocupacao"]),
                        "receita_ano": float(r["receita_ano"]),
                        "periodo": f'{r["período_inicio"]}..{r["período_fim"]}',
                    })
                except (ValueError, KeyError) as e:
                    print(f"linha ignorada ({cep}): {e}")
        # agrega por CEP (média ponderada por receita)
        agg = {}
        for cep, regs in cache.items():
            tot = sum(x["receita_ano"] for x in regs) or 1
            agg[cep] = {
                "amostras": len(regs),
                "adr_medio": round(sum(x["adr_medio"]*x["receita_ano"] for x in regs)/tot, 2),
                "ocupacao": round(sum(x["ocupacao"]*x["receita_ano"] for x in regs)/tot, 3),
                "receita_ano_media": round(tot/len(regs), 2),
            }
        status = f"{len(agg)} CEPs agregados a partir de {sum(len(v) for v in cache.values())} registros"
    else:
        agg = {}
        status = "SEM FONTE — cache vazio; calculadora usará modo 'estimativa base'"

    json.dump({"gerado_em": date.today().isoformat(), "por_cep": agg},
              open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"[{status}]\nCache: {OUT}")

if __name__ == "__main__":
    main()
