"""
Testes de compatibilidade estrutural para os 64 cursos da Academy.

Objetivo:
- Verificar que todos os 64 cursos são reconhecidos pelo endpoint de conteúdo
- Validar o fallback de módulos em arquivo único
- Garantir que nenhum curso real seja liberado sem pagamento confirmado
"""
from pathlib import Path
import json

from fastapi.testclient import TestClient
from academy.main import app
from academy.core.database import Base, get_db
from academy.tests._shared_test_db import override_get_db, TestingSessionLocal, engine as test_engine
from academy.core.models import Course, User, Enrollment, CourseContentSource
from academy.core.security import hash_password

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
REPO = Path("C:/Users/Carolina/praia-digital")
CURSOS_DIR = REPO / "academy" / "cursos"
MAPA = REPO / "academy" / "tests" / "mapeamento-cursos-20260817.json"


def _login():
    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.email == "teste-compatibilidade-20260817@example.com").first()
        if not user:
            db.add(User(name="Teste Compatibilidade", email="teste-compatibilidade-20260817@example.com", password_hash=hash_password("123456"), role="student"))
            db.commit()
            user = db.query(User).filter(User.email == "teste-compatibilidade-20260817@example.com").first()
        courses = db.query(Course).all()
        for course in courses:
            enrollment = db.query(Enrollment).filter(Enrollment.user_id == user.id, Enrollment.course_id == course.id).first()
            if not enrollment:
                db.add(Enrollment(user_id=user.id, course_id=course.id, status="active"))
        db.commit()
    r = client.post("/auth/login", json={"email": "teste-compatibilidade-20260817@example.com", "password": "123456"})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def _setup_test_courses():
    Base.metadata.create_all(bind=test_engine)
    with TestingSessionLocal() as db:
        if db.query(Course).count() == 0:
            mapa = json.loads(MAPA.read_text(encoding="utf-8"))
            for item in mapa["cursos"]:
                slug = item["slug"]
                db.add(Course(slug=slug, title=slug, status="published"))
            db.commit()
        courses = db.query(Course).all()
        # Garantir CourseContentSource para cada curso
        repo_root = REPO
        cursos_root = repo_root / "academy" / "cursos"
        for course in courses:
            existing = db.query(CourseContentSource).filter(CourseContentSource.course_id == course.id).first()
            if not existing:
                fs_path = cursos_root / course.slug
                module_index = fs_path / "aulas" / "sumario.md"
                if not module_index.exists():
                    module_index = fs_path / "curso-completo" / "sumario.md"
                db.add(CourseContentSource(
                    course_id=course.id,
                    source_type="filesystem",
                    fs_root=str(fs_path),
                    module_index_path=str(module_index) if module_index.exists() else None,
                    is_active=True,
                ))
        db.commit()
        return [c.slug for c in courses]


def test_64_cursos_estao_mapeados():
    slugs = _setup_test_courses()
    assert len(slugs) == 64, f"Expected 64 courses, found {len(slugs)}"
    for slug in slugs:
        assert (CURSOS_DIR / slug).exists(), f"Missing curso dir: {slug}"


def test_64_cursos_endpoint_modules():
    slugs = _setup_test_courses()
    headers = _login()
    results = []
    for slug in slugs:
        r = client.get(f"/academy/content/courses/{slug}/filesystem-modules", headers=headers)
        results.append({
            "slug": slug,
            "status_code": r.status_code,
            "modules": r.json().get("modules", []) if r.status_code == 200 else None,
        })
    ok = [x for x in results if x["status_code"] == 200]
    err = [x for x in results if x["status_code"] != 200]
    assert len(err) == 0, f"Cursos com erro: {err}"
    for item in ok:
        modules = item["modules"] or []
        assert len(modules) > 0, f"Curso sem módulos reconhecidos: {item['slug']}"
    assert len(ok) == 64


def test_64_cursos_fallback_modulos_arquivo_unico():
    slugs = _setup_test_courses()
    headers = _login()
    fallback_count = 0
    for slug in slugs:
        r = client.get(f"/academy/content/courses/{slug}/filesystem-modules", headers=headers)
        assert r.status_code == 200, f"Slug {slug}: {r.status_code} {r.text}"
        modules = r.json().get("modules", [])
        assert len(modules) > 0
        for module in modules:
            lessons = module.get("lessons", [])
            assert len(lessons) > 0
            if len(lessons) == 1 and module.get("directory", "").lower().startswith("modulo"):
                fallback_count += 1
    assert fallback_count >= 64


def test_64_cursos_sem_entrega_sem_pagamento():
    slugs = _setup_test_courses()
    with TestingSessionLocal() as db:
        user = db.query(User).filter(User.email == "teste-bloqueio-20260817@example.com").first()
        if not user:
            db.add(User(name="Teste Bloqueio", email="teste-bloqueio-20260817@example.com", password_hash=hash_password("123456"), role="student"))
            db.commit()
    r = client.post("/auth/login", json={"email": "teste-bloqueio-20260817@example.com", "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Sem enrollment ativa, o endpoint de conteúdo deve bloquear acesso com 403.
    # A trava de pagamento é validada separadamente nos testes financeiros.
    for slug in slugs:
        r = client.get(f"/academy/content/courses/{slug}/filesystem-modules", headers=headers)
        assert r.status_code == 403, f"Slug {slug}: esperado 403, obtido {r.status_code}: {r.text}"


if __name__ == "__main__":
    test_64_cursos_estao_mapeados()
    test_64_cursos_endpoint_modules()
    test_64_cursos_fallback_modulos_arquivo_unico()
    test_64_cursos_sem_entrega_sem_pagamento()
    print("=== TESTES DE COMPATIBILIDADE ESTRUTURAL PASSARAM ===")
