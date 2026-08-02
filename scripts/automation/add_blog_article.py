#!/usr/bin/env python3
"""
add_blog_article.py
Adiciona Article JSON-LD nas páginas de blog que ainda não têm esse schema.
"""
from pathlib import Path
import re, json

BASE = Path(__file__).resolve().parents[2]
BLOG = BASE / 'blog'

def extract_title(text: str, fallback: str):
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    return fallback

def extract_meta_description(text: str):
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        return m.group(1).strip()
    return ''

def extract_image(text: str, path: Path):
    m = re.search(r'<img[^>]+src=["\'](.*?)["\']', text, re.S|re.I)
    if m:
        src = m.group(1).strip()
        if src.startswith('http'):
            return src
        return 'https://acarolmourad.github.io/praia-digital/' + str(path.relative_to(BASE)).replace('\\', '/')
    return 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/default-home.jpg'

updated = 0
skipped = 0
errors = 0
for path in sorted(BLOG.glob('*.html')):
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        errors += 1
        continue
    if 'Article' in text and 'application/ld+json' in text:
        skipped += 1
        continue
    title = extract_title(text, path.stem)
    description = extract_meta_description(text) or title
    image = extract_image(text, path)
    rel_path = str(path.relative_to(BASE)).replace('\\', '/')
    url = 'https://acarolmourad.github.io/praia-digital/' + rel_path
    article = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': title,
        'description': description,
        'url': url,
        'image': image,
        'author': {
            '@type': 'Organization',
            'name': 'Litoral Prime Imóveis',
        },
        'publisher': {
            '@type': 'Organization',
            'name': 'Litoral Prime Imóveis',
            'logo': {
                '@type': 'ImageObject',
                'url': 'https://acarolmourad.github.io/praia-digital/litoral-prime-imoveis/img/logo.png',
            },
        },
    }
    article_json = json.dumps(article, ensure_ascii=False, indent=2)
    injection = f'<script type="application/ld+json">\n{article_json}\n</script>\n'
    if '</main>' in text:
        text = text.replace('</main>', injection + '</main>', 1)
    elif '</body>' in text:
        text = text.replace('</body>', injection + '</body>', 1)
    else:
        text += '\n' + injection
    try:
        path.write_text(text, encoding='utf-8')
        print('updated', path.relative_to(BASE))
        updated += 1
    except Exception as e:
        print('write error', path.relative_to(BASE), e)
        errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
