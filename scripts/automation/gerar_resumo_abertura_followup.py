import csv
from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
tracker = root / "docs/sales/followup-registro.md"
out_dir = root / "outreach/resumo-followup-por-lead"
out_dir.mkdir(parents=True, exist_ok=True)

if not tracker.exists():
    print("Tracker não encontrado.")
    raise SystemExit(1)

# Perfis por cidade/canal para abertura de follow-up
city_openers = {
    "Santos": "Olá, tudo bem? Vi que a Praia Digital pode ajudar sua imobiliária a captar leads qualificados no litoral...",
    "Guarujá": "Oi, tudo bem? Temos uma parceria para imobiliárias do Guarujá com ferramentas de IA sem custo inicial...",
    "São Vicente": "Olá! Tudo bem? A Praia Digital tem um piloto sem custo para imobiliárias de São Vicente...",
    "Praia Grande": "Oi! Tudo bem? Estamos montando cases em Praia Grande e queremos incluir sua imobiliária...",
    "Bertioga": "Olá, tudo bem? Temos uma parceria com avaliação de preço e atendimento IA para Bertioga...",
    "default": "Olá, tudo bem? Tive uma ideia de parceria entre a Praia Digital e sua imobiliária...",
}

text = tracker.read_text(encoding="utf-8")
today = date.today().isoformat()
count = 0

for line in text.splitlines():
    if today in line and "follow-up" in line.lower():
        count += 1
        cidade = "default"
        for key in city_openers:
            if key in line:
                cidade = key
                break
        opener = city_openers[cidade]

        filename = f"resumo-followup-{count:03d}.txt"
        content = f"""RESUMO DE ABERTURA PARA FOLLOW-UP
Data: {today}
Linha do tracker: {line.strip()}

ABERTURA SUGERIDA (WhatsApp/e-mail):
{opener}

Próximos passos:
1. Responder em até 1h.
2. Enviar link do site: https://acarolmourad-commits.github.io/praia-digital/
3. Enviar ferramentas gratuitas: https://praia.digital
4. Agendar call de 15min se houver interesse.
"""
        (out_dir / filename).write_text(content, encoding="utf-8")

print(f"Resumos gerados: {count}")
print(f"Pasta: {out_dir}")
