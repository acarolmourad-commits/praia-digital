#!/usr/bin/env python3
"""
Captura de lead da Calculadora Yield-CEP -> tracker do outbound.
Grava no tracker-whatsapp-proprietarios.csv com Status=pendente_msg1 e origem=calc-cep,
para o cron das 18h disparar a sequencia de 3 msgs automaticamente (zero acao manual).

Schema do tracker: Lote,Nome,Telefone,Cidade,Data_Msg1,Status,Resposta,Valor_Estimado,Obs,Acao_Conversao
"""
import csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
TRACKER = os.path.join(REPO, "docs/sales/csv-lotes-email/tracker-whatsapp-proprietarios.csv")
TRACKER_WL = os.path.join(REPO, "docs/sales/csv-lotes-b2b/tracker-whitelabel.csv")
CAMPOS = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status",
          "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao"]

def capturar(nome, telefone, cidade, cep=None, yield_estimado=None,
             email=None, consentimento_lgpd=False, parceiro_id=None):
    if not consentimento_lgpd:
        raise ValueError("LGPD: consentimento obrigatorio")
    if not (nome and telefone):
        raise ValueError("nome e whatsapp obrigatorios")
    os.makedirs(os.path.dirname(TRACKER), exist_ok=True)
    rows = []
    if os.path.exists(TRACKER):
        rows = list(csv.DictReader(open(TRACKER, encoding="utf-8-sig"), delimiter=";"))
    # idempotencia: nao duplicar mesmo telefone ja existente
    tel_norm = "".join(filter(str.isdigit, telefone))
    for r in rows:
        if "".join(filter(str.isdigit, r.get("Telefone", ""))) == tel_norm:
            return {"status": "ja_existente", "telefone": telefone}
    obs = "Origem: calc-cep"
    if parceiro_id: obs += f" | parceiro_id {parceiro_id}"
    if cep: obs += f" | CEP {cep}"
    if yield_estimado is not None: obs += f" | Yield estimado {yield_estimado}"
    if email: obs += f" | email {email}"
    linha = {
        "Lote": "calc-cep", "Nome": nome, "Telefone": telefone, "Cidade": cidade or "",
        "Data_Msg1": date.today().isoformat(), "Status": "pendente_msg1",
        "Resposta": "", "Valor_Estimado": "", "Obs": obs, "Acao_Conversao": "",
    }
    rows.append(linha)
    # grava no tracker B2C geral (outbound ja existente)
    with open(TRACKER, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader(); w.writerows(rows)
    # se white-label, grava tambem no tracker dedicado da parceira (atribuicao)
    if parceiro_id:
        wl_rows = []
        if os.path.exists(TRACKER_WL):
            wl_rows = list(csv.DictReader(open(TRACKER_WL, encoding="utf-8-sig"), delimiter=";"))
        wl_rows.append({**linha, "Lote": f"wl-{parceiro_id}"})
        os.makedirs(os.path.dirname(TRACKER_WL), exist_ok=True)
        with open(TRACKER_WL, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
            w.writeheader(); w.writerows(wl_rows)
    return {"status": "criado", "telefone": telefone,
            "origem": "calc-cep", "parceiro_id": parceiro_id}

if __name__ == "__main__":
    print(capturar("Teste Calc", "(13) 98888-0000", "Santos", cep="11010-000",
                   yield_estimado=0.179, consentimento_lgpd=True))
