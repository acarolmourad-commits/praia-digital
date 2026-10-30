#!/usr/bin/env python3
"""Deterministic static Academy catalog. No payment/authentication side effects.
Full learning plans and workbook output must be supplied outside this repository.
Public prices and offer structure remain under docs/academy.
"""
import json, html, hashlib, argparse, re
from pathlib import Path
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text())
def esc(s): return html.escape(str(s),quote=True)
def write(p,s):
 f=ROOT/p; f.parent.mkdir(parents=True,exist_ok=True)
 if f.suffix=='.html':s=s.replace('><','>\n<')+'\n'
 f.write_text(s,encoding='utf-8')
def money(n): return 'R$ '+f'{n:.2f}'.replace('.',',')
def ul(items): return '<ul>'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul>'
POLICY='100% digital • leitura e exercícios • estudo no seu ritmo'
LIMITS='Não inclui videoaulas, aulas ao vivo, tutoria individual, assinatura de ferramentas ou certificado. Não é formação profissional habilitante. Não há promessa de renda ou resultado.'
DELIVERY='Matrícula assistida: antes de pagar, confirme com a equipe o material, o valor final, o formato de entrega digital e o prazo. Esta página não processa pagamentos. Não depende de acesso automático à área do aluno.'
def shell(title,desc,path,body,schema=None,noindex=False):
 structured=json.dumps(schema or {'@context':'https://schema.org','@type':'WebPage','name':title,'url':'https://praia.digital'+path},ensure_ascii=False).replace('</','<\\/')
 return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — Praia Digital Academy</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{'noindex, follow' if noindex else 'index, follow'}"><link rel="canonical" href="https://praia.digital{path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="https://praia.digital{path}"><link rel="stylesheet" href="/education/assets/academy.css"><script type="application/ld+json">{structured}</script></head><body><a class="skip" href="#main">Pular para o conteúdo</a><div class="wrap"><nav class="academy-nav" aria-label="Navegação Academy"><a href="/">Praia Digital</a><a href="/education/index.html">Academy</a><a href="/education/cursos/index.html">Cursos digitais</a><a href="/education/formacoes/index.html">Trilhas</a><a href="/education/aluno/login.html">Acesso e ajuda</a></nav><main id="main">{body}</main><footer><p>Praia Digital Academy · {POLICY}</p><p><a href="/education/checkout.html">Atendimento e matrícula</a> · <a href="mailto:comercial@praia.digital">comercial@praia.digital</a></p><p>Material educacional. Para decisões jurídicas, tributárias, financeiras ou atuação profissional regulamentada, procure profissional habilitado e consulte as fontes oficiais vigentes.</p></footer></div></body></html>'''
def lesson_html(lesson):
 body=lesson['body']; body=[body] if isinstance(body,str) else body
 return '<section><h2>'+esc(lesson['title'])+'</h2>'+''.join('<p>'+esc(p)+'</p>' for p in body)+'</section>'
def sources_html(c):
 return ('<section><h2>Para continuar estudando</h2><ul>'+''.join('<li><a href="'+esc(s['url'])+'">'+esc(s.get('title',s.get('label',s['url'])))+'</a>'+(' — '+esc(s['note']) if s.get('note') else '')+'</li>' for s in c.get('sources',[]))+'</ul></section>') if c.get('sources') else ''
def workbook_html(c):
 example=c.get('worked_example'); out=''
 if example:
  out='<section><h2>Exemplo resolvido</h2><p>'+esc(example['scenario'])+'</p>'+ul(example['walkthrough'])+'<p><strong>Resultado:</strong> '+esc(example['result'])+'</p><p>'+esc(example.get('limits',''))+'</p></section>'
 if c.get('worksheet'):
  out+='<section><h2>Ficha para preencher</h2>'+''.join('<h3>'+esc(prompt)+'</h3><div class="answer"></div>' for prompt in c['worksheet'])+'</section>'
 return out
def paras(value):
 return ''.join('<p>'+esc(v)+'</p>' for v in (value if isinstance(value,list) else [value]))
def application_outline(c):
 a=c.get('application')
 return ('<h3>Aplicação prática desta edição</h3>'+ul([step['title'] for step in a['procedure']])+'<p>Inclui modelo preenchido, diagnóstico de uma falha e critérios para verificar a correção.</p>') if a else ''
def application_html(c):
 a=c.get('application')
 if not a:return ''
 out='<section><h2>Procedimento demonstrado</h2>'
 for step in a['procedure']:
  out+='<h3>'+esc(step['title'])+'</h3>'+paras(step['body'])
 out+='</section><section><h2>Modelo preenchido — exemplo didático</h2><p>Os dados são ilustrativos. Adapte a ficha ao seu contexto, sem tratar o exemplo como resultado real ou recomendação individual.</p>'
 for row in a['filled_template']:
  out+='<div class="card"><h3>'+esc(row['field'])+'</h3>'+paras(row['value'])+'<p><strong>Por quê:</strong> '+esc(row['why'])+'</p></div>'
 f=a['failure_case'];out+='</section><section class="card"><h2>Quando o plano falha</h2>'
 for key,label in [('scenario','Situação'),('diagnosis','Diagnóstico'),('correction','Correção'),('verification','Como verificar')]:
  out+='<h3>'+label+'</h3>'+paras(f[key])
 return out+'</section>'
def practice_html(p):
 return '<section class="card"><h2>Atividade prática</h2><p>'+esc(p['scenario'])+'</p><ol>'+''.join('<li>'+esc(s)+'</li>' for s in p['steps'])+'</ol><h3>Entregável</h3><p>'+esc(p['deliverable'])+'</p><h3>Como revisar seu trabalho</h3>'+ul(p['review'])+'</section>'
def card(c): return f'<article class="card" data-course><span class="tag">{esc(c.get("category") or c["kind"])}</span><h3><a href="{c["path"]}">{esc(c["title"])}</a></h3><p>{esc(c["scope"])}</p><p class="price">{money(c["price"])}</p><a href="{c["path"]}">Ver conteúdo e amostra →</a></article>'
def external_path(value,label):
 if not value:raise ValueError(label+' is required; full course material must stay outside the public repository')
 path=Path(value).expanduser().resolve()
 if path==ROOT.resolve() or ROOT.resolve() in path.parents:raise ValueError(label+' must be outside the public repository')
 return path
def private_target(directory,slug):
 target=directory/(slug+'.html')
 if target.is_symlink() or (target.exists() and target.stat().st_nlink>1):raise ValueError('Private output must not use linked files')
 resolved=target.resolve()
 if directory not in resolved.parents or ROOT.resolve() in resolved.parents:raise ValueError('Private output escaped its external directory')
 return target
def build(plans_path=None,private_output=None):
 plans_path=external_path(plans_path,'Private learning plans')
 private_output=external_path(private_output,'Private workbook output')
 plans=json.loads(plans_path.read_text(encoding='utf-8')); prices=read('docs/academy/course-prices.json')
 courses=plans['courses']; aliases=plans.get('aliases',{}); catalog=[]
 missing=[slug for slug,c in courses.items() if slug not in aliases and not c.get('application')]
 if missing:raise ValueError('Instructional applications must be complete before generating paid offers: '+', '.join(missing))
 for slug,c in courses.items():
  if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',slug):raise ValueError('Unsafe course identifier')
  if slug in aliases:continue
  a=c['application']
  if len(a.get('procedure',[]))<3 or len(a.get('filled_template',[]))<3 or set(a.get('failure_case',{}))!={'scenario','diagnosis','correction','verification'}:raise ValueError('Incomplete application: '+slug)
  if slug not in prices['courses']:raise ValueError('Missing price: '+slug)
  private_target(private_output,slug)
 for slug,c in courses.items():
  if slug in aliases: continue
  price=prices['courses'][slug]; path=f'/education/cursos/{slug}/index.html'
  item={'slug':slug,'title':c['title'],'price':price,'path':path,'kind':'Curso curto digital','scope':c['scope'],'category':c.get('category',''),'aliases':[old for old,target in aliases.items() if target==slug]};catalog.append(item)
  buy='/education/checkout.html?course='+quote(slug)
  body=f'<header class="hero"><p class="eyebrow">Curso curto digital · material escrito</p><h1>{esc(c["title"])}</h1><p class="lead">{esc(c["scope"])}</p><p>{POLICY}</p></header><div class="grid"><section class="card"><h2>Para quem é</h2><p>{esc(c["audience"])}</p><h3>O que você vai praticar</h3>{ul(c["objectives"])}</section><section class="card"><h2>Material digital</h2><p class="price">{money(price)}</p><p>Pagamento único pelo material descrito nesta página. Apostila de leitura com {len(c["lessons"])} lições curtas em texto, 1 exemplo resolvido, procedimento demonstrado, modelo preenchido, análise de falha e ficha de trabalho. Sem produto físico.</p><a class="cta" href="{buy}">Solicitar matrícula</a><a class="cta secondary" href="amostra.html">Ler amostra gratuita</a><p>{esc(DELIVERY)}</p></section></div><h2>Conteúdo desta edição</h2>{ul([x["title"] for x in c["lessons"]])}{application_outline(c)}{practice_html(c["practice"])}{sources_html(c)}<section><h2>Escopo transparente</h2><p>{LIMITS}</p><h3>Não incluído neste material</h3>{ul(c.get("not_included",[]))}<p>Conteúdo introdutório e aplicado. Os nomes históricos das URLs não significam curso extensivo ou domínio completo do tema.</p></section>'
  schema={'@context':'https://schema.org','@type':'Course','name':c['title'],'description':c['scope'],'inLanguage':'pt-BR','provider':{'@type':'Organization','name':'Praia Digital','url':'https://praia.digital/'},'offers':{'@type':'Offer','price':price,'priceCurrency':'BRL','url':'https://praia.digital'+buy,'category':'Paid'}}
  write(path.lstrip('/'),shell(c['title'],c['scope'],path,body,schema))
  # Historical sales URL remains usable, with one source for every price/promise.
  write(f'education/cursos/{slug}/vendas.html',shell(c['title'],c['scope'],path,body,schema))
  sample=f'<article class="reading"><p class="eyebrow">Amostra gratuita · curso curto digital</p><h1>{esc(c["title"])}</h1>{lesson_html(c["lessons"][0])}{sources_html(c)}<p><a class="cta" href="{path}">Ver programa e valor</a></p></article>'
  write(f'education/cursos/{slug}/amostra.html',shell('Amostra: '+c['title'],c['scope'],f'/education/cursos/{slug}/amostra.html',sample,noindex=True))
  full=f'<article class="reading"><p class="eyebrow">Apostila digital · edição outubro de 2026</p><h1>{esc(c["title"])}</h1><p>{esc(c["scope"])}</p><p>{POLICY}</p>{ul(c["objectives"])}'+''.join(lesson_html(x) for x in c['lessons'])+workbook_html(c)+application_html(c)+practice_html(c['practice'])+sources_html(c)+f'<h2>Seu caderno de respostas</h2><p>Salve ou imprima esta página em PDF pelo navegador. Registre suas respostas em um documento próprio; esta página não envia nem armazena seus dados.</p><div class="answer">Observações, hipóteses, resultados e próximos passos:</div><p>{LIMITS}</p></article>'
  delivery=shell(c['title'],c['scope'],path,full,noindex=True)
  delivery=delivery.replace('<link rel="stylesheet" href="/education/assets/academy.css">','<style>'+(ROOT/'education/assets/academy.css').read_text()+'</style>').replace('href="/','href="https://praia.digital/')
  private_output.mkdir(parents=True,exist_ok=True)
  private_target(private_output,slug).write_text(delivery.replace('><','>\n<')+'\n',encoding='utf-8')
 for old,new in aliases.items():
  target=f'/education/cursos/{new}/index.html';title=courses[new]['title']
  body=f'<h1>{esc(title)}</h1><p>Este endereço é uma versão anterior do mesmo conteúdo. Para evitar uma compra duplicada, consulte a edição atual; não é um curso adicional.</p><a class="cta" href="{target}">Ver a edição atual</a>'
  for prefix in (old,'_archive_'+old):
   if not (ROOT/f'education/cursos/{prefix}').exists():continue
   for f in ('index.html','vendas.html'):write(f'education/cursos/{prefix}/{f}',shell(title,'Endereço anterior do curso.',target,body,noindex=True))
 # Bundles use only reviewed, explicitly enumerated courses; never imply a qualification.
 for slug,f in plans.get('formations',{}).items():
  if f.get('same_product'):
   target='/education/cursos/'+f['same_product']+'/index.html'
   body='<h1>'+esc(f['title'])+'</h1><p>'+esc(f['scope'])+'</p><a class="cta" href="'+target+'">Ver o guia digital e seu valor</a>'
   write(f'education/formacoes/{slug}.html',shell(f['title'],f['scope'],target,body))
   next(c for c in catalog if c['slug']==f['same_product'])['aliases'].append(slug)
   continue
  included=f['courses']; price=prices['formations'][slug];path=f'/education/formacoes/{slug}.html'; title=f['title'];desc=f['scope']
  links='<ul>'+''.join(f'<li><a href="/education/cursos/{s}/index.html">{esc(courses[s]["title"])}</a></li>' for s in included)+'</ul>'
  bundle_slug='trilha-'+slug
  body=f'<header class="hero"><p class="eyebrow">Trilha de leitura digital</p><h1>{esc(title)}</h1><p class="lead">{esc(desc)}</p><p>{POLICY}</p></header><div class="card"><h2>Materiais incluídos</h2>{links}<p>Esta trilha reúne os cursos curtos acima; não acrescenta videoaulas, acompanhamento ou certificado. Se você já possui um material, informe a equipe antes de contratar para evitar duplicidade.</p><p class="price">{money(price)}</p><a class="cta" href="/education/checkout.html?course={quote(bundle_slug)}">Solicitar esta trilha</a><p>{DELIVERY}</p></div><div class="notice">Não habilita ao exercício de profissão, não substitui TTI, registro profissional ou requisitos para emissão de laudos. {LIMITS}</div>'
  write(path.lstrip('/'),shell(title,desc,path,body));catalog.append({'slug':'trilha-'+slug,'title':title,'price':price,'path':path,'kind':'Trilha digital','scope':desc})
 write('education/assets/catalog.json',json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 release={'edition':'2026-10-30-digital','offerings':len(catalog),'catalog_sha256':hashlib.sha256((ROOT/'education/assets/catalog.json').read_bytes()).hexdigest(),'learning_plan_sha256':hashlib.sha256(plans_path.read_bytes()).hexdigest()}
 write('education/assets/release.json',json.dumps(release,ensure_ascii=False,indent=2)+'\n')
 guides=[c for c in catalog if c['kind']=='Curso curto digital'];bundles=[c for c in catalog if c['kind']=='Trilha digital']
 for path,title,items in [('/education/cursos/index.html','Cursos curtos digitais',guides),('/education/vendas.html','Cursos e trilhas digitais',catalog),('/education/formacoes/index.html','Trilhas de leitura digital',bundles)]:
  body=f'<header class="hero"><p class="eyebrow">Praia Digital Academy</p><h1>{title}</h1><p class="lead">Conteúdo escrito, atividades práticas e escopo claro para o mercado imobiliário. {POLICY}.</p></header><div class="notice">Cursos curtos de leitura, não cursos extensivos em vídeo. Sem certificado, suporte individual ou resultado financeiro. Matrícula e entrega digital assistidas.</div><label for="course-search">Buscar por assunto</label><input id="course-search" type="search" placeholder="Ex.: Airbnb, captação, fotografia"><p id="result-count" role="status">{len(items)} opções</p><h2>Materiais disponíveis</h2><div class="grid">'+''.join(card(c) for c in items)+'</div><script src="/education/assets/catalog-search.js" defer></script>'
  if path=='/education/formacoes/index.html':
   body+='<p>A antiga formação em fotografia corresponde ao <a href="/education/cursos/fotografia-imoveis-temporada/index.html">guia digital de fotografia</a>, uma única oferta, sem cobrança adicional por outro nome.</p>'
  write(path.lstrip('/'),shell(title,'Conteúdo escrito e exercícios para estudo autônomo, 100% digital.',path,body))
 featured_slugs=('airbnb-do-zero','pricelabs-completo','captacao-imoveis-corretores','analise-de-rentabilidade','fotografia-imoveis-temporada','ia-para-corretores')
 featured=[next(c for c in guides if c['slug']==s) for s in featured_slugs if any(c['slug']==s for c in guides)]
 body=f'<header class="hero"><p class="eyebrow">Aprenda para aplicar</p><h1>Praia Digital Academy</h1><p class="lead">Conhecimento imobiliário em pequenas doses: leitura objetiva, exemplos e exercícios para transformar estudo em uma decisão ou entrega concreta.</p><p>{POLICY}</p><a class="cta" href="/education/cursos/index.html">Explorar cursos digitais</a><a class="cta secondary" href="/education/formacoes/index.html">Conhecer trilhas</a></header><div class="grid"><section class="card"><h2>Saiba o que está comprando</h2><p>Guia digital curto, exemplo resolvido e ficha de exercício específica por tema. Leia uma amostra antes de escolher.</p></section><section class="card"><h2>Estude sem horário marcado</h2><p>Conteúdo escrito para leitura autônoma. Sem deslocamento, aulas presenciais ou material físico.</p></section><section class="card"><h2>Entrega orientada pela equipe</h2><p>Confirme curso, preço e instruções de entrega antes do pagamento. O checkout não efetua cobrança automática.</p></section></div><h2>Escolha seu próximo aprendizado</h2><div class="grid">'+''.join(card(c) for c in featured)+f'</div><p><a href="/education/cursos/index.html">Ver todos os {len(guides)} cursos curtos →</a></p><div class="notice">{LIMITS}</div>'
 write('education/index.html',shell('Cursos curtos 100% digitais','Academy: leitura, exercícios e materiais digitais para o mercado imobiliário.','/education/index.html',body))
 # Keep historical URL inventory but remove unsupported sales-readiness labels.
 historical=read('docs/academy/inventory-64-cursos.json')
 for record in historical:
  slug=record['slug']; target=aliases.get(slug,slug); course=courses[target]
  record.update(title=course['title'],h1=course['title'],description=course['scope'],classificacao='alias' if slug in aliases else 'curso_curto_digital',status_final='ALIAS_CONSOLIDADO' if slug in aliases else 'CURSO_CURTO_DIGITAL',audit_status='ESCOPO_TEXTUAL_REVISADO_2026_10_30')
  record.pop('percentual_geral',None)
 write('docs/academy/inventory-64-cursos.json',json.dumps(historical,ensure_ascii=False,indent=2)+'\n')
 write('docs/academy/catalog-64-cursos.json',json.dumps({'generated_at':'2026-10-30','historical_url_count':64,'total':len(catalog),'items':catalog},ensure_ascii=False,indent=2)+'\n')
 print(f'Built {len(guides)} courses,{len(bundles)} bundles,{len(aliases)} aliases; catalog {len(catalog)} items')
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--private-plans',required=True,type=Path)
 parser.add_argument('--private-output',required=True,type=Path)
 args=parser.parse_args();build(args.private_plans,args.private_output)
