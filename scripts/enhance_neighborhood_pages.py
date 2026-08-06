from pathlib import Path

neighborhood_data = {
    'santos': {
        'gonzaga': {
            'title': 'Imóveis em Gonzaga — Santos',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Gonzaga, Santos. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Gonzaga combina orla ativa, comércio forte e valorização histórica. É referência de liquidez em Santos, com apartamentos vista mar e edifícios consolidados.',
            'valuation': 'Valorização média do m² em alta; temporada forte e procura por moradia o ano todo. Perfil de comprador que valoriza serviços, acesso e renda por locação.',
            'risks': 'Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Em orla, atenção a marinas e restrições ambientais.'
        },
        'embare': {
            'title': 'Imóveis em Embaré — Santos',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Embaré, Santos. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Embaré é um bairro tradicional de Santos, com ruas arborizadas e boa oferta de imóveis familiares. Próximo à orla e com fácil acesso ao centro.',
            'valuation': 'Valorização estável com boa liquidez. Perfil de moradia familiar e procura consistente por temporada.',
            'risks': 'Verificar documentação regular, IPTU em dia e eventuais restrições de zoneamento. Atenção a imóveis em áreas de mangue.'
        },
        'boqueirao': {
            'title': 'Imóveis em Boqueirão — Santos',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Boqueirão, Santos. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Boqueirão combina residencial e comercial, com proximidade à orla e ao centro de Santos. Oferta diversificada de apartamentos e casas.',
            'valuation': 'Valorização consistente com demanda por moradia permanente e temporada. Boa conectividade e serviços locais.',
            'risks': 'Checar regularidade de construções, área de marinha e ônus. Em zonas comerciais, verificar uso permitido.'
        }
    },
    'guaruja': {
        'pitangueiras': {
            'title': 'Imóveis em Pitangueiras — Guarujá',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Pitangueiras, Guarujá. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Pitangueiras é conhecido por vista mar, comércio e vida social, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.',
            'valuation': 'Alta temporada e valorização consistente. Perfil de comprador que busca lazer e renda por temporada.',
            'risks': 'Atenção a condomínios e regulamentações de orla. Verificar área de marinha e restrições ambientais.'
        },
        'asturias': {
            'title': 'Imóveis em Astúrias — Guarujá',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Astúrias, Guarujá. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Astúrias oferece equilíbrio entre residencial e turismo, com orla charmosa e estrutura de serviços completa.',
            'valuation': 'Valorização média-alta com procura por segunda residência. Temporada forte e ocupação elevada.',
            'risks': 'Verificar regularidade de construções, IPTU e taxas de condomínio. Atenção a restrições de orla.'
        },
        'enseada': {
            'title': 'Imóveis em Enseada — Guarujá',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Enseada, Guarujá. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Enseada é conhecida por mar calmo, família e temporada, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.',
            'valuation': 'Valorização crescente com demanda por moradia familiar e temporada. Oferta diversificada de casas e apartamentos.',
            'risks': 'Checar documentação, área de marinha e regulamentações de orla. Verificar infraestrutura de acesso.'
        }
    },
    'praia-grande': {
        'guilhermina': {
            'title': 'Imóveis em Guilhermina — Praia Grande',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Guilhermina, Praia Grande. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Guilhermina é conhecido por passeio, famílias e temporada, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.',
            'valuation': 'Valorização média do m², taxa de ocupação na temporada e perfil do comprador em Praia Grande.',
            'risks': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação e infraestrutura.'
        },
        'ocian': {
            'title': 'Imóveis em Ocian — Praia Grande',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Ocian, Praia Grande. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Ocian combina orla e estrutura urbana, com boa oferta de apartamentos e casas. Próximo ao centro e com serviços variados.',
            'valuation': 'Valorização crescente com procura por moradia permanente e temporada. Boa conectividade com São Paulo.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento. Atenção a áreas de mangue.'
        },
        'tupi': {
            'title': 'Imóveis em Tupi — Praia Grande',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Tupi, Praia Grande. Valorização, acessos, documentação e particularidades do bairro.',
            'about': 'Tupi é referência de orla, famílias e temporada, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.',
            'valuation': 'Valorização média-alta com temporada forte. Perfil de comprador que valoriza lazer e renda por locação.',
            'risks': 'Checar área de marinha, ônus e regulamentações de orla. Verificar infraestrutura de acesso.'
        }
    },
    'bertioga': {
        'centro': {
            'title': 'Imóveis no Centro — Bertioga',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Bertioga. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Bertioga combina serviços, comércio e acesso à orla. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização crescente com demanda por moradia permanente e temporada. Acesso facilitado por estrada.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento. Atenção a áreas de mangue.'
        },
        'riviera': {
            'title': 'Imóveis na Riviera — Bertioga',
            'description': 'Guia completo para comprar, vender e investir em imóveis na Riviera de Bertioga. Valorização, acessos, documentação e particularidades.',
            'about': 'Riviera de Bertioga é um dos bairros mais valorizados do Litoral Norte, com condomínios de alto padrão e acesso direto à praia.',
            'valuation': 'Valorização alta com procura por segunda residência de alto padrão. Temporada forte e ocupação elevada.',
            'risks': 'Verificar regulamentações de condomínio, área de marinha e ônus. Atenção a restrições ambientais.'
        },
        'guaratuba': {
            'title': 'Imóveis em Guaratuba — Bertioga',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Guaratuba, Bertioga. Valorização, acessos, documentação e particularidades.',
            'about': 'Guaratuba oferece natureza preservada e tranquilidade, com oferta de casas e apartamentos em áreas verdes.',
            'valuation': 'Valorização gradual com demanda crescente por segunda residência. Ambiente tranquilo e exclusivo.',
            'risks': 'Checar documentação, IPTU e eventuais restrições de construção. Verificar acesso e infraestrutura.'
        }
    },
    'itanhaem': {
        'centro': {
            'title': 'Imóveis no Centro — Itanhaém',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Itanhaém. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Itanhaém combina história, serviços e acesso à orla. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização crescente com demanda por moradia acessível. Boa relação custo-benefício no Litoral Sul.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'cibratel': {
            'title': 'Imóveis no Cibratel — Itanhaém',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Cibratel, Itanhaém. Valorização, acessos, documentação e particularidades.',
            'about': 'Cibratel é conhecido por tranquilidade, famílias e temporada, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.',
            'valuation': 'Valorização média com procura por segunda residência. Ambiente familiar e seguro.',
            'risks': 'Checar documentação, IPTU e infraestrutura de acesso.'
        },
        'jardim-sao-fernando': {
            'title': 'Imóveis no Jardim São Fernando — Itanhaém',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Jardim São Fernando, Itanhaém. Valorização, acessos, documentação e particularidades.',
            'about': 'Jardim São Fernando oferece imóveis acessíveis em área tranquila, com boa oferta para primeira moradia no litoral.',
            'valuation': 'Valorização gradual com demanda crescente. Boa relação custo-benefício.',
            'risks': 'Verificar documentação, IPTU e infraestrutura local.'
        }
    },
    'mongagua': {
        'centro': {
            'title': 'Imóveis no Centro — Mongaguá',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Mongaguá. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Mongaguá oferece serviços, comércio e acesso à orla. Oferta diversificada de imóveis acessíveis.',
            'valuation': 'Valorização crescente com demanda por moradia permanente. Ambiente tranquilo e infraestrutura em expansão.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'jardim-sao-paulo': {
            'title': 'Imóveis no Jardim São Paulo — Mongaguá',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Jardim São Paulo, Mongaguá. Valorização, acessos, documentação e particularidades.',
            'about': 'Jardim São Paulo é um bairro tranquilo de Mongaguá, com oferta de imóveis acessíveis e ambiente familiar.',
            'valuation': 'Valorização gradual com demanda crescente. Boa opção para primeira moradia.',
            'risks': 'Checar documentação, IPTU e infraestrutura local.'
        },
        'balneario': {
            'title': 'Imóveis no Balneário — Mongaguá',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Balneário de Mongaguá. Valorização, acessos, documentação e particularidades.',
            'about': 'Balneário de Mongaguá combina orla e tranquilidade, com oferta de imóveis para temporada e moradia.',
            'valuation': 'Valorização crescente com temporada relevante. Procura por segunda residência.',
            'risks': 'Verificar área de marinha, regulamentações de orla e documentação.'
        }
    },
    'sao-vicente': {
        'centro': {
            'title': 'Imóveis no Centro — São Vicente',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de São Vicente. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de São Vicente é o coração da cidade, com história, serviços e acesso à orla. Oferta diversificada de imóveis.',
            'valuation': 'Valorização estável com demanda por moradia permanente e temporada. Infraestrutura consolidada.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'gonzaguinha': {
            'title': 'Imóveis em Gonzaguinha — São Vicente',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Gonzaguinha, São Vicente. Valorização, acessos, documentação e particularidades.',
            'about': 'Gonzaguinha é um bairro tradicional de São Vicente, com acesso à orla e serviços variados.',
            'valuation': 'Valorização consistente com procura por moradia familiar. Boa oferta de imóveis.',
            'risks': 'Checar documentação, IPTU e infraestrutura de acesso.'
        },
        'itarare': {
            'title': 'Imóveis em Itararé — São Vicente',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Itararé, São Vicente. Valorização, acessos, documentação e particularidades.',
            'about': 'Itararé combina orla e área residencial, com oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização média com temporada relevante. Perfil de comprador que valoriza lazer e serviços.',
            'risks': 'Verificar área de marinha, regulamentações de orla e documentação.'
        }
    },
    'peruibe': {
        'centro': {
            'title': 'Imóveis no Centro — Peruíbe',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Peruíbe. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Peruíbe oferece serviços, comércio e acesso à orla. Oferta diversificada de imóveis acessíveis.',
            'valuation': 'Valorização gradual com demanda crescente. Ambiente tranquilo e natureza preservada.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'jardim-sao-paulo': {
            'title': 'Imóveis no Jardim São Paulo — Peruíbe',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Jardim São Paulo, Peruíbe. Valorização, acessos, documentação e particularidades.',
            'about': 'Jardim São Paulo é um bairro tranquilo de Peruíbe, com oferta de imóveis acessíveis e ambiente familiar.',
            'valuation': 'Valorização gradual com demanda crescente. Boa opção para primeira moradia.',
            'risks': 'Checar documentação, IPTU e infraestrutura local.'
        },
        'balneario': {
            'title': 'Imóveis no Balneário — Peruíbe',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Balneário de Peruíbe. Valorização, acessos, documentação e particularidades.',
            'about': 'Balneário de Peruíbe combina orla e tranquilidade, com oferta de imóveis para temporada e moradia.',
            'valuation': 'Valorização gradual com temporada relevante. Procura por segunda residência.',
            'risks': 'Verificar área de marinha, regulamentações de orla e documentação.'
        }
    },
    'caraguatatuba': {
        'centro': {
            'title': 'Imóveis no Centro — Caraguatatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Caraguatatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Caraguatatuba oferece serviços, comércio e acesso à orla. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização consistente com temporada forte. Perfil de comprador que valoriza acesso e serviços.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'jaguaribe': {
            'title': 'Imóveis em Jaguaribe — Caraguatatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Jaguaribe, Caraguatatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'Jaguaribe é conhecido por temporada e lazer, com oferta diversificada de imóveis e acesso à praia.',
            'valuation': 'Valorização média-alta com temporada forte. Procura por segunda residência.',
            'risks': 'Checar área de marinha, regulamentações de orla e documentação.'
        },
        'prainha': {
            'title': 'Imóveis na Prainha — Caraguatatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis na Prainha, Caraguatatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'Prainha é um bairro familiar de Caraguatatuba, com oferta de imóveis acessíveis e ambiente tranquilo.',
            'valuation': 'Valorização gradual com demanda crescente. Boa opção para primeira moradia.',
            'risks': 'Verificar documentação, IPTU e infraestrutura local.'
        }
    },
    'ilhabela': {
        'centro': {
            'title': 'Imóveis no Centro — Ilhabela',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Ilhabela. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Ilhabela é o coração da ilha, com serviços, comércio e acesso às praias. Oferta diversificada de imóveis.',
            'valuation': 'Valorização alta com procura por segunda residência. Temporada forte e ocupação elevada.',
            'risks': 'Verificar regulamentações de orla, área de marinha e documentação. Atenção a restrições ambientais.'
        },
        'vila': {
            'title': 'Imóveis na Vila — Ilhabela',
            'description': 'Guia completo para comprar, vender e investir em imóveis na Vila de Ilhabela. Valorização, acessos, documentação e particularidades.',
            'about': 'Vila de Ilhabela oferece serviços, comércio e acesso às praias. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização alta com demanda por segunda residência. Perfil exclusivo e natureza preservada.',
            'risks': 'Checar regulamentações de orla, área de marinha e documentação.'
        },
        'pernambuco': {
            'title': 'Imóveis em Pernambuco — Ilhabela',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Pernambuco, Ilhabela. Valorização, acessos, documentação e particularidades.',
            'about': 'Pernambuco é uma das praias mais famosas de Ilhabela, com oferta de imóveis de alto padrão e temporada forte.',
            'valuation': 'Valorização alta com temporada consolidada. Procura por segunda residência de luxo.',
            'risks': 'Verificar área de marinha, regulamentações de orla e documentação. Atenção a restrições ambientais.'
        },
        'bonete': {
            'title': 'Imóveis em Bonete — Ilhabela',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Bonete, Ilhabela. Valorização, acessos, documentação e particularidades.',
            'about': 'Bonete é uma das praias mais exclusivas de Ilhabela, com oferta limitada de imóveis e natureza preservada.',
            'valuation': 'Valorização muito alta com oferta limitada. Perfil exclusivo e temporada forte.',
            'risks': 'Checar regulamentações de orla, área de marinha e documentação. Verificar acesso e infraestrutura.'
        }
    },
    'sao-sebastiao': {
        'centro-historico': {
            'title': 'Imóveis no Centro Histórico — São Sebastião',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro Histórico de São Sebastião. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro Histórico de São Sebastião combina história, cultura e serviços. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização média-alta com demanda por moradia permanente e temporada. Infraestrutura consolidada.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'juquehy': {
            'title': 'Imóveis em Juquehy — São Sebastião',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Juquehy, São Sebastião. Valorização, acessos, documentação e particularidades.',
            'about': 'Juquehy é uma das praias mais procuradas do Litoral Norte, com oferta de imóveis de alto padrão e temporada forte.',
            'valuation': 'Valorização alta com temporada consolidada. Procura por segunda residência de luxo.',
            'risks': 'Verificar área de marinha, regulamentações de orla e documentação. Atenção a restrições ambientais.'
        },
        'maresias': {
            'title': 'Imóveis em Maresias — São Sebastião',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Maresias, São Sebastião. Valorização, acessos, documentação e particularidades.',
            'about': 'Maresias é referência de surf, juventude e temporada, com oferta de imóveis para moradia e lazer.',
            'valuation': 'Valorização média-alta com temporada forte. Perfil de comprador jovem e internacional.',
            'risks': 'Checar regulamentações de orla, área de marinha e documentação. Verificar infraestrutura de acesso.'
        }
    },
    'ubatuba': {
        'centro': {
            'title': 'Imóveis no Centro — Ubatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis no Centro de Ubatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'Centro de Ubatuba oferece serviços, comércio e acesso às praias. Oferta diversificada de imóveis para moradia e temporada.',
            'valuation': 'Valorização média com temporada relevante. Perfil de comprador que valoriza natureza e lazer.',
            'risks': 'Verificar documentação, IPTU e eventuais restrições de zoneamento.'
        },
        'itagua': {
            'title': 'Imóveis em Itagua — Ubatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis em Itagua, Ubatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'Itagua é um bairro de Ubatuba com oferta diversificada de imóveis, próximo às praias e com estrutura de serviços.',
            'valuation': 'Valorização gradual com demanda crescente. Boa opção para moradia e temporada.',
            'risks': 'Checar documentação, IPTU e infraestrutura local.'
        },
        'sao-lourenco': {
            'title': 'Imóveis em São Lourenço — Ubatuba',
            'description': 'Guia completo para comprar, vender e investir em imóveis em São Lourenço, Ubatuba. Valorização, acessos, documentação e particularidades.',
            'about': 'São Lourenço é um bairro tranquilo de Ubatuba, com oferta de imóveis acessíveis e proximidade com a natureza.',
            'valuation': 'Valorização gradual com demanda crescente. Ambiente residencial e tranquilo.',
            'risks': 'Verificar documentação, IPTU e infraestrutura local.'
        }
    }
}

img_map = {
    'santos': 'img/santos-apartamento-vista-mar.webp',
    'guaruja': 'img/gua-casa-duplex.webp',
    'praia-grande': 'img/pg-studio-moderno.webp',
    'bertioga': 'img/berta-alto-padrao.webp',
    'itanhaem': 'img/it-casa-terrea.webp',
    'mongagua': 'img/mon-ap-compacto.webp',
    'sao-vicente': 'img/sv-cobertura-duplex.webp',
    'peruibe': 'img/per-sobrado.webp',
    'caraguatatuba': 'img/default-home.jpg',
    'ilhabela': 'img/default-home.jpg',
    'sao-sebastiao': 'img/default-home.jpg',
    'ubatuba': 'img/default-home.jpg',
}

base = Path('bairros')
for city_dir in sorted(base.iterdir()):
    if not city_dir.is_dir() or city_dir.name in ('index.html',):
        continue
    city = city_dir.name
    img = img_map.get(city, 'img/default-home.jpg')
    
    for p in sorted(city_dir.glob('*.html')):
        if p.name == 'index.html':
            continue
        neighborhood = p.stem
        data = neighborhood_data.get(city, {}).get(neighborhood)
        if not data:
            print(f'skip {p}: no data')
            continue
        
        txt = p.read_text(encoding='utf-8', errors='ignore')
        
        # Update title and meta
        txt = txt.replace(f'<title>Imóveis em {neighborhood.replace("-", " ").title()} — {city.replace("-", " ").title()} | Praia Digital</title>',
                         f'<title>{data["title"]} | Praia Digital</title>')
        txt = txt.replace(f'<meta name="description" content="Guia completo para comprar, vender e investir em imóveis em {neighborhood.replace("-", " ").title()}, {city.replace("-", " ").title()}. Valorização, acessos, documentação e particularidades do bairro.">',
                         f'<meta name="description" content="{data["description"]}">')
        txt = txt.replace(f'<meta property="og:title" content="Imóveis em {neighborhood.replace("-", " ").title()} — {city.replace("-", " ").title()}">',
                         f'<meta property="og:title" content="{data["title"]}">')
        txt = txt.replace(f'<meta property="og:description" content="Guia completo para comprar, vender e investir em imóveis em {neighborhood.replace("-", " ").title()}, {city.replace("-", " ").title()}.">',
                         f'<meta property="og:description" content="{data["description"]}">')
        
        # Update cards content
        txt = txt.replace('<h3>Sobre o bairro</h3>', '<h3>Sobre o bairro</h3>')
        txt = txt.replace('<h3>Valorização e mercado</h3>', '<h3>Valorização e mercado</h3>')
        txt = txt.replace('<h3>Documentação e riscos</h3>', '<h3>Documentação e riscos</h3>')
        
        # Find and replace card contents
        import re
        txt = re.sub(r'<p>Gonzaga combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Pitangueiras é conhecido.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Guilhermina é conhecido.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Bertioga combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Riviera de Bertioga é um dos bairros.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Guaratuba oferece natureza.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Itanhaém combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Cibratel é conhecido.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Jardim São Fernando oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Mongaguá oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Jardim São Paulo é um bairro tranquilo.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Balneário de Mongaguá combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de São Vicente é o coração.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Gonzaguinha é um bairro tradicional.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Itararé combina orla.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Peruíbe oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Jardim São Paulo é um bairro tranquilo.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Balneário de Peruíbe combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Caraguatatuba oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Jaguaribe é conhecido.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Prainha é um bairro familiar.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Ilhabela é o coração.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Vila de Ilhabela oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Pernambuco é uma das praias.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Bonete é uma das praias.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro Histórico de São Sebastião combina.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Juquehy é uma das praias.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Maresias é referência de surf.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Centro de Ubatuba oferece.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>Itagua é um bairro de Ubatuba.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        txt = re.sub(r'<p>São Lourenço é um bairro tranquilo.*?</p>', f'<p>{data["about"]}</p>', txt, count=1, flags=re.DOTALL)
        
        # Update valuation and risks cards
        txt = txt.replace('<p>Valorização média do m² em alta; temporada forte e procura por moradia o ano todo. Perfil de comprador que valoriza serviços, acesso e renda por locação.</p>',
                         f'<p>{data["valuation"]}</p>')
        txt = txt.replace('<p>Valorização média do m², taxa de ocupação na temporada e perfil do comprador em Guaruja.</p>',
                         f'<p>{data["valuation"]}</p>')
        txt = txt.replace('<p>Valorização média do m², taxa de ocupação na temporada e perfil do comprador em Praia Grande.</p>',
                         f'<p>{data["valuation"]}</p>')
        txt = txt.replace('<p>Valorização média do m², taxa de ocupação na temporada e perfil do comprador em Praia Grande.</p>',
                         f'<p>{data["valuation"]}</p>')
        
        txt = txt.replace('<p>Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Em orla, atenção a marinas e restrições ambientais.</p>',
                         f'<p>{data["risks"]}</p>')
        txt = txt.replace('<p>Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Atenção a condomínios e regulamentações de orla.</p>',
                         f'<p>{data["risks"]}</p>')
        txt = txt.replace('<p>Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação e infraestrutura.</p>',
                         f'<p>{data["risks"]}</p>')
        
        # Add image if not present
        if img not in txt:
            img_html = f'<img src="https://praia.digital/{img}" alt="{neighborhood}" style="max-width:100%;border-radius:12px;margin-top:18px;">'
            txt = txt.replace('</div>\n\n      <a class="cta"', f'{img_html}\n\n      <a class="cta"')
        
        # Update OG image
        txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')
        
        p.write_text(txt, encoding='utf-8')
        print(f'updated {p}')
    
    # Update city index
    idx = city_dir / 'index.html'
    if idx.exists():
        txt = idx.read_text(encoding='utf-8', errors='ignore')
        if img not in txt:
            marker = '<div class="highlight">'
            img_html = f'<img src="https://praia.digital/{img}" alt="{city}" style="max-width:100%;border-radius:12px;margin-top:18px;">\n\n      <div class="highlight">'
            txt = txt.replace(marker, img_html, 1)
            txt = txt.replace('content="https://praia.digital/img/default-home.jpg"', f'content="https://praia.digital/{img}"')
            idx.write_text(txt, encoding='utf-8')
            print(f'updated {idx}')

print('done')
