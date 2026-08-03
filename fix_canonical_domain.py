import glob
count = 0
files = glob.glob('**/*.html', recursive=True)
for path in files:
    if any(skip in path for skip in ['.git', 'dashboard', 'leads', 'backups']):
        continue
    try:
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    if 'acarolmourad.github.io/praia-digital/litoral-prime-imoveis/' in txt:
        new = txt.replace('acarolmourad.github.io/praia-digital/litoral-prime-imoveis/', 'praia.digital/')
        open(path, 'w', encoding='utf-8').write(new)
        count += 1
print('fixed', count)
