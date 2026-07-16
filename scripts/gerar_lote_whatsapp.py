#!/usr/bin/env python3
"""
Gerador de lote WhatsApp para proprietarios autogestores (Airbnb/Booking).
Recebe o numero do lote Brevo e gera:
  - docs/sales/csv-lotes-email/lote-whatsapp-proprietarios-<LOTE>-<DATA>.csv
  - outreach/followup-registro-<LOTE>.md

Padrao de mensagens: outreach/template-whatsapp-proprietarios.md
(Template base, ROI, Gestao Completa, Precificacao Dinamica)

Uso:
  python scripts/gerar_lote_whatsapp.py --lote 150 --data 2026-07-15
"""
import argparse, csv, os
from datetime import date

REPO = r"C:/Users/Carolina/praia-digital"
BREVO_DIR = os.path.join(REPO, "docs/sales/csv-lotes-email")
WHATS_DIR = BREVO_DIR
REG_DIR = os.path.join(REPO, "outreach")

def msg1(nome, regiao):
    return (f"Olá, {nome}! Tudo bem? Sou da Praia Digital e vi que o seu imóvel em {regiao} "
            "está anunciado direto no Airbnb/Booking. 👋\n\n"
            "Sem compromisso nenhum: muitos proprietários que cuidam sozinhos acabam perdendo horas "
            "com limpeza, check-in e uma precificação que não acompanha a demanda — e deixam dinheiro "
            "na mesa sem perceber. Você sente isso aí também?")

def msg2(nome, regiao):
    return (f"{nome}, só pra complementar: a Praia Digital oferece Gestão Completa + Tecnologia de "
            "Precificação Dinâmica. A gente assume limpeza, check-in e o preço certo em cada dia — e "
            "você ganha mais trabalhando zero horas. 💡\n\n"
            "Quem adota o modelo costuma ver o faturamento subir enquanto o trabalho cai a zero. "
            "Posso te mandar um exemplo real de ROI de um imóvel parecido com o seu?")

def msg3(nome, regiao):
    return (f"{nome}, não vou insistir — só não queria que esse tempo perdido com limpeza e preço "
            "errado continuasse custando o seu lucro. 🤝\n\n"
            "Se um dia quiser ganhar mais sem levantar um dedo, a Praia Digital resolve. Fico à "
            "disposição quando fizer sentido. Um abraço e bom proveito do seu imóvel!")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lote", required=True, help="numero do lote Brevo (ex: 150)")
    p.add_argument("--data", required=True, help="data Msg1 (AAAA-MM-DD)")
    args = p.parse_args()
    lote = args.lote
    base = date.fromisoformat(args.data)

    src = os.path.join(BREVO_DIR, f"lote-brevo-{lote}-2026-07-14.csv")
    if not os.path.exists(src):
        # tenta glob por lote
        cand = [f for f in os.listdir(BREVO_DIR) if f.startswith(f"lote-brevo-{lote}-") and f.endswith(".csv")]
        if not cand:
            print(f"Lote {lote} não encontrado em {BREVO_DIR}")
            return
        src = os.path.join(BREVO_DIR, cand[0])

    out_csv = os.path.join(WHATS_DIR, f"lote-whatsapp-proprietarios-{lote}-{base:%Y-%m-%d}.csv")
    out_reg = os.path.join(REG_DIR, f"followup-registro-{lote}.md")

    rows = []
    with open(src, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            nome = r.get("Nome", "").strip()
            tel = r.get("Telefone", "").strip()
            cidade = r.get("Cidade", "").strip()
            if not nome:
                continue
            rows.append((nome, tel, cidade))

    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Nome","Telefone","Cidade","Data_Msg1","Status",
                    "Mensagem_1_Abordagem","Mensagem_2_Solucao","Mensagem_3_Encerramento"])
        for nome, tel, cidade in rows:
            w.writerow([nome, tel, cidade, base.isoformat(), "contato_inicial_pendente",
                        msg1(nome, cidade), msg2(nome, cidade), msg3(nome, cidade)])

    # registro
    linhas = [f"# Follow-up Registro — Lote WhatsApp Proprietários Autogestores {lote}\n",
              f"**Data base (Msg 1):** {base:%d/%m/%Y}\n",
              "**Timing:** Msg 2 em +1 a 2 dias · Msg 3 em +3 a 4 dias\n",
              "**Canal:** WhatsApp manual (sem API/SMTP) — copiar do CSV e colar por contato.\n\n",
              "## Status por lead\n\n",
              "| Nome | Cidade | Tel | Msg1 | Msg2 | Msg3 | Status final |\n",
              "|------|--------|-----|------|------|------|--------------|\n"]
    for nome, tel, cidade in rows:
        linhas.append(f"| {nome} | {cidade} | {tel} | ☐ {base:%d/%m} | ☐ +1-2d | ☐ +3-4d | pendente |\n")
    linhas.append("\n## Regras\n")
    linhas.append("- Após enviar cada msg, marcar ☑ e atualizar Status final.\n")
    linhas.append("- Sem resposta após Msg 3 → marcar `sem_interesse`.\n")
    linhas.append("- Resposta positiva → pipeline de proposta (Gestão Completa + Precificação Dinâmica).\n")
    with open(out_reg, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print(f"CSV: {out_csv}")
    print(f"Registro: {out_reg}")
    print(f"Leads: {len(rows)}")

if __name__ == "__main__":
    main()
