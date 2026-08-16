#!/usr/bin/env python3
"""
Auditoria automática de vazamentos de valor — rotina reutilizável.
Escopo por padrão: blog/*.html
Saída: docs/comercial/auditoria_vazamentos_valor_<data>.md
"""
import re, csv
from pathlib import Path
from datetime import datetime

root = Path('C:/Users/Carolina/praia-digital')
OUT_DIR = root / 'docs' / 'comercial'
BLOG_DIR = root / 'blog'

SERVICES = [
    'administração airbnb', 'administracao airbnb', 'administração temporada', 'administracao temporada',
    'edição de anúncio', 'edicao de anuncio', 'fotografia', 'seo local'
]
ACADEMY_KEYWORDS = ['academy', 'curso', 'aula']
CTA_PATTERNS = re.compile(r'class="[^"]*cta|cta|compre|matricule|contrat|agende|fale.*whatsapp|whatsapp.*contato', re.I)
TRAFFIC_SIGNALS = re.compile(r'invest|temporada|aluguel|turismo|receita|rentabilidade|lucratividade|diária|diaria|alta temporada', re.I)


def classify_page(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    lower = text.lower()
    title = re.search(r'<title[^>]*>(.*?)</title>', text, re.I)
    title_text = title.group(1) if title else path.name

    has_cta = bool(CTA_PATTERNS.search(text))
    svc_found = [s for s in SERVICES if s in lower]
    aca_found = [a for a in ACADEMY_KEYWORDS if a in lower]
    traffic = bool(TRAFFIC_SIGNALS.search(lower))

    issues = []
    if not has_cta and traffic:
        issues.append('sem_cta_com_trafego')
    if not has_cta:
        issues.append('sem_cta')
    if has_cta and not svc_found and not aca_found:
        issues.append('cta_sem_destino_forte')
    if svc_found and not aca_found:
        issues.append('conteudo_comercial_sem_curso')
    if not svc_found and aca_found:
        issues.append('curso_sem_conteudo_entrada')
    if svc_found and not has_cta:
        issues.append('servico_sem_cta')

    return {
        'file': path.name,
        'title': title_text,
        'issues': issues,
        'traffic': traffic,
        'svc': svc_found,
        'aca': aca_found,
    }


def run():
    files = sorted(BLOG_DIR.glob('*.html'))
    results = [classify_page(p) for p in files]

    counts = {}
    for r in results:
        for issue in r['issues']:
            counts[issue] = counts.get(issue, 0) + 1

    today = datetime.now().strftime('%Y-%m-%d')
    out_path = OUT_DIR / f'auditoria_vazamentos_valor_{today}.md'
    lines = [
        f'# Auditoria de vazamentos de valor — {today}\n',
        f'Escopo: {len(results)} páginas do blog.\n',
        '## Contagem por tipo de problema\n'
    ]
    for issue, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f'- {issue}: {count}')
    lines.append('\n## Páginas prioritárias (sem CTA e com tráfego potencial)\n')
    priority = [r for r in results if 'sem_cta_com_trafego' in r['issues']]
    for r in priority[:20]:
        lines.append(f"- {r['file']} | {r['title']}")
    lines.append('\n## Amostras — conteúdo comercial sem curso correspondente\n')
    content_no_course = [r for r in results if 'conteudo_comercial_sem_curso' in r['issues']]
    for r in content_no_course[:20]:
        lines.append(f"- {r['file']} | serviços: {r['svc']}")
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Auditoria gerada em {out_path} — {len(results)} páginas, {len(priority)} prioritárias')
    return str(out_path)


if __name__ == '__main__':
    run()
