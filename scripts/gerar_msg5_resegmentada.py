#!/usr/bin/env python3
"""
Expansao H — Re-segmentacao de follow-up (Msg5 inteligente por sinal).
Para leads B2C WPP que chegaram em Msg3 (encerramento) sem resposta, gera Msg5
variando por micro-segmento deduzido do Status/Obs do tracker. Reusa o padrao B2C.

Micro-segmentos:
  - 'preco': mencionou preco/duvida de ROI -> Msg5 foca em simulacao de ROI
  - 'tempo': mencionou falta de tempo -> Msg5 foca em zero horas
  - 'desconfia': resposta negativa leve -> Msg5 foca em prova/transparencia
  - default: ultima chance curta

Uso: python scripts/gerar_msg5_resegmentada.py
"""
import csv, os, re
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-email/tracker-whatsapp-proprietarios.csv")
OUT = os.path.join(REPO, "docs/sales/csv-lotes-whatsapp", "lote-msg5-resegmentada-2026-07-16.csv")

def seg(r):
    txt = f"{r.get('Obs','')} {r.get('Resposta','')}".lower()
    if re.search(r"preço|preco|valor|roi|caro|quanto", txt): return "preco"
    if re.search(r"tempo|ocupad|correria|nao tenho", txt): return "tempo"
    if re.search(r"nao|depois|não|obrigad", txt): return "desconfia"
    return "default"

def msg5(nome, regiao, s):
    if s == "preco":
        return (f"{nome}, última tentativa e vou te deixar em paz 😉 — mas antes: eu simulo o ROI do SEU "
                 f"imóvel em {regiao} sem custo. Você me diz quartos + bairro e eu te mostro quanto pode "
                 f"render/mês com Gestão Completa (muitos donos subestimam em 40%+). topa?")
    if s == "tempo":
        return (f"{nome}, sei que o tempo é curto. Por isso a Praia Digital existe: a gente faz TUDO "
                 f"(limpeza, check-in, preço) e você ganha mais trabalhando zero horas no {regiao}. "
                 f"Se um dia quiser, é 1 ligação e a gente assume. Abraço!")
    if s == "desconfia":
        return (f"{nome}, tranquilo, sem pressão. Só pra você saber: trabalhamos com relatório mensal "
                 f"de receita e contrato sem fidelidade no {regiao}. Quando quiser testar, a porta tá aberta. "
                 f"Um abraço!")
    return (f"{nome}, não vou insistir — mas fica o convite: a Praia Digital cuida de TUDO no seu imóvel "
            f"em {regiao} e você ganha mais trabalhando zero horas. Se um dia fizer sentido, é só me avisar. "
            f"Bom proveito! 🤝")

def main():
    rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    out = []
    for r in rows:
        # alvo: chegou em msg3/encerrado sem fechar e sem resposta positiva
        if r.get("Status") in ("msg3_enviada", "encerrado", "sem_interesse") and not r.get("Acao_Conversao"):
            s = seg(r)
            out.append({"Nome": r["Nome"], "Telefone": r["Telefone"], "Cidade": r["Cidade"],
                        "Segmento": s, "Status": "pendente_msg5",
                        "Msg5_Resegmentada": msg5(r["Nome"], r["Cidade"], s)})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["Nome", "Telefone", "Cidade", "Segmento", "Status", "Msg5_Resegmentada"], delimiter=";")
        w.writeheader(); w.writerows(out)
    print(f"Msg5 re-segmentada: {OUT}\n{len(out)} leads B2C WPP para última chance inteligente.")

if __name__ == "__main__":
    main()
