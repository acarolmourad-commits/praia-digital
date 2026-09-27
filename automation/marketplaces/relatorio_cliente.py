#!/usr/bin/env python3
"""
Gerador de relatório de desempenho para o cliente (texto pronto p/ WhatsApp/e-mail).

Substitui o fluxo manual: Upseller -> ChatGPT -> apresentação.

Uso:
    python relatorio_cliente.py vendas.csv --loja "Loja do Rafael" --periodo "01/09 a 30/09"

CSV esperado (export Upseller): produto,vendas,receita,estoque
"""
import argparse, csv

def carregar(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        low = {k.strip().lower(): (v or '').strip() for k, v in r.items()}
        out.append({
            'produto': low.get('produto') or low.get('product') or '?',
            'vendas': int(float(low.get('vendas') or low.get('unidades') or 0)),
            'receita': float((low.get('receita') or low.get('gmv') or '0').replace(',', '.')),
        })
    return out

def brl(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--loja', default='Sua loja')
    ap.add_argument('--periodo', default='últimos 30 dias')
    a = ap.parse_args()
    rows = carregar(a.csv)
    total_u = sum(r['vendas'] for r in rows)
    total_r = sum(r['receita'] for r in rows)
    ticket = total_r / total_u if total_u else 0
    top = sorted(rows, key=lambda r: r['receita'], reverse=True)[:5]
    zerados = [r for r in rows if r['vendas'] == 0]

    print(f"📊 *Relatório de desempenho — {a.loja}*")
    print(f"Período: {a.periodo}\n")
    print(f"• Pedidos: *{total_u}*")
    print(f"• Faturamento: *{brl(total_r)}*")
    print(f"• Ticket médio: *{brl(ticket)}*\n")
    if top:
        print("🏆 *Top produtos do período:*")
        for i, r in enumerate(top, 1):
            print(f"{i}. {r['produto']} — {r['vendas']} un. ({brl(r['receita'])})")
    if zerados:
        print(f"\n⚠️ {len(zerados)} produto(s) sem venda no período — vamos revisar preço/anúncio ou trocar nas ofertas relâmpago.")
    print("\nQualquer dúvida, estamos à disposição! 🚀")

if __name__ == '__main__':
    main()
