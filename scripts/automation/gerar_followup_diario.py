#!/usr/bin/env python3
"""
Gera follow-ups do dia a partir do log em docs/sales/followup-registro.md.
Hoje: 2026-07-11.
Gera follow-ups para leads com envio inicial em 2026-07-08 (D3) e antes disso.
"""
import re, json
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path("C:/Users/Carolina/praia-digital")
TRACKER = BASE / "docs/sales/followup-registro.md"
OUTPUT = BASE / "docs/sales/followup-diario-2026-07-11.md"

TODAY = datetime.now().date()
DELTAS = {
    "D3": timedelta(days=3),
    "D7": timedelta(days=7),
    "D14": timedelta(days=14),
}


def parse_envios(texto: str):
    envíos = {}
    pattern = re.compile(
        r"- (\d{2}/\d{2}/\d{4}) \d{2}:\d{2}:\s*envio inicial para lead (\d+) — ([^\(]+)\(([^)]+)\) → e-mail: ([^\s]+)",
    )
    for m in pattern.finditer(texto):
        data_str, lead_id, nome, cidade, email = m.groups()
        data = datetime.strptime(data_str, "%d/%m/%Y").date()
        envíos[lead_id] = {
            "nome": nome.strip(),
            "cidade": cidade.strip(),
            "email": email.strip(),
            "data_envio": data,
        }
    return envíos


def gerar_followup_diario():
    texto = TRACKER.read_text(encoding="utf-8", errors="ignore")
    envios = parse_envios(texto)

    alvos = []
    for lead_id, info in envios.items():
        dias = (TODAY - info["data_envio"]).days
        labels = [label for label, delta in DELTAS.items() if dias == delta.days]
        if labels:
            alvos.append({
                "lead_id": lead_id,
                "nome": info["nome"],
                "cidade": info["cidade"],
                "email": info["email"],
                "dias": dias,
                "label": labels[0],
            })

    alvos.sort(key=lambda x: x["dias"])

    linhas = [
        f"# Follow-ups do dia — {TODAY}",
        "",
        "Gerado automaticamente por `scripts/automation/gerar_followup_diario.py`.",
        "",
        f"Leads com follow-up agendado para hoje: **{len(alvos)}**",
        "",
    ]
    if not alvos:
        linhas += [
            "Nenhum follow-up de D3/D7/D14 cai exatamente hoje.",
            "Use este dia para follow-ups adicionais ou limpeza de tracker.",
        ]
    else:
        for a in alvos:
            linhas += [
                f"## Lead {a['lead_id']} — {a['nome']} ({a['cidade']})",
                f"- Envio inicial: {TODAY - timedelta(days=a['dias'])}",
                f"- Dias desde envio: {a['dias']}",
                f"- Tipo: {a['label']}",
                f"- E-mail: {a['email']}",
                "",
                "### Template rápido",
                f"Olá, tudo bem? Estou acompanhando o envio que fizemos há {a['dias']} dias.",
                "",
                "1) Quer seguir com o piloto gratuito?",
                "2) Posso enviar o onboarding simplificado?",
                "3) Se for melhor para você, agendamos uma demo de 15min.",
                "",
                "Aguardo um ok para eu já adiantar o primeiro passo por aqui.",
                "",
                "---",
                "",
            ]

    OUTPUT.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Gerado: {OUTPUT}")
    print(f"Follow-ups para hoje: {len(alvos)}")
    for a in alvos:
        print(f"- {a['lead_id']} | {a['nome']} | {a['label']}")


if __name__ == "__main__":
    gerar_followup_diario()
