#!/usr/bin/env python3
"""
Gera relatório de desempenho de prospecção WhatsApp a partir do CSV de enviados.
Uso:
  python scripts/automation/gerar_relatorio_performance_whatsapp.py docs/sales/whatsapp-enviados-2026-07-11.csv docs/sales/leads-litoral-enriquecido.csv
Saída: docs/sales/relatorio-performance-whatsapp-YYYY-MM-DD.md
"""
import csv, collections, sys
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Users/Carolina/praia-digital")

def load_csv(path: Path):
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8", errors="ignore")))

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    sent_csv = BASE / "docs/sales/whatsapp-enviados-2026-07-11.csv"
    master_csv = BASE / "docs/sales/leads-litoral-enriquecido.csv"

    if len(sys.argv) >= 3:
        sent_csv = Path(sys.argv[1])
        master_csv = Path(sys.argv[2])

    sent_rows = load_csv(sent_csv)
    master_rows = load_csv(master_csv)
    master_by_id = {r["id"]: r for r in master_rows}

    city_counts = collections.Counter()
    status_counts = collections.Counter()
    score_sum = 0
    missing = 0
    rows_out = []

    for r in sent_rows:
        lid = (r.get("id") or "").strip()
        base = master_by_id.get(lid)
        if not base:
            missing += 1
            continue
        city_counts[base.get("cidade", "")] += 1
        status_counts[base.get("status", "")] += 1
        score_sum += int(base.get("_score", "0") or "0")
        rows_out.append({
            "id": lid,
            "nome_da_imobiliaria": base.get("nome_da_imobiliaria", ""),
            "cidade": base.get("cidade", ""),
            "contato": base.get("pessoa_de_contato", ""),
            "whatsapp": base.get("whatsapp", ""),
            "score": base.get("_score", "0"),
            "status": base.get("status", ""),
        })

    output_path = BASE / f"docs/sales/relatorio-performance-whatsapp-{today}.md"
    lines = [
        f"# Relatório de desempenho — WhatsApp outreach — {today}\n",
        f"- Enviados: {len(rows_out)}",
        f"- Score médio: {score_sum / max(len(rows_out),1):.1f}",
        f"- Sem match com base mestra: {missing}\n",
        "## Por cidade",
    ]
    for cidade, qtd in sorted(city_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {cidade}: {qtd}")
    lines.append("\n## Por status")
    for status, qtd in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {status}: {qtd}")
    lines.append("\n## Detalhamento")
    lines.append("| ID | Imobiliária | Cidade | Score | Status |")
    lines.append("|-----|----------------|---------|-------|--------|")
    for r in rows_out:
        lines.append(f"| {r['id']} | {r['nome_da_imobiliaria']} | {r['cidade']} | {r['score']} | {r['status']} |")
    out = "\n".join(lines) + "\n"
    output_path.write_text(out, encoding="utf-8")
    print(f"Relatório: {output_path}")
    print(f"Enviados: {len(rows_out)} | Score médio: {score_sum / max(len(rows_out),1):.1f}")

if __name__ == "__main__":
    main()
