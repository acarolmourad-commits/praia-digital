from pathlib import Path

# Clean up temporary fix scripts that were superseded
temp_scripts = [
    'scripts/fix_cidade_servico.py',
    'scripts/fix_cidade_servico_v2.py',
    'scripts/fix_cidade_servico_v3.py',
    'scripts/fix_cidade_servico_v4.py',
]

for s in temp_scripts:
    p = Path(s)
    if p.exists():
        p.unlink()
        print(f'removed {s}')

# Remove obsolete scripts that were replaced by better versions
obsolete = [
    'scripts/create_lead_pages.py',
]
for s in obsolete:
    p = Path(s)
    if p.exists():
        p.unlink()
        print(f'removed {s}')

print('cleanup done')
