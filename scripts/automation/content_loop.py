#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orquestrador do loop de criação de conteúdo Praia Digital.
Unifica: geração de landings + atualização de sitemap + opção de commit/push.
"""
import sys
import subprocess
from pathlib import Path

REPO = Path('.').resolve()

def run(cmd, label):
    print(f'\n=== {label} ===')
    result = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f'FALHOU: {label} (exit {result.returncode})')
        sys.exit(result.returncode)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'landings'

    if mode == 'landings':
        run('python scripts/automation/generate_landings_safe.py', 'Gerar landings')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git commit -m "feat: new landings + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de landings concluído.')

    elif mode == 'blog':
        run('python scripts/automation/gerador_lote_artigos_seo_diario.py', 'Gerar artigos SEO')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git commit -m "feat: new blog articles + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de blog concluído.')

    elif mode == 'full':
        run('python scripts/automation/generate_landings_safe.py', 'Gerar landings')
        run('python scripts/automation/gerador_lote_artigos_seo_diario.py', 'Gerar artigos SEO')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git commit -m "feat: content batch (landings+blog) + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop full concluído.')

    else:
        print('Uso: python content_loop.py [landings|blog|full]')

if __name__ == '__main__':
    main()
