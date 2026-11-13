/* Praia Digital: seletor local. Não envia dados nem aciona serviços externos. */
(function (root) {
  'use strict';
  var choices = {
    temporada: {
      anuncio: {label:'Criar ou revisar meu anúncio',free:'/apps/oficina-ia-imobiliaria/',paid:'/servicos/anuncios-airbnb-booking.html',title:'Anúncios Airbnb e Booking',note:'Confira o escopo por imóvel e plataforma. Fotografias e gestão contínua são serviços separados.'},
      precos: {label:'Revisar diária e custos',free:'/ferramentas/calculadora-diaria-ideal-airbnb-2026.html',paid:'/anfitrioes/central-priceplabs.html#gestao-pricelabs',title:'Gestão de preços',note:'Escopo, frequência, custos e acessos precisam ser combinados. A assinatura da plataforma não está incluída automaticamente.'},
      operacao: {label:'Organizar a operação da temporada',free:'/anfitrioes/index.html',paid:'/servicos/gestao-imoveis.html',title:'Gestão de imóvel',note:'Consulte disponibilidade, responsabilidades e proposta para o seu imóvel.'}
    },
    venda: {
      anuncio: {label:'Melhorar a apresentação do anúncio',free:'/apps/oficina-ia-imobiliaria/',paid:'/servicos/propaganda-imobiliaria.html',title:'Propaganda imobiliária',note:'Texto, estrutura e roteiro de divulgação para venda ou locação. Confirme quem será responsável pela publicação.'},
      fotos: {label:'Melhorar fotos e apresentação visual',free:'/proprietarios/guia-do-proprietario.html',paid:'/servico-fotografia-edicao.html',title:'Fotografia e edição',note:'Orçamento conforme o imóvel e os materiais. Confirme quais imagens e entregas são necessárias.'}
    },
    profissional: {
      conteudo: {label:'Organizar conteúdo e descrições',free:'/apps/oficina-ia-imobiliaria/',paid:'/servicos/ia-para-imobiliarias.html',title:'IA para imobiliárias',note:'Comece por um anúncio e uma necessidade concreta. A amostra inicial e os serviços contratados têm escopos separados.'},
      atendimento: {label:'Planejar respostas e atendimento',free:'/apps/oficina-ia-imobiliaria/',paid:'/servicos/ia-para-imobiliarias.html',title:'Planejamento do atendimento',note:'O diagnóstico identifica o fluxo e os acessos necessários. Integrações e automações dependem de proposta e validação.'}
    },
    decidir: {
      valor: {label:'Estimar preço do imóvel',free:'/ferramentas/avaliacao-preco.html',paid:'/contato.html',title:'Conversa sobre avaliação',note:'Informe o objetivo e confirme o escopo antes de contratar. A estimativa gratuita não substitui avaliação profissional.'},
      retorno: {label:'Comparar custos e retorno de temporada',free:'/apps/simulador-roi-temporada/index.html',paid:'/contato.html',title:'Revisão das premissas',note:'Os cenários dependem dos custos e hipóteses informados; não há garantia de rendimento.'},
      comprar: {label:'Comparar compra e aluguel',free:'/apps/alugar-ou-comprar/index.html',paid:'/contato.html',title:'Conversa sobre seu cenário',note:'Use premissas adequadas ao seu caso e confirme qual apoio profissional está disponível.'}
    }
  };
  function recommend(objective,need,start) {
    if (!Object.prototype.hasOwnProperty.call(choices,objective) || !Object.prototype.hasOwnProperty.call(choices[objective],need) || ['sozinho','ajuda'].indexOf(start)<0) return null;
    var item=choices[objective][need];
    return {title:start==='sozinho'?'Comece pelo recurso gratuito':item.title,
      href:start==='sozinho'?item.free:item.paid,
      cta:start==='sozinho'?'Abrir recurso gratuito':'Conferir escopo e próximo passo',
      note:start==='sozinho'?'Você pode explorar este recurso antes de decidir sobre um serviço.':item.note,
      need:item.label};
  }
  if (typeof module!=='undefined' && module.exports) module.exports={choices:choices,recommend:recommend};
  if (typeof document==='undefined') return;
  var form=document.getElementById('service-selector');
  if (!form) return;
  form.hidden=false;
  var objective=form.elements.objective, need=form.elements.need, start=form.elements.start;
  var result=document.getElementById('service-selector-result');
  function resetResult(){result.hidden=true;}
  objective.addEventListener('change',function(){
    need.replaceChildren(new Option('Selecione uma prioridade',''));
    Object.keys(choices[objective.value]||{}).forEach(function(key){need.add(new Option(choices[objective.value][key].label,key));});
    need.disabled=!objective.value;
    resetResult();
  });
  need.addEventListener('change',resetResult);
  start.addEventListener('change',resetResult);
  form.addEventListener('submit',function(event){
    event.preventDefault();
    var recommendation=recommend(objective.value,need.value,start.value);
    if(!recommendation || !form.reportValidity()) return;
    document.getElementById('service-selector-title').textContent=recommendation.title;
    document.getElementById('service-selector-note').textContent=recommendation.note;
    var link=document.getElementById('service-selector-link');
    link.textContent=recommendation.cta;link.href=recommendation.href;
    result.hidden=false;result.focus();
  });
})(typeof window!=='undefined'?window:this);
