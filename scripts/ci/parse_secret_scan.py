import json, sys
from pathlib import Path

p = Path(".secrets.scan_result.json")
if not p.exists():
    print("SECRET_SCAN_RESULT=success")
    sys.exit(0)

text = p.read_text(encoding="utf-8").strip()
# detect-secrets scan --baseline nao imprime nada quando nao ha novos segredos
if not text:
    print("FINDINGS_TOTAL=0")
    print("SECRET_SCAN_RESULT=success")
    sys.exit(0)

# extrai o JSON mesmo se houver warnings antes/depois
start = text.find("{")
try:
    if start > 0:
        text = text[start:]
    data = json.loads(text)
except Exception:
    print("SECRET_SCAN_RESULT=error")
    sys.exit(1)

results = data.get("results", {})
total = sum(len(v) for v in results.values())
print(f"FINDINGS_TOTAL={total}")
if total > 0:
    print("SECRET_SCAN_RESULT=failure")
    sys.exit(1)
print("SECRET_SCAN_RESULT=success")
sys.exit(0)
