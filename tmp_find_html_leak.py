from pathlib import Path
import re

REPO = Path(".")
issues = []
for p in list(REPO.glob("assets/*.html")) + list(REPO.glob("servicos/*.html")):
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    rel = str(p.relative_to(REPO)).replace("\\", "/")
    m = re.search(r"</html>([\s\S]*)$", text, re.I)
    if m:
        after = m.group(1).strip()
        if after:
            issues.append((rel, "AFTER_HTML", after[:180]))
    open_html = len(re.findall(r"<html[\s>]", text, re.I))
    close_html = len(re.findall(r"</html>", text, re.I))
    if close_html > open_html:
        issues.append((rel, f"CLOSE_HTML={close_html} OPEN_HTML={open_html}", ""))
for rel, kind, snippet in issues[:50]:
    print(rel, kind, snippet)
print("TOTAL_ISSUES", len(issues))
