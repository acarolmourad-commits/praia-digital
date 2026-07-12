import csv
from pathlib import Path
from datetime import date, datetime

root = Path("C:/Users/Carolina/praia-digital")
source = root / "docs/sales/parcerias-leads-capturados.csv"
prioritized = root / "docs/sales/leads-priorizados-2026-07-12.csv"
followup_dir = root / "outreach/followups-pendentes"
brevo_csv = root / "docs/sales/csv-lotes-email/lote-brevo-leads-capturados-2026-07-12.csv"

followup_dir.mkdir(parents=True, exist_ok=True)

if not source.exists():
    print("Fonte de leads não encontrada.")
    raise SystemExit(1)

# Priority map
score_map = {"Santos": 25, "Guarujá": 20, "Praia Grande": 20, "São Vicente": 15, "Bertioga": 15, "Outra": 5}
intent = ["parceria", "cliente", "venda", "recurso", "ferramenta", "ia", "seo", "automação", "leads", "imoveis", "imóveis", "agencia", "agência"]
reject = ["revenda", "spam", "teste", "não", "sem", "fake"]

with source.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

scored = []
generated = 0

for row in rows:
    nome = (row.get("Seu nome") or "").strip()
    empresa = (row.get("Nome da imobiliária") or "").strip()
    email = (row.get("E-mail comercial") or "").strip()
    whatsapp = (row.get("WhatsApp") or "").strip()
    cidade = (row.get("Cidade") or "").strip()
    mensagem = (row.get("Mensagem") or "").strip().lower()
    timestamp = (row.get("Timestamp") or "").strip()

    if not email and not whatsapp:
        continue

    score = 0
    score += score_map.get(cidade, 0)
    score += 15 if any(k in mensagem for k in intent) else 0
    score += -20 if any(k in mensagem for k in reject) else 0
    score += 10 if whatsapp else 0
    score += 5 if email and "@" in email and "." in email.split("@")[-1] else 0
    score += 5 if len(empresa) > 2 else 0
    score += 5 if timestamp else 0
    score = max(score, 0)

    priority = "Alta" if score >= 40 else "Média" if score >= 20 else "Baixa"

    if priority in ("Alta", "Média"):
        opener = f"Olá, tudo bem? Vi que a Praia Digital pode ajudar sua imobiliária em {cidade or 'sua região'}... ({nome or empresa})"
        content = f"""RESUMO DE CONTATO
Nome: {nome or '—'}
Empresa: {empresa or '—'}
E-mail: {email or '—'}
WhatsApp: {whatsapp or '—'}
Cidade: {cidade or '—'}
Prioridade: {priority}
Score: {score}
Origem: site

ABERTURA SUGERIDA:
{opener}

Próximos passos:
1. Responder em até 1h.
2. Enviar site: https://acarolmourad-commits.github.io/praia-digital/
3. Ferramentas gratuitas: https://praia.digital
4. Agendar call se houver interesse.
"""
        out_path = followup_dir / f"followup-rapido-{nome or empresa or 'lead'}-{datetime.now().strftime('%H%M%S')}.txt"
        out_path.write_text(content, encoding="utf-8")
        generated += 1

    scored.append({
        "NOME": nome or "",
        "EMAIL": email,
        "WHATSAPP": whatsapp,
        "CIDADE": cidade,
        "EMPRESA": empresa,
        "ASSUNTO": f"Parceria — {cidade}",
        "LINK_EMAIL_PERSONALIZADO": f"mailto:{email}?subject=Parceria%20Praia%20Digital" if email else "",
        "ORIGEM": row.get("Origem") or "site",
        "INTERESSE": row.get("Mensagem") or "",
        "STATUS": "capturado",
        "PRIORIDADE": priority,
        "SCORE": str(score),
    })

scored.sort(key=lambda x: int(x["SCORE"]), reverse=True)
fields = [
    "NOME", "EMAIL", "WHATSAPP", "CIDADE", "EMPRESA",
    "ASSUNTO", "LINK_EMAIL_PERSONALIZADO", "ORIGEM", "INTERESSE",
    "STATUS", "PRIORIDADE", "SCORE"
]

with prioritized.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(scored)

with brevo_csv.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(fields)
    for r in scored:
        w.writerow([r[k] for k in fields])

print(f"Leads processados: {len(scored)}")
print(f"Follow-ups rápidos gerados: {generated}")
print(f"Priorizados: {prioritized}")
print(f"Brevo CSV atualizado: {brevo_csv}")
