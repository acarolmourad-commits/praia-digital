import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DIR = REPO / 'imoveis'

FIXED = 0
SKIPPED = 0
REPAIRED = 0

for path in sorted(DIR.glob('*.html')):
    txt = path.read_text(encoding='utf-8', errors='ignore')
    has_h1_open = bool(re.search(r'<h1\b', txt, re.I))
    has_h1_close = bool(re.search(r'</h1>', txt, re.I))
    if has_h1_open and has_h1_close:
        SKIPPED += 1
        continue
    if has_h1_open and not has_h1_close:
        # repair broken <h1>...</h2> from previous run
        repaired = re.sub(r'(<h1\b[^>]*>)(.*?)(</h2>)', r'\1\2</h1>', txt, count=1, flags=re.I|re.S)
        if repaired == txt:
            ERRORS += 1
            print(f'REPAIR_FAIL: {path.name}')
            continue
        txt = repaired
        REPAIRED += 1
    # now fix first <h2>...</h2> -> <h1>...</h1>
    new_txt = re.sub(r'(<h2\b[^>]*>)(.*?)(</h2>)', r'<h1\1>\2</h1>', txt, count=1, flags=re.I|re.S)
    if new_txt == txt:
        print(f'NO_H2: {path.name}')
        continue
    path.write_text(new_txt, encoding='utf-8')
    FIXED += 1

print(f'FIXED={FIXED} REPAIRED={REPAIRED} SKIPPED={SKIPPED}')
