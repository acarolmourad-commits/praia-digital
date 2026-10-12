"""Read-only, bounded static dependency audit. Never approves a manifest.
No network, JavaScript execution, copying, or page-body output.
Not a full JS/CSS parser, secret scanner, content review, or runtime test.
"""
import argparse
from collections import deque
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location("pages_policy", Path(__file__).with_name("prepare_pages_public.py"))
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)
MAX_BYTES = 2 * 1024 * 1024
MAX_FILES = 500
MAX_EDGES = 10000
SAFE = re.compile(r"[A-Za-z0-9_./-]{1,240}\Z")
TEXT_TYPES = {".html", ".css", ".js", ".json", ".webmanifest", ".xml", ".svg"}
OWN_HOSTS = {"praia.digital", "www.praia.digital"}


def path_valid(name):
    if not isinstance(name, str) or not SAFE.fullmatch(name): return False
    return not name.startswith("/") and all(p not in {"", ".", ".."} for p in name.split("/"))


def policy_blocked(name):
    low = name.casefold()
    if any(low == p or low.startswith(p + "/") for p in POLICY.BLOCKED_PATHS): return True
    if any(p.casefold() in POLICY.BLOCKED or p.startswith(".") for p in name.split("/")) and name != ".nojekyll": return True
    return PurePosixPath(name).suffix.lower() not in POLICY.EXTENSIONS and name not in POLICY.SPECIAL


def resolve_reference(owner, raw):
    if not isinstance(raw, str) or not raw.strip(): return None, None
    raw = raw.strip()
    if raw.startswith("#"): return None, None
    if "\\" in raw or any(ord(c) < 32 for c in raw): return None, "unsafe_reference"
    try: url = urlsplit(raw)
    except ValueError: return None, "unsafe_reference"
    if url.scheme or url.netloc:
        # Contacts, embedded data, and external URLs are never emitted.
        if url.scheme not in {"http", "https"} or url.hostname not in OWN_HOSTS:
            return None, "external_or_nonfile_reference"
        if url.username or url.password: return None, "unsafe_reference"
        path = url.path
    else: path = url.path
    if not path: return None, None
    path = unquote(path)
    if "\\" in path or "%" in path or any(ord(c) < 32 for c in path): return None, "unsafe_reference"
    if path.startswith("/"): target = posixpath.normpath(path.lstrip("/"))
    else: target = posixpath.normpath(posixpath.join(posixpath.dirname(owner), path))
    if target == ".": target = "index.html"
    elif path.endswith("/"): target += "/index.html"
    if not path_valid(target): return None, "unsafe_reference"
    return target, None


class HTMLReferences(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.refs=[]; self.base=False
    def handle_starttag(self, tag, attrs):
        if tag == "base": self.base=True
        for key, value in attrs:
            if key in {"href", "src", "poster", "data-src"} and value: self.refs.append(value)
            elif key == "srcset" and value:
                self.refs.extend(item.strip().split()[0] for item in value.split(",") if item.strip())
    handle_startendtag = handle_starttag


def references(name, text):
    suffix=PurePosixPath(name).suffix.lower(); refs=[]; alerts=[]
    if suffix == ".html":
        parser=HTMLReferences(); parser.feed(text); refs=parser.refs
        if parser.base: alerts.append("base_url_requires_manual_review")
        if re.search(r"<script\b|\bon\w+\s*=", text, re.I): alerts.append("dynamic_content_requires_manual_review")
        # Inline CSS is scanned only as CSS; script bodies require manual review.
        refs.extend(m.group(1) for m in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", text))
    elif suffix == ".css":
        refs.extend(m.group(1) for m in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", text))
        refs.extend(m.group(1) for m in re.finditer(r"@import\s+['\"]([^'\"]+)['\"]", text))
    elif suffix == ".js":
        alerts.append("javascript_requires_manual_review")
        patterns=(r"\b(?:fetch|import|require)\s*\(\s*['\"]([^'\"]+)['\"]", r"\b(?:from|import)\s+['\"]([^'\"]+)['\"]")
        for pattern in patterns: refs.extend(m.group(1) for m in re.finditer(pattern,text))
    elif suffix in {".json", ".webmanifest"}:
        data=json.loads(text)
        if isinstance(data,dict):
            for key in ("start_url", "scope"):
                if isinstance(data.get(key),str): refs.append(data[key])
            for key in ("icons", "screenshots"):
                for item in data.get(key,[]) if isinstance(data.get(key),list) else []:
                    if isinstance(item,dict) and isinstance(item.get("src"),str): refs.append(item["src"])
        alerts.append("json_content_requires_manual_review")
    elif suffix in {".xml", ".svg"}:
        if re.search(r"<!DOCTYPE|<!ENTITY",text,re.I): return [],["xml_entities_not_parsed"]
        doc=ET.fromstring(text)
        for element in doc.iter():
            if element.tag.rsplit("}",1)[-1] == "loc" and element.text: refs.append(element.text.strip())
            for key,value in element.attrib.items():
                if key.rsplit("}",1)[-1] in {"href","src"}: refs.append(value)
    return refs,alerts


def audit(source, manifest, entries=(), max_files=MAX_FILES):
    raw_source=Path(source).absolute()
    if any(p.is_symlink() for p in (raw_source,*raw_source.parents)): raise ValueError("unsafe_source")
    source=raw_source.resolve()
    if not source.is_dir(): raise ValueError("invalid_source")
    if not isinstance(manifest,dict) or type(manifest.get("version")) is not int or manifest["version"] != 1 or type(manifest.get("reviewed")) is not bool or not isinstance(manifest.get("files"),list): raise ValueError("invalid_manifest")
    files=manifest["files"]
    if len(files)>MAX_FILES or len(entries)>MAX_FILES or not all(path_valid(p) for p in files): raise ValueError("invalid_manifest_paths")
    if not all(path_valid(p) for p in entries): raise ValueError("invalid_entry_paths")
    if not 1<=max_files<=MAX_FILES: raise ValueError("invalid_limit")
    listed=set(files); queue=deque(sorted(listed|set(entries))); seen=set(); scanned=[]; edges=set(); alerts=set()
    def warn(code, path=None): alerts.add((code,path or ""))
    if not manifest["reviewed"]: warn("manifest_not_reviewed")
    if not files: warn("manifest_empty")
    if len(listed)!=len(files): warn("duplicate_manifest_paths")
    while queue:
        name=queue.popleft()
        if name in seen: continue
        if len(seen)>=max_files: warn("file_limit_reached"); break
        seen.add(name)
        if policy_blocked(name): warn("blocked_path",name); continue
        current=source
        symlink=False
        for part in PurePosixPath(name).parts:
            current=current/part
            if current.is_symlink(): symlink=True; break
        if symlink: warn("symlink_not_read",name); continue
        if not current.is_file(): warn("missing_file",name); continue
        if source not in current.resolve().parents: warn("outside_source",name); continue
        if name not in listed: warn("not_in_manifest",name)
        scanned.append(name)
        if current.suffix.lower() not in TEXT_TYPES: continue
        try:
            if current.stat().st_size>MAX_BYTES: warn("file_too_large",name); continue
            with current.open("rb") as stream: data=stream.read(MAX_BYTES+1)
            if len(data)>MAX_BYTES: warn("file_too_large",name); continue
            refs,codes=references(name,data.decode("utf-8"))
        except (OSError,UnicodeError,ValueError,ET.ParseError): warn("file_not_parsed",name); continue
        for code in codes: warn(code,name)
        for raw in refs:
            target,code=resolve_reference(name,raw)
            if code: warn(code,name)
            if target:
                if len(edges)>=MAX_EDGES: warn("edge_limit_reached"); break
                edges.add((name,target))
                if target not in seen: queue.append(target)
    return {"version":1,"publication_approved":False,"coverage":"bounded_static_only", "paths":sorted(scanned),"dependencies":[{"from":a,"to":b} for a,b in sorted(edges)],"alerts":[dict(code=code,**({"path":path} if path else {})) for code,path in sorted(alerts)]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",required=True)
    parser.add_argument("--manifest",required=True)
    parser.add_argument("--entry",action="append",default=[])
    args=parser.parse_args()
    try:
        manifest_path=Path(args.manifest)
        if manifest_path.is_symlink() or any(p.is_symlink() for p in manifest_path.absolute().parents): raise ValueError("unsafe_manifest")
        with manifest_path.open("rb") as stream: raw=stream.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES: raise ValueError("manifest_too_large")
        report=audit(args.source,json.loads(raw),args.entry)
    except (OSError,UnicodeError,ValueError):
        # Never print input, exception details, or a traceback containing private paths.
        print(json.dumps({"publication_approved":False,"alerts":[{"code":"audit_input_error"}]})); return 2
    print(json.dumps(report,sort_keys=True,indent=2))
    return 0

if __name__ == "__main__": raise SystemExit(main())
