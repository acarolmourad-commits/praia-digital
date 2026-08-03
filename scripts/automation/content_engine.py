#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de conteúdo Praia Digital.
Modos:
  landings        -> gera landings de imóveis (generate_landings_safe + sitemap + commit/push)
  blog            -> gera artigos SEO (gerador_lote_artigos_seo_diario + sitemap + commit/push)
  social          -> gera posts sociais a partir de temas (docs/materiais/calendario_conteudo_30dias + commit)
  full            -> landings + blog + social + sitemap + commit/push
  regenerate_sitemap -> apenas atualiza lastmod do sitemap
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

def ensure_content_loop():
    # content_loop já commitado, só referenciar
    return 'python scripts/automation/content_loop.py'

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'landings'

    if mode == 'landings':
        run('python scripts/automation/generate_landings_safe.py', 'Gerar landings')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "feat: new landings + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de landings concluído.')

    elif mode == 'blog':
        run('python scripts/automation/gerador_lote_artigos_seo_diario.py', 'Gerar artigos SEO')
        run('python scripts/automation/update_blog_index.py', 'Atualizar blog/index.html')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "feat: new blog articles + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de blog concluído.')

    elif mode == 'social':
        run('python scripts/automation/gerar_calendario_conteudo_30dias.py', 'Gerar calendário de conteúdo')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "chore: update content calendar (social)"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de social concluído.')

    elif mode == 'full':
        run('python scripts/automation/generate_landings_safe.py', 'Gerar landings')
        run('python scripts/automation/gerador_lote_artigos_seo_diario.py', 'Gerar artigos SEO')
        run('python scripts/automation/update_blog_index.py', 'Atualizar blog/index.html')
        run('python scripts/automation/gerar_calendario_conteudo_30dias.py', 'Gerar calendário de conteúdo')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "feat: content batch (landings+blog+social) + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop full concluído.')

    elif mode == 'regenerate_sitemap':
        run('python litoral-prime-imoveis/scripts/update_sitemap_lastmod.py', 'Atualizar lastmod do sitemap')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "chore: sitemap lastmod refresh"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Sitemap atualizado.')

    elif mode == 'cities':
        run('python scripts/automation/generate_city_service_pages.py', 'Gerar páginas cidade-servico')
        run('python scripts/automation/add_landings_to_sitemap.py', 'Atualizar sitemap')
        run('git add -A', 'Git add')
        run('git diff --cached --quiet || git commit -m "feat: regenerate city-service pages + sitemap update"', 'Git commit')
        run('git push origin main', 'Git push')
        print('\n✅ Loop de cidades concluído.')

    else:
        print('Uso: python scripts/automation/content_engine.py [landings|blog|social|full|regenerate_sitemap|cities]')
        sys.exit(1)

if __name__ == '__main__':
    main()
