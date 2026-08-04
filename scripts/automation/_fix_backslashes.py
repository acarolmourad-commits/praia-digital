import re
from pathlib import Path
root=Path('.').resolve()
fixed=0
for p in root.rglob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if '\\' in txt:
        new_txt=txt.replace('\\', '/')
        if new_txt!=txt:
            p.write_text(new_txt, encoding='utf-8')
            fixed+=1
print('fixed_files', fixed)
