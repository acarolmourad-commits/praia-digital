from sqlalchemy.orm import Session
from academy.core.models import Course, Module, Lesson
from academy.core.database import SessionLocal

def seed_pilot_course(db: Session):
    course = db.query(Course).filter(Course.slug == "formacao-fotografia-edicao-imoveis-temporada-2026").first()
    if not course:
        course = Course(
            slug="formacao-fotografia-edicao-imoveis-temporada-2026",
            title="Formação em Fotografia e Edição de Imóveis para Temporada",
            subtitle="Curso prático para proprietários, gestores e corretores",
            headline="Fotos que convertem em Airbnb, Booking e VRBO",
            description="Aprenda a produzir fotos e anúncios que convertem mais em Airbnb, Booking e VRBO no litoral paulista.",
            level="Iniciante",
            duration="4h",
            price=9900,
            currency="BRL",
            status="published",
        )
        db.add(course)
        db.flush()
        db.refresh(course)

        module1 = Module(course_id=course.id, order=1, title="Fundamentos de fotografia para temporada")
        module2 = Module(course_id=course.id, order=2, title="Composição, luz e ângulos para imóveis litorâneos")
        module3 = Module(course_id=course.id, order=3, title="Edição profissional: cor, contraste e correção de lente")
        module4 = Module(course_id=course.id, order=4, title="Before/after e análise de conversão")
        module5 = Module(course_id=course.id, order=5, title="Título, copy e estrutura de anúncio")
        module6 = Module(course_id=course.id, order=6, title="Entrega e padronização para portais")
        
        for m in [module1, module2, module3, module4, module5, module6]:
            db.add(m)
            db.flush()
            db.refresh(m)
            lesson = Lesson(module_id=m.id, order=1, title=f"Aula 1 — {m.title}", content_type="video", duration_minutes=30)
            db.add(lesson)

        db.commit()
        print(f"Curso piloto criado: id={course.id}, slug={course.slug}")
    else:
        print(f"Curso piloto já existe: id={course.id}, slug={course.slug}")
    
    return course

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_pilot_course(db)
    finally:
        db.close()
