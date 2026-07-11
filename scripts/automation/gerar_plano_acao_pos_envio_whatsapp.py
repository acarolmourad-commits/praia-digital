#!/usr/bin/env python3
"""
Gera plano de ação pós-envio cruzando cidade, status e score.
Entrada sugerida: docs/sales/whatsapp-enviados-YYYY-MM-DD.csv
Saída: docs/sales/plano-acao-pos-envio-YYYY-MM-DD.md
"""
import csv, collections
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")
SENT_CSV = BASE / "docs/sales/whatsapp-enviados-2026-07-11.csv"
MASTER_CSV = BASE / "docs/sales/leads-litoral-enriquecido.csv"
TODAY = datetime.now().strftime("%Y-%m-%d")
OUTPUT = BASE / f"docs/sales/plano-acao-pos-envio-{TODAY}.md"


def load_csv(path: Path):
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8", errors="ignore")))


def acao_por_status(status: str) -> str:
    s = (status or "").lower()
    if "interessado" in s:
        return "Enviar follow-up D3 + case + onboarding simplificado"
    if "negociacao" in s:
        return "Avancar com proposta comercial por perfil e agendar demo"
    if "parceria_fechada" in s:
        return "Follow-up pós-fechamento: onboarding + checklist de sucesso"
    if "nao_interessado" in s or "nao interessado" in s:
        return "Back-off 30 dias + reenvio com novidade"
    if "contato_inicial_enviado" in s:
        return "Follow-up D3: oferecer onboarding + demo"
    return "Follow-up D3: identificacao de dor + passo a passo do piloto"


master = {r["id"]: r for r in load_csv(MASTER_CSV)}
sent = load_csv(SENT_CSV)

lines = [
    f"# Plano de ação pós-envio — {TODAY}",
    "",
    f"- Enviados: {len(sent)}",
    "",
    "## Ações sugeridas por status",
    "",
]

for status, qtd in sorted(collections.Counter(master.get(r.get("id", ""), {}).get("status", "") for r in sent).items(), key=lambda x: -x[1]):
    lines.append(f"- {status}: {qtd}")
lines.append("")

lines.append("## Por cidade")
for cidade, qtd in sorted(collections.Counter(master.get(r.get("id", ""), {}).get("cidade", "") for r in sent).items(), key=lambda x: -x[1]):
    lines.append(f"- {cidade}: {qtd}")
lines.append("")

lines.append("## Detalhamento")
lines.append("| ID | Imobiliária | Cidade | Score | Status | Próxima ação |")
lines.append("|-----|----------------|---------|-------|--------|----------------|")
for r in sent:
    base = master.get(r.get("id", ""), {})
    status = base.get("status", "")
    acao = acao_por_status(status)
    lines.append(f"| {r.get('id','')} | {base.get('nome_da_imobiliaria','')} | {base.get('cidade','')} | {base.get('_score','0')} | {status} | {acao} |")

out = "\n".join(lines) + "\n"
OUTPUT.write_text(out, encoding="utf-8")
print(f"Plano: {OUTPUT}")
print(f"Enviados: {len(sent)}")
