#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rotina diária automática unificada:
1) Valida lote de prospecção
2) Gera onboardings de parceiros
3) Gera relatório diário de outbound
Saída: relatório consolidado em docs/sales/relatorio-rotina-diaria-YYYY-MM-DD.md
"""
import os, subprocess
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE)
TODAY = datetime.now().strftime("%Y-%m-%d")
OUT_MD = os.path.join(ROOT, "docs", "sales", f"relatorio-rotina-diaria-{TODAY}.md")

VALIDADOR = os.path.join(ROOT, "scripts", "automation", "validar_lote_prospeccao_diaria.py")
ONBOARDING = os.path.join(ROOT, "scripts", "automation", "gerar_onboarding_parceiro.py")
RELATORIO = os.path.join(ROOT, "scripts", "automation", "gerar_relatorio_diario_outbound.py")

PYTHON = "python"


def run_script(path, label):
    print(f"=== {label} ===")
    try:
        result = subprocess.run([PYTHON, path], capture_output=True, text=True, timeout=300)
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        status = "OK" if result.returncode == 0 else f"FALHOU ({result.returncode})"
        print(f"Status: {status}")
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
        return {"label": label, "status": status, "stdout": stdout, "stderr": stderr}
    except Exception as e:
        print(f"Erro ao executar {label}: {e}")
        return {"label": label, "status": "ERRO", "stdout": "", "stderr": str(e)}


def main():
    steps = [
        run_script(VALIDADOR, "Validação de lote"),
        run_script(ONBOARDING, "Onboarding de parceiros"),
        run_script(RELATORIO, "Relatório diário de outbound"),
    ]

    lines = [
        "# Relatório — Rotina Diária Praia Digital",
        "",
        f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "## Status das etapas",
        ""
    ]
    for step in steps:
        lines.append(f"- **{step['label']}**: {step['status']}")
    lines.extend([
        "",
        "## Próximas ações",
        "- Enviar follow-ups pendentes",
        "- Revisar respostas de leads",
        "- Agendar demonstrações de 15min",
        "- Publicar conteúdo SEO do dia",
        "",
        "Site: https://acarolmourad-commits.github.io/praia-digital/",
        "Ferramentas: https://praia.digital",
        ""
    ])

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Relatório consolidado: {OUT_MD}")


if __name__ == "__main__":
    main()
