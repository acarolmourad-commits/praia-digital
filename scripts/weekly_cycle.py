#!/usr/bin/env python3
"""
Automação semanal — Praia Digital.
- Notícias: pesquisa fontes oficiais, avalia pautas, publica se houver qualidade suficiente
- Academy: verifica necessidades e oportunidades, registra sem criar material automaticamente
- PROTEÇÃO: não toca na Batch 147 sob nenhuma circunstância
"""
import json, re, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path('.').resolve()
REGISTRY = REPO / 'docs' / 'banco-editorial.json'
SITEMAP_SCRIPT = REPO / 'scripts' / 'gerar_sitemap.py'

def run_cmd(cmd: str, cwd: Path = REPO):
    """Run shell command safely."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
    return result.returncode, result.stdout, result.stderr

def update_sitemap():
    """Regenerate sitemap."""
    code, out, err = run_cmd(f'python "{SITEMAP_SCRIPT}"')
    if code == 0:
        print('[WEEKLY] sitemap atualizado')
        return True
    else:
        print(f'[WEEKLY] erro ao atualizar sitemap: {err[:200]}')
        return False

def commit_and_push(files: list, message: str):
    """Commit and push changes."""
    # git add
    for f in files:
        run_cmd(f'git add "{f}"')
    # git commit
    code, out, err = run_cmd(f'git commit -m "{message}"')
    if code != 0:
        print(f'[WEEKLY] commit falhou: {err[:200]}')
        return False
    # git push
    code, out, err = run_cmd('git push origin main')
    if code != 0:
        print(f'[WEEKLY] push falhou: {err[:200]}')
        return False
    print(f'[WEEKLY] commit/push OK: {message}')
    return True

def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f'[WEEKLY] Início — {timestamp}')

    # 1. Academy check
    code, out, err = run_cmd('python scripts/weekly_academy_check.py')
    if code == 0:
        print('[WEEKLY] Academy check OK')
    else:
        print(f'[WEEKLY] Academy check falhou: {err[:200]}')

    # 2. News check — se houver seed file, tentar publicar
    seed_file = REPO / 'docs' / 'news_seed.json'
    news_published = False
    news_files = ['noticias/index.html', 'docs/banco-editorial.json']

    if seed_file.exists():
        code, out, err = run_cmd('python scripts/weekly_news.py')
        if code == 0 and 'publicação concluída' in out:
            news_published = True
            print('[WEEKLY] Notícia publicada com sucesso')
        else:
            print(f'[WEEKLY] Notícia não publicada: {err[:200]}')
    else:
        # Registrar sem_pauta_suficiente
        registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
        if 'news_audit' not in registry:
            registry['news_audit'] = []
        registry['news_audit'].append({
            'date': timestamp,
            'status': 'sem_pauta_suficiente',
            'reason': 'Nenhuma pauta encontrada na semana',
        })
        REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding='utf-8')
        print('[WEEKLY] sem_pauta_suficiente')

    # 3. Update sitemap
    update_sitemap()
    news_files.append('sitemap.xml')

    # 4. Commit and push
    if news_published or True:  # Always commit audit updates
        commit_and_push(
            news_files,
            f'feat: automação semanal — notícias e Academy {datetime.now(timezone.utc).strftime("%Y-%m-%d")}'
        )

    print('[WEEKLY] Ciclo concluído — Batch 147 não foi tocada')

if __name__ == '__main__':
    main()
