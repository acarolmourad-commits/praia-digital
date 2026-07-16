#!/usr/bin/env python3
"""
Gerador de lote EMAIL para proprietarios autogestores (Airbnb/Booking).
Le o CSV Brevo (formato Nome,Email,Telefone,Cidade,...) e gera:
  - docs/sales/csv-lotes-email/lote-email-proprietarios-<LOTE>-<DATA>.csv
  - outreach/followup-registro-email-<LOTE>.md

Padrao: outreach/template-email-proprietarios.md

Uso:
  python scripts/gerar_lote_email.py --lote 149 --data 2026-07-15
"""
import argparse, csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
BREVO_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
EMAIL_DIR = BREVO_DIR
REG_DIR = os.path.join(REPO, "outreach")

def em1(nome, regiao):
    return (f"Assunto: {nome}, seu imóvel em {regiao} pode estar rendendo mais (sem seu trabalho)\n\n"
            f"Olá, {nome}.\n\nSou da Praia Digital e vi que seu imóvel em {regiao} está anunciado "
            "direto no Airbnb/Booking.\n\nSem compromisso: muitos proprietários que cuidam sozinhos "
            "perdem horas com limpeza, check-in e uma precificação que não acompanha a demanda — e "
            "deixam dinheiro na mesa sem perceber.\n\nVocê sente isso aí também?\n\nUm abraço,\nEquipe Praia Digital")

def em2(nome, regiao):
    return (f"Assunto: Re: seu imóvel em {regiao} — ganhar mais trabalhando zero horas\n\n"
            f"{nome}, complementando:\n\nA Praia Digital oferece Gestão Completa + Tecnologia de "
            "Precificação Dinâmica. Assumimos limpeza, check-in e o preço certo em cada dia — e você "
            "ganha mais trabalhando zero horas.\n\n"
            f"Exemplo real (imóvel parecido em {regiao}): ~R$ 2.100/mês autogestão → "
            "~R$ 3.450/mês conosco (+64%), zero horas do dono.\n\n"
            "Quer que eu simule o ROI no SEU imóvel? É só responder com quartos e bairro.\n\nEquipe Praia Digital")

def em3(nome, regiao):
    return (f"Assunto: Última mensagem sobre seu imóvel em {regiao}\n\n"
            f"{nome}, não vou insistir — só não queria que esse tempo perdido com limpeza e preço "
            "errado continuasse custando seu lucro.\n\n"
            "Se um dia quiser ganhar mais sem levantar um dedo, a Praia Digital resolve. Fico à "
            "disposição quando fizer sentido.\n\nUm abraço e bom proveito do seu imóvel!\n\nEquipe Praia Digital")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lote", required=True)
    p.add_argument("--data", required=True, help="data Email1 (AAAA-MM-DD)")
    args = p.parse_args()
    lote = args.lote
    base = date.fromisoformat(args.data)

    src = os.path.join(BREVO_DIR, f"lote-brevo-{lote}-2026-07-14.csv")
    if not os.path.exists(src):
        import glob
        cand = [f for f in os.listdir(BREVO_DIR) if f.startswith(f"lote-brevo-{lote}-") and f.endswith(".csv")]
        if not cand:
            print(f"Lote {lote} não encontrado."); return
        src = os.path.join(BREVO_DIR, cand[0])

    out_csv = os.path.join(EMAIL_DIR, f"lote-email-proprietarios-{lote}-{base:%Y-%m-%d}.csv")
    out_reg = os.path.join(REG_DIR, f"followup-registro-email-{lote}.md")

    rows = []
    with open(src, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # aceita tanto 'Nome' quanto formatos alternativos
        for r in reader:
            nome = (r.get("Nome") or r.get("nome") or "").strip()
            email = (r.get("Email") or r.get("email") or "").strip()
            cidade = (r.get("Cidade") or r.get("cidade") or "").strip()
            if not nome or not email:
                continue
            rows.append((nome, email, cidade))

    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Nome","Email","Cidade","Data_Email1","Status",
                    "Email_1_Abordagem","Email_2_Solucao","Email_3_Encerramento"])
        for nome, email, cidade in rows:
            w.writerow([nome, email, cidade, base.isoformat(), "pendente_email1",
                        em1(nome, cidade), em2(nome, cidade), em3(nome, cidade)])

    linhas = [f"# Follow-up Registro EMAIL — Proprietários Autogestores {lote}\n",
              f"**Data base (Email 1):** {base:%d/%m/%Y}\n",
              "**Timing:** Email 2 em +2 dias · Email 3 em +5 dias\n",
              "**Canal:** e-mail manual (Brevo/Gmail/Outlook) — SMTP não configurado.\n\n",
              "## Status por lead\n\n",
              "| Nome | Cidade | Email | E1 | E2 | E3 | Status final |\n",
              "|------|--------|------|----|----|----|--------------|\n"]
    for nome, email, cidade in rows:
        linhas.append(f"| {nome} | {cidade} | {email} | ☐ {base:%d/%m} | ☐ +2d | ☐ +5d | pendente |\n")
    linhas.append("\n## Regras\n- Após enviar cada email, marcar ☑ e Status final.\n")
    linhas.append("- Sem resposta após E3 → `sem_interesse`.\n- Resposta positiva → pipeline de proposta.\n")
    with open(out_reg, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print(f"CSV: {out_csv}\nRegistro: {out_reg}\nLeads: {len(rows)}")

if __name__ == "__main__":
    main()
