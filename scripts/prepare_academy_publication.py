#!/usr/bin/env python3
"""Exclude team-delivery source and unlinked obsolete sales collateral from Pages only.
Does not touch backend academy/cursos or legacy course-completo student fallback.
Run --check for a read-only list/audit, without removal.
"""
import argparse,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COLLATERAL=('marketing','email-sequence','instagram','seo-articles')
def candidates():
 return [ROOT/'docs/academy/delivery',*sorted((ROOT/'docs/academy').glob('course-learning-plans*.json')),*sorted((ROOT/'docs/academy').glob('course-application-*.json')),*sorted(p for name in COLLATERAL for p in (ROOT/'education/cursos').glob('*/'+name))]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args();paths=[p for p in candidates() if p.exists()]
 # Refuse to remove any collateral with an active HTML link to its published path.
 prefixes=['/'+p.relative_to(ROOT).as_posix()+'/' for p in paths if p.is_dir() and 'education' in p.parts]
 broken=[]
 for page in ROOT.rglob('*.html'):
  if '.git' in page.parts or 'delivery' in page.parts:continue
  for link in re.findall(r'(?:href|src)=[\"\']([^\"\']+)',page.read_text(errors='replace')):
   target=link.removeprefix('https://praia.digital')
   if not target.startswith('/') and not re.match(r'\w+:',target):target='/'+(page.parent/target).resolve().relative_to(ROOT).as_posix() if (page.parent/target).resolve().is_relative_to(ROOT) else target
   if any(target.startswith(prefix) for prefix in prefixes):broken.append((str(page.relative_to(ROOT)),link))
 if broken:raise SystemExit('Refusing to break active links: '+json.dumps(broken,ensure_ascii=False))
 print(json.dumps({'mode':'check' if args.check else 'publication-only cleanup','excluded':[str(p.relative_to(ROOT)) for p in paths],'preserved':['academy/cursos/**','education/cursos/*/curso-completo/**','education/cursos/*/materiais/**','education/cursos/*/planilhas/**']},ensure_ascii=False,indent=2))
 if not args.check:
  for p in paths:
   if p.is_dir():shutil.rmtree(p)
   else:p.unlink()
if __name__=='__main__':main()
