#!/usr/bin/env python3
from pathlib import Path

BASE = Path("C:/Users/Carolina/praia-digital")
BLOG = BASE / "blog"

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header>
    <h1>{h1}</h1>
    <p>{subtitle}</p>
    <nav>
      <a href="../index.html">Home</a> |
      <a href="../ferramentas.html">Ferramentas Gratuitas</a>
    </nav>
  </header>
  <main>
    <article>
      <h2>Introdução</h2>
      <p>{intro}</p>
      <h2>Pontos principais</h2>
      <ul>
        <li>{p1}</li>
        <li>{p2}</li>
        <li>{p3}</li>
        <li>{p4}</li>
      </ul>
      <h2>Conclusão</h2>
      <p>{conclusion}</p>
      <p><strong>Quer mais? Veja também:</strong></p>
      <ul>
        <li><a href="automacao-captacao-imoveis-litoral-2026.html">Automação de captação</a></li>
        <li><a href="seo-local-imobiliarias-litoral-paulista-2026.html">SEO local</a></li>
      </ul>
    </article>
  </main>
  <footer>
    <p>Praia Digital — <a href="https://praia.digital" target="_blank">https://praia.digital</a></p>
  </footer>
</body>
</html>"""

TOPICS = [
  ("imoveis-pet-friendly-litoral-paulista-2026|Imóveis pet friendly no litoral paulista em 2026|Como escolher imóveis pet friendly no litoral paulista|Dicas para compradores com pets no litoral|Verifique regras do condomínio antes de comprar|Priorize áreas comuns e parques|Avalie proximidade de veterinários|Considere espaço interno e externo|Imóveis pet friendly valorizam mais no litoral."),
  ("locacao-temporada-pet-friendly-litoral-2026|Locação por temporada pet friendly no litoral paulista em 2026|Como anunciar locação pet friendly no litoral|Destaque regras claras para hóspedes com pets|Mostre áreas de lazer e acesso a praias pet friendly|Use fotos que inspirem confiança|Ofereça dicas locais para pets|Deixe regras explícitas no anúncio|Locação pet friendly reduz objeções e amplia público."),
  ("imoveis-energia-solar-litoral-paulista-2026|Imóveis com energia solar no litoral paulista em 2026|Economia e sustentabilidade no litoral|Imóveis com energia solar reduzem custos|Verifique incentivos fiscais|Avalie área de telhado|Energia solar valoriza imóveis no litoral|Sustentabilidade é diferencial de venda."),
  ("imoveis-acessibilidade-litoral-paulista-2026|Imóveis com acessibilidade no litoral paulista em 2026|Acessibilidade como diferencial no litoral|Rampas e banheiros adaptados|Localização com acesso fácil|Condomínios com acessibilidade|Acessibilidade amplia mercado e valoriza imóveis."),
  ("imoveis-seguranca-litoral-paulista-2026|Segurança em imóveis no litoral paulista em 2026|Segurança como critério de compra no litoral|Condomínios fechados e monitoramento|Regras de acesso e portaria|Proximidade de delegacias|Segurança influencia decisão de compra."),
  ("imoveis-investimento-estrangeiro-litoral-2026|Investimento estrangeiro em imóveis no litoral paulista em 2026|Oportunidades para investidores estrangeiros|Documentação para estrangeiros|Vantagens fiscais e retorno|Parcerias com agentes internacionais|Mercado internacional cresce no litoral."),
  ("retrofit-imoveis-litoral-paulista-2026|Retrofit em imóveis no litoral paulista em 2026|Como o retrofit valoriza imóveis no litoral|Modernização sem perder identidade|Eficiência energética|Retrofit agrega valor e reduz custos."),
  ("paisagismo-imoveis-litoral-paulista-2026|Paisagismo para imóveis no litoral paulista em 2026|Paisagismo valoriza imóveis no litoral|Plantas resistentes a vento e sal|Áreas de lazer integradas|Paisagismo melhora experiência do comprador."),
  ("smart-home-imoveis-litoral-paulista-2026|Smart home em imóveis no litoral paulista em 2026|Automação residencial no litoral|Iluminação e climatização inteligentes|Segurança conectada|Smart home agrega valor e modernidade."),
  ("imoveis-vista-mar-litoral-paulista-2026|Imóveis com vista mar no litoral paulista em 2026|Vista mar como diferencial no litoral|Valorização por vista|Orientação solar e ventilação|Vista mar aumenta retorno de temporada."),
  ("imoveis-sustentaveis-litoral-paulista-2026|Imóveis sustentáveis no litoral paulista em 2026|Sustentabilidade e valorização no litoral|Materiais ecológicos e eficientes|Economia de água e energia|Sustentabilidade atrai compradores exigentes."),
  ("imoveis-multipropriedade-litoral-paulista-2026|Multipropriedade no litoral paulista em 2026|Como funciona a multipropriedade no litoral|Vantagens e legislação|Gestão profissional compartilhada|Ideal para temporada e investimento."),
  ("imoveis-na-planta-litoral-paulista-2026|Imóveis na planta no litoral paulista em 2026|Vantagens e riscos de comprar na planta|Verifique incorporadora e CRECI|Acompanhe obra e prazos|Na planta pode ter desconto e valorização."),
  ("imoveis-usados-vs-novos-litoral-paulista-2026|Usados vs novos no litoral paulista em 2026|Quando escolher imóvel usado ou novo|Usado: preço menor e negociação|Novo: garantia e planejamento|Depende do perfil e prazo do comprador."),
  ("imoveis-primeira-viagem-litoral-paulista-2026|Primeiro imóvel no litoral paulista em 2026|Guia para compradores de primeira viagem|Defina orçamento e cidade|Visite vários imóveis antes de decidir|Documentação e financiamento são etapas-chave."),
]

existing = {f.stem for f in BLOG.glob("*.html") if BLOG.exists()}

created = 0
for line in TOPICS:
    parts = line.split("|")
    if len(parts) < 9:
        continue
    slug, title, h1, intro, p1, p2, p3, p4, conclusion = parts[:9]
    if slug in existing:
        continue
    description = f"{h1}. Saiba mais sobre {intro.lower()} no litoral paulista em 2026."
    html = TEMPLATE.format(
        title=title,
        description=description,
        h1=h1,
        subtitle="Guia prático para o litoral paulista",
        intro=intro,
        p1=p1,
        p2=p2,
        p3=p3,
        p4=p4,
        conclusion=conclusion,
    )
    out = BLOG / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    created += 1

print(f"Criados {created} artigos SEO novos")
