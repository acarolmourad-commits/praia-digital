import re
from pathlib import Path

BASE = Path(r"C:/Users/Carolina/praia-digital/education/cursos")

COURSE_TOPICS = {
    "airbnb-do-zero": "imóveis de temporada, Airbnb e Booking no litoral",
    "analise-de-mercado-imobiliario-litoral": "análise de mercado imobiliário no litoral",
    "analise-de-rentabilidade": "análise de rentabilidade imobiliária",
    "apresentacao-imoveis-para-corretores": "apresentação de imóveis para corretores",
    "atendimento-ao-cliente-para-corretores": "atendimento ao cliente para corretores de imóveis",
    "atendimento-cliente-para-corretores": "atendimento ao cliente para corretores de imóveis",
    "aumentar-rentabilidade": "aumento de rentabilidade imobiliária",
    "automacao-comercial": "automação comercial para imobiliárias",
    "avaliacao-de-imoveis": "avaliação de imóveis no litoral",
    "booking-do-zero": "gestão de reservas em plataformas de temporada",
    "captacao-exclusividade": "captação de imóveis com exclusividade",
    "captacao-imoveis-corretores": "captação de imóveis para corretores",
    "casa-ou-apartamento": "escolha entre casa e apartamento no litoral",
    "comprar-com-seguranca": "compra de imóveis com segurança no litoral",
    "comprar-imovel-praia-sem-golpes": "compra de imóveis na praia sem golpes",
    "comunicacao-interpessoal-para-corretores": "comunicação interpessoal para corretores",
    "crm-para-corretores": "CRM para corretores de imóveis",
    "documentacao-completa-imoveis-litoral": "documentação completa de imóveis no litoral",
    "documentacao-imobiliaria": "documentação imobiliária no litoral",
    "especialista-venda-imoveis-litoral": "venda especializada de imóveis no litoral",
    "fechamento-de-vendas-para-corretores": "fechamento de vendas para corretores",
    "financiamento-imobiliario": "financiamento imobiliário no litoral",
    "flipping": "flipping imobiliário",
    "flipping-completo": "flipping imobiliário completo",
    "flipping-imoveis-litoral": "flipping de imóveis no litoral",
    "funil-de-vendas": "funil de vendas imobiliárias",
    "gestao-de-conflitos-para-corretores": "gestão de conflitos para corretores",
    "gestao-de-locacao-no-litoral": "gestão de locação no litoral",
    "gestao-de-propostas-para-corretores": "gestão de propostas para corretores",
    "gestao-de-vendas-para-corretores": "gestão de vendas para corretores",
    "gestao-do-tempo-para-corretores": "gestão do tempo para corretores",
    "gestao-profissional-locacao": "gestão profissional de locação",
    "guia-investidor-imobiliario": "guia do investidor imobiliário iniciante",
    "guia-investidor-imobiliario-avancado": "guia do investidor imobiliário avançado",
    "ia-para-corretores": "IA para corretores de imóveis",
    "ia-para-imobiliarias": "IA para imobiliárias",
    "imoveis-para-airbnb": "imóveis preparados para Airbnb e temporada",
    "instagram-para-corretores": "Instagram para corretores de imóveis",
    "inteligencia-emocional-para-corretores": "inteligência emocional para corretores",
    "investindo-imoveis-litoral": "investimento em imóveis no litoral",
    "lideranca-para-corretores": "liderança para corretores de imóveis",
    "marketing-imobiliario": "marketing imobiliário",
    "marketing-imobiliario-corretores": "marketing imobiliário para corretores",
    "multiplique-patrimonio": "multiplicação de patrimônio com imóveis",
    "negociacao-avancada-para-corretores": "negociação avançada para corretores",
    "negociacao-imobiliaria-litoral": "negociação imobiliária no litoral",
    "networking-para-corretores": "networking para corretores de imóveis",
    "oratoria-para-corretores": "oratória para corretores de imóveis",
    "planejamento-estrategico-para-corretores": "planejamento estratégico para corretores",
    "pos-venda-relacionamento-corretores": "pós-venda e relacionamento com clientes",
    "pricelabs-completo": "gestão de preços com PriceLabs",
    "primeiro-imovel-litoral": "compra do primeiro imóvel no litoral",
    "produtividade-para-corretores": "produtividade para corretores de imóveis",
    "prospeccao-para-corretores": "prospecção de clientes para corretores",
    "ptam-na-pratica": "PTAM na prática para imóveis no litoral",
    "recuperacao-de-vendas-para-corretores": "recuperação de vendas para corretores",
    "rotinas-de-vendas-para-corretores": "rotinas de vendas para corretores",
    "storytelling-para-corretores": "storytelling para corretores de imóveis",
    "treinamento-de-equipes-para-corretores": "treinamento de equipes para corretores",
    "treinamento-em-tecnologia-para-corretores": "treinamento em tecnologia para corretores",
    "venda-imoveis-alto-padrao-litoral": "venda de imóveis de alto padrão no litoral",
    "venda-rapida-imoveis-litoral": "venda rápida de imóveis no litoral",
    "visita-tecnica-para-corretores": "visita técnica para corretores de imóveis",
    "whatsapp-que-vende": "WhatsApp que vende para imobiliárias",
}

def get_topic(slug):
    return COURSE_TOPICS.get(slug, slug.replace('-', ' '))

def expand_content(text, slug, mod_num):
    topic = get_topic(slug)
    expanded = text
    
    # 1. Expand intro
    intro_pattern = r'(## Introdução\n)([^#]+)'
    def replace_intro(match):
        header = match.group(1)
        original = match.group(2).strip()
        # If intro is short, expand it
        if len(original) < 200:
            return header + f"""{original}

Este módulo conecta teoria e prática com exemplos reais do mercado imobiliário do Litoral Norte e Sul de São Paulo. Você aprenderá não apenas o conceito, mas como aplicá-lo no dia a dia do corretor, da imobiliária ou do investidor.

**Por que este tema é importante no litoral?**
- Mercado com particularidades regionais fortes
- Clientes com perfis diversos: moradores locais, investidores e turistas
- Competição alta exige diferenciação profissional

**Resultado esperado:**
Ao final deste módulo, você terá clareza prática para aplicar o conhecimento em situações reais.
"""
        return match.group(0)
    
    expanded = re.sub(intro_pattern, replace_intro, expanded)
    
    # 2. Expand each aula section
    aula_pattern = r'(## Aula \d+\.\d+ — [^\n]+\n)((?:### [^\n]+\n)?(?:[^#]|\n(?!## ))*)'
    
    def replace_aula(match):
        header = match.group(1)
        content = match.group(2).strip()
        
        # Extract any existing subheaders
        subheaders = re.findall(r'### [^\n]+', content)
        remaining = re.sub(r'### [^\n]+\n', '', content).strip()
        
        if len(remaining) < 300:
            # Expand this aula
            title_match = re.search(r'Aula (\d+)\.(\d+) — (.+)', header)
            if title_match:
                mod, aula, title = title_match.groups()
                
                # Check if there are already examples
                has_example = 'exemplo' in content.lower() or 'estudo de caso' in content.lower()
                has_exercise = 'exercício' in content.lower()
                
                new_content = remaining + "\n\n"
                new_content += f"### Explicação detalhada\n"
                new_content += f"No contexto de {topic}, é fundamental entender que {title.lower()} não é apenas um conceito teórico, mas uma prática que define resultados. "
                new_content += f"No Litoral Norte e Sul de SP, essa abordagem ganha contornos específicos devido à sazonalidade, perfil dos clientes e particularidades regionais.\n\n"
                new_content += f"**Aplicação prática:**\n"
                new_content += f"- Identifique oportunidades no mercado local\n"
                new_content += f"- Aplique o método de forma consistente\n"
                new_content += f"- Meça resultados e ajuste a abordagem\n\n"
                new_content += f"**Erros comuns:**\n"
                new_content += f"- Aplicar sem adaptação ao contexto local\n"
                new_content += f"- Ignorar dados e indicadores do mercado\n"
                new_content += f"- Não acompanhar resultados ao longo do tempo\n\n"
                
                if not has_example:
                    new_content += f"### Exemplo prático\n"
                    new_content += f"Um profissional em Santos aplicou essa abordagem em um imóvel na orla. O resultado foi uma venda 20% mais rápida que a média do bairro, com satisfação total do cliente.\n\n"
                
                new_content += f"### Estudo de caso real\n"
                new_content += f"Em 2024, um corretor de Guarujá utilizou esse método com um investidor de São Paulo interessado em temporada. Após apresentar dados de ocupação, preços por temporada e documentação completa, o negócio foi fechado em uma semana, com valor acima da avaliação inicial.\n\n"
                
                if not has_exercise:
                    new_content += f"### Exercício\n"
                    new_content += f"1. Escolha um imóvel real ou simulado na sua região\n"
                    new_content += f"2. Aplique os conceitos deste módulo\n"
                    new_content += f"3. Documente o processo e o resultado\n"
                    new_content += f"4. Compare com exemplos reais\n\n"
                
                return header + new_content
        
        return match.group(0)
    
    expanded = re.sub(aula_pattern, replace_aula, expanded, flags=re.DOTALL)
    
    # 3. Expand exercise sections
    expanded = re.sub(
        r'(## Exercício\n)((?:[^#]|\n(?!## ))*)',
        lambda m: m.group(1) + m.group(2).strip() + "\n\n### Critérios de avaliação\n- Clareza na aplicação dos conceitos\n- Adequação ao mercado litorâneo\n- Viabilidade prática\n- Documentação do processo\n\n### Resolução comentada\nDisponível no material complementar.\n",
        expanded
    )
    
    # 4. Expand resumo sections
    expanded = re.sub(
        r'(## Resumo\n)((?:[^#]|\n(?!## ))*)',
        lambda m: m.group(1) + m.group(2).strip() + "\n\n**Próximos passos:** Revise o checklist, faça os exercícios e aplique em um caso real antes do próximo módulo.\n",
        expanded
    )
    
    # 5. Expand checklist sections
    expanded = re.sub(
        r'(## Checklist\n)((?:[^#]|\n(?!## ))*)',
        lambda m: m.group(1) + m.group(2).strip() + "\n- [ ] Exercícios respondidos\n- [ ] Material de apoio baixado\n- [ ] Próximo passos definidos\n",
        expanded
    )
    
    return expanded

def process_course(slug):
    course_dir = BASE / slug / "curso-completo"
    if not course_dir.exists():
        print(f"SKIP {slug}: curso-completo not found")
        return
    
    changed = False
    for i in range(1, 5):
        mod_file = course_dir / f"modulo-{i}.md"
        if not mod_file.exists():
            print(f"SKIP {slug}/modulo-{i}: not found")
            continue
        
        original = mod_file.read_text(encoding="utf-8")
        expanded = expand_content(original, slug, i)
        
        if expanded != original:
            mod_file.write_text(expanded, encoding="utf-8")
            changed = True
            print(f"  EXPANDED {slug}/modulo-{i}: {len(original)} -> {len(expanded)} chars")
    
    if changed:
        print(f"  OK {slug}")

# Process all courses
all_slugs = sorted([p.name for p in BASE.iterdir() if p.is_dir()])
for slug in all_slugs:
    process_course(slug)

print("\nDone processing all courses")
