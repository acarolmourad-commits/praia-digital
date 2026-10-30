#!/usr/bin/env python3
"""Validate actual public offerings; the historical64-entry inventory is not a sales-readiness proof."""
import json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
def main():
 old=json.loads((BASE/'docs/academy/inventory-64-cursos.json').read_text())
 plans=json.loads((BASE/'docs/academy/course-learning-plans.json').read_text())
 catalog=json.loads((BASE/'education/assets/catalog.json').read_text())
 aliases=plans.get('aliases',{});offered={c['slug']:c for c in catalog};errors=[]
 if len(old)!=64:errors.append('historical inventory count changed without reconciliation')
 for item in old:
  slug=item['slug']
  if slug not in offered and slug not in aliases:errors.append(f'unreconciled: {slug}')
 for slug,c in offered.items():
  if not (BASE/c['path'].lstrip('/')).is_file():errors.append(f'missing page: {slug}')
  if c['kind']=='Curso curto digital':
   plan=plans['courses'].get(slug,{})
   if len(plan.get('lessons',[]))<3 or not plan.get('practice'):errors.append(f'missing learning plan: {slug}')
   if not plan.get('application') or not plan.get('worked_example') or len(plan.get('worksheet',[]))<4:errors.append(f'incomplete instructional delivery: {slug}')
   if not (BASE/f'docs/academy/delivery/{slug}.html').is_file():errors.append(f'missing delivery material: {slug}')
 for alias,target in aliases.items():
  if alias in offered or target not in offered:errors.append(f'invalid alias: {alias}')
 print(f'{len(old)} historical URLs reconciled; {len(offered)} public offerings; {len(aliases)} duplicate aliases')
 if errors:print('\n'.join(errors));sys.exit(1)
 print('Actual catalog and delivery inventory validation passed; no claim of video/LMS/certification readiness.')
if __name__=='__main__':main()
