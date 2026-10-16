import argparse, json, shutil, unicodedata
from pathlib import Path, PurePosixPath
BLOCKED = {"docs", "leads", "outreach", "csv-lotes-email", "propostas", "backup", "backups", "backend", "automation", "scripts", "tests", "admin", "uploads", "api", "dashboard", "dashboards", "lead", "node_modules"}
BLOCKED_PATHS = {"ferramentas/airbnb-admin.html", "education/cursos/_archive", "education/marketing/campaigns", "acoes-hoje.html", "acompanhamento-prospeccao.html", "top5-leads-hoje.html"}
EXTENSIONS = {".html", ".css", ".js", ".json", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".xml", ".webmanifest"}
SPECIAL = {"CNAME", "robots.txt", "ads.txt", ".nojekyll"}
def reject_symlink_components(value):
    path = Path(value).absolute()
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("Symlinks are not allowed")
    return path

def validate_explicit_paths(files):
    if not isinstance(files, list) or not files or any(not isinstance(p, str) for p in files):
        raise ValueError("A nonempty explicit file list is required")
    names = set()
    reserved = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}
    for name in files:
        path = PurePosixPath(name)
        parts = name.split("/")
        if (not name or path.is_absolute() or "\\" in name
                or any(p in {"", ".", ".."} for p in parts)
                or any(unicodedata.category(c) in {"Cc", "Cs"} or c in ':*?"<>|' for c in name)
                or any(p.endswith((".", " ")) or p.split(".", 1)[0].casefold() in reserved for p in parts)):
            raise ValueError("Invalid relative path")
        canonical = name.casefold()
        if canonical in names:
            raise ValueError("Duplicate paths")
        names.add(canonical)
    for name in names:
        parts = name.split("/")
        if any("/".join(parts[:i]) in names for i in range(1, len(parts))):
            raise ValueError("File and directory path conflict")

def prepare(source, destination, manifest):
    source = reject_symlink_components(source).resolve()
    destination = reject_symlink_components(destination).resolve(strict=False)
    if destination == source or source in destination.parents:
        raise ValueError("Output must be outside the checkout")
    if destination.exists() or destination.is_symlink():
        raise ValueError("Output must be a new path")
    if not isinstance(manifest, dict) or (type(manifest.get("version")) is not int or manifest["version"] != 1) or manifest.get("reviewed") is not True:
        raise ValueError("A reviewed version-1 manifest is required")
    files = manifest.get("files")
    validate_explicit_paths(files)
    planned = []
    for name in files:
        path = PurePosixPath(name)
        if not name or path.is_absolute() or "\\" in name or any(p in {"", ".", ".."} for p in name.split("/")):
            raise ValueError("Invalid relative path")
        normalized = path.as_posix().casefold()
        if any(normalized == blocked or normalized.startswith(blocked + "/") for blocked in BLOCKED_PATHS):
            raise ValueError("Blocked internal or hidden path")
        if any(p.casefold() in BLOCKED or p.startswith(".") for p in path.parts) and name != ".nojekyll":
            raise ValueError("Blocked internal or hidden path")
        if path.suffix.lower() not in EXTENSIONS and name not in SPECIAL:
            raise ValueError("File type is not allowed")
        current = source
        for part in path.parts:
            current = current / part
            if current.is_symlink():
                raise ValueError("Symlinks are not allowed")
        if not current.is_file() or source not in current.resolve().parents:
            raise ValueError("Source file missing or outside checkout")
        planned.append((current, name))
    destination.mkdir(parents=True)
    try:
        for current, name in planned:
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(current, target)
    except Exception:
        shutil.rmtree(destination)
        raise
    return len(planned)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    count = prepare(args.source, args.destination, json.loads(Path(args.manifest).read_text()))
    print(f"Public artifact prepared: {count} explicitly approved files")
if __name__ == "__main__":
    main()
