#!/usr/bin/env python3
# Praia Digital 2026-10-18: home/Academy/avulsos. Sem alterar precos, sem tocar index.html.
from pathlib import Path
from urllib.parse import quote
R = Path(__file__).resolve().parents[1]

def rd(p):
    f = R / p
    if not f.exists():
        raise SystemExit('ERRO ausente: ' + p)
    return f.read_text(encoding='utf-8')

def wr(p, t):
    f = R / p
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(t, encoding='utf-8')
    print('OK ' + p + ': ' + str(len(t.encode('utf-8'))) + ' bytes')

def once(t, a, b, label):
    if t.count(a) != 1:
        raise SystemExit('ERRO ' + label + ': ocorrencias=' + str(t.count(a)))
    return t.replace(a, b)

# 1) js/shared.js - secao de planos antes do footer
p = 'js/shared.js'
s = rd(p)
if 'insertBefore(sec, footer)' not in s:
    s = once(s, '(document.body||document.documentElement).appendChild(sec);', "var footer=document.querySelector('footer'); if(footer && footer.parentNode){ footer.parentNode.insertBefore(sec, footer); } else { (document.body||document.documentElement).appendChild(sec); }", 'shared')
wr(p, s)

# 2) partials/header.html - Planos -> /planos.html
p = 'partials/header.html'
h = rd(p)
if '<a href="/planos-assinatura.html">Planos</a>' in h:
    h = once(h, '<a href="/planos-assinatura.html">Planos</a>', '<a href="/planos.html">Planos</a>', 'header')
wr(p, h)

# 3) education/vendas.html - matricula assistida
p = 'education/vendas.html'
v = rd(p)
if 'Matrícula assistida neste momento' not in v:
    a = '<a class="cta" href="https://wa.me/5511954346288?text=Quero%20saber%20mais%20sobre%20os%20cursos%20da%20Praia%20Digital%20Academy" target="_blank" rel="noopener" style="background:#fff;color:#F4EBD0;margin-left:10px">Falar com especialista</a>'
    n = ' <div class="highlight" role="note"><h2>Matrícula assistida neste momento</h2><p>Os valores exibidos nesta página são os valores de referência dos cursos. Para preservar a qualidade da entrega, a matrícula é confirmada com atendimento humano: escolha o curso, fale com a equipe e receba as instruções de pagamento e acesso. Ainda não há checkout automático ativo nesta página.</p><p><a href="https://wa.me/5511954346288?text=Quero%20fazer%20minha%20matr%C3%ADcula%20na%20Praia%20Digital%20Academy" target="_blank" rel="noopener">Solicitar matrícula assistida no WhatsApp</a> · <a href="/education/index.html">Voltar para a Academy</a></p></div>'
    v = once(v, a, a + n, 'vendas')
wr(p, v)

# 4) education/checkout.html - pagina segura de matricula assistida
checkout = """<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Matrícula assistida — Praia Digital Academy</title><meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://praia.digital/education/checkout.html">
<meta name="description" content="Matrícula assistida da Praia Digital Academy. Escolha o curso e fale com a equipe para receber as instruções de pagamento e acesso.">
<style>*{box-sizing:border-box}body{font-family:'Segoe UI',system-ui,sans-serif;background:#F4EBD0;color:#023047;margin:0;padding:32px 20px;line-height:1.65}.wrap{max-width:900px;margin:0 auto}.card{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:16px;padding:22px;margin:18px 0}.cta{display:inline-block;background:#00B4D8;color:#fff;padding:.75rem 1.25rem;border-radius:999px;font-weight:700;text-decoration:none;margin:.35rem}.secondary{background:#023047}.muted{color:#41525f}.notice{background:#fff8e6;border-left:5px solid #f2b705;padding:16px;border-radius:10px}</style></head>
<body><div class="wrap"><main id="main"><p><a href="/education/vendas.html">← Voltar para os cursos</a></p>
<h1>Matrícula assistida — Praia Digital Academy</h1>
<p>A Academy está em fase de matrícula assistida. A equipe confirma o curso ideal para o seu objetivo antes de enviar as instruções finais de pagamento e acesso.</p>
<div class="card"><h2>Como funciona</h2><ol><li>Escolha o curso no catálogo da Academy.</li><li>Fale com a equipe informando o curso desejado.</li><li>Receba a confirmação do valor, as instruções de pagamento e o próximo passo para acessar o conteúdo.</li></ol>
<p><a class="cta" href="https://wa.me/5511954346288?text=Quero%20fazer%20minha%20matr%C3%ADcula%20na%20Praia%20Digital%20Academy" target="_blank" rel="noopener">Solicitar matrícula no WhatsApp</a>
<a class="cta secondary" href="mailto:comercial@praia.digital?subject=Matr%C3%ADcula%20assistida%20%E2%80%94%20Praia%20Digital%20Academy&body=Ol%C3%A1%2C%20equipe%20Praia%20Digital!%0A%0AQuero%20fazer%20minha%20matr%C3%ADcula%20na%20Academy.%0A%0ACurso%20desejado%3A%0ANome%3A%0AWhatsApp%3A%0AObjetivo%20com%20o%20curso%3A%0A%0AObrigado(a).">Solicitar matrícula por e-mail</a></p></div>
<div class="notice"><strong>Importante:</strong> esta página não processa pagamentos automaticamente. Não informe dados de cartão aqui. O pagamento só deve ser feito após a confirmação da equipe Praia Digital.</div>
<h2>Perguntas frequentes</h2><div class="card">
<p><strong>Como acesso o curso após a matrícula?</strong><br><span class="muted">Após a confirmação da matrícula pela equipe, você recebe as instruções de acesso à área do aluno e ao conteúdo contratado.</span></p>
<p><strong>Emite certificado?</strong><br><span class="muted">Os cursos e formações indicam no catálogo quando há certificado após a conclusão.</span></p>
<p><strong>Quais formas de pagamento estão disponíveis?</strong><br><span class="muted">A equipe confirma as opções disponíveis no momento da matrícula, antes de qualquer pagamento.</span></p></div>
<p><a href="/education/index.html">Conhecer a Academy</a> · <a href="/education/cursos/index.html">Ver catálogo de cursos</a> · <a href="/planos.html">Ver planos Praia Digital</a></p>
</main></div></body></html>
"""
wr('education/checkout.html', checkout)

# 5) Paginas pos-compra dos avulsos
STYLE = 'body{font-family:Arial,sans-serif;max-width:900px;margin:0 auto;padding:28px;line-height:1.65;color:#17202b}a{color:#0969da}.cta{display:inline-block;background:#0969da;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:bold}.box{background:#f4f7fb;padding:18px;border-radius:10px;margin:18px 0}.warn{background:#fff8e6;padding:16px;border-left:5px solid #f2b705}'

def mail(subject, body):
    return 'mailto:comercial@praia.digital?subject=' + quote(subject) + '&body=' + quote(body)

def obrigado(path, title, desc, h1, intro, items, subject, body, links):
    lis = ''.join('<li>' + x + '</li>' for x in items)
    lnk = ' · '.join('<a href="' + u + '">' + t + '</a>' for t, u in links)
    return ('<!DOCTYPE html>\n<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>' + title + ' | Praia Digital</title><meta name="description" content="' + desc + '"><meta name="robots" content="noindex, follow"><link rel="canonical" href="https://praia.digital/' + path + '"><style>' + STYLE + '</style></head><body>\n<h1>' + h1 + '</h1><p>' + intro + '</p>\n<div class="box"><h2>Envie agora os dados para iniciarmos</h2><ol>' + lis + '</ol><p><a class="cta" href="' + mail(subject, body) + '">Enviar dados para comercial@praia.digital</a></p></div>\n<div class="warn"><strong>Confirmação:</strong> guardaremos o e-mail usado no checkout como referência. Se você enviar os dados de outro e-mail, informe também o e-mail da compra para localizarmos o pagamento.</div>\n<h2>Próximos passos</h2><p>Após recebermos seus dados, a equipe confirma o recebimento, valida o escopo contratado e informa o prazo de produção/entrega neste mesmo e-mail. Guarde o comprovante do Stripe.</p>\n<p>' + lnk + '</p></body></html>\n')

wr('obrigado-relatorio-avaliacao.html', obrigado('obrigado-relatorio-avaliacao.html', 'Compra confirmada — Relatório de Avaliação', 'Página pós-compra do Relatório Completo de Avaliação Praia Digital: envie os dados do imóvel para iniciarmos a produção.', 'Compra confirmada — Relatório de Avaliação de Imóvel', 'Obrigado pela compra do <strong>Relatório Completo de Avaliação de Imóvel em PDF — R$ 49</strong>. Para produzirmos o relatório correto, precisamos dos dados do imóvel.', ['E-mail usado no checkout Stripe.', 'Endereço completo do imóvel e link do anúncio, se houver.', 'Cidade, bairro, tipologia, área, dormitórios, suítes, vagas e padrão.', 'Preço pretendido ou faixa que você quer avaliar.', 'Diferenciais: vista mar, mobiliado, lazer, andar, reforma e conservação.', 'Objetivo: vender, comprar, negociar ou definir preço de anúncio.'], 'Intake pós-compra — Relatório de Avaliação R$ 49', 'Olá, equipe Praia Digital!\n\nAcabei de adquirir o Relatório Completo de Avaliação de Imóvel em PDF (R$ 49) e seguem os dados para produção:\n\nE-mail usado no checkout Stripe:\nEndereço do imóvel:\nLink do anúncio (se houver):\nCidade/bairro:\nTipologia, área, dormitórios, suítes e vagas:\nPreço pretendido:\nDiferenciais do imóvel:\nObjetivo da avaliação:\n\nObrigado(a).', [('Ver o conteúdo do relatório', 'entrega-relatorio-avaliacao.html'), ('Voltar aos planos', 'planos.html'), ('Falar no WhatsApp', 'https://wa.me/5511954346288')]))

wr('obrigado-kit-temporada.html', obrigado('obrigado-kit-temporada.html', 'Assinatura confirmada — Kit Temporada', 'Página pós-compra do Kit Temporada Praia Digital: cadastre seus imóveis para iniciarmos o acompanhamento mensal.', 'Assinatura confirmada — Kit Temporada por Imóvel', 'Obrigado por assinar o <strong>Kit Temporada — R$ 39 por imóvel/mês</strong>. Agora precisamos cadastrar cada imóvel para organizar o acompanhamento mensal.', ['E-mail usado no checkout Stripe e quantidade de imóveis contratada.', 'Para cada imóvel: apelido/endereço, cidade e link do anúncio.', 'Diária atual, ocupação estimada e objetivo de receita.', 'Custos fixos e variáveis conhecidos: limpeza, condomínio, plataforma e manutenção.', 'Calendário ou períodos de bloqueio, se já existirem.'], 'Intake pós-compra — Kit Temporada R$ 39/imóvel/mês', 'Olá, equipe Praia Digital!\n\nAcabei de assinar o Kit Temporada por Imóvel (R$ 39/imóvel/mês) e seguem os dados iniciais:\n\nE-mail usado no checkout Stripe:\nQuantidade de imóveis contratada:\n\nImóvel 1 — apelido/endereço:\nCidade e link do anúncio:\nDiária atual e ocupação estimada:\nCustos conhecidos:\nObjetivo de receita:\n\nImóvel 2 — apelido/endereço:\nCidade e link do anúncio:\nDiária atual e ocupação estimada:\nCustos conhecidos:\nObjetivo de receita:\n\nObrigado(a).', [('Ver o conteúdo do Kit', 'entrega-kit-temporada.html'), ('Testar calculadoras gratuitas', 'ferramentas/'), ('Voltar aos planos', 'planos.html')]))

wr('obrigado-pacote-descricoes.html', obrigado('obrigado-pacote-descricoes.html', 'Compra confirmada — Pacote 20 Descrições', 'Página pós-compra do Pacote 20 Descrições Praia Digital: envie os dados dos imóveis para produzirmos seus textos.', 'Compra confirmada — Pacote 20 Descrições com IA', 'Obrigado pela compra do <strong>Pacote 20 Descrições com IA — R$ 97</strong>. Envie os dados dos imóveis para produzirmos as versões para portal, Instagram e WhatsApp.', ['E-mail usado no checkout Stripe.', 'Para cada um dos até 20 imóveis: cidade, bairro e link ou ficha do imóvel.', 'Tipo, área, dormitórios, suítes, vagas, mobiliado e diferenciais.', 'Objetivo de cada anúncio: venda, locação anual ou temporada.', 'Tom desejado: direto, premium, acolhedor ou técnico.', 'Observações obrigatórias ou informações que não devem aparecer.'], 'Intake pós-compra — Pacote 20 Descrições R$ 97', 'Olá, equipe Praia Digital!\n\nAcabei de adquirir o Pacote 20 Descrições com IA (R$ 97) e seguem os dados dos imóveis:\n\nE-mail usado no checkout Stripe:\nTom desejado:\n\nImóvel 1 — cidade/bairro:\nLink ou ficha:\nTipo, área, dormitórios, suítes e vagas:\nDiferenciais:\nObjetivo (venda, locação ou temporada):\nObservações:\n\nImóvel 2 — cidade/bairro:\nLink ou ficha:\nTipo, área, dormitórios, suítes e vagas:\nDiferenciais:\nObjetivo (venda, locação ou temporada):\nObservações:\n\nPosso completar os demais imóveis neste mesmo e-mail ou em planilha anexa.\n\nObrigado(a).', [('Ver modelos e conteúdo do pacote', 'entrega-descricoes-ia.html'), ('Testar gerador gratuito', 'ferramentas/geracao-descricoes.html'), ('Voltar aos planos', 'planos.html')]))

# 6) Blocos pos-pagamento nas paginas de entrega
def block(rel, html):
    t = rd(rel)
    if 'Após o pagamento' in t or 'Após a assinatura' in t:
        wr(rel, t)
        return
    m = '<p><a class="cta"'
    if m not in t:
        raise SystemExit('ERRO ' + rel + ': CTA ausente')
    wr(rel, t.replace(m, html + '\n' + m, 1))

block('entrega-relatorio-avaliacao.html', '<div class="box"><h2>Após o pagamento</h2><p>Você será direcionado para a página de confirmação com o checklist de intake. Envie os dados do imóvel para <strong>comercial@praia.digital</strong> para iniciarmos a produção. Se o botão de confirmação não abrir, acesse <a href="obrigado-relatorio-avaliacao.html">obrigado-relatorio-avaliacao.html</a> e siga as instruções.</p></div>')
block('entrega-descricoes-ia.html', '<div class="box"><h2>Após o pagamento</h2><p>Você será direcionado para a página de confirmação com o checklist de intake. Envie os dados de até 20 imóveis para <strong>comercial@praia.digital</strong> para produzirmos os textos. Se o botão de confirmação não abrir, acesse <a href="obrigado-pacote-descricoes.html">obrigado-pacote-descricoes.html</a>.</p></div>')
block('entrega-kit-temporada.html', '<div class="box"><h2>Após a assinatura</h2><p>Você será direcionado para a página de confirmação com o checklist de cadastro dos imóveis. Envie os dados para <strong>comercial@praia.digital</strong> para ativarmos o acompanhamento. Se o botão de confirmação não abrir, acesse <a href="obrigado-kit-temporada.html">obrigado-kit-temporada.html</a>.</p></div>')

for rel, needle in [('js/shared.js', 'insertBefore(sec, footer)'), ('partials/header.html', '/planos.html'), ('education/vendas.html', 'Matrícula assistida neste momento'), ('education/checkout.html', 'não processa pagamentos automaticamente'), ('obrigado-relatorio-avaliacao.html', 'mailto:comercial@praia.digital'), ('obrigado-kit-temporada.html', 'mailto:comercial@praia.digital'), ('obrigado-pacote-descricoes.html', 'mailto:comercial@praia.digital')]:
    t = rd(rel)
    if needle not in t or len(t.encode('utf-8')) < 500:
        raise SystemExit('ERRO validacao ' + rel)
print('VALIDACAO OK - lote aplicado')
