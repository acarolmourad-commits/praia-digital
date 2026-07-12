from pathlib import Path
from datetime import date

root = Path("C:/Users/Carolina/praia-digital")
tracker = root / "docs/sales/followup-registro.md"
out_dir = root / "outreach/followups-pendentes"
out_dir.mkdir(parents=True, exist_ok=True)

if not tracker.exists():
    print("Tracker não encontrado.")
    raise SystemExit(1)

text = tracker.read_text(encoding="utf-8")
today = date.today().isoformat()

lines = []
count = 0
for line in text.splitlines():
    if today in line and "follow-up" in line.lower():
        count += 1
        safe = line.strip().replace(" ", "_").replace("|", "_")
        filename = f"followup-pendente-{count:03d}.html"
        content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Follow-up pendente — {today}</title>
</head>
<body>
<h1>Follow-up pendendo</h1>
<pre>{line}</pre>
<p>Use este arquivo para copiar o texto para WhatsApp/formulário/Brevo.</p>
</body>
</html>"""
        (out_dir / filename).write_text(content, encoding="utf-8")
    lines.append(line)

print(f"Follow-ups pendentes gerados: {count}")
print(f"Pasta: {out_dir}")
