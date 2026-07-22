#!/usr/bin/env python3
"""
runner_lote_automacao.py
Prepara o lote de automação para envio externo e valida campos mínimos.
Uso:
  python scripts/automation/runner_lote_automacao.py --csv docs/sales/csv-lotes-b2b/lote-b2b-automacao-2026-07-22.csv --out docs/sales/csv-lotes-b2b/lote-b2b-automacao-pronto-envio-2026-07-22.csv
"""
import csv, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
FIELDS = ["Lote","Nome","Telefone","Cidade","Data_Msg1","Status","Resposta","Valor_Estimado","Obs","Acao_Conversao","Msg1","Msg2","Msg3","Email","Imobiliaria"]
PHONE_RE = re.compile(r'^\(\d{2}\)\s?\d{4,5}-\d{4}$')


def main():
    csv_in = Path(sys.argv[sys.argv.index('--csv')+1]) if '--csv' in sys.argv else BASE/'docs/sales/csv-lotes-b2b/lote-b2b-automacao-2026-07-22.csv'
    csv_out = Path(sys.argv[sys.argv.index('--out')+1]) if '--out' in sys.argv else BASE/'docs/sales/csv-lotes-b2b/lote-b2b-automacao-pronto-envio-2026-07-22.csv'
    if not csv_in.exists():
        print(f"CSV não encontrado: {csv_in}")
        return
    with csv_in.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    ready, skip = [], []
    for r in rows:
        tel = (r.get('Telefone') or '').strip()
        nome = (r.get('Nome') or '').strip()
        cidade = (r.get('Cidade') or '').strip()
        msg1 = (r.get('Msg1') or '').strip()
        if not tel or not PHONE_RE.match(tel):
            skip.append((nome, tel, 'telefone_invalido'))
            continue
        if not nome or not cidade or not msg1:
            skip.append((nome, tel, 'campos_faltando'))
            continue
        r.setdefault('Acao_Conversao', '')
        ready.append(r)
    with csv_out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter=';', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(ready)
    print(f"Pronto: {csv_out}")
    print(f"Validados: {len(ready)} | Ignorados: {len(skip)}")
    for s in skip:
        print(f" - {s}")


if __name__ == '__main__':
    main()
