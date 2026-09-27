#!/usr/bin/env python3
"""
Monitor semáforo de lojas — painel diário da operação.

Para cada loja (um CSV por loja na pasta informada), avalia:
- estoque crítico (produtos com vendas e estoque < 10)
- produtos zerados há período inteiro (candidatos a revisão)
- resumo de vendas/receita do período

Status: 🟢 ok | 🟡 atenção | 🔴 ação urgente

Uso:
    python monitor_lojas.py pasta_csvs/ [--estoque-min 10]

O resultado pode ser colado em Google Sheets (aba 'Semáforo') ou enviado
por e-mail/WhatsApp no fechamento do dia.
"""
import argparse, csv, glob, os

def carregar(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        low = {k.strip().lower(): (v or '').strip() for k, v in r.items()}
        out.append({
            'produto': low.get('produto') or '?',
            'vendas': int(float(low.get('vendas') or 0)),
            'receita': float((low.get('receita') or '0').replace(',', '.')),
            'estoque': int(float(low.get('estoque') or 0)),
        })
    return out

def avaliar(rows, estoque_min):
    critico = [r for r in rows if r['vendas'] > 0 and r['estoque'] < estoque_min]
    zerados = [r for r in rows if r['vendas'] == 0]
    receita = sum(r['receita'] for r in rows)
    vendas = sum(r['vendas'] for r in rows)
    if critico: status = '🔴'
    elif len(zerados) > len(rows) * 0.5: status = '🟡'
    else: status = '🟢'
    return status, vendas, receita, critico, zerados

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta')
    ap.add_argument('--estoque-min', type=int, default=10)
    a = ap.parse_args()
    print(f"{'Status':<7} {'Loja':<32} {'Vendas':>7} {'Receita':>12}  Alertas")
    print('-' * 80)
    for path in sorted(glob.glob(os.path.join(a.pasta, '*.csv'))):
        loja = os.path.splitext(os.path.basename(path))[0]
        rows = carregar(path)
        st, v, rec, crit, zer = avaliar(rows, a.estoque_min)
        alertas = []
        if crit: alertas.append(f"estoque crítico: {', '.join(r['produto'] for r in crit[:3])}")
        if zer: alertas.append(f"{len(zer)} produto(s) zerado(s)")
        print(f"{st:<7} {loja:<32} {v:>7} R${rec:>10.2f}  {'; '.join(alertas) or '—'}")

if __name__ == '__main__':
    main()
