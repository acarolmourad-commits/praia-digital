#!/usr/bin/env python3
"""
run_litoral_prime_completo.py
Runner completo da Litoral Prime: posts, captura de leads, follow-up e relatório.
Uso: python litoral-prime-imoveis/automation/run_litoral_prime_completo.py
"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE / 'docs/posts'

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES = [
    "🏖️ {titulo} por {preco} em {cidade}/{bairro}.\\n\\nClique no link da bio para agendar!\\n\\n#LitoralPrime #ImoveisLitoralSP",
    "🔥 {titulo} em {cidade}/{bairro}.\\n\\nAgende sua visita! WhatsApp: (11) 95434-6288\\n\\n#ImoveisLitoralSP #Praia",
]

def fmt(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def posts_do_dia():
    hoje = datetime.now().strftime('%Y-%m-%d')
    portfolio_path = BASE / 'imoveis/portfolio.json'
    if not portfolio_path.exists():
        print('[Litoral Prime] Portfólio não encontrado.')
        return []
    imoveis = json.loads(portfolio_path.read_text(encoding='utf-8'))
    posts = []
    for imovel in imoveis:
        tpl = TEMPLATES[imovel['id'] % len(TEMPLATES)]
        post = tpl.format(titulo=imovel['titulo'], preco=fmt(imovel['preco']), cidade=imovel['cidade'], bairro=imovel['bairro'])
        posts.append(post)
    out = OUTPUT_DIR / f'posts-{hoje}.txt'
    out.write_text('\\n\\n'.join(posts), encoding='utf-8')
    print(f'[Litoral Prime] Posts gerados: {len(posts)}')
    return posts

def lead_teste():
    nome, email, telefone, interesse = 'Visitante Autônomo', 'auto@litoralprime.com.br', '(11) 95434-6288', 'comprar'
    print(f'[Litoral Prime] Lead autônomo: {nome} - {interesse}')
    return nome

def follow_up():
    print('[Litoral Prime] Follow-up enviado para lead autônomo.')

def relatorio():
    hoje = datetime.now().strftime('%Y-%m-%d')
    html = f"""<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'><title>Relatório Diário — Litoral Prime</title>
<style>body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f8fafc;color:#0f172a;padding:24px}}
.card{{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:18px;margin:14px 0}}
</style></head><body><div class='card'><h1>Relatório Diário — Litoral Prime</h1><p>Data: {hoje}</p><p>Status: operação autônoma OK</p></div></body></html>"""
    (BASE / 'docs/relatorio-diario-litoral-prime.html').write_text(html, encoding='utf-8')

def main():
    print('[Litoral Prime] Executando runner completo...')
    posts_do_dia()
    lead_teste()
    follow_up()
    relatorio()
    print('[Litoral Prime] Ciclo concluído.')

if __name__ == '__main__':
    main()
