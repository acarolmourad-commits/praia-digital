#!/usr/bin/env python3
"""
agendar_followup_automacao.py
Gera follow-ups automáticos para o lote de automação do dia e atualiza o tracker.
Uso: python scripts/automation/agendar_followup_automacao.py
"""

import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
ENTRADA = BASE / "docs/sales/csv-lotes-b2b/lote-b2b-automacao-2026-07-22.csv"
SAIDA_PAIRS = BASE / "docs/sales/csv-lotes-b2b/followup-pairs-automacao-2026-07-22.csv"
SAIDA_TRACKER = BASE / "docs/sales/csv-lotes-b2b/tracker-automacao-2026-07-22.csv"
DATA_REF = date(2026, 7, 22)


def mascarar(v):
    s = str(v or "").strip()
    if not s:
        return s
    if len(s) > 6:
        return s[:2] + "****" + s[-2:]
    return "****"


def main():
    if not ENTRADA.exists():
        print(f"Arquivo não encontrado: {ENTRADA}")
        return
    rows = []
    with ENTRADA.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows.extend(reader)
    if not rows:
        print("Lote vazio.")
        return

    pairs = []
    tracker = []
    for r in rows:
        tel = r.get("Telefone", "").strip()
        nome = r.get("Nome", "").strip()
        cidade = r.get("Cidade", "").strip()
        if not tel or not nome:
            continue
        base_id = f"automacao-{tel}".replace("+", "").replace(" ", "")
        msg1_tpl = (
            "Olá {nome}! Tudo bem? Sou da Praia Digital. "
            "Automatizamos e-mails, atendimento e prospecção para imobiliárias em {cidade} — "
            "menos trabalho repetitivo, mais leads qualificados. Quer ver como funciona na prática?"
        )
        msg2_tpl = (
            "{nome}, seguindo nosso papo: sem compromisso, posso enviar uma proposta objetiva de automação "
            "para a operação de {cidade}?"
        )
        msg3_tpl = (
            "{nome}, encerrando este ciclo por aqui. Quando quiser testar a automação na prática, "
            "é só chamar no (11) 95434-6288 ou responder por aqui."
        )
        q1 = DATA_REF.strftime("%Y-%m-%dT09:00:00")
        q2 = (DATA_REF + timedelta(days=2)).strftime("%Y-%m-%dT09:00:00")
        q3 = (DATA_REF + timedelta(days=5)).strftime("%Y-%m-%dT09:00:00")
        pairs.append({
            "id": base_id,
            "nome": nome,
            "cidade": cidade,
            "telefone": mascarar(tel),
            "telefone_raw": tel,
            "q1_em": q1,
            "msg1": msg1_tpl.format(nome=nome.split()[0], cidade=cidade),
            "q2_em": q2,
            "msg2": msg2_tpl.format(nome=nome.split()[0], cidade=cidade),
            "q3_em": q3,
            "msg3": msg3_tpl.format(nome=nome.split()[0], cidade=cidade),
        })
        tracker.append({
            "id": base_id,
            "nome": nome,
            "imobiliaria": r.get("Imobiliaria", ""),
            "telefone": tel,
            "cidade": cidade,
            "q1_em": q1,
            "q2_em": q2,
            "q3_em": q3,
            "status": "pendente_q1",
            "servico": "automacao",
        })

    with SAIDA_PAIRS.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "nome", "cidade", "telefone", "telefone_raw", "q1_em", "msg1", "q2_em", "msg2", "q3_em", "msg3"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(pairs)

    with SAIDA_TRACKER.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["id", "nome", "imobiliaria", "telefone", "cidade", "q1_em", "q2_em", "q3_em", "status", "servico"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(tracker)

    print("Pares:")
    print(f" - {SAIDA_PAIRS}")
    print(f" - {len(pairs)} follow-ups")
    print("Tracker:")
    print(f" - {SAIDA_TRACKER}")
    status_counter = Counter(r.get("status", "") for r in tracker)
    print("Status:")
    for k, v in status_counter.most_common():
        print(f"  - {k or 'vazio'}: {v}")


if __name__ == "__main__":
    main()
