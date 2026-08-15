from sqlalchemy.orm import Session
from academy.core.models import Course, Module, Lesson
from academy.core.database import SessionLocal

def seed_all_approved_courses(db: Session):
    approved = [
        "airbnb-do-zero",
        "analise-de-mercado-imobiliario-litoral",
        "analise-de-rentabilidade",
        "apresentacao-imoveis-para-corretores",
        "atendimento-ao-cliente-para-corretores",
        "atendimento-cliente-para-corretores",
        "aumentar-rentabilidade",
        "automacao-comercial",
        "avaliacao-de-imoveis",
        "booking-do-zero",
        "captacao-exclusividade",
        "captacao-imoveis-corretores",
        "casa-ou-apartamento",
        "comprar-com-seguranca",
        "comprar-imovel-praia-sem-golpes",
        "comunicacao-interpessoal-para-corretores",
        "crm-para-corretores",
        "documentacao-completa-imoveis-litoral",
        "documentacao-imobiliaria",
        "especialista-venda-imoveis-litoral",
        "fechamento-de-vendas-para-corretores",
        "financiamento-imobiliario",
        "flipping",
        "flipping-completo",
        "flipping-imoveis-litoral",
        "funil-de-vendas",
        "gestao-de-conflitos-para-corretores",
        "gestao-de-locacao-no-litoral",
        "gestao-de-propostas-para-corretores",
        "gestao-de-vendas-para-corretores",
        "gestao-do-tempo-para-corretores",
        "gestao-profissional-locacao",
        "guia-investidor-imobiliario-avancado",
        "guia-investidor-imobiliario",
        "ia-para-corretores",
        "ia-para-imobiliarias",
        "imoveis-para-airbnb",
        "instagram-para-corretores",
        "inteligencia-emocional-para-corretores",
        "investindo-imoveis-litoral",
        "lideranca-para-corretores",
        "marketing-imobiliario-corretores",
        "marketing-imobiliario",
        "multiplique-patrimonio",
        "negociacao-avancada-para-corretores",
        "negociacao-imobiliaria-litoral",
        "networking-para-corretores",
        "oratoria-para-corretores",
        "planejamento-estrategico-para-corretores",
        "pos-venda-relacionamento-corretores",
        "pricelabs-completo",
        "primeiro-imovel-litoral",
        "produtividade-para-corretores",
        "prospeccao-para-corretores",
        "ptam-na-pratica",
        "recuperacao-de-vendas-para-corretores",
        "rotinas-de-vendas-para-corretores",
        "storytelling-para-corretores",
        "treinamento-de-equipes-para-corretores",
        "treinamento-em-tecnologia-para-corretores",
        "venda-imoveis-alto-padrao-litoral",
        "venda-rapida-imoveis-litoral",
        "visita-tecnica-para-corretores",
        "whatsapp-que-vende",
    ]
    existing = {row[0] for row in db.query(Course.slug).all()}
    created = 0
    for slug in approved:
        if slug in existing:
            continue
        course = Course(
            slug=slug,
            title=slug.replace('-', ' ').title(),
            subtitle="Curso aplicado ao mercado imobiliário do litoral.",
            headline="Conteúdo prático para corretores, proprietários e investidores.",
            description="Curso da Praia Digital Academy.",
            level="Intermediário",
            duration="4h",
            price=9900,
            currency="BRL",
            status="published",
        )
        db.add(course)
        db.flush()
        db.refresh(course)
        module = Module(course_id=course.id, order=1, title="Módulo 1")
        db.add(module)
        db.flush()
        db.refresh(module)
        lesson = Lesson(module_id=module.id, order=1, title="Aula 1", content_type="video", duration_minutes=30)
        db.add(lesson)
        created += 1
    db.commit()
    print(f"Seeded {created} new courses. Existing skipped: {len(existing)}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_all_approved_courses(db)
    finally:
        db.close()
