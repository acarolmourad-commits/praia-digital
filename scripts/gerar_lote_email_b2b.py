#!/usr/bin/env python3
"""
Expansao E — E-mail B2B para imobiliarias/construtoras (canal paralelo ao WhatsApp B2B).
Reusa o padrao do gerador de e-mail B2C, mas com copy B2B (parceria/gestao completa).
Le a base B2B real (docs/materiais/leads-litoral-enriquecido.csv) filtrando por status.

Uso:
  python scripts/gerar_lote_email_b2b.py [--status contato_inicial_enviado] [--whitelabel]
  python scripts/gerar_lote_email_b2b.py --status parceria_fechada --whitelabel
"""
import csv, os, argparse
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
SRC = os.path.join(REPO, "docs/materiais/leads-litoral-enriquecido.csv")
OUTDIR = os.path.join(REPO, "docs/sales/csv-lotes-b2b")
OUT_DEFAULT = os.path.join(OUTDIR, "lote-email-b2b-reativacao-2026-07-16.csv")

def ola(cargo):
    return "Prezada" if cargo and ("gerente" in cargo.lower() or "diretora" in cargo.lower()) else "Olá"

def em1(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: {imob} ({cidade}): lotar o calendário de temporada sem anúncio pago\n\n"
            f"{o} {nome}.\n\nSou da Praia Digital e acompanho a {imob} em {cidade}. O desafio de sempre é "
            "manter o calendário de temporada cheio fora dos feriados — e sem depender só de anúncio pago.\n\n"
            "A gente resolve: levamos proprietários qualificados pra você e cuidamos da gestão completa. "
            "Você foca em fechar; a operação entra por nós.\n\nUm abraço,\nEquipe Praia Digital")

def em2(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: Re: {imob} — ocupação no talo sem virar agência\n\n"
            f"{nome}, complementando:\n\nNosso modelo de Gestão Completa + Precificação Dinâmica eleva a ocupação "
            f"da sua carteira e ainda entrega proprietários novos pelo nosso funil de aquisição (blog com 1.300+ "
            f"artigos de SEO no litoral). Já fechamos 101 parcerias no litoral de SP.\n\n"
            "É parceria, não concorrência. Quer ver 1 case real em 90 dias?\n\nEquipe Praia Digital")

def em3(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: Última sobre parceria {imob}\n\n"
            f"{nome}, não vou insistir — só não queria que o calendário ocioso continuasse custando seu lucro.\n\n"
            "Se um dia quiser captar mais proprietários sem gastar com mídia, a Praia Digital resolve. "
            "Fico à disposição quando fizer sentido.\n\nUm abraço,\nEquipe Praia Digital")

def em1_wl(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: {imob}: calculadora de yield no SEU site (grátis p/ parceiro)\n\n"
            f"{o} {nome}. Como a {imob} já é nossa parceira em {cidade}, trouxe um ativo pronto: uma Calculadora "
            "de Yield por CEP que embedamos no SEU site (com a sua marca). O dono simula o rendimento e vira seu "
            "lead — setup grátis pra parceiro.\n\nQuer ver o protótipo?\n\nEquipe Praia Digital")

def em2_wl(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: Re: calculadora white-label {imob}\n\n"
            f"{nome}, resumindo: a calculadora roda no site da {imob} e capta o proprietário no seu canal. "
            "Quando fechamos a gestão, dividimos a comissão (70% pra você / 30% Praia Digital). Mais inventário "
            "pro seu portfólio, sem custo de aquisição.\n\nEquipe Praia Digital")

def em3_wl(nome, imob, cidade, cargo):
    o = ola(cargo)
    return (f"Assunto: Última sobre white-label {imob}\n\n"
            f"{nome}, só não queria que esse canal de captação próprio ficasse de fora do seu crescimento. "
            "Quando fizer sentido, o white-label está pronto pra {imob}.\n\nEquipe Praia Digital")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", default="contato_inicial_enviado")
    ap.add_argument("--whitelabel", action="store_true")
    ap.add_argument("--out", default=OUT_DEFAULT)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
    sel = [r for r in rows if r["status"] == a.status]
    sel.sort(key=lambda r: float(r.get("_score") or 0), reverse=True)
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    for r in sel:
        nome = r["pessoa_de_contato"].strip()
        imob = r["nome_da_imobiliaria"].strip()
        cidade = r["cidade"].strip()
        cargo = r["cargo"].strip()
        email = r.get("email", "").strip()
        if not (nome and email):
            continue
        if a.whitelabel:
            e1, e2, e3 = em1_wl(nome, imob, cidade, cargo), em2_wl(nome, imob, cidade, cargo), em3_wl(nome, imob, cidade, cargo)
        else:
            e1, e2, e3 = em1(nome, imob, cidade, cargo), em2(nome, imob, cidade, cargo), em3(nome, imob, cidade, cargo)
        out.append({"Nome": nome, "Email": email, "Imobiliaria": imob, "Cidade": cidade,
                    "Data_Email1": date.today().isoformat(), "Status": "pendente_email1",
                    "Email_1_Abordagem": e1, "Email_2_Solucao": e2, "Email_3_Encerramento": e3})
    cols = ["Nome", "Email", "Imobiliaria", "Cidade", "Data_Email1", "Status",
            "Email_1_Abordagem", "Email_2_Solucao", "Email_3_Encerramento"]
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        w.writeheader(); w.writerows(out)
    print(f"Lote EMAIL B2B: {a.out}\n{len(out)} leads (status={a.status}, whitelabel={a.whitelabel})")

if __name__ == "__main__":
    main()
