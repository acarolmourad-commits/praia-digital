from pathlib import Path
import re

p = Path('scripts/regenerate_landings.py')
text = p.read_text(encoding='utf-8', errors='ignore')

# Find last item start
item_starts = list(re.finditer(r'\n    \{', text))
start = item_starts[-1].start()

# Find end of last item by brace counting
brace_count = 0
in_string = False
escape = False
i = start
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

end = i + 1
print('LAST_ITEM_ENDS_AT', end)
print('AFTER_LAST_ITEM:', repr(text[end:end+100]))
