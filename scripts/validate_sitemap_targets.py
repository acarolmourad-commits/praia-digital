#!/usr/bin/env python3
"""Check that sitemap URLs resolve to files in the published static checkout.

This is an offline pre-deploy check, not a replacement for Search Console or
production HTTP checks. Directory URLs resolve to index.html; URL-encoded paths
are decoded before lookup. No files are modified.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
DEFAULT_ROOT = Path(__file__).resolve().parents[1]


class IndexingDirectives(HTMLParser):
    """Read existing indexing directives without changing a page's intent."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.reasons = set()

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attrs = {key: (value or "") for key, value in attrs}
        name = attrs.get("name", "").lower().strip()
        directives = attrs.get("content", "").lower().replace(",", " ").split()
        if name in ("robots", "googlebot") and any(value in ("noindex", "none") for value in directives):
            self.reasons.add("noindex")
        if attrs.get("http-equiv", "").lower().strip() == "refresh":
            self.reasons.add("meta refresh")


def indexing_exclusions(path: Path) -> list[str]:
    """Return explicit HTML reasons to omit a URL from a search sitemap."""
    if path.suffix.lower() not in (".html", ".htm"):
        return []
    parser = IndexingDirectives()
    parser.feed(path.read_text(encoding="utf-8"))
    return sorted(parser.reasons)


def validate_sitemap(sitemap: Path, root: Path) -> list[str]:
    """Return actionable errors without fetching any external URLs."""
    root = root.resolve()
    try:
        document = ET.parse(sitemap)
    except (OSError, ET.ParseError) as exc:
        return [f"{sitemap.name}: cannot read sitemap: {exc}"]
    if document.getroot().tag != f"{{{NAMESPACE}}}urlset":
        return [f"{sitemap.name}: expected sitemap urlset"]
    errors: list[str] = []
    seen: set[str] = set()
    entries = document.findall(f"{{{NAMESPACE}}}url")
    if not entries:
        return [f"{sitemap.name}: sitemap contains no URLs"]
    for entry in entries:
        loc = entry.find(f"{{{NAMESPACE}}}loc")
        url = (loc.text or "").strip() if loc is not None else ""
        if not url:
            errors.append(f"{sitemap.name}: URL entry is missing loc")
            continue
        if url in seen:
            errors.append(f"{sitemap.name}: duplicate URL: {url}")
        seen.add(url)
        try:
            parts = urlsplit(url)
        except ValueError:
            errors.append(f"{sitemap.name}: invalid URL: {url}")
            continue
        if parts.scheme != "https" or parts.netloc != "praia.digital":
            errors.append(f"{sitemap.name}: unexpected site URL: {url}")
            continue
        if parts.query or parts.fragment:
            errors.append(f"{sitemap.name}: query or fragment in sitemap URL: {url}")
            continue
        decoded = unquote(parts.path)
        if "\x00" in decoded or "\\" in decoded or ".." in Path(decoded).parts:
            errors.append(f"{sitemap.name}: unsafe URL path: {url}")
            continue
        target = (root / decoded.lstrip("/")).resolve()
        if not target.is_relative_to(root):
            errors.append(f"{sitemap.name}: URL escapes site root: {url}")
            continue
        if not target.is_file():
            target = (target / "index.html").resolve()
        if not target.is_relative_to(root):
            errors.append(f"{sitemap.name}: URL escapes site root: {url}")
        elif not target.is_file():
            errors.append(f"{sitemap.name}: missing local target: {url}")
        else:
            try:
                reasons = indexing_exclusions(target)
            except (OSError, UnicodeError) as exc:
                errors.append(f"{sitemap.name}: cannot read target {url}: {exc}")
            else:
                if reasons:
                    errors.append(f"{sitemap.name}: non-indexable target ({', '.join(reasons)}): {url}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sitemaps", nargs="*", default=["sitemap.xml", "sitemap-apps.xml"])
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    errors = []
    for name in args.sitemaps:
        path = Path(name)
        if not path.is_absolute():
            path = args.root / path
        errors.extend(validate_sitemap(path, args.root))
    if errors:
        print("\n".join(errors))
        print(f"Sitemap validation failed: {len(errors)} error(s)")
        return 1
    print(f"Sitemap targets validated: {len(args.sitemaps)} sitemap(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
