#!/usr/bin/env python3
"""
Gera lote B2B de reativacao para imobiliarias/construtoras (Expansao A).
Fonte: docs/materiais/leads-litoral-enriquecido.csv (status=contato_inicial_enviado).
Ordena por _score (Partner Score do plano de expansao) e gera CSV de outreach B2B.
Reusa a mesma engine de outbound (tracker compativel: Lote,Nome,Telefone,Cidade,Data_Msg1,Status,...).

Uso: python scripts/gerar_lote_b2b.py [--limite N] [--out ARQUIVO]
"""
import csv, os, argparse
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
SRC = os.path.join(REPO, "docs/materiais/leads-litoral-enriquecido.csv")
OUTDIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
OUT_DEFAULT = os.path.join(OUTDIR, "lote-b2b-reativacao-2026-07-16.csv")
TRACKER_COLS = ["Lote", "Nome", "Telefone", "Cidade", "Data_Msg1", "Status",
                "Resposta", "Valor_Estimado", "Obs", "Acao_Conversao"]

M1 = ("{ola} {contato}! Tudo bem? Sou da Praia Digital. Acompanho a {imob} em {cidade} e "
      "sei que o desafio de sempre é lotar o calendário de temporada sem depender só de "
      "anúncio pago. A gente resolve isso: levamos proprietários qualificados pra você e "
      "cuidamos da gestão completa. Sem você virar agência nem correr atrás de check-in.")
M2 = ("{contato}, pra ser direto: nosso modelo de Gestão Completa + Precificação Dinâmica "
      "eleva a ocupação da sua carteira e ainda te entrega proprietários novos pelo nosso "
      "funil de aquisição (blog com 1.300+ artigos de SEO no litoral). Você foca em fechar; "
      "a operação e os leads entram por nós. É parceria, não concorrência.")
M3 = ("{contato}, sem compromisso: posso te mandar 1 case real de imobiliária parceira nossa "
      "em {cidade} que dobrou a ocupação em 90 dias? Leva 2 min e mostra o retorno no seu bolso. "
      "Se fizer sentido, a gente estrutura a parceria.")

def ola(cargo):
    return "Olá" if not cargo else ("Prezada" if "gerente" in cargo.lower() or "diretora" in cargo.lower() else "Olá")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--out", default=OUT_DEFAULT)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    pend = [r for r in rows if r["status"] == "contato_inicial_enviado"]
    pend.sort(key=lambda r: float(r.get("_score") or 0), reverse=True)
    if a.limite: pend = pend[:a.limite]
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    for r in pend:
        contato = r["pessoa_de_contato"].strip()
        imob = r["nome_da_imobiliaria"].strip()
        cidade = r["cidade"].strip()
        cargo = r["cargo"].strip()
        f = lambda t: t.format(ola=ola(cargo), contato=contato, imob=imob, cidade=cidade)
        out.append({
            "Lote": "b2b-rev", "Nome": contato, "Telefone": r["whatsapp"].strip(),
            "Cidade": cidade, "Data_Msg1": date.today().isoformat(),
            "Status": "pendente_msg1", "Resposta": "", "Valor_Estimado": "",
            "Obs": f"Origem: b2b-reativacao | Imob: {imob} | Perfil: {r['perfil']} | Score: {r.get('_score')} | Dor: {r.get('dor_principal')}",
            "Acao_Conversao": "",
            # colunas extras reaproveitadas no follow-up
            "Msg1": f(t1 := M1), "Msg2": f(M2), "Msg3": f(M3),
            "Email": r.get("email","").strip(), "Imobiliaria": imob,
        })
    # escreve CSV (delimiter ; p/ Excel/Brevo)
    cols = TRACKER_COLS + ["Msg1", "Msg2", "Msg3", "Email", "Imobiliaria"]
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        w.writeheader(); w.writerows(out)
    print(f"Lote B2B gerado: {a.out}\n{len(out)} leads (top score: {out[0]['Obs'].split('Score: ')[1].split(' |')[0] if out else 'n/a'})")

if __name__ == "__main__":
    main()
