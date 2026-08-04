import re
from pathlib import Path
root=Path('.').resolve()
fixed=0
for p in root.rglob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    new_txt=re.sub(r'(href=")([^"]*?)\\([^"]*?)(")', lambda m: m.group(1)+m.group(2).replace('\\','/')+m.group(3)+m.group(4), txt)
    if new_txt!=txt:
        p.write_text(new_txt, encoding='utf-8')
        fixed+=1
print('fixed_files', fixed)
