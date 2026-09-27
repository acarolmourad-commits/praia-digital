#!/usr/bin/env python3
"""Neutraliza geracao de breadcrumbs nos scripts de automacao (one-shot, 2026-09-27)."""
import re

# 1) add_listing_schema.py: remove breadcrumb, mantem RealEstateListing
f='scripts/automation/add_listing_schema.py'; t=open(f,encoding='utf-8').read()
t=t.replace('Adiciona RealEstateListing + BreadcrumbList JSON-LD nas p\u00e1ginas de imoveis/.','Adiciona RealEstateListing JSON-LD nas p\u00e1ginas de imoveis/. (breadcrumb removido em 2026-09-27)')
t=re.sub(r'def make_breadcrumb.*?\n\ndef make_listing', 'def make_listing', t, flags=re.S)
t=t.replace('    bc = make_breadcrumb(title, url)\n','').replace('    bc_json = json.dumps(bc, ensure_ascii=False, indent=2)\n','')
t=t.replace('injection = f\'<script type="application/ld+json">\\n{bc_json}\\n</script>\\n<script type="application/ld+json">\\n{rl_json}\\n</script>\\n\'','injection = f\'<script type="application/ld+json">\\n{rl_json}\\n</script>\\n\'')
open(f,'w',encoding='utf-8').write(t)

# 2) generate_personas.py: remove no breadcrumb do JSON-LD WebPage
f='scripts/automation/generate_personas.py'; t=open(f,encoding='utf-8').read()
t=re.sub(r'",\n    "breadcrumb": \{\{.*?\]\n    \}\}\n', '"\n', t, flags=re.S)
assert 'breadcrumb' not in t.lower()
open(f,'w',encoding='utf-8').write(t)

# 3) generate_city_service_pages.py: remove placeholders mortos
f='scripts/automation/generate_city_service_pages.py'; t=open(f,encoding='utf-8').read()
t=t.replace("        '{{breadcrumb_city}}': city_label,\n","").replace("        '{{breadcrumb_service}}': service_title,\n","")
assert 'breadcrumb' not in t.lower()
open(f,'w',encoding='utf-8').write(t)

# 4) arquitetura-b-apply.py: neutraliza injecao de breadcrumb (mantem CTAs)
f='scripts/arquitetura-b-apply.py'; t=open(f,encoding='utf-8').read()
t=re.sub(r'# Mapa de breadcrumbs por arquivo\nBREADCRUMBS = \{.*?\n\}\n', '', t, flags=re.S)
t=re.sub(r'def breadcrumb_json.*?\n\ndef ', 'def ', t, flags=re.S)
t=re.sub(r'def inject_breadcrumb.*?\n\ndef ', 'def ', t, flags=re.S)
t=t.replace('        # Apply breadcrumb if defined\n        if rel in BREADCRUMBS:\n            text = inject_breadcrumb(text, BREADCRUMBS[rel])\n','')
t=t.replace("'breadcrumb': rel in BREADCRUMBS,","'breadcrumb': False,  # breadcrumbs descontinuados em 2026-09-27")
assert 'BREADCRUMBS' not in t
open(f,'w',encoding='utf-8').write(t)

import py_compile
for f in ['scripts/automation/add_listing_schema.py','scripts/automation/generate_personas.py','scripts/automation/generate_city_service_pages.py','scripts/arquitetura-b-apply.py']:
    py_compile.compile(f, doraise=True); print('OK', f)
