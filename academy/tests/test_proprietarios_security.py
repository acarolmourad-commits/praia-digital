import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from academy.core.database import Base, get_db
from academy.core import models_proprietarios
from academy.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    from academy.core.models_proprietarios import Proprietario  # noqa: F401
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def _create_owner(payload):
    r = client.post("/proprietarios", json=payload)
    assert r.status_code == 200, r.text
    return r.json()["codigo"]


def test_cpf_cnpj_nao_exposto_na_pagina_publica():
    codigo = _create_owner({
        "nome_completo": "Ana",
        "cpf_cnpj": "11122233344",
        "email": "ana@example.com",
        "whatsapp": "11977777777",
        "cidade": "Santos",
        "tipo_imovel": "apartamento",
        "valor_anunciado": 800000,
        "valor_liquido_desejado": 720000,
        "declaracao_aceite": True,
    })
    r = client.post(f"/proprietarios/{codigo}/documentos", files=[("file", ("doc.jpg", b"fakeimagebytes", "image/jpeg"))], data={"tipo_documento": "identidade"})
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/fotos", files=[("file", ("f1.jpg", b"fakeimagebytes", "image/jpeg"))])
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/analisar")
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/publicar")
    assert r.status_code == 200
    pub = r.json()
    html = client.get(pub["pagina_url"].replace("https://praia.digital", "")).text
    assert "11122233344" not in html
    assert "cpf" not in html.lower()
    assert "cnpj" not in html.lower()


def test_valor_liquido_privado():
    codigo = _create_owner({
        "nome_completo": "Pedro",
        "cpf_cnpj": "44455566677",
        "email": "pedro@example.com",
        "whatsapp": "11966666666",
        "cidade": "Santos",
        "tipo_imovel": "apartamento",
        "valor_anunciado": 800000,
        "valor_liquido_desejado": 720000,
        "declaracao_aceite": True,
    })
    r = client.post(f"/proprietarios/{codigo}/documentos", files=[("file", ("doc.jpg", b"fakeimagebytes", "image/jpeg"))], data={"tipo_documento": "identidade"})
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/fotos", files=[("file", ("f1.jpg", b"fakeimagebytes", "image/jpeg"))])
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/analisar")
    assert r.status_code == 200
    r = client.post(f"/proprietarios/{codigo}/publicar")
    assert r.status_code == 200
    pub = r.json()
    html = client.get(pub["pagina_url"].replace("https://praia.digital", "")).text
    assert "720000" not in html
    assert "800.000" in html or "800000" in html


def test_isolamento_entre_proprietarios():
    codigo_a = _create_owner({
        "nome_completo": "A",
        "cpf_cnpj": "12345678900",
        "email": "a@example.com",
        "whatsapp": "11999999999",
        "declaracao_aceite": True,
    })
    codigo_b = _create_owner({
        "nome_completo": "B",
        "cpf_cnpj": "98765432100",
        "email": "b@example.com",
        "whatsapp": "11988888888",
        "declaracao_aceite": True,
    })
    r_a = client.get(f"/proprietarios/{codigo_a}")
    assert r_a.status_code == 200
    r_b = client.get(f"/proprietarios/{codigo_b}")
    assert r_b.status_code == 200
    assert r_a.json()["nome_completo"] == "A"
    assert r_b.json()["nome_completo"] == "B"
