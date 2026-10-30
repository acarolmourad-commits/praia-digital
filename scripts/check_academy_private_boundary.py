#!/usr/bin/env python3
"""Fail public build if full revised Academy authoring/delivery is present.
This is an accident-prevention check, NOT authorization or deletion of public Git history.
"""
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
def violations(root):
 root=Path(root)
 candidates=[*root.glob('docs/academy/course-learning-plans*.json'),*root.glob('docs/academy/course-application-*.json')]
 for folder in ['docs/academy/delivery','private-content','academy-private-pdf']:
  path=root/folder
  if path.exists():candidates.extend(p for p in path.rglob('*') if p.is_file())
 return sorted(str(p.relative_to(root)) for p in candidates if p.is_file())
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT);args=parser.parse_args()
 found=violations(args.root)
 print(json.dumps({'status':'BLOCK' if found else 'PASS','unexpected_private_paths':found,'limit':'Does not remove Git history, forks or prior copies; does not validate buyer access.'},indent=2))
 return 1 if found else 0
if __name__=='__main__':raise SystemExit(main())
