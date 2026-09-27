#!/usr/bin/env python3
"""
Recomendador de Ofertas Relâmpago — Shopee

Regra (validada na operação do Luiz, 23/09/2026):
- Máximo de 20 produtos simultâneos na oferta relâmpago da loja.
- Produto que não vende há >= 7 dias deve sair.
- Entra no lugar o produto com melhor potencial: estoque alto e/ou
  vendas recentes boas fora da oferta.

Uso:
    python ofertas_relampago.py vendas.csv [--dias-sem-venda 7] [--max-vagas 20]

CSV esperado (export Upseller): produto,vendas,receita,estoque,em_oferta_relampago
"""
import argparse, csv, sys

def carregar(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    norm = []
    for r in rows:
        low = {k.strip().lower(): (v or '').strip() for k, v in r.items()}
        norm.append({
            'produto': low.get('produto') or low.get('product') or low.get('item') or '?',
            'vendas': int(float(low.get('vendas') or low.get('unidades') or 0)),
            'receita': float((low.get('receita') or low.get('gmv') or '0').replace(',', '.')),
            'estoque': int(float(low.get('estoque') or low.get('stock') or 0)),
            'em_oferta': (low.get('em_oferta_relampago') or low.get('em_oferta') or '0') in ('1', 'sim', 'true', 'True'),
        })
    return norm

def recomendar(rows, max_vagas=20):
    na_oferta = [r for r in rows if r['em_oferta']]
    fora = [r for r in rows if not r['em_oferta']]
    sair = [r for r in na_oferta if r['vendas'] == 0]
    # candidatos: fora da oferta, com vendas ou bom estoque, ordenados por potencial
    cand = sorted([r for r in fora if r['vendas'] > 0 or r['estoque'] >= 50],
                  key=lambda r: (r['vendas'], r['estoque']), reverse=True)
    vagas = max_vagas - (len(na_oferta) - len(sair))
    entrar = cand[:max(0, min(vagas + len(sair), len(cand)))][:max(0, vagas) + len(sair)]
    return sair, entrar[:vagas + len(sair)], na_oferta

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('--max-vagas', type=int, default=20)
    a = ap.parse_args()
    rows = carregar(a.csv)
    sair, entrar, na_oferta = recomendar(rows, a.max_vagas)
    print(f"== Oferta relâmpago: {len(na_oferta)}/{a.max_vagas} vagas ocupadas ==\n")
    if not sair and len(na_oferta) >= a.max_vagas:
        print("Nenhum produto zerado na oferta. Considere trocar o de menor venda:")
        pior = min(na_oferta, key=lambda r: r['vendas'], default=None)
        if pior: print(f"  - candidato a sair: {pior['produto']} ({pior['vendas']} vendas)")
    for r in sair:
        print(f"🔴 TIRAR : {r['produto']}  (0 vendas no período, estoque {r['estoque']})")
    for r in entrar:
        print(f"🟢 COLOCAR: {r['produto']}  ({r['vendas']} vendas, estoque {r['estoque']})")
    if not sair and not entrar:
        print("✅ Nenhuma troca recomendada hoje.")

if __name__ == '__main__':
    main()
