import os, datetime, random

repo = r"C:\Users\Carolina\praia-digital"
blog_dir = os.path.join(repo, "blog")
os.makedirs(blog_dir, exist_ok=True)

now = datetime.date.today().isoformat()

temas = [
    ("marketing-", ["imobiliário","para corretores","no litoral","digital","2026","redes sociais"], ["Marketing digital","imobiliárias","litoral"]),
    ("automacao-", ["imobiliária","corretores","visitas","leads","vendas","2026"], ["Automação","imobiliárias","produtividade"]),
    ("ia-", ["imobiliária","corretores","litoral","avaliação","recomendação","2026"], ["IA","imobiliário","tecnologia"]),
    ("seo-", ["imobiliária","litoral","blog","conteúdo","2026","google"], ["SEO","imobiliárias","litoral"]),
    ("captacao-", ["imóveis","leads","imobiliária","litoral","2026"], ["Captação","imóveis","leads"]),
]

temas_hoje = random.sample(temas, 3)

for prefixo, palavras, contexto in temas_hoje:
    palavras_escolhidas = random.sample(palavras, 3)
    titulo = f"{' '.join(contexto)} {' '.join(palavras_escolhidas)} em {now}"
    slug = f"{prefixo}{'-'.join(palavras_escolhidas)}-{now}.html".replace(" ","-").lower()
    tags_html = ", ".join(palavras_escolhidas + ["litoral paulista", "2026"])
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="{titulo}. Conteúdo atualizado para {now}.">
<meta name="keywords" content="{tags_html}">
<style>
body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.7; }}
h1 {{ color: #2c3e50; }}
h2 {{ color: #34495e; margin-top: 35px; }}
</style>
</head>
<body>
<h1>{titulo}</h1>
<p class="meta">Publicado em {now} | Praia Digital</p>
<article>
<h2>Pontos principais</h2>
<ul>
  <li>Estratégias práticas</li>
  <li>Dicas profissionais</li>
  <li>Ferramentas recomendadas</li>
</ul>
<p>Use a Praia Digital: <a href="https://praia.digital">https://praia.digital</a></p>
</article>
</body>
</html>
"""
    path = os.path.join(blog_dir, slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

total = len([f for f in os.listdir(blog_dir) if f.endswith(".html")])
print(f"SEO diário executado em {now}. Total artigos: {total}")
