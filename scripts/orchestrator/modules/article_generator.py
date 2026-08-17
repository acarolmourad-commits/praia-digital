#!/usr/bin/env python3
"""
Article generator for Praia Digital editorial expansion.
Produces SEO-ready HTML articles aligned with the design system
and shared navigation template.
"""
import re
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[3]
BLOG_DIR = REPO / 'blog'
TEMPLATE_PATH = REPO / 'partials' / 'article-template.html'

# Required design system links
DESIGN_CSS = 'https://praia.digital/css/style.css'
SHARED_JS = 'https://praia.digital/js/shared.js'
CANONICAL_BASE = 'https://praia.digital/blog/'


def load_template():
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f'Template não encontrado: {TEMPLATE_PATH}')
    return TEMPLATE_PATH.read_text(encoding='utf-8')


def slugify(text):
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text.strip('-')


def generate_article(target, template=None):
    """
    Generate an article HTML file from an expansion target.
    
    Expected target keys:
    - title/titulo
    - city
    - cluster
    - primary_keyword
    - keywords (list)
    - meta_description
    - recommended_cta
    - hotmart_link (optional)
    - product_related_id (optional)
    """
    if template is None:
        template = load_template()
    
    title = target.get('title') or target.get('titulo') or 'Artigo'
    city = target.get('city') or 'litoral'
    cluster = target.get('cluster') or 'editorial'
    pk = target.get('primary_keyword') or title
    keywords = target.get('keywords') or [pk]
    meta_desc = target.get('meta_description') or ''
    cta = target.get('recommended_cta') or 'Fale conosco pelo WhatsApp: (11) 95434-6288.'
    hotmart = target.get('hotmart_link') or 'https://wa.me/5511954346288'
    if 'wa.me' not in hotmart:
        cta = cta + ' Fale conosco pelo WhatsApp: (11) 95434-6288.'
    
    slug = slugify(f"{city} {title}")
    filename = f"{slug}.html"
    path = BLOG_DIR / filename
    
    # Build article HTML
    article = template
    
    # Replace placeholders
    article = article.replace('{{TITLE}}', title)
    article = article.replace('{{META_DESCRIPTION}}', meta_desc)
    article = article.replace('{{PRIMARY_KEYWORD}}', pk)
    article = article.replace('{{CITY}}', city.replace('_', ' ').title())
    article = article.replace('{{CLUSTER}}', cluster)
    article = article.replace('{{URL}}', f"{CANONICAL_BASE}{filename}")
    article = article.replace('{{KEYWORDS_LIST}}', ', '.join(keywords[:5]))
    article = article.replace('{{CTA_TEXT}}', cta)
    article = article.replace('{{HOTMART_LINK}}', hotmart or '#')
    article = article.replace('{{DATE}}', datetime.now().strftime('%Y-%m-%d'))
    
    # Inject shared navigation markers
    if '<meta name="pd-shared-nav">' not in article:
        article = article.replace('</head>', '<meta name="pd-shared-nav">\n</head>')
    if '<meta name="pd-shared-footer">' not in article:
        article = article.replace('</body>', '<meta name="pd-shared-footer">\n</body>')
    if SHARED_JS not in article:
        article = article.replace('</body>', f'<script src="{SHARED_JS}"></script>\n</body>')
    if DESIGN_CSS not in article:
        article = article.replace('</head>', f'<link rel="stylesheet" href="{DESIGN_CSS}">\n</head>')
    
    return path, article, filename


def write_article(target, template=None, dry_run=False):
    path, article, filename = generate_article(target, template)
    
    if dry_run:
        print(f'[DRY RUN] {path}')
        return path
    
    if path.exists():
        print(f'SKIP (exists): {path}')
        return None
    
    path.write_text(article, encoding='utf-8')
    print(f'WRITE: {path}')
    return path


def generate_batch(targets, batch_size=10, dry_run=False):
    """
    Generate a batch of articles from expansion targets.
    Returns list of written paths.
    """
    template = load_template()
    written = []
    
    for target in targets[:batch_size]:
        path = write_article(target, template, dry_run=dry_run)
        if path:
            written.append(path)
    
    return written


if __name__ == '__main__':
    # Quick smoke test
    test_target = {
        'title': 'Guia de locação de temporada em Ubatuba — análise 2026',
        'city': 'ubatuba',
        'cluster': 'locacao_temporada',
        'primary_keyword': 'locação de temporada ubatuba',
        'keywords': ['locação ubatuba', 'temporada ubatuba', 'aluguel ubatuba'],
        'meta_description': 'Guia completo de locação de temporada em Ubatuba: preços, ocupação, dicas e rentabilidade em 2026.',
        'recommended_cta': 'Quer profissionalizar seu imóvel? Veja a formação completa.',
        'hotmart_link': 'https://www.hotmart.com/pt-br/producto/curso-gestao-temporada',
    }
    
    path, article, filename = generate_article(test_target)
    print(f'SMOKE_TEST: {path}')
    print(f'FILENAME: {filename}')
    print(f'SIZE: {len(article)} bytes')
