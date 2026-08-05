import os
import json
import urllib.request
import urllib.error

base = 'education/cursos'
cursos = sorted([d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))])

required_dirs = [
    'curso-completo',
    'checklists',
    'planilhas',
    'avaliacao',
    'certificado',
    'ebook',
    'mini-curso',
    'email-sequence',
    'instagram',
    'seo-articles',
    'marketing'
]

required_files = [
    'index.html',
    'vendas.html',
    'curso-completo/ficha-completa.md',
    'curso-completo/sumario.md',
    'curso-completo/modulo-1.md',
    'curso-completo/modulo-2.md',
    'curso-completo/modulo-3.md',
    'curso-completo/modulo-4.md',
    'checklists/checklist-cadastro.md',
    'planilhas/planilha-precificacao.md',
    'avaliacao/avaliacao-final.md',
    'certificado/certificado.md',
    'ebook/lead-magnet.md',
    'mini-curso/sumario.md',
    'email-sequence/sequencia.md',
    'instagram/posts.md',
    'seo-articles/sumario.md',
    'marketing/webinar.md',
    'marketing/youtube.md',
    'marketing/meta-ads.md',
    'marketing/google-ads.md',
    'marketing/instagram-posts.md',
    'marketing/reels.md',
    'marketing/tiktok.md',
    'marketing/shorts.md',
    'marketing/faq.md'
]

print(f"Total de cursos: {len(cursos)}\n")

incomplete = []
urls_to_test = []

for curso in cursos:
    root = os.path.join(base, curso)
    missing_dirs = [d for d in required_dirs if not os.path.isdir(os.path.join(root, d))]
    missing_files = [f for f in required_files if not os.path.exists(os.path.join(root, f))]
    
    if missing_dirs or missing_files:
        incomplete.append({
            'curso': curso,
            'missing_dirs': missing_dirs,
            'missing_files': missing_files
        })
    
    urls_to_test.append(f"https://praia.digital/education/cursos/{curso}/index.html")
    urls_to_test.append(f"https://praia.digital/education/cursos/{curso}/vendas.html")

print(f"Cursos incompletos: {len(incomplete)}")
for item in incomplete:
    print(f"  - {item['curso']}")
    if item['missing_dirs']:
        print(f"    Pastas faltando: {', '.join(item['missing_dirs'])}")
    if item['missing_files']:
        print(f"    Arquivos faltando: {', '.join(item['missing_files'])}")

print(f"\nTestando {len(urls_to_test)} URLs...")
accessible = 0
inaccessible = []

for url in urls_to_test:
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                accessible += 1
            else:
                inaccessible.append((url, resp.status))
    except urllib.error.HTTPError as e:
        inaccessible.append((url, e.code))
    except Exception as e:
        inaccessible.append((url, str(e)))

print(f"URLs acessíveis: {accessible}/{len(urls_to_test)}")
if inaccessible:
    print(f"URLs inacessíveis: {len(inaccessible)}")
    for url, status in inaccessible[:10]:
        print(f"  - {url}: {status}")
