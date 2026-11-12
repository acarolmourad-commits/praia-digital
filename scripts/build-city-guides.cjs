// Static city guides: edit data/city-guides.json, then run this file.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const data = JSON.parse(fs.readFileSync(path.join(root, 'data/city-guides.json'), 'utf8'));
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link = (url, text, cls='') => `<a${cls ? ` class="${cls}"` : ''} href="${esc(url)}">${esc(text)}</a>`;
const section = (id, title, body, alt=false) => `<section id="${id}"${alt?' class="alt"':''}><div class="wrap"><h2>${esc(title)}</h2>${body}</div></section>`;
const p = text => `<p class="lead">${esc(text)}</p>`;
function shell(title, description, url, body, schema) {
  return `<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} | Praia Digital</title>
<meta name="description" content="${esc(description)}">
<meta name="robots" content="index, follow"><link rel="canonical" href="https://praia.digital${url}">
<meta property="og:type" content="website"><meta property="og:title" content="${esc(title)} | Praia Digital">
<meta property="og:description" content="${esc(description)}"><meta property="og:url" content="https://praia.digital${url}">
<link rel="stylesheet" href="/assets/css/pd-design-system.css"><link rel="stylesheet" href="/assets/css/city-guides.css">
<script type="application/ld+json">${JSON.stringify(schema).replace(/</g,'\\u003c')}</script>
</head><body>
<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
<meta name="pd-shared-nav">
<header class="pd"><div class="wrap city-fallback"><a class="logo" href="/">Praia<span>Digital</span></a><nav aria-label="Navegação principal">${link('/cidades/','Cidades')} ${link('/bairros/index.html','Bairros')} ${link('/imoveis.html','Imóveis')}</nav></div></header>
<main id="conteudo">${body}</main>
<footer class="pd"><div class="wrap">${link('/cidades/','Todas as cidades')} · ${link('/politica-editorial.html','Política editorial')} · ${link('/contato.html','Contato')}<p>Praia Digital — guias para pesquisar imóveis no litoral paulista.</p></div></footer>
</body></html>
`;
}
function neighborhoods(c) {
  const hub = `/bairros/${c.slug}/index.html`;
  if (!fs.existsSync(path.join(root, hub))) return p(`Ainda não há guia dedicado de bairros de ${c.name} nesta seção. Use as referências locais e confira o endereço do imóvel nos canais municipais.`);
  // The PR88 curated index is primary; preserve the older municipal hub as a secondary route.
  return p(`Explore os guias já publicados para ${c.name}. Nomes de praias, regiões e bairros podem aparecer juntos; confirme o endereço exato ao comparar imóveis.`)
    + `<div class="actions">${link('/bairros/index.html#'+c.slug,`Explorar bairros de ${c.name}`,'btn')} ${link(hub,`Bairros de ${c.name} em detalhe`,'text-link')}</div>`;
}
function city(c) {
  const url = `/cidades/${c.slug}.html`, search = '/imoveis.html?cidade='+encodeURIComponent(c.name);
  const cta = link(search, `Ver imóveis em ${c.name}`, 'btn');
  const faq = [
    [`Em qual região fica ${c.name}?`, `${c.name} integra ${c.region} no recorte regional deste guia. A classificação segue os setores litorâneos apresentados pela Semil.`],
    [`Como consultar imóveis em ${c.name}?`, `Use a busca com o filtro de ${c.name}. Se não houver correspondências no catálogo, a busca informa que nenhum imóvel foi encontrado; isso não significa ausência de imóveis na cidade.`],
    [`Há dados de preço e rentabilidade para ${c.name}?`, 'Este guia não publica uma média verificada de preço, ocupação ou rentabilidade. Compare anúncios semelhantes e despesas do imóvel; simulações dependem dos valores informados e não garantem resultados.']
  ];
  const schema = {'@context':'https://schema.org','@graph':[
    {'@type':'WebPage','@id':'https://praia.digital'+url, url:'https://praia.digital'+url, name:`Guia de ${c.name}`,dateModified:data.reviewed,about:{'@type':'City',name:c.name,address:{'@type':'PostalAddress',addressLocality:c.name,addressRegion:'SP',addressCountry:'BR'}}},
    {'@type':'BreadcrumbList',itemListElement:[{'@type':'ListItem',position:1,name:'Início',item:'https://praia.digital/'},{'@type':'ListItem',position:2,name:'Cidades',item:'https://praia.digital/cidades/index.html'},{'@type':'ListItem',position:3,name:c.name,item:'https://praia.digital'+url}]},
    {'@type':'FAQPage',mainEntity:faq.map(([q,a])=>({'@type':'Question',name:q,acceptedAnswer:{'@type':'Answer',text:a}}))}
  ]};
  let body = `<div class="pd-hero"><div class="wrap"><nav class="crumb" aria-label="Você está aqui">${link('/','Início')} › ${link('/cidades/','Cidades')} › ${esc(c.name)}</nav><p class="kicker">${esc(c.region)}</p><h1>Imóveis em ${esc(c.name)}</h1><p class="sub">${esc(c.intro)}</p><div class="actions">${cta} ${link('#bairros','Conhecer bairros','btn btn-ghost')}</div></div></div>
<nav class="wrap city-sections" aria-label="Nesta página">${link('#visao-geral','Visão geral')} ${link('#bairros','Bairros')} ${link('#visita','Referências locais')} ${link('#analise','Antes de decidir')} ${link('#fontes','Fontes')}</nav>`;
  body += section('visao-geral',`Como é ${c.name}`,p(c.local)+`<p class="src">Referência territorial: ${link(c.source,c.sourceLabel)}. Consulta em <time datetime="${data.reviewed}">02/11/2026</time>.</p>`);
  body += section('bairros',`Bairros e regiões de ${c.name}`,neighborhoods(c),true);
  const related={bertioga:['/blog/riviera-sao-lourenco-seguranca-infraestrutura-valorizacao-2026.html','Riviera de São Lourenço: infraestrutura e critérios de análise'],'praia-grande':['/blog/estudo-rental-yield-apartamentos-1-2-dormitorios-praia-grande-2026.html','Praia Grande: cenários de locação para apartamentos de 1 e 2 dormitórios']}[c.slug];
  if(related) body += section('leitura','Aprofunde a pesquisa',`<article class="card"><h3>${link(...related)}</h3><p>Conteúdo já publicado e revisado na Praia Digital. Consulte suas fontes e limitações antes de aplicar qualquer cenário ao seu imóvel.</p></article>`);
  body += section('visita',c.slug==='cubatao'?'Paisagem e patrimônio de Cubatão':`Praias e referências locais de ${c.name}`,p(c.visit));
  body += section('analise','Acesso, rotina e pontos de atenção',`<div class="proscons"><div class="pc pos"><h3>Na visita</h3><p>${esc(c.check)}</p></div><div class="pc att"><h3>Na comparação</h3><p>Peça documentos, despesas e informações de conservação do imóvel. Confirme serviços e deslocamentos no endereço, em vez de presumir condições iguais em toda a cidade.</p></div></div>`,true);
  body += section('ferramentas',`Ferramentas para pesquisar em ${c.name}`,`<div class="grid g3">${[
    ['/apps/custo-de-compra/','Custos da compra','Organize despesas e confira as alíquotas aplicáveis ao seu caso.'],
    ['/apps/calculadora-financiamento/','Financiamento','Simule parcelas com seus dados e compare propostas.'],
    ['/apps/simulador-roi-temporada/','Temporada','Teste cenários de receita e despesa, sem garantia de retorno.']
  ].map(([u,t,d])=>`<article class="card"><h3>${link(u,t)}</h3><p>${esc(d)}</p></article>`).join('')}</div><p class="src">Não há média verificada de preço/m², valorização ou ocupação publicada neste guia. ${link('/metodologia.html','Consulte a metodologia')}.</p>`);
  let listings = p(`A busca mantém ${c.name} selecionada e mostra somente as correspondências do catálogo. Confira os detalhes e a disponibilidade diretamente com o responsável pelo anúncio.`)+cta;
  if(c.slug==='bertioga') listings += `<div class="card city-listings"><h3>Imóveis cadastrados em Bertioga</h3><p>Ofertas publicadas na Praia Digital. Consulte as fichas para os dados de cada imóvel; imagens identificadas como renders e cenários financeiros continuam ilustrativos.</p><ul><li>${link('/casa-condominio-fechado-bertioga.html','Casa em condomínio fechado')}</li><li>${link('/imoveis/casas-lancamento-sao-lourenco.html','Lançamento de casas em São Lourenço')}</li></ul></div>`;
  body += section('imoveis',`Consultar imóveis em ${c.name}`,listings,true);
  body += section('perguntas',`Perguntas frequentes sobre ${c.name}`,faq.map(([q,a])=>`<details><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join(''));
  body += section('fontes','Fontes e atualização',`<p>Revisão editorial: <time datetime="${data.reviewed}">02/11/2026</time>. Fontes para localização, paisagem e referências de visita:</p><ul><li>${link(data.regionalSource,'Semil — setores do gerenciamento costeiro paulista')}</li><li>${link(c.source,c.sourceLabel)}</li></ul><p class="src">As orientações de comparação são editoriais. Fontes turísticas não comprovam preços, segurança, disponibilidade ou rendimento de imóveis. Operação de atrativos e condições de acesso devem ser consultadas antes da visita.</p>`,true);
  fs.writeFileSync(path.join(root,url),shell(`Imóveis em ${c.name}: bairros e guia local`,c.intro,url,body,schema));
}
function index() {
  const description='Conheça 16 municípios do Litoral Norte, Baixada Santista e Litoral Sul (Lagamar): guias locais, bairros e busca de imóveis por cidade.';
  let body=`<div class="pd-hero"><div class="wrap"><p class="kicker">Explore por região</p><h1>Cidades do litoral paulista</h1><p class="sub">${description}</p></div></div>`;
  body+=section('cobertura','Escolha onde pesquisar',p('O recorte reúne quatro municípios do Litoral Norte, nove da Baixada Santista e três do Litoral Sul (Lagamar). Cubatão integra a cobertura regional, embora não tenha praia oceânica. O setor interior do Vale do Ribeira, também abrangido pelo Gerco, não faz parte desta seleção.')+`<p>${link(data.regionalSource,'Veja a classificação regional da Semil')} · Revisão em <time datetime="${data.reviewed}">02/11/2026</time>.</p>`);
  const groups=['Litoral Norte','Baixada Santista','Litoral Sul (Lagamar)'];
  groups.forEach((region,i)=>body+=section('regiao-'+i,region,`<div class="grid g3">${data.cities.filter(c=>c.region===region).map(c=>`<article class="card city-card"><h3>${link('/cidades/'+c.slug+'.html',c.name)}</h3><p>${esc(c.intro)}</p><p class="city-card-link">${link('/cidades/'+c.slug+'.html','Conhecer '+c.name)}</p></article>`).join('')}</div>`,i%2===0));
  body += '<section aria-labelledby="conteudos-relacionados" style="max-width:1120px;margin:1.5rem auto;padding:1.25rem;border:1px solid #ccd8da;border-radius:12px;background:#fff;color:#123047"><h2 id="conteudos-relacionados">Da cidade ao endereço</h2><p><a href="/guias/ficha-comparacao-bairros-litoral.html" style="display:inline-block;padding:10px 0;text-decoration:underline">Preparar a visita ao bairro</a> · <a href="/bairros/index.html" style="display:inline-block;padding:10px 0;text-decoration:underline">Explorar os guias de bairros</a></p></section>\n';
  const schema={'@context':'https://schema.org','@type':'CollectionPage',name:'Cidades do litoral paulista',url:'https://praia.digital/cidades/index.html',mainEntity:{'@type':'ItemList',numberOfItems:16,itemListElement:data.cities.map((c,i)=>({'@type':'ListItem',position:i+1,name:c.name,url:'https://praia.digital/cidades/'+c.slug+'.html'}))}};
  fs.writeFileSync(path.join(root,'cidades/index.html'),shell('Cidades do litoral paulista: 16 guias locais',description,'/cidades/index.html',body,schema));
}
data.cities.forEach(city);index();console.log('Generated 16 city guides and regional index.');
