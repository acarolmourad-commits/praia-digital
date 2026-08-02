from pathlib import Path
import re

p = Path('scripts/regenerate_landings.py')
text = p.read_text(encoding='utf-8', errors='ignore')

last_item_match = None
for m in re.finditer(r'\{\s*"slug":\s*"[^"]+"', text):
    last_item_match = m

if not last_item_match:
    print('NO_ITEMS_FOUND')
    exit()

item_start = last_item_match.start()
brace_count = 0
in_string = False
escape = False
i = item_start
while i < len(text):
    c = text[i]
    if escape:
        escape = False
    elif c == '\\':
        escape = True
    elif c == '"' and not escape:
        in_string = not in_string
    elif not in_string:
        if c == '{':
            brace_count += 1
        elif c == '}':
            brace_count -= 1
            if brace_count == 0:
                break
    i += 1

item_end = i + 1
print('LAST_ITEM_ENDS_AT', item_end)
print('CONTEXT:', repr(text[item_end:item_end+50]))
