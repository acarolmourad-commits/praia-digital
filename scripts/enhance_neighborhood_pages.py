from pathlib import Path

city_neighborhoods = {
    'santos': {
        'gonzaga': {
            'name': 'Gonzaga',
            'about': 'Gonzaga combina orla ativa, comércio forte e valorização histórica. É referência de liquidez em Santos, com apartamentos vista mar e edifícios consolidados.',
            'market': 'Valorização média do m² em alta; temporada forte e procura por moradia o ano todo. Perfil de comprador que valoriza serviços, acesso e renda por locação.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Em orla, atenção a marinas e restrições ambientais.',
        },
        'embare': {
            'name': 'Embaré',
            'about': 'Embaré oferece perfil residencial tranquilo com acesso rápido ao centro e à orla. Oferta variada de apartamentos e casas para famílias.',
            'market': 'Valorização estável com liquidez crescente. Temporada relevante e procura por moradia permanente. Perfil de comprador que valoriza calmaria e serviços.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha próximas à orla.',
        },
        'boqueirao': {
            'name': 'Boqueirão',
            'about': 'Boqueirão combina temporada, famílias e diversidade de oferta. Próximo à orla, com comércio local e fluxo de segunda residência.',
            'market': 'Valorização acessível com liquidez sazonal. Temporada forte e procura por apartamentos compactos e casas. Perfil de comprador que valoriza custo-benefício.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de ocupação e distâncias de área de marinha.',
        },
    },
    'guaruja': {
        'pitangueiras': {
            'name': 'Pitangueiras',
            'about': 'Pitangueiras combina vista mar, comércio e vida social no Guarujá. Oferta madura de apartamentos e casas com acesso rápido à orla.',
            'market': 'Valorização média do m² com temporada consolidada. Perfil de comprador que valoriza vista mar, serviços e fluxo de caixa.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Atenção a condomínios e regulamentações de orla.',
        },
        'asturias': {
            'name': 'Astúrias',
            'about': 'Astúrias oferece oferta madura e proximidade da orla no Guarujá. Perfil residencial e de temporada com comércio local.',
            'market': 'Valorização estável com temporada relevante. Oferta de apartamentos e casas bem posicionados. Perfil de comprador que valoriza liquidez e acesso.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar condições de acesso e regularidade de área.',
        },
        'enseada': {
            'name': 'Enseada',
            'about': 'Enseada combina mercado amplo e fluxo de caixa no Guarujá. Oferta variada de apartamentos, casas e condomínios.',
            'market': 'Valorização competitiva com temporada consistente. Perfil de comprador que valoriza custo-benefício, espaço e proximidade da capital.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a condomínios fechados e infraestrutura local.',
        },
    },
    'praia-grande': {
        'guilhermina': {
            'name': 'Guilhermina',
            'about': 'Guilhermina combina temporada e comércio ativo em Praia Grande. Oferta variada de apartamentos e casas próximas à orla.',
            'market': 'Valorização acessível com liquidez crescente. Temporada forte e procura por entrada. Perfil de comprador que valoriza custo-benefício.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação e infraestrutura.',
        },
        'ocian': {
            'name': 'Ocian',
            'about': 'Ocian oferece entrada competitiva e liquidez em Praia Grande. Oferta ampla para famílias e investidores.',
            'market': 'Valorização em alta com temporada consolidada. Perfil de comprador que valoriza espaço, acesso e potencial de valorização.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de expansão e serviços públicos.',
        },
        'tupi': {
            'name': 'Tupi',
            'about': 'Tupi combina perfil familiar e oferta variada em Praia Grande. Próximo à orla, com comércio local e fluxo de segunda residência.',
            'market': 'Valorização estável com temporada relevante. Oferta de apartamentos e casas para diferentes perfis. Perfil de comprador que valoriza liquidez.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de ocupação e acesso.',
        },
    },
    'bertioga': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Bertioga oferece serviços, acesso e liquidez. Oferta diversificada entre apartamentos e casas para moradia e temporada.',
            'market': 'Valorização sustentada com temporada alta. Perfil de comprador que valoriza conveniência e acesso.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e regulamentações locais.',
        },
        'riviera': {
            'name': 'Riviera de São Lourenço',
            'about': 'Riviera combina alto padrão, golfe e temporada forte em Bertioga. Oferta exclusiva de casas e apartamentos em condomínios.',
            'market': 'Valorização alta com procura por alto padrão. Temporada consolidada e fluxo de segunda residência. Perfil de comprador que valoriza exclusividade.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus. Verificar regulamentação de condomínio e golfe.',
        },
        'guaratuba': {
            'name': 'Guaratuba',
            'about': 'Guaratuba oferece perfil familiar e praias arredadas em Bertioga. Oferta de casas e apartamentos com acesso rápido.',
            'market': 'Valorização crescente com temporada relevante. Oferta direcionada a famílias e quem busca privacidade.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar acesso e regularidade de área.',
        },
    },
    'itanhaem': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Itanhaém combina serviços, acesso e temporada. Oferta de apartamentos e casas para moradia e investimento.',
            'market': 'Valorização acessível com ocupação crescente. Perfil de comprador que valoriza custo-benefício e estabilidade.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar documentação e serviços públicos.',
        },
        'praia': {
            'name': 'Praia',
            'about': 'Praia de Itanhaém oferece temporada e vizinhança tranquila. Oferta variada de apartamentos e casas próximas ao mar.',
            'market': 'Valorização estável com temporada relevante. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'condominios': {
            'name': 'Condomínios',
            'about': 'Condomínios em Itanhaém oferecem perfil residencial com segurança e lazer. Oferta direcionada a famílias e investidores.',
            'market': 'Valorização consistente com temporada crescente. Perfil de comprador que valoriza estabilidade e serviços.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, convenção de condomínio e ônus. Verificar regulamentação interna.',
        },
    },
    'mongagua': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Mongaguá combina serviços, acesso e temporada. Oferta de apartamentos e casas para moradia e investimento.',
            'market': 'Valorização acessível com liquidez em alta. Perfil de comprador que valoriza custo-benefício e acesso.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação.',
        },
        'praia': {
            'name': 'Praia',
            'about': 'Praia de Mongaguá oferece temporada e lazer. Oferta variada de apartamentos e casas próximas ao mar.',
            'market': 'Valorização crescente com temporada relevante. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'condominios': {
            'name': 'Condomínios',
            'about': 'Condomínios em Mongaguá oferecem perfil familiar com segurança e lazer. Oferta direcionada a famílias e investidores.',
            'market': 'Valorização estável com temporada em alta. Perfil de comprador que valoriza calmaria e potencial.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, convenção de condomínio e ônus. Verificar regulamentação.',
        },
    },
    'sao-vicente': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de São Vicente combina acesso rápido e estrutura consolidada. Oferta variada de apartamentos e casas.',
            'market': 'Valorização competitiva com temporada forte. Perfil de comprador que valoriza liquidez e serviços.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação.',
        },
        'praia': {
            'name': 'Praia',
            'about': 'Praia de São Vicente oferece temporada e lazer. Oferta de apartamentos e casas próximas ao mar.',
            'market': 'Valorização em alta com temporada relevante. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'jardim': {
            'name': 'Jardim',
            'about': 'Jardim em São Vicente oferece perfil residencial e valorização. Oferta de casas e apartamentos em bairros internos.',
            'market': 'Valorização crescente com temporada consolidada. Perfil de comprador que valoriza estabilidade e serviços.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar acesso e infraestrutura.',
        },
    },
    'peruibe': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Peruíbe combina serviços e acesso. Oferta de apartamentos e casas para moradia e temporada.',
            'market': 'Valorização acessível com potencial de valorização. Perfil de comprador que valoriza custo-benefício e natureza.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação.',
        },
        'praia': {
            'name': 'Praia',
            'about': 'Praia de Peruíbe oferece temporada e lazer. Oferta variada de apartamentos e casas próximas ao mar.',
            'market': 'Valorização crescente com temporada relevante. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'condominios': {
            'name': 'Condomínios',
            'about': 'Condomínios em Peruíbe oferecem perfil residencial com segurança e lazer. Oferta direcionada a famílias e investidores.',
            'market': 'Valorização estável com temporada em alta. Perfil de comprador que valoriza experiência e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições, convenção de condomínio e ônus. Verificar regulamentação.',
        },
    },
    'caraguatatuba': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Caraguatatuba combina serviços, acesso e temporada. Oferta de apartamentos e casas para moradia e investimento.',
            'market': 'Valorização acessível com temporada forte. Perfil de comprador que valoriza liquidez e lazer.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação.',
        },
        'jaguaribe': {
            'name': 'Jaguaribe',
            'about': 'Jaguaribe oferece temporada e lazer em Caraguatatuba. Oferta variada de apartamentos e casas próximas à orla.',
            'market': 'Valorização crescente com temporada consolidada. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'prainha': {
            'name': 'Prainha',
            'about': 'Prainha combina perfil familiar e oferta variada em Caraguatatuba. Próximo à orla, com comércio local.',
            'market': 'Valorização estável com temporada relevante. Oferta de apartamentos e casas para diferentes perfis.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de ocupação e acesso.',
        },
    },
    'ilhabela': {
        'vila': {
            'name': 'Vila',
            'about': 'Vila de Ilhabela oferece serviços e acesso. Oferta de apartamentos e casas para moradia e temporada.',
            'market': 'Valorização alta com temporada forte. Perfil de comprador que valoriza conveniência e acesso.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regulamentação local.',
        },
        'pernambuco': {
            'name': 'Pernambuco',
            'about': 'Pernambuco combina temporada e natureza em Ilhabela. Oferta de casas e apartamentos com acesso à praia.',
            'market': 'Valorização crescente com temporada relevante. Perfil de comprador que valoriza lazer e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de preservação.',
        },
        'bonete': {
            'name': 'Bonete',
            'about': 'Bonete oferece exclusividade e mar preservado em Ilhabela. Oferta direcionada a perfis de alto padrão.',
            'market': 'Valorização alta com procura por exclusividade. Temporada consolidada e fluxo de segunda residência.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regulamentação de área preservada.',
        },
    },
    'sao-sebastiao': {
        'centro-historico': {
            'name': 'Centro Histórico',
            'about': 'Centro Histórico de São Sebastião combina história, acesso e serviços. Oferta de apartamentos e casas no coração da cidade.',
            'market': 'Valorização estável com temporada relevante. Perfil de comprador que valoriza cultura e conveniência.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de área histórica.',
        },
        'juquehy': {
            'name': 'Juquehy',
            'about': 'Juquehy oferece temporada e lazer de alto padrão em São Sebastião. Oferta de casas e apartamentos próximos à orla.',
            'market': 'Valorização alta com temporada forte. Perfil de comprador que valoriza exclusividade e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e condomínios.',
        },
        'maresias': {
            'name': 'Maresias',
            'about': 'Maresias combina temporada forte e perfil internacional em São Sebastião. Oferta de apartamentos e casas bem posicionados.',
            'market': 'Valorização crescente com temporada consolidada. Perfil de comprador que valoriza lazer e rentabilidade.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regulamentação de orla e acesso.',
        },
    },
    'ubatuba': {
        'centro': {
            'name': 'Centro',
            'about': 'Centro de Ubatuba combina acesso e temporada. Oferta de apartamentos e casas para moradia e investimento.',
            'market': 'Valorização acessível com temporada relevante. Perfil de comprador que valoriza natureza e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar regularidade de documentação.',
        },
        'itagua': {
            'name': 'Itaguá',
            'about': 'Itaguá oferece acesso e temporada em Ubatuba. Oferta variada de apartamentos e casas próximas à orla.',
            'market': 'Valorização crescente com temporada consolidada. Perfil de comprador que valoriza lazer e potencial.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Atenção a áreas de marinha e ocupação.',
        },
        'sao-lourenco': {
            'name': 'São Lourenço',
            'about': 'São Lourenço combina perfil residencial e lazer em Ubatuba. Oferta de casas e apartamentos em bairros tranquilos.',
            'market': 'Valorização estável com temporada relevante. Perfil de comprador que valoriza calmaria e retorno.',
            'docs': 'Checklist essencial: escritura, IPTU, débitos, restrições e ônus. Verificar acesso e regularidade.',
        },
    },
}

for city, neighborhoods in city_neighborhoods.items():
    for slug, data in neighborhoods.items():
        p = Path(f'bairros/{city}/{slug}.html')
        if not p.exists():
            continue
        txt = p.read_text(encoding='utf-8', errors='ignore')
        # replace generic cards with specific content
        old_about = '          <p>Gonzaga é conhecido por orla famosa, comércio e valorização, com acesso rodovias e transporte público e vista/alcance para orla e pontos turísticos.</p>'
        if old_about in txt:
            txt = txt.replace(old_about, f'          <p>{data["about"]}</p>')
        old_market = '          <p>Valorização média do m², taxa de ocupação na temporada e perfil do comprador em Santos.</p>'
        if old_market in txt:
            txt = txt.replace(old_market, f'          <p>{data["market"]}</p>')
        old_docs = '          <p>Checklist essencial: escritura, IPTU, débitos, restrições, área de marinha e ônus.</p>'
        if old_docs in txt:
            txt = txt.replace(old_docs, f'          <p>{data["docs"]}</p>')
        p.write_text(txt, encoding='utf-8')
        print(f'updated {p}')

print('done')
