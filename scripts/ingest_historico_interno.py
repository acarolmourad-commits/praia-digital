#!/usr/bin/env python3
"""
INGESTÃO DE HISTÓRICO INTERNO — Calculadora de Yield Preditivo por CEP
Pré-requisito para modo 'precisao_interna': a calculadora precisa de
ocupação/ADR reais por CEP. Esses dados vêm dos CONTRATOS DE GESTÃO da Praia
Digital (PMS / planilha de reservas) — não de API pública (ViaCEP só dá geografia;
FipeZap está bloqueada; AirDNA é paga).

FORMATOS DE ENTRADA ACEITOS (docs/data/reservas-internas.csv):
  A) Por reserva:
     cep, tipo, quartos, adr_medio, ocupacao, n_noites_ano, receita_ano, periodo_inicio, periodo_fim
  B) Por contrato de gestão (mais simples de exportar do PMS):
     cep, tipo, quartos, adr_medio, ocupacao_anual, receita_ano
  Em ambos, ocupacao em 0..1 (ex: 0.68). adr_medio e receita_ano em R$.

Saída: docs/data/historico_interno_cep.json consumido por /api/v1/yield/estimate.

Uso:
  python scripts/ingest_historico_interno.py            # gera cache do CSV real
  python scripts/ingest_historico_interno.py --template # cria planilha vazia p/ equipe preencher
  python scripts/ingest_historico_interno.py --demo     # 1 linha sintética (modo demonstrativo, marcada)
"""
import csv, json, os, sys
from collections import defaultdict
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
SRC = os.path.join(REPO, "docs/data/reservas-internas.csv")
OUT = os.path.join(REPO, "docs/data/historico_interno_cep.json")
COLS = ["cep", "tipo", "quartos", "adr_medio", "ocupacao", "n_noites_ano",
        "receita_ano", "periodo_inicio", "periodo_fim"]

def gerar_template():
    p = SRC
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        # 3 linhas-exemplo comentadas via # não roda em CSV; deixamos cabeçalho + 1 linha guia
        w.writerow(["11010-000", "apartamento", 2, 320.50, 0.68, 182, 58331.00, "2025-01-01", "2025-12-31"])
    print(f"Template criado: {p}\nPreencha com os contratos reais de gestão da Praia Digital (1 linha por imóvel/ano).")

def main(demo=False):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cache = defaultdict(list)
    if demo:
        regs = [{"cep": "11010-000", "tipo": "apartamento", "quartos": 2,
                 "adr_medio": 459.0, "ocupacao": 0.73, "receita_ano": 122000.0,
                 "periodo": "DEMO"}]
        print("MODO DEMO (sintético) — NÃO usar em produção.")
    elif os.path.exists(SRC):
        regs = []
        with open(SRC, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                try:
                    regs.append({
                        "cep": r["cep"].strip(),
                        "tipo": r["tipo"].strip(),
                        "quartos": int(r["quartos"]),
                        "adr_medio": float(r["adr_medio"]),
                        "ocupacao": float(r["ocupacao"]),
                        "receita_ano": float(r.get("receita_ano") or r.get("receita_ano_anual") or 0),
                        "periodo": f'{r.get("periodo_inicio","")}..{r.get("periodo_fim","")}',
                    })
                except (ValueError, KeyError) as e:
                    print(f"linha ignorada ({r.get('cep','?')}): {e}")
    else:
        regs = []

    for x in regs:
        cache[x["cep"]].append(x)

    if cache:
        agg = {}
        for cep, rs in cache.items():
            tot = sum(x["receita_ano"] for x in rs) or 1
            agg[cep] = {
                "amostras": len(rs),
                "adr_medio": round(sum(x["adr_medio"]*x["receita_ano"] for x in rs)/tot, 2),
                "ocupacao": round(sum(x["ocupacao"]*x["receita_ano"] for x in rs)/tot, 3),
                "receita_ano_media": round(tot/len(rs), 2),
                "demo": demo,
            }
        status = f"{len(agg)} CEPs agregados de {sum(len(v) for v in cache.values())} registros | modo=precisao_interna"
    else:
        agg = {}
        status = "SEM FONTE — cache vazio; calculadora usará modo 'estimativa base'"

    json.dump({"gerado_em": date.today().isoformat(), "por_cep": agg},
              open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"[{status}]\nCache: {OUT}")

if __name__ == "__main__":
    if "--template" in sys.argv:
        gerar_template()
    else:
        main(demo="--demo" in sys.argv)
