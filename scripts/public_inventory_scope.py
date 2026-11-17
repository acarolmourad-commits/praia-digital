"""Keep public indexes limited to the active catalog and public editorial content."""
import json
import re
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PREFIXES = ('newsletter/drafts/', 'exclusivos/')


@lru_cache(maxsize=16)
def catalog_paths(root=ROOT):
    source = Path(root) / 'js/main.js'
    if not source.is_file():
        return frozenset()
    match = re.search(r'const properties\s*=\s*(\[[\s\S]*?\]);', source.read_text(encoding='utf-8'))
    if not match:
        raise ValueError('Active property catalog could not be read')
    records = json.loads(match[1])
    if not records:
        raise ValueError('Refusing to index properties from an empty catalog')
    paths = set()
    for record in records:
        slug = record['slug']
        path = slug[3:] + '.html' if slug.startswith('../') else 'imoveis/' + slug + '.html'
        if '..' in Path(path).parts or path.startswith('/'):
            raise ValueError('Unsafe active property path')
        paths.add(unquote(path))
    return frozenset(paths)


def excluded_from_public_index(rel, root=ROOT):
    rel = unquote(rel).lstrip('/')
    if rel.startswith(PRIVATE_PREFIXES):
        return True
    if rel.startswith('imoveis/') and rel != 'imoveis/index.html':
        return rel not in catalog_paths(root)
    return False
