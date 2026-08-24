#!/usr/bin/env python3
"""
Publication gate for Praia Digital editorial pipeline.
Fail-closed validator for blog/ articles before they are committed/published.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BLOG_DIR = REPO / 'blog'

# Thresholds
MIN_WORDS = 120
MIN_CONTENT_SIZE = 800
MIN_H2_COUNT = 2
MIN_INTERNAL_LINKS = 1

# Known minimal/placeholder markers
PLACEHOLDER_MARKERS = [
    'conteúdo completo em breve',
    'conteúdo em desenvolvimento',
    'em breve',
    'coming soon',
    'content coming soon',
    'placeholder',
    'a ser definido',
    'a definir',
    'em construção',
    'em construcao',
    'site em manutenção',
    'site em manutencao',
]

# Generic repeated phrase pattern
GENERIC_PATTERNS = [
    r'Aluguel de temporada exige gestão profissional de reservas, limpeza, regras de cancelamento e atendimento ao hóspede\.',
    r'Imóvel no litoral: investimento em imóvel usado\.',
    r'Imóvel usado exige avaliação\.',
    r'Investimento exige inspeção\.',
    r'Dica reduz risco\.',
    r'Obra exige orçamento\.',
    r'Reforma exige controle\.',
    r'Averbação reduz risco\.',
    r'Imóvel exige atualização\.',
    r'Dica reduz custo\.',
    r'Dica reduz desperdício\.',
]

# Required SEO elements
REQUIRED_TITLE = re.compile(r'<title[^>]*>.*?</title>', re.I | re.S)
REQUIRED_META_DESCRIPTION = re.compile(r'<meta[^>]+name=["\']description["\'][^>]*>', re.I)
REQUIRED_CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
REQUIRED_H1 = re.compile(r'<h1[^>]*>.*?</h1>', re.I | re.S)
REQUIRED_H2 = re.compile(r'<h2[^>]*>.*?</h2>', re.I | re.S)
REQUIRED_LINK = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>', re.I)


def count_words(html_text: str) -> int:
    """Count visible words, stripping HTML tags."""
    text = re.sub(r'<[^>]+>', ' ', html_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return len(text.split())


def extract_internal_links(html_text: str):
    hrefs = REQUIRED_LINK.findall(html_text)
    domain = 'praia.digital'
    internal = []
    for h in hrefs:
        if h.startswith(('/blog/', '/education/', '/noticias/', 'blog/', 'education/', 'noticias/')):
            internal.append(h)
            continue
        if h.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:')):
            if domain in h:
                internal.append(h)
            continue
        if h.endswith('.html') or h.endswith('.htm'):
            internal.append(h)
    return internal


def check_placeholder(html_text: str) -> str | None:
    """Return first matched placeholder marker, or None."""
    lower = html_text.lower()
    for marker in PLACEHOLDER_MARKERS:
        if marker in lower:
            return marker
    return None


def check_generic_repetition(html_text: str) -> str | None:
    """Detect if the body is mostly generic template phrases."""
    body_match = re.search(r'<body[^>]*>(.*)</body>', html_text, re.I | re.S)
    body = body_match.group(1) if body_match else html_text
    matched = 0
    total = len(GENERIC_PATTERNS)
    for pattern in GENERIC_PATTERNS:
        if re.search(pattern, body, re.I):
            matched += 1
    if matched >= 3:
        return f'{matched}/{total} generic patterns matched'
    return None


def diversity_ratio(text: str) -> float:
    words = re.findall(r'\w+', text.lower())
    total = len(words)
    if total == 0:
        return 0.0
    unique = len(set(words))
    return unique / total


def check_low_specificity(html_text: str) -> dict | None:
    """Block when lexical diversity is extremely low regardless of sentence count."""
    body_match = re.search(r'<body[^>]*>(.*)</body>', html_text, re.I | re.S)
    body = body_match.group(1) if body_match else html_text
    text = re.sub(r'<[^>]+>', ' ', body)
    ratio = diversity_ratio(text)
    if ratio < 0.02:
        return {
            'rule': 'low_specificity',
            'reason': 'Conteúdo com baixa especificidade lexical',
            'found': f'{ratio:.4f} (extremely_low_diversity)',
            'expected': 'diversidade lexical >= 0.02',
            'action': 'Enriquecer conteúdo com termos específicos e variados antes da publicação',
        }
    return None


def validate_article(html_path: Path) -> dict:
    """Validate a single article against publication gate rules."""
    if not html_path.exists():
        return {
            'file': str(html_path.relative_to(REPO)),
            'pass': False,
            'blocked': True,
            'reason': 'file_missing',
            'detail': 'Arquivo não existe',
            'expected': 'existente',
            'found': 'ausente',
            'action': 'Criar o arquivo com conteúdo completo antes de publicar',
        }

    txt = html_path.read_text(encoding='utf-8', errors='ignore')
    rel = str(html_path.resolve().relative_to(REPO))
    issues = []

    # 1) Placeholder / minimal content
    placeholder = check_placeholder(txt)
    if placeholder:
        issues.append({
            'rule': 'placeholder_detected',
            'reason': 'Página contém placeholder mínimo',
            'found': placeholder,
            'expected': 'Conteúdo desenvolvido sem placeholder',
            'action': 'Remover placeholder e enriquecer o conteúdo antes da publicação',
        })

    # 2) Generic repetition
    generic = check_generic_repetition(txt)
    if generic:
        issues.append({
            'rule': 'generic_repetition',
            'reason': 'Página contém repetição de texto genérico mínimo',
            'found': generic,
            'expected': 'Conteúdo original e desenvolvido',
            'action': 'Substituir textos genéricos por conteúdo específico do tema',
        })

    # 3) Low specificity / lexical diversity
    low_spec = check_low_specificity(txt)
    if low_spec:
        issues.append({
            'rule': low_spec['rule'],
            'reason': low_spec['reason'],
            'found': low_spec['found'],
            'expected': low_spec['expected'],
            'action': low_spec['action'],
        })

    # 4) Word count / content size
    words = count_words(txt)
    if words < MIN_WORDS:
        issues.append({
            'rule': 'min_words',
            'reason': 'Conteúdo insuficiente',
            'found': f'{words} palavras',
            'expected': f'>= {MIN_WORDS} palavras',
            'action': 'Expandir o artigo até atingir o mínimo de palavras',
        })
    if len(txt) < MIN_CONTENT_SIZE:
        issues.append({
            'rule': 'min_content_size',
            'reason': 'Tamanho mínimo do conteúdo não atingido',
            'found': f'{len(txt)} bytes',
            'expected': f'>= {MIN_CONTENT_SIZE} bytes',
            'action': 'Adicionar seções e conteúdo para atingir o tamanho mínimo',
        })

    # 4) H2 count
    h2_count = len(REQUIRED_H2.findall(txt))
    if h2_count < MIN_H2_COUNT:
        issues.append({
            'rule': 'min_h2',
            'reason': 'Número insuficiente de H2',
            'found': f'{h2_count} H2',
            'expected': f'>= {MIN_H2_COUNT} H2',
            'action': 'Adicionar seções H2 com conteúdo desenvolvido',
        })

    # 5) Required SEO elements
    if not REQUIRED_TITLE.search(txt):
        issues.append({
            'rule': 'missing_title',
            'reason': 'Título ausente',
            'found': 'ausente',
            'expected': '<title>',
            'action': 'Incluir tag <title> com título do artigo',
        })
    if not REQUIRED_META_DESCRIPTION.search(txt):
        issues.append({
            'rule': 'missing_meta_description',
            'reason': 'Meta description ausente',
            'found': 'ausente',
            'expected': '<meta name="description">',
            'action': 'Incluir meta description coerente',
        })
    if not REQUIRED_CANONICAL.search(txt):
        issues.append({
            'rule': 'missing_canonical',
            'reason': 'Canonical ausente',
            'found': 'ausente',
            'expected': '<link rel="canonical">',
            'action': 'Incluir canonical apontando para a própria URL',
        })
    if not REQUIRED_H1.search(txt):
        issues.append({
            'rule': 'missing_h1',
            'reason': 'H1 ausente',
            'found': 'ausente',
            'expected': '<h1>',
            'action': 'Incluir um H1 com o título do artigo',
        })

    # 6) Internal links
    internal_links = extract_internal_links(txt)
    if len(internal_links) < MIN_INTERNAL_LINKS:
        issues.append({
            'rule': 'min_internal_links',
            'reason': 'Links internos insuficientes',
            'found': f'{len(internal_links)} links',
            'expected': f'>= {MIN_INTERNAL_LINKS} link(s) interno(s)',
            'action': 'Adicionar links internos relevantes para o site',
        })

    blocked = len(issues) > 0
    return {
        'file': rel,
        'pass': not blocked,
        'blocked': blocked,
        'issues': issues,
        'words': words,
        'size': len(txt),
        'h2_count': h2_count,
        'internal_links': len(internal_links),
    }


def validate_directory(path: Path) -> dict:
    """Validate all HTML files in a directory."""
    results = []
    blocked = 0
    passed = 0
    for html in sorted(path.glob('*.html')):
        result = validate_article(html)
        results.append(result)
        if result['blocked']:
            blocked += 1
        else:
            passed += 1
    return {
        'checked': len(results),
        'passed': passed,
        'blocked': blocked,
        'results': results,
    }


def block_report(result: dict) -> str:
    """Format a clear block message for CLI/CI."""
    lines = [
        f"BLOCK_PUBLICATION: {result['file']}",
        f"  Regras violadas: {len(result['issues'])}",
    ]
    for issue in result['issues']:
        lines.append(f"  - [{issue['rule']}] {issue['reason']}")
        lines.append(f"      encontrado : {issue['found']}")
        lines.append(f"      esperado  : {issue['expected']}")
        lines.append(f"      ação       : {issue['action']}")
    return '\n'.join(lines)


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print('Usage: publication_gate.py <path_or_dir> [...]')
        return 2

    total_checked = 0
    total_blocked = 0
    all_results = []
    for raw in argv:
        p = Path(raw)
        if not p.exists():
            result = {
                'file': str(p),
                'pass': False,
                'blocked': True,
                'issues': [{
                    'rule': 'missing_path',
                    'reason': 'Caminho informado não existe',
                    'found': str(p),
                    'expected': 'arquivo ou diretório existente',
                    'action': 'Verificar o caminho e tentar novamente',
                }],
            }
            all_results.append(result)
            total_blocked += 1
            total_checked += 1
            continue

        if p.is_dir():
            batch = validate_directory(p)
            total_checked += batch['checked']
            total_blocked += batch['blocked']
            all_results.extend(batch['results'])
        else:
            total_checked += 1
            result = validate_article(p)
            all_results.append(result)
            if result['blocked']:
                total_blocked += 1

    for result in all_results:
        if result.get('blocked'):
            print(block_report(result))

    if total_blocked > 0:
        print(f'\nBLOCK_PUBLICATION: {total_blocked}/{total_checked} arquivos bloqueados')
        return 1

    print(f'PASS: {total_checked}/{total_checked} arquivos válidos para publicação')
    return 0


def run(paths):
    """Batch interface expected by orchestrator_24h."""
    results = {}
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            batch = validate_directory(p)
            for r in batch['results']:
                results[r['file']] = r
        else:
            r = validate_article(p)
            results[str(r['file'])] = r
    return results


if __name__ == '__main__':
    sys.exit(main())
