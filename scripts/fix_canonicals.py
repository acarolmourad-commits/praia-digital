import re
LOTE = [
"automacao-pre-venda-lancamentos-imobiliarios-2026.html",
"automacao-visitas-2026-imobiliária-2026-07-10.html",
"automacao-visitas-corretores-2026-2026-08-02.html",
"automacao-visitas-corretores-imobiliária-2026-08-25.html",
"automacao-visitas-corretores-leads-2026-07-23.html",
"automacao-visitas-imobiliarias-litoral-2026.html",
"automacao-visitas-vendas-corretores-2026-07-20.html",
"automacao-whatsapp-corretores-litoral-2026.html",
"automacao-whatsapp-imobiliarias-litoraneas-checklist-2026.html",
"avaliacao-automatica-anuncios-imoveis-litoral.html",
"avaliacao-automatica-preco-mercado-litoral-2026.html",
"avaliacao-automatica-preco-mercado-litoral-passos-2026-07-21.html",
"avaliacao-corretor-litoral-paulista-2026.html",
"avaliacao-de-imoveis-automatizada-ferramenta-gratuita-litoral-em-bertioga-2026-07-12.html",
"avaliacao-imoveis-litoral-guia-profissional.html",
"avaliacao-performance-parcerias-imobiliarias-litoral-2026.html",
"avaliacao-preco-temporada-litoral-2026.html",
"avaliacao-risco-credito-locacao-temporada-litoral-2026.html",
"avaliacao-risco-credito-locatario-temporada-2026.html",
"avaliar-imovel-antes-comprar-litoral-paulista-em-mongaguá-2026-07-13.html",
"avaliar-imovel-na-planta-litoral-checklist.html",
"avaliar-potencial-valorizacao-bairro-litoral-2026.html",
"avenida-da-praia-santos-imoveis-oportunidades-2026.html",
"avenida-da-praia-santos-imoveis-precos-dicas-2026.html",
"backlinks-imobiliaria-litoral-2026.html",
"backup-seguranca-dados-imobiliarias-litoral-2026.html",
"baixa-temporada-litoral-captar-imoveis-2026.html",
"balneario-camboriu-compras-praia-2026-sp-2026-07-14.html",
"barra-do-sul-compra-venda-imoveis-2026.html",
"barra-do-sul-investimento-imoveis-2026.html",
"barra-do-sul-rentabilidade-imoveis-2026.html",
"barra-do-sul-temporada-gestao-imoveis-2026.html",
"barra-velha-ilhabela-imoveis-oportunidades-2026.html",
"beneficios-investir-imovel-na-planta-em-ubatuba-2026-07-12.html",
"bertioga-administracao-aluguel-temporada-2026.html",
"bertioga-aluguel-por-temporada-em-bertioga-como-aumentar-ocupacao-e-renda.html",
"bertioga-artigo-cases-imoveis-2026.html",
"bertioga-artigo-compra-imoveis-2026.html",
"bertioga-artigo-editorial-imoveis-2026.html",
"bertioga-artigo-financiamento-imoveis-2026.html",
"bertioga-artigo-parcerias-imoveis-2026.html",
"bertioga-artigo-seo-local-imoveis-2026.html",
"bertioga-automacao-ia-imoveis-2026.html",
"bertioga-automacao-imobiliarias-2026.html",
"bertioga-automacao-imoveis-2026.html",
"bertioga-bairros-imoveis-2026.html",
"bertioga-bertioga-checklist-para-investimento-imobiliario-guia-2026.html",
"bertioga-bertioga-checklist-para-locacao-de-temporada-guia-2026.html",
"bertioga-bertioga-compra-e-venda-de-imoveis-analise-2026.html",
"bertioga-bertioga-curso-de-investimento-imobiliario-guia-2026.html",
"bertioga-bertioga-curso-para-corretor-de-imoveis-guia-2026.html",
"bertioga-bertioga-guia-para-compra-de-imoveis-analise-2026.html",
"bertioga-bertioga-guia-para-investimento-imobiliario-analise-2026.html",
"bertioga-bertioga-guia-para-locacao-de-temporada-analise-2026.html",
"bertioga-bertioga-investimento-imobiliario-analise-2026.html",
"bertioga-bertioga-locacao-de-temporada-analise-2026.html",
"bertioga-bertioga-marketing-digital-para-imoveis-guia-2026.html",
"bertioga-boraceia-guaratuba-morar-investir-2026.html",
"bertioga-case-de-sucesso-marketing-digital-para-imoveis-em-bertioga-em-2026.html",
"bertioga-case-social-rapido-para-parcerias-em-bertioga.html",
"bertioga-case-sucesso-automacao-imoveis-2026.html",
"bertioga-case-sucesso-cases-imoveis-2026.html",
"bertioga-case-sucesso-editorial-imoveis-2026.html",
"bertioga-case-sucesso-financiamento-imoveis-2026.html",
"bertioga-case-sucesso-juridico-imoveis-2026.html",
"bertioga-case-sucesso-parcerias-imoveis-2026.html",
"bertioga-case-sucesso-seo-local-imoveis-2026.html",
"bertioga-cases-imoveis-2026.html",
"bertioga-checklist-automacao-imoveis-2026.html",
"bertioga-checklist-cases-imoveis-2026.html",
"bertioga-checklist-editorial-imoveis-2026.html",
"bertioga-checklist-financiamento-imoveis-2026.html",
"bertioga-checklist-investimento-imoveis-2026.html",
"bertioga-checklist-juridico-imoveis-2026.html",
"bertioga-checklist-locacao-temporada-imoveis-2026.html",
"bertioga-checklist-marketing-digital-imoveis-2026.html",
"bertioga-checklist-parcerias-imoveis-2026.html",
"bertioga-checklist-seo-local-imoveis-2026.html",
"bertioga-como-captar-leads-em-bertioga-sem-anuncios.html",
"bertioga-compra-venda-imoveis-2026.html",
"bertioga-curso-automacao-imoveis-2026.html",
"bertioga-curso-bairros-imoveis-2026.html",
"bertioga-curso-cases-imoveis-2026.html",
"bertioga-curso-editorial-imoveis-2026.html",
"bertioga-curso-financiamento-imoveis-2026.html",
"bertioga-curso-juridico-imoveis-2026.html",
"bertioga-curso-locacao-temporada-imoveis-2026.html",
"bertioga-curso-marketing-digital-imoveis-2026.html",
"bertioga-curso-seo-local-imoveis-2026.html",
"bertioga-editorial-2026.html",
"bertioga-editorial-imoveis-2026.html",
"bertioga-faq.html",
"bertioga-financiamento-imoveis-2026.html",
"bertioga-guia-compra-imoveis-2026.html",
"bertioga-guia-investimento-imoveis-2026.html",
"bertioga-guia-locacao-temporada-imoveis-2026.html",
"bertioga-imoveis-temporada-oportunidades-2026.html",
"bertioga-indaia-vista-linda-morar-investir-2026.html",
"bertioga-investimento-imobiliario-em-bertioga-2026-oportunidades-e-retorno.html"
]
def fix(path):
    name = path.split('/')[-1]
    expected = 'https://praia.digital/blog/' + name
    t = open(path, encoding='utf-8').read()
    if not re.search(r"rel=['\"]canonical['\"]", t, re.I):
        return False
    t2 = re.sub(r"[ \t]*<link[^>]*?rel=['\"]canonical['\"][^>]*?>\s*\n?", '', t, flags=re.I)
    def add(m):
        return m.group(1) + '  <link rel="canonical" href="' + expected + '">' + '\n'
    t2 = re.sub(r'(<head>\s*\n)', add, t2, count=1, flags=re.I)
    if t2 != t:
        open(path, 'w', encoding='utf-8').write(t2)
        return True
    return False
changed = []
for f in LOTE:
    p = 'blog/' + f
    try:
        if fix(p):
            changed.append(p)
    except Exception as e:
        print('ERRO', p, e)
print('corrigidos:', len(changed))
