from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.main import app
from academy.core.models import Course

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def seed_course(slug: str):
    db = TestingSessionLocal()
    try:
        course = Course(slug=slug, title=slug.replace("-", " ").title(), description="Teste", status="published")
        db.add(course)
        db.commit()
    finally:
        db.close()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "academy-api"

def test_register_login_course_flow():
    r = client.post("/auth/register", json={
        "name": "Carol Teste",
        "email": "carol@example.com",
        "password": "123456"
    })
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    r = client.post("/auth/login", json={
        "email": "carol@example.com",
        "password": "123456"
    })
    assert r.status_code == 200, r.text
    assert r.json()["access_token"]

    seed_course("curso-teste")

    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/courses", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert any(c["slug"] == "curso-teste" for c in data), data

if __name__ == "__main__":
    test_health()
    print("health ok")
    test_register_login_course_flow()
    print("flow ok")
