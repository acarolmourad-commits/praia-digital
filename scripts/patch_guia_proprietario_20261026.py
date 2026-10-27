import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / 'proprietarios' / 'guia-do-proprietario.html'
def rep(t, old, new):
    assert old in t, 'NOT FOUND: ' + old[:90]
    return t.replace(old, new, 1)
def main():
    t = P.read_text(encoding='utf-8')
    if 'apps-proprietario' in t:
        print('already applied'); return 0
    orig = t
    t = rep(t, '"dateModified": "2026-08-16"', '"dateModified": "2026-10-26"')
    t = rep(t, 'Atualizado em 16/08/2026', 'Atualizado em 26/10/2026')
    t = rep(t, 'ferramentas/avaliacao-preco.html"><h3>Ferramentas</h3>', 'apps/"><h3>Ferramentas</h3>')
    t = rep(t, 'veja indicadores da cidade e do bairro.</p>', 'veja <a href="https://praia.digital/blog/dados-mercado-imobiliario-litoral-2026.html">indicadores da cidade e do bairro</a> e <a href="https://praia.digital/apps/comparador-cidades/">compare cidades</a>.</p>')
    t = rep(t, 'venda, aluguel ou temporada.</p>', 'venda, aluguel ou temporada \u2014 compare com <a href="https://praia.digital/apps/temporada-ou-anual/">Temporada ou Anual</a> e <a href="https://praia.digital/apps/simulador-roi-temporada/">Simulador de ROI de Temporada</a>.</p>')
    t = rep(t, 'pre\u00e7o e documentos.</p>', 'pre\u00e7o e documentos \u2014 use o <a href="https://praia.digital/apps/checklist-vistoria/">Checklist de Vistoria</a>.</p>')
    t = rep(t, 'perfil do im\u00f3vel.</p>', 'perfil do im\u00f3vel \u2014 siga o <a href="https://praia.digital/proprietarios/como-publicar-seu-imovel.html">passo a passo de publica\u00e7\u00e3o</a>.</p>')
    t = rep(t, 'conte com IA ou gest\u00e3o profissional.</p>', 'conte com IA ou gest\u00e3o profissional \u2014 conhe\u00e7a os <a href="https://praia.digital/servicos.html">servi\u00e7os para propriet\u00e1rios</a>.</p>')
    t = rep(t, 'Booking</a>.</p>', 'Booking</a>. Acompanhe tamb\u00e9m as <a href="https://praia.digital/blog/novidades-airbnb-booking.html">novidades do Airbnb e da Booking</a>, a partir de fontes oficiais.</p>')
    cards = [('valor-imovel','Valor do Im\u00f3vel','Estimativa inicial de valor de mercado para precificar com dados.'), ('simulador-roi-temporada','Simulador de ROI de Temporada','Rentabilidade estimada do aluguel de temporada.'), ('temporada-ou-anual','Temporada ou Anual','Compare temporada com loca\u00e7\u00e3o anual antes de decidir.'), ('alugar-ou-comprar','Alugar ou Comprar','Compare o custo de alugar versus comprar no litoral.'), ('checklist-vistoria','Checklist de Vistoria','Vistoria de entrada e sa\u00edda sem esquecer itens.'), ('comparador-cidades','Comparador de Cidades','Compare cidades do litoral por perfil, or\u00e7amento e objetivo.')]
    grid = ''.join(f'<div class="card"><a href="https://praia.digital/apps/{s}/"><h3>{n}</h3><p>{d}</p></a></div>' for s, n, d in cards)
    sec = '<section class="section" id="apps-proprietario"><h2>Use os aplicativos na jornada do propriet\u00e1rio</h2><p>Os aplicativos gratuitos da Praia Digital foram feitos para se conectar: estime o valor, compare vender, alugar ou temporada e feche com a vistoria. Voc\u00ea tamb\u00e9m pode entrar direto na sua etapa.</p><div class="grid grid-3">' + grid + '</div><p>Hub completo: <a href="https://praia.digital/apps/">todos os aplicativos gratuitos</a>. Veja tamb\u00e9m <a href="https://praia.digital/cases.html">exemplos e casos ilustrativos</a> \u2014 sem pre\u00e7os e sem dados confidenciais de clientes.</p></section>'
    t = rep(t, '<section class="faq">', sec + '<section class="faq">')
    t = rep(t, 'Como publicar seu im\u00f3vel</a>\n        <a class="btn btn-purple"', 'Como publicar seu im\u00f3vel</a>\n        <a class="btn btn-amber" href="https://praia.digital/apps/valor-imovel/">Estimar o valor do im\u00f3vel</a>\n        <a class="btn btn-purple"')
    assert t != orig
    P.write_text(t, encoding='utf-8')
    print('patched')
    return 0
if __name__ == '__main__':
    sys.exit(main())
