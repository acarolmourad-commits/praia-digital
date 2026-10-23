#!/usr/bin/env python3
"""Praia Digital 2026-10-23: elimina residuos /apps/<slug>/index.html.

Idempotente. Altera apenas:
- partials/header.html: /apps/<slug>/index.html -> /apps/<slug>/ (3 links da navegacao compartilhada injetada no deploy)
- apps/index.html: https://praia.digital/apps/index.html -> https://praia.digital/apps/ (canonical JSON-LD + og:url)
- scripts/validate_render_deploy.py: modo PR so aceita refs/pull/N/merge (remove atalho branch == HEAD que fazia test_pr_mode_is_validation_only falhar)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_LINK = re.compile(r"(/apps/[a-z0-9\-]+)/index\.html")


def patch(path, transforms):
    p = ROOT / path
    if not p.exists():
        print(f"SKIP missing {path}")
        return 0
    text = p.read_text(encoding="utf-8", errors="ignore")
    original = text
    total = 0
    for fn in transforms:
        text, n = fn(text)
        total += n
    if text != original:
        p.write_text(text, encoding="utf-8")
    print(f"{path}: {total} substituicao(oes)")
    return total


def app_links(text):
    return APP_LINK.subn(r"\1/", text)


def canonical(text):
    old = "https://praia.digital/apps/index.html"
    return text.replace(old, "https://praia.digital/apps/"), text.count(old)


def validator_fix(text):
    old = ' or branch == "HEAD"'
    return text.replace(old, ""), text.count(old)


def main():
    total = 0
    total += patch("partials/header.html", [app_links])
    total += patch("apps/index.html", [canonical, app_links])
    total += patch("scripts/validate_render_deploy.py", [validator_fix])
    print(f"TOTAL: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
