(function(){
  var STORAGE_KEY = 'praia_digital_assistant_opened';
  var opened = false;
  try { opened = sessionStorage.getItem(STORAGE_KEY) === '1'; } catch(e){}

  function getAssistant(){
    return document.getElementById('assistantModal');
  }

  function openAssistant(){
    var a = getAssistant();
    if(!a || a.dataset.open === '1') return;
    a.setAttribute('aria-hidden', 'false');
    a.classList.add('is-open');
    a.dataset.open = '1';
    try { sessionStorage.setItem(STORAGE_KEY, '1'); } catch(e){}
  }

  function closeAssistant(){
    var a = getAssistant();
    if(!a) return;
    a.setAttribute('aria-hidden', 'true');
    a.classList.remove('is-open');
    a.dataset.open = '0';
  }

  function addMessage(text, sender){
    var messages = document.getElementById('assistantMessages');
    if(!messages) return;
    var msg = document.createElement('div');
    msg.className = 'assistant-message ' + (sender || 'bot');
    msg.textContent = text;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }

  function getContext(){
    var path = location.pathname.replace(/\/$/, '') || '/index.html';
    if(path.includes('guia-dos-modulos')) return 'modules';
    if(path.includes('rentabilidade')) return 'rentability';
    if(path.includes('top-10-acessorios')) return 'beach-accessories';
    if(path.includes('guia-churrasco')) return 'gourmet-bbq';
    if(path.includes('guia-pet-friendly')) return 'pet-friendly';
    if(path.includes('guia-sushi')) return 'sushi-japanese';
    if(path.includes('guia-supermercados')) return 'supermarkets';
    if(path.includes('guia-decoracao')) return 'decoration-maintenance';
    if(path.includes('guia-festas')) return 'events-catering';
    if(path.includes('guia-home-office')) return('home-office');
    if(path.includes('guia-saude')) return 'health-spa';
    if(path.includes('como-comprar-investir')) return 'buy-invest';
    if(path.includes('links')) return 'links';
    if(path.includes('enxoval-automacao')) return 'enxoval';
    return 'general';
  }

  function getAnswers(){
    return {
      modules: {
        title: 'Guia dos Módulos da Riviera',
        answers: {
          'qual modulo': 'Os módulos com vista mar e proximidade ao golf costumam se valorizar mais. Quer comparar opções? Veja o Simulador de Rentabilidade.',
          'pet friendly': 'Muitos módulos aceitam pets, mas com regras específicas. Consulte o regulamento do condomínio antes de fechar.',
          'golf': 'O Riviera Golf Club tem campo par 3 e aulas com profissionais. Veja também o Guia de Golfe.',
          'compra': 'Para compra, comece pelo Guia de Compra e Investimento e cadastre seu interesse no Wizard.'
        }
      },
      rentability: {
        title: 'Simulador de Rentabilidade',
        answers: {
          'ocupacao': 'Na alta temporada, imóveis bem localizados podem atingir mais de 70% de ocupação.',
          'preco': 'Preços variam por módulo, tamanho e padrão. Use o simulador e confira o Guia de Compra e Investimento.',
          'gestao': 'Gestão profissional costuma ter melhor resultado em imóveis de alto padrão.'
        }
      },
      'beach-accessories': {
        title: 'Top 10 Acessórios de Praia',
        answers: {
          'cadeira': 'Cadeiras de alumínio são leves e resistentes à maresia. Confira as opções na Amazon.',
          'cooler': 'Coolers térmicos mantêm bebidas geladas por horas. Ideal para praia e piscina.',
          'comprar': 'Você pode comprar diretamente nos cards deste guia ou ver mais itens na Central de Automação e Enxoval.'
        }
      },
      'gourmet-bbq': {
        title: 'Guia de Churrasco e Área Gourmet',
        answers: {
          'grelha': 'Grelhas em inox e churrasqueiras portáteis são as mais recomendadas.',
          'adega': 'Adegas térmicas preservam vinhos e espumantes na temperatura ideal.',
          'facas': 'Facas artesanais oferecem precisão e durabilidade para área gourmet.'
        }
      },
      'pet-friendly': {
        title: 'Guia Pet Friendly',
        answers: {
          'praia': 'Leve sempre água, coleira e protetor solar para pets.',
          'restaurante': 'Alguns restaurantes aceitam pets na área externa.',
          'veterinario': 'Existem clínicas 24h na região; consulte a lista do guia.'
        }
      },
      'sushi-japanese': {
        title: 'Guia de Gastronomia Japonesa',
        answers: {
          'sushiman': 'Sushiman privativo oferece menu personalizado e experiência exclusiva.',
          'delivery': 'Delivery premium entrega pokes e temakis com embalagens térmicas.',
          'harmonizacao': 'Saquês gelados e vinhos brancos leves combinam com pratos orientais.'
        }
      },
      'supermarkets': {
        title: 'Guia de Supermercados e Empórios',
        answers: {
          'pao-de-acucar': 'O Pão de Açúcar Riviera tem opções completas para a casa de praia.',
          'empório': 'Empórios no Riviera Shopping oferecem vinhos, frios e itens gourmet.',
          'hortifruti': 'Hortifrútis da Enseada têm frutas e pescados frescos.'
        }
      },
      'decoration-maintenance': {
        title: 'Guia de Decoração e Manutenção',
        answers: {
          'maresia': 'Prefira alumínio anodizado, inox 316 e madeira tratada.',
          'iluminacao': 'Refletores solares LED com sensor crepuscular são ideais.',
          'piscina': 'Robôs limpadores reduzem custos de manutenção.'
        }
      },
      'events-catering': {
        title: 'Guia de Festas e Eventos',
        answers: {
          'buffet': 'Buffets renomados entregam menu personalizado e equipe completa.',
          'sonorizacao': 'Sonorização direcionada respeita as normas da Riviera.',
          'espaco': 'O Riviera Shopping tem espaços para recepções e lounges.'
        }
      },
      'home-office': {
        title: 'Guia de Home Office e Conectividade',
        answers: {
          'starlink': 'Starlink é uma opção robusta onde a fibra não alcança.',
          'coworking': 'Coworkings no Módulo 2 oferecem Wi-Fi rápido e ambiente profissional.',
          'protecao': 'No-breaks senoidais e filtros de linha protegem equipamentos.'
        }
      },
      'health-spa': {
        title: 'Guia de Saúde e Spa',
        answers: {
          'spa': 'Spas privativos oferecem protocolos antiestresse e hidromassagem.',
          'massoterapia': 'Profissionais atendem mansões com massagem e estética.',
          'academia': 'Academias de alto padrão ficam próximas ao golf e ao Módulo 2.'
        }
      },
      'buy-invest': {
        title: 'Guia de Compra e Investimento',
        answers: {
          'valorizacao': 'Módulos com vista mar e proximidade ao golf tendem a valorizar mais.',
          'financiamento': 'Compare SBPE, Minha Casa Minha Vida e financiamento próprio.',
          'aluguel': 'Alta temporada pode atingir mais de 70% de ocupação em imóveis bem localizados.'
        }
      },
      'links': {
        title: 'Central de Links',
        answers: {
          'links': 'Aqui você encontra os guias e ferramentas mais úteis do portal.',
          'wizard': 'Use o Wizard para cadastrar seu imóvel para temporada.',
          'whatsapp': 'Para atendimento VIP, use os botões de serviços pagos do site.'
        }
      },
      'enxoval': {
        title: 'Guia de Automação e Enxoval',
        answers: {
          'fechadura': 'Fechaduras digitais oferecem acesso inteligente e histórico.',
          'robot': 'Robôs aspiradores mantêm o imóvel limpo com programação.',
          'comprar': 'Compre diretamente nos cards com link para a Amazon.'
        }
      }
    };
  }

  function getBotReply(question){
    var ctx = getContext();
    var answers = getAnswers();
    var group = answers[ctx] || answers['general'];
    var lower = question.toLowerCase();
    for(var key in group.answers){
      if(lower.includes(key)){
        return group.answers[key];
      }
    }
    return 'Posso ajudar com informações sobre ' + group.title + '. O que você quer saber?';
  }

  function bindEvents(){
    var a = getAssistant();
    if(!a) return;

    a.addEventListener('click', function(e){
      if(e.target.classList.contains('assistant-modal-backdrop') || e.target.classList.contains('assistant-modal-close')){
        closeAssistant();
      }
    });

    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && a.dataset.open === '1') closeAssistant();
    });

    var form = document.getElementById('assistantForm');
    if(form){
      form.addEventListener('submit', function(e){
        e.preventDefault();
        var input = document.getElementById('assistantInput');
        var question = (input && input.value || '').trim();
        if(!question) return;
        addMessage(question, 'user');
        var reply = getBotReply(question);
        setTimeout(function(){ addMessage(reply, 'bot'); }, 400);
        if(input) input.value = '';
      });
    }

    setTimeout(function(){
      if(!opened){
        openAssistant();
        addMessage('Olá! Sou o assistente virtual do Praia Digital. Pergunte sobre guias, produtos ou serviços.', 'bot');
      }
    }, 1200);
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', bindEvents);
  } else {
    bindEvents();
  }
})();
