from pathlib import Path

cleaned = 0
for p in Path('.').rglob('*.html'):
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    if 'GA4_MEASUREMENT_ID' in text:
        parts = text.split('GA4_MEASUREMENT_ID')
        if len(parts) > 2:
            new_text = parts[0] + 'GA4_MEASUREMENT_ID' + parts[1] + ''.join(parts[2:])
            p.write_text(new_text, encoding='utf-8')
            cleaned += 1
print(f'Removed duplicate GA4 placeholders in {cleaned} files')
