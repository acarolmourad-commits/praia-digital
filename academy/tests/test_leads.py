import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\Users\Carolina\praia-digital").resolve()))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from academy.core.database import Base, get_db
from academy.core.models import Lead, LeadEvent, User, Course
from academy.core.security import hash_password
from academy.main import app
from fastapi.testclient import TestClient

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
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

db = TestingSessionLocal()
try:
    course = Course(slug="curso-lead-teste", title="Curso Lead Teste", description="Teste", status="published", price=9900, currency="BRL")
    db.add(course)
    db.commit()
    db.refresh(course)
    course_id = course.id
    user = User(name="Admin Teste", email="admin@example.com", password_hash=hash_password("test"), role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
finally:
    db.close()

r = client.post("/auth/register", json={"name": "Lead User", "email": "lead@example.com", "password": "123456"})
assert r.status_code == 200, r.text

r = client.post("/leads", json={"name": "Lead Teste", "email": "lead@example.com", "phone": "(11) 99999-9999", "city": "Caraguatatuba", "source": "/lead/caraguatatuba", "magnet": "guia-caraguatatuba"})
assert r.status_code == 200, r.text
lead = r.json()
lead_id = lead["id"]

r = client.post(f"/leads/{lead_id}/events?event=opened&payload=%7B%7D")
assert r.status_code == 200, r.text

r = client.get("/admin/leads")
assert r.status_code == 403, r.text

admin_token = client.post("/auth/login", json={"email": "admin@example.com", "password": "test"}).json()["access_token"]
admin_headers = {"Authorization": f"Bearer {admin_token}"}
r = client.get("/admin/leads", headers=admin_headers)
assert r.status_code == 200, r.text
leads = r.json()
assert len(leads) == 1, leads

r = client.get(f"/admin/leads/{lead_id}/events", headers=admin_headers)
assert r.status_code == 200, r.text
events = r.json()
assert len(events) == 2, events

r = client.patch(f"/admin/leads/{lead_id}/status?status=contacted", headers=admin_headers)
assert r.status_code == 200, r.text
assert r.json()["new_status"] == "contacted"

print("leads admin checks passed")
