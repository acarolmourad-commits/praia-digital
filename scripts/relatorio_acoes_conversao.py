#!/usr/bin/env python3
"""Relatorio de ACOES DE CONVERSAO (fechamento do lacuna do funil).
Lista leads que responderam (acao: enviar Msg2.5 + landing) e que fecharam
(acao: enviar Msg4 + onboarding) e ainda nao tiveram a acao registrada.
Le os trackers WPP+e-mail (coluna Acao_Conversao)."""
import csv, os
from datetime import date
REPO = r"C:/Users/Carolina/praia-digital"
DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
TRACKERS = {"WhatsApp": os.path.join(DIR,"tracker-whatsapp-proprietarios.csv"),
            "E-mail": os.path.join(DIR,"tracker-email-proprietarios.csv")}
FEITO = {"msg25_feita","onboarding_feito"}

def main():
    saida = []
    total_pendentes = 0
    for canal, arq in TRACKERS.items():
        if not os.path.exists(arq): continue
        resp, fech = [], []
        for r in csv.DictReader(open(arq, encoding="utf-8-sig"), delimiter=";"):
            ac = r.get("Acao_Conversao","")
            if r["Status"] == "respondeu" and ac != "msg25_feita":
                resp.append(r)
            if r["Status"] == "fechou" and ac != "onboarding_feito":
                fech.append(r)
        if not resp and not fech: continue
        saida.append(f"\n### {canal}")
        if resp:
            saida.append(f"📨 Responderam — enviar Msg2.5 (prova ROI) + link retorno-gestao-completa.html ({len(resp)}):")
            for r in resp:
                saida.append(f"  • {r['Nome']} ({r['Cidade']}) — {r.get('Telefone') or r.get('Email')}")
        if fech:
            saida.append(f"🎉 Fechados — enviar Msg4 (onboarding) + link onboarding-proprietario.html ({len(fech)}):")
            for r in fech:
                saida.append(f"  • {r['Nome']} ({r['Cidade']}) — {r.get('Telefone') or r.get('Email')}")
        total_pendentes += len(resp) + len(fech)
    print(f"=== Ações de Conversão — {date.today():%d/%m/%Y} ===")
    if saida:
        print("\n".join(saida))
        print("\nApós enviar, marque: python scripts/marcar_acao_conversao.py --canal <wpp|email> --lote <N> --nome \"X\" --acao <msg25_feita|onboarding_feito>")
        print("Réplicas de objeção: outreach/objecoes-proprietarios.md")
        print("Simulador interativo p/ lead: assets/simulador-roi-proprietario.html")
    else:
        print("Nenhuma ação de conversão pendente. 🎯")

if __name__ == "__main__":
    main()
