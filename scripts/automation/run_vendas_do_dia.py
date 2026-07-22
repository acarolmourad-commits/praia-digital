#!/usr/bin/env python3
"""
run_vendas_do_dia.py
Ponto único para operação diária dos serviços B2B.
Uso:
  python scripts/automation/run_vendas_do_dia.py
"""
import subprocess
import sys
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()

# Automacao para Imobiliarias
AUTOMACAO = [
    BASE / 'scripts/automation/sanitize_lote_automacao.py',
    BASE / 'scripts/automation/agendar_followup_automacao.py',
    BASE / 'scripts/automation/relatorio_diario_automacao.py',
    BASE / 'scripts/automation/notificar_automacao.py',
    BASE / 'scripts/automation/disparar_lote_automacao.py',
]

# Captacao Digital
CAPTACAO = [
    BASE / 'scripts/automation/agendar_followup_captacao.py',
    BASE / 'scripts/automation/disparar_lote_captacao.py',
]

# Solucao Proptech Unificada
PROPTECH = [
    BASE / 'scripts/automation/sanitize_lote_proptech.py',
    BASE / 'scripts/automation/agendar_followup_proptech.py',
]

# Geracao de Descricao de Imoveis com IA
DESCRICAO = [
    BASE / 'scripts/automation/agendar_followup_descricao.py',
    BASE / 'scripts/automation/disparar_lote_descricao.py',
]

# SEO Local
SEO_LOCAL = [
    BASE / 'scripts/automation/agendar_followup_seo_local.py',
    BASE / 'scripts/automation/disparar_lote_seo_local.py',
]

SCRIPTS = AUTOMACAO + CAPTACAO + PROPTECH + DESCRICAO + SEO_LOCAL


def run(path: Path):
    print(f'>>> {path.name}')
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(BASE),
        text=True,
        capture_output=False,
    )
    if result.returncode != 0:
        print(f'[WARN] {path.name} saiu com código {result.returncode}')


def main():
    print(f'Operacao Vendas B2B — {TODAY}')
    for path in SCRIPTS:
        run(path)
    print('\nConcluido.')


if __name__ == '__main__':
    main()
