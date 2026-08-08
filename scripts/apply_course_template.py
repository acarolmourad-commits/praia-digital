from pathlib import Path
import re

base = Path('C:/Users/Carolina/praia-digital')
courses_dir = base / 'education' / 'cursos'

# Template genérico por tipo de curso
TEMPLATES = {
    'airbnb': {
        'title': 'Airbnb do Zero no Litoral',
        'desc': 'Montar um Airbnb lucrativo do zero, com exemplos reais do litoral paulista.',
        'modules': [
            ('Fundamentos do Aluguel por Temporada', 'Entenda o mercado, regras, tributos e oportunidades no litoral.'),
            ('Preparação do Imóvel', 'Checklist, fotos, descrição e regras de estadia que atraem hóspedes.'),
            ('Cadastro nas Plataformas', 'Airbnb, Booking e outras: perfil, políticas, preços e disponibilidade.'),
            ('Gestão e Crescimento', 'Check-in, limpeza, avaliações, automação e escalada para mais imóveis.'),
        ]
    },
    'booking': {
        'title': 'Booking do Zero no Litoral',
        'desc': 'Usar o Booking como canal principal de reservas, com otimização e gestão profissional.',
        'modules': [
            ('Fundamentos do Booking', 'Como funciona o Booking, algoritmo, ranking e perfil do hóspede.'),
            ('Cadastro e Apresentação', 'Perfil completo, fotos, descrição e diferenciais que convertem.'),
            ('Preços e Disponibilidade', 'Tabelas, temporadas, preços dinâmicos e gestão de disponibilidade.'),
            ('Atendimento e Avaliações', 'Reservas, check-in, avaliações e fidelização no Booking.'),
        ]
    },
    'venda': {
        'title': 'Venda Rápida de Imóveis no Litoral',
        'desc': 'Vender imóveis mais rápido com diagnóstico, apresentação profissional e negociação.',
        'modules': [
            ('Mercado e Diagnóstico', 'Por que alguns imóveis vendem rápido e outros não? Diagnóstico local.'),
            ('Preparação e Apresentação', 'Fotos, descrição, divulgação e atração de compradores qualificados.'),
            ('Negociação e Fechamento', 'Ofertas, contrapropostas, documentação e segurança jurídica.'),
            ('Pós-venda e Indicação', 'Relacionamento, pós-venda e sistema de indicações.'),
        ]
    },
    'locacao': {
        'title': 'Gestão Profissional de Locação no Litoral',
        'desc': 'Operar imóveis alugados com profissionalismo, reduzir conflitos e aumentar receita.',
        'modules': [
            ('Fundamentos da Locação', 'Mercado de locação no litoral, tipos de contrato e oportunidades.'),
            ('Operação do Imóvel', 'Limpeza, manutenção, equipes, fornecedores e rotina.'),
            ('Atendimento e Satisfação', 'Relacionamento com inquilinos, conflitos e renovação.'),
            ('Escala e Profissionalização', 'Mais imóveis, processos, indicadores e crescimento.'),
        ]
    },
    'analise': {
        'title': 'Análise de Mercado Imobiliário no Litoral',
        'desc': 'Interpretar dados, comparativos e tendências para tomar decisões de investimento.',
        'modules': [
            ('Mercado e Dinâmica Local', 'Cidades, bairros, acesso, sazonalidade e valorização.'),
            ('Métricas e Comparativos', 'Preço/m², rentabilidade, oferta/demanda e benchmarks.'),
            ('Investimento na Prática', 'Escolha de imóvel, reforma, precificação e revenda.'),
            ('Cenários e Decisão', 'Análise de cenários, riscos e planejamento de entrada/saída.'),
        ]
    },
    'rentabilidade': {
        'title': 'Análise de Rentabilidade no Litoral',
        'desc': 'Calcular ROI, fluxo de caixa e indicadores para investir com segurança.',
        'modules': [
            ('Fundamentos da Rentabilidade', 'Tipos de retorno, custos ocultos e expectativas realistas.'),
            ('Indicadores e Comparativos', 'ROI, cap rate, payback, comparáveis e simulações.'),
            ('Maximização de Receita', 'Temporada, preço, ocupação e redução de custos.'),
            ('Decisão e Acompanhamento', 'Decisão de investimento, monitoramento e saída.'),
        ]
    },
}

def guess_template(slug: str):
    s = slug.lower()
    if 'airbnb' in s or 'temporada' in s:
        return 'airbnb'
    if 'booking' in s:
        return 'booking'
    if 'venda' in s or 'vender' in s or 'fechamento' in s or 'corretor' in s:
        return 'venda'
    if 'locacao' in s or 'gestao' in s or 'gestão' in s or 'imovel' in s:
        return 'locacao'
    if 'analise' in s or 'mercado' in s:
        return 'analise'
    if 'rentabilidade' in s or 'invest' in s or 'roi' in s:
        return 'rentabilidade'
    return 'venda'

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def generate_course_content(course_path: Path, template_key: str):
    tpl = TEMPLATES[template_key]
    course_name = course_path.name
    
    # curso-completo dir
    completo = course_path / 'curso-completo'
    completo.mkdir(parents=True, exist_ok=True)
    
    # MANIFESTO
    manifesto = completo / 'MANIFESTO_DO_CURSO.md'
    manifesto.write_text(f"""# {tpl['title']} — {course_name.replace('-', ' ').title()}

## Visão geral
{tpl['desc']}

## Para quem é
- Para quem quer atuar no mercado imobiliário do litoral paulista.
- Para iniciantes e profissionais que querem atualizar processos.
- Para corretores, investidores, proprietários e gestores.

## O que você vai aprender
{chr(10).join([f'- {m[0]}' for m in tpl['modules']])}

## Formato
- Conteúdo direto ao ponto, aplicável na prática.
- Exemplos reais do litoral (Santos, Guarujá, Praia Grande, Bertioga, Itanhaém, Mongaguá, São Vicente, Peruíbe).
- Exercícios, checklists e modelos prontos.

## Entregáveis
- Conclusão de cada módulo com aplicação prática.
- Checklist por módulo.
- Materiais complementares (planilhas, scripts, modelos).
""", encoding='utf-8')
    
    # Módulos
    for idx, (mod_title, mod_desc) in enumerate(tpl['modules'], 1):
        mod_file = completo / f'modulo-{idx}.md'
        mod_file.write_text(f"""# Módulo {idx} — {mod_title}

## Introdução
Neste módulo você vai entender e aplicar na prática: {mod_desc}

## O que você vai aprender
- {mod_title}: fundamentos, exemplos e aplicação no litoral.
- Exercício prático com checklist.
- Material complementar.

## Aula principal
{tpl['title']} — módulo {idx}: {mod_title}. Aplicação direta no mercado imobiliário do litoral.

## Exercício
1. Identifique um caso real relacionado a: {mod_desc.lower()}
2. Aplique o checklist ao final do módulo.
3. Documente o resultado para revisão.

## Checklist
- [ ] Liu o material do módulo
- [ ] Fez o exercício prático
- [ ] Aplicou no seu contexto (imóvel/cliente)
- [ ] Salvou o resultado/documento

## Próximo módulo
Módulo {idx+1}: {tpl['modules'][idx][0] if idx < len(tpl['modules']) else 'Em breve'}
""", encoding='utf-8')

# Listar cursos
course_dirs = [d for d in courses_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

processed = []
for course_path in course_dirs:
    completo = course_path / 'curso-completo'
    if completo.exists():
        files = list(completo.glob('*.md'))
        if len(files) >= 4:
            continue
    
    template_key = guess_template(course_path.name)
    try:
        generate_course_content(course_path, template_key)
        processed.append((course_path.name, template_key))
    except Exception as e:
        print(f'Erro em {course_path.name}: {e}')

print(f'Cursos processados: {len(processed)}')
for name, tpl in processed[:10]:
    print(f'- {name}: {tpl}')
if len(processed) > 10:
    print(f'... e mais {len(processed) - 10}')
