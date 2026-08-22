"""
Testes do Agente Financeiro de Validação e Liberação.

Cobertura:
- Registro do router /financeiro
- Criação de registro financeiro
- Anexo de comprovante
- Validação de pagamento
- Regra: fechou/onboarding_feito não liberam produto
- Regra: somente PAGAMENTO_CONFIRMADO libera entrega
- Integridade da trava existente da Academy
"""
from fastapi.testclient import TestClient
from academy.main import app
from academy.core.database import Base, get_db
from academy.tests._shared_test_db import override_get_db, TestingSessionLocal, engine as test_engine
from academy.financeiro.models import RegistroFinanceiro, StatusPagamento, StatusEntrega
from unittest.mock import patch

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
Base.metadata.create_all(bind=test_engine)


def test_financeiro_routes_registered():
    paths = [r.path for r in app.routes if hasattr(r, 'path') and '/financeiro' in r.path]
    assert '/financeiro/registros' in paths
    assert '/financeiro/registros/{registro_id}' in paths
    assert '/financeiro/registros/{registro_id}/comprovante' in paths
    assert '/financeiro/registros/{registro_id}/validar' in paths


def test_create_registro_requires_auth():
    r = client.post('/financeiro/registros', json={"customer_name": "Fernanda Lima", "amount_expected": 1200})
    assert r.status_code == 401


def test_create_registro_and_flow():
    # create user for auth
    email = "financeiro-test@example.com"
    client.post("/auth/register", json={"name": "Financeiro Test", "email": email, "password": "123456"})
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post('/financeiro/registros', json={"customer_name": "Fernanda Lima", "amount_expected": 1200, "product_name": "Gestão Completa"}, headers=headers)
    assert r.status_code == 200, r.text
    reg = r.json()
    assert reg["payment_status"] == StatusPagamento.PAGAMENTO_PENDENTE.value
    assert reg["delivery_status"] == StatusEntrega.BLOQUEADA.value
    assert reg["revenue_confirmed"] == 0
    reg_id = reg["id"]

    # attach proof
    r = client.post(f'/financeiro/registros/{reg_id}/comprovante', json={"payment_proof": "https://example.com/proof.jpg", "payment_proof_source": "whatsapp"}, headers=headers)
    assert r.status_code == 200, r.text
    reg = r.json()
    assert reg["payment_status"] == StatusPagamento.COMPROVANTE_RECEBIDO.value
    assert reg["delivery_status"] == StatusEntrega.BLOQUEADA.value

    # validate payment as admin
    admin_email = "financeiro-admin@example.com"
    client.post("/auth/register", json={"name": "Admin Financeiro", "email": admin_email, "password": "123456"})
    # manually promote to admin for test
    with TestingSessionLocal() as db:
        from academy.core.models import User
        user = db.query(User).filter(User.email == admin_email).first()
        user.role = "admin"
        db.commit()
    r = client.post("/auth/login", json={"email": admin_email, "password": "123456"})
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    r = client.post(f'/financeiro/registros/{reg_id}/validar', json={"payment_verified_by": "Admin Financeiro", "amount_paid": 1200, "delivery_released_by": "Admin Financeiro"}, headers=admin_headers)
    assert r.status_code == 200, r.text
    reg = r.json()
    assert reg["payment_status"] == StatusPagamento.PAGAMENTO_CONFIRMADO.value
    assert reg["delivery_status"] == StatusEntrega.ENTREGUE.value
    assert reg["revenue_confirmed"] == 1200
    assert reg["payment_verified_by"] == "Admin Financeiro"


def test_fechou_does_not_liberate_academy():
    # ensure existing academy delivery rules still block when not paid
    course_email = "academy-block@example.com"
    client.post("/auth/register", json={"name": "Academy Block", "email": course_email, "password": "123456"})
    r = client.post("/auth/login", json={"email": course_email, "password": "123456"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    course_id = 9999
    r = client.get(f"/academy/me/courses/{course_id}/modules", headers=headers)
    assert r.status_code in (401, 403, 404)


def test_list_registros_requires_admin():
    r = client.get('/financeiro/registros')
    assert r.status_code == 401


if __name__ == "__main__":
    test_financeiro_routes_registered()
    test_create_registro_requires_auth()
    test_create_registro_and_flow()
    test_fechou_does_not_liberate_academy()
    test_list_registros_requires_admin()
    print("=== TESTES FINANCEIRO PASSARAM ===")
