import os, re, json

MAP = {
 "aluguel-temporada-litoral":"gestao-de-locacao-no-litoral",
 "analise-mercado":"analise-de-mercado-imobiliario-litoral",
 "atendimento-ao-cliente-para-corretores":"atendimento-ao-cliente-para-corretores",
 "atendimento-clientes-internacionais-imobiliarias":"atendimento-ao-cliente-para-corretores",
 "atendimento-imobiliario":"atendimento-ao-cliente-para-corretores",
 "automacao-comercial":"automacao-comercial",
 "avaliacao-imoveis":"avaliacao-de-imoveis",
 "avaliacao-imoveis-litoral":"avaliacao-de-imoveis",
 "captacao-digital-imobiliarias-litoral":"captacao-imoveis-corretores",
 "captacao-imoveis-corretores":"captacao-imoveis-corretores",
 "captacao-imoveis-economicos-litoral":"captacao-imoveis-corretores",
 "captacao-imoveis-internacionais-litoral":"captacao-imoveis-corretores",
 "carteira-temporada-imoveis-litoral":"gestao-de-locacao-no-litoral",
 "comercial-imobiliaria":"gestao-de-vendas-para-corretores",
 "compra-imoveis-litoral":"comprar-com-seguranca",
 "documentacao-compra-imovel-litoral":"documentacao-completa-imoveis-litoral",
 "estrategia-imobiliaria-litoral":"planejamento-estrategico-para-corretores",
 "fechamento-vendas-imoveis-litoral":"fechamento-de-vendas-para-corretores",
 "ferramentas-imobiliarias":"treinamento-em-tecnologia-para-corretores",
 "fidelizacao-clientes-imobiliarias":"pos-venda-relacionamento-corretores",
 "financiamento-imobiliario":"financiamento-imobiliario",
 "financiamento-imoveis-litoral":"financiamento-imobiliario",
 "gestao-comercial-imobiliarias":"gestao-de-vendas-para-corretores",
 "gestao-temporada-imoveis":"gestao-de-locacao-no-litoral",
 "gestao-temporada-imoveis-litoral":"gestao-de-locacao-no-litoral",
 "ia-imobiliarias-litoral":"ia-para-imobiliarias",
 "ia-para-imobiliarias":"ia-para-imobiliarias",
 "instagram-imobiliarias":"instagram-para-corretores",
 "instagram-para-corretores":"instagram-para-corretores",
 "instagram-reels-imobiliarias-litoral":"instagram-para-corretores",
 "investimento-imoveis-litoral":"investindo-imoveis-litoral",
 "investimento-imovel-litoral":"investindo-imoveis-litoral",
 "leads-internacionais-imoveis":"prospeccao-para-corretores",
 "locacao-temporada-litoral":"gestao-de-locacao-no-litoral",
 "marketing-conteudo-imobiliarias-litoral":"marketing-imobiliario",
 "marketing-digital-imobiliarias":"marketing-imobiliario",
 "marketing-digital-imobiliarias-litoral":"marketing-imobiliario",
 "marketing-imobiliario":"marketing-imobiliario",
 "mercado-premium-imoveis-litoral":"venda-imoveis-alto-padrao-litoral",
 "negociacao-imoveis-litoral":"negociacao-imobiliaria-litoral",
 "operacao-imobiliaria-enxuta":"produtividade-para-corretores",
 "parcerias-construtoras-litoral":"networking-para-corretores",
 "priceplabs":"pricelabs-completo",
 "retencao-clientes-imobiliarias":"pos-venda-relacionamento-corretores",
 "seo-local-imobiliarias":"marketing-imobiliario",
 "seo-local-imobiliarias-litoral":"marketing-imobiliario",
 "seo-para-corretores":"marketing-imobiliario",
 "temporada-imoveis-litoral":"gestao-de-locacao-no-litoral",
 "venda-imoveis-litoral":"venda-rapida-imoveis-litoral",
 "vendas-imobiliarias":"especialista-venda-imoveis-litoral",
 "vendas-imobiliarias-litoral":"especialista-venda-imoveis-litoral",
 "whatsapp-corretores-litoral":"whatsapp-que-vende",
 "formacao-corretores":"__INDEX__",
}

pat = re.compile(r'https://academy\.praia\.digital/courses/([a-z0-9-]+)')
exts = ('.html', '.md', '.json')
changed, replaced, unmatched = [], 0, set()
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        if not fn.endswith(exts): continue
        p = os.path.join(root, fn)
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:
            continue
        if 'academy.praia.digital/courses/' not in t: continue
        def sub(m):
            global replaced
            slug = m.group(1)
            tgt = MAP.get(slug)
            if not tgt:
                unmatched.add(slug); return m.group(0)
            replaced += 1
            return 'https://praia.digital/education/cursos/' if tgt=='__INDEX__' else f'https://praia.digital/education/cursos/{tgt}/'
        nt = pat.sub(sub, t)
        if nt != t:
            open(p, 'w', encoding='utf-8').write(nt)
            changed.append(p[2:])
print(json.dumps({"files_changed": len(changed), "links_replaced": replaced, "unmatched": sorted(unmatched)}, ensure_ascii=False))
