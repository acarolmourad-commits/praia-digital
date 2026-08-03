fix_list = open('pd_canonical_fix.txt', 'r', encoding='utf-8').read().splitlines()
print('to fix', len(fix_list))
done = 0
for path in fix_list:
    try:
        txt = open(path, 'r', encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    new = txt.replace('acarolmourad.github.io/praia-digital/litoral-prime-imoveis/', 'praia.digital/')
    if new != txt:
        open(path, 'w', encoding='utf-8').write(new)
        done += 1
print('fixed', done)
