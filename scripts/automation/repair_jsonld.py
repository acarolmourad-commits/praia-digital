#!/usr/bin/env python3
"""
repair_jsonld.py
Repara blocos JSON-LD inválidos que contêm múltiplos objetos JSON
separando-os em múltiplas tags <script> distintas.
"""
from pathlib import Path
import re, json

BASE = Path(__file__).resolve().parents[2]

def split_json_objects(text: str):
    objs = []
    decoder = json.JSONDecoder()
    start = 0
    while start < len(text):
        obj, end = decoder.raw_decode(text, start)
        objs.append(json.dumps(obj, ensure_ascii=False, indent=2))
        start = end
        while start < len(text) and text[start] in ' \t\n\r,':
            start += 1
    return objs

updated = 0
skipped = 0
errors = 0
for path in sorted(BASE.rglob('*.html')):
    rel = path.relative_to(BASE)
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        errors += 1
        continue
    flag = {'changed': False}

    def repl(m):
        json_text = m.group(1).strip()
        try:
            json.loads(json_text)
            return m.group(0)
        except Exception:
            try:
                objs = split_json_objects(json_text)
                if len(objs) <= 1:
                    return m.group(0)
                flag['changed'] = True
                return '\n'.join(
                    '<script type="application/ld+json">\n' + obj + '\n</script>'
                    for obj in objs
                )
            except Exception as e2:
                print('repair failed', rel, e2)
                return m.group(0)

    new_text = re.sub(r'<script type="application/ld\+json">(.*?)</script>\s*', repl, text, flags=re.S)
    if flag['changed']:
        try:
            path.write_text(new_text, encoding='utf-8')
            print('repaired', rel)
            updated += 1
        except Exception as e:
            print('write error', rel, e)
            errors += 1
print('done', 'updated=', updated, 'skipped=', skipped, 'errors=', errors)
