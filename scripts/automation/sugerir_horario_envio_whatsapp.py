#!/usr/bin/env python3
"""
Sugere horários ideais de envio WhatsApp por cidade/litoral.
Regras genéricas:
  - Manhã: 09:00–11:00
  - Almoço: 12:00–13:00
  - Tarde: 14:00–16:00
  - Final tarde: 16:30–18:00
Asaid: docs/sales/horarios-ideais-envio-whatsapp-2026-07-11.md
"""
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
OUTPUT = BASE / "docs/sales/horarios-ideais-envio-whatsapp-2026-07-11.md"

HORARIOS = {
    "Santos": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Guarujá": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Bertioga": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Praia Grande": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "São Vicente": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Itanhaém": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Peruíbe": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
    "Mongaguá": ["09:00–11:00", "14:00–16:00", "16:30–18:00"],
}

lines = [
    "# Horários ideais de envio WhatsApp — 2026-07-11",
    "",
    "Gerado por scripts/automation/sugerir_horario_envio_whatsapp.py",
    "",
    "## Regras gerais",
    "- Máximo 100 mensagens por dia útil.",
    "- Respeite horário comercial: 09:00–18:00, de segunda a sexta.",
    "- Intervalo mínimo de 2h entre blocos para não parecer spam.",
    "",
    "## Por cidade",
    "",
]
for cidade, horarios in HORARIOS.items():
    lines.append(f"### {cidade}")
    for h in horarios:
        lines.append(f"- {h}")
    lines.append("")

lines += [
    "## Dicas adicionais",
    "- Segunda e terça tendem a ter maior taxa de abertura.",
    "- Evite sexta-feira após 16h para mensagens de prospecção fria.",
    "- Se o lead responder, responda em até 2h.",
    "",
    "## Exemplo de distribuição diária",
    "| Bloco | Horário | Leads | Cidade sugerida |",
    "|-------|---------|-------|----------------|",
    "| 1 | 09:00–11:00 | 30 | Guarujá |",
    "| 2 | 14:00–16:00 | 40 | Santos |",
    "| 3 | 16:30–18:00 | 30 | Praia Grande |",
]

OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Horários: {OUTPUT}")
