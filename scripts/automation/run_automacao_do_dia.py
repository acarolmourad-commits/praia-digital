#!/usr/bin/env python3
"""
run_automacao_do_dia.py
Ponto único para operação diária do serviço de Automação para Imobiliárias.
Uso:
  python scripts/automation/run_automacao_do_dia.py
"""
import subprocess
import sys
from pathlib import Path
from datetime import date

BASE = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()
SCRIPTS = [
    BASE / 'scripts/automation/sanitize_lote_automacao.py',
    BASE / 'scripts/automation/agendar_followup_automacao.py',
    BASE / 'scripts/automation/relatorio_diario_automacao.py',
    BASE / 'scripts/automation/notificar_automacao.py',
    BASE / 'scripts/automation/disparar_lote_automacao.py',
]


def run(path: Path):
    print(f'>>> {path.name}')
    result = subprocess.run( # nosec B603
        [sys.executable, str(path)],
        cwd=str(BASE),
        text=True,
        capture_output=False,
    )
    if result.returncode != 0:
        print(f'[WARN] {path.name} saiu com código {result.returncode}')


def main():
    print(f'Operacao Automacao para Imobiliarias — {TODAY}')
    for path in SCRIPTS:
        run(path)
    print('\nConcluido.')


if __name__ == '__main__':
    main()
