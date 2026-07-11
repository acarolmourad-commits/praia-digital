#!/usr/bin/env python3
"""Gera lista de follow-ups do dia a partir do tracker unificado."""
from pathlib import Path
from datetime import datetime

BASE = Path(r'C:\Users\Carolina\praia-digital')
TRACKER = BASE / 'docs/sales/tracker-envios-unificado-2026-07-10.md'
OUT = BASE / 'docs/sales/followups-para-hoje-2026-07-10.md'


def main():
    hoje = datetime.now().strftime('%Y-%m-%d')
    linhas = [f'# Follow-ups para hoje — {hoje}', '']
    if TRACKER.exists():
        texto = TRACKER.read_text(encoding='utf-8')
        for linha in texto.splitlines():
            if '72h' in linha or '7d' in linha:
                linhas.append(linha)
    OUT.write_text('\n'.join(linhas), encoding='utf-8')
    print(f'GENERATED {OUT}')


if __name__ == '__main__':
    main()
