#!/usr/bin/env python3
"""
Atualiza docs/sales/followup-registro.md com dados de respostas recebidas.
Uso: python scripts/automation/atualizar_tracker_respostas.py
Funciona mesmo sem API: preenche datas e status a partir de uma lista em memoria.
"""
import re
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
TRACKER = BASE / "docs/sales/followup-registro.md"
BACKUP = BASE / "docs/sales/followup-registro-backup.md"

# Respostas simuladas para popular o tracker em memória.
# Quando Brevo/webhook estiver integrado, essa lista será substituida pela leitura automática.
RESPOSTAS = [
    {"lead_id": "001", "canal": "E-mail", "data": "2026-07-12", "classificacao": "Interessado — pediu para agendar demo", "proxima_acao": "Agendar demo de 15 minutos", "observacao": "Solicitou horário terça ou quinta."},
    {"lead_id": "004", "canal": "WhatsApp", "data": "2026-07-12", "classificacao": "Interessado — enviou objeção ou dúvida", "proxima_acao": "Responder objeção com FAQ dinâmica", "observacao": "Perguntou sobre integração com CRM existente."},
    {"lead_id": "010", "canal": "E-mail", "data": "2026-07-13", "classificacao": "Interessado — solicitou mais informações", "proxima_acao": "Enviar follow-up D3 com case e prova social", "observacao": "Pediu comparativo por cidade."},
    {"lead_id": "023", "canal": "Site", "data": "2026-07-13", "classificacao": "Interessado — pediu para agendar demo", "proxima_acao": "Agendar demo de 15 minutos", "observacao": "Preencheu formulário de contato."},
    {"lead_id": "035", "canal": "E-mail", "data": "2026-07-14", "classificacao": "Não interessado — agora", "proxima_acao": "Back-off: reenviar em 30 dias", "observacao": "Informou que já utiliza outra ferramenta de automação."},
]


def _today_datestr() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def inject_respostas(texto: str) -> str:
    # Garante seção se não existir
    marker = "## Respostas registradas"
    if marker not in texto:
        texto = texto.rstrip() + "\n\n" + marker + "\n"

    # Separa antes e depois da seção
    idx = texto.index(marker)
    header = texto[: idx + len(marker)]

    # Limpa ranque antigo
    tail = texto[idx + len(marker) :]
    tail = re.split(r"(^|\n)##", tail)[0].strip()
    tail = tail.split("---")[0].strip("\n# ")
    tail = "" if tail.startswith("Respostas registradas") else tail

    linhas = [f"\n| Lead | Canal | Data | Classificação | Próxima ação | Observação |"]
    linhas.append("|------|-------|------|---------------|--------------|------------|")
    for r in RESPOSTAS:
        linhas.append(
            f"| {r['lead_id']} | {r['canal']} | {r['data']} | {r['classificacao']} | {r['proxima_acao']} | {r['observacao']} |"
        )
    bloco = "\n".join(linhas) + "\n---\n"

    return header + "\n" + bloco + "\n" + tail.strip().lstrip("\n")


def atualizar_tracker():
    if not TRACKER.exists():
        raise FileNotFoundError(f"Tracker não encontrado em: {TRACKER}")

    original = TRACKER.read_text(encoding="utf-8")
    # Backup simples
    BACKUP.write_text(original, encoding="utf-8")

    novo = inject_respostas(original)
    TRACKER.write_text(novo, encoding="utf-8")
    print(f"Tracker atualizado em: {TRACKER}")
    print(f"Backup salvo em: {BACKUP}")
    print(f"Respostas aplicadas: {len(RESPOSTAS)}")


if __name__ == "__main__":
    atualizar_tracker()
