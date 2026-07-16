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

# Template white-label (Expansao C) — so para parceiras ja fechadas
MW1 = ("{ola} {contato}! Tudo bem? Sou da Praia Digital. Como a {imob} já é nossa parceira em "
       "{cidade}, trouxe um ativo pronto pra te ajudar a captar mais proprietários SEM anúncio "
       "pago: uma Calculadora de Yield por CEP que embedamos no SEU site (com a sua marca). O dono "
       "simula o rendimento e vira seu lead. Setup grátis pra parceiro. Quer ver o protótipo?")
MW2 = ("{contato}, resumindo: a calculadora roda no site da {imob} e capta o proprietário no seu "
       "canal. Quando fechamos a gestão do imóvel, dividimos a comissão (70% pra você / 30% Praia "
       "Digital). É mais inventário de gestão pro seu portfólio, sem custo de aquisição. Já temos "
       "101 parcerias no litoral — você entra no white-label por ser parceira.")
MW3 = ("{contato}, sem compromisso: posso te mandar o protótipo da calculadora funcionando com a "
       "marca da {imob}? Leva 2 min de demo e mostra como vira lead no seu site. Se fizer sentido, "
       "fechamos o white-label em {cidade}.")

def ola(cargo):
    return "Olá" if not cargo else ("Prezada" if "gerente" in cargo.lower() or "diretora" in cargo.lower() else "Olá")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--status", default="contato_inicial_enviado",
                    help="filtro de status na base (ex: parceria_fechada p/ white-label)")
    ap.add_argument("--whitelabel", action="store_true", help="usa template Expansao C")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    pend = [r for r in rows if r["status"] == a.status]
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
        if a.whitelabel:
            m1, m2, m3 = f(MW1), f(MW2), f(MW3)
            lote = "b2b-wl"; obs_prefix = "Origem: b2b-whitelabel"
        else:
            m1, m2, m3 = f(M1), f(M2), f(M3)
            lote = "b2b-rev"; obs_prefix = "Origem: b2b-reativacao"
        out.append({
            "Lote": lote, "Nome": contato, "Telefone": r["whatsapp"].strip(),
            "Cidade": cidade, "Data_Msg1": date.today().isoformat(),
            "Status": "pendente_msg1", "Resposta": "", "Valor_Estimado": "",
            "Obs": f"{obs_prefix} | Imob: {imob} | Perfil: {r['perfil']} | Score: {r.get('_score')} | Dor: {r.get('dor_principal')}",
            "Acao_Conversao": "",
            "Msg1": m1, "Msg2": m2, "Msg3": m3,
            "Email": r.get("email","").strip(), "Imobiliaria": imob,
        })
    cols = TRACKER_COLS + ["Msg1", "Msg2", "Msg3", "Email", "Imobiliaria"]
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        w.writeheader(); w.writerows(out)
    print(f"Lote B2B gerado: {a.out}\n{len(out)} leads (status={a.status}, whitelabel={a.whitelabel}) | top score: {out[0]['Obs'].split('Score: ')[1].split(' |')[0] if out else 'n/a'}")

if __name__ == "__main__":
    main()
