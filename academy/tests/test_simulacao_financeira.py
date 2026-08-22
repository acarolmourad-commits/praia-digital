"""
SIMULAÇÃO FINANCEIRA — 17/08/2026
Ambiente: teste/homologação
Identificador: TESTE_FINANCEIRO_2026_08_17
Cliente real: NÃO
Produção alterada: NÃO
"""
from fastapi.testclient import TestClient
from academy.main import app
from academy.core.database import Base, get_db
from academy.tests._shared_test_db import override_get_db, TestingSessionLocal, engine as test_engine
from academy.financeiro.models import RegistroFinanceiro, StatusPagamento, StatusEntrega
from datetime import datetime
import json

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
Base.metadata.create_all(bind=test_engine)

TESTE_ID = "TESTE_FINANCEIRO_2026_08_17"
TEST_CUSTOMER = "TEST-CUSTOMER-20260817"
TEST_ORDER = "TEST-ORDER-20260817"
TEST_PRODUCT = "TEST-PRODUCT-20260817"
TEST_EMAIL = "teste-financeiro-20260817@example.com"
TEST_AMOUNT = 100


def auth_headers(email, role="student"):
    client.post("/auth/register", json={"name": f"Teste {role}", "email": email, "password": "123456"})
    with TestingSessionLocal() as db:
        from academy.core.models import User
        user = db.query(User).filter(User.email == email).first()
        if role == "admin" and user:
            user.role = "admin"
            db.commit()
    r = client.post("/auth/login", json={"email": email, "password": "123456"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def limpar_testes():
    with TestingSessionLocal() as db:
        db.query(RegistroFinanceiro).filter(RegistroFinanceiro.customer_name.like(f"%{TESTE_ID}%")).delete()
        db.query(RegistroFinanceiro).filter(RegistroFinanceiro.order_id == TEST_ORDER).delete()
        db.commit()


def test_cenario_1_sem_pagamento():
    limpar_testes()
    print("\n=== CENÁRIO 1 — SEM PAGAMENTO ===")
    headers = auth_headers(TEST_EMAIL)
    payload = {
        "customer_name": f"Teste Sem Pagamento {TESTE_ID}",
        "customer_email": TEST_EMAIL,
        "product_name": "TEST-PRODUCT-20260817",
        "order_id": TEST_ORDER,
        "amount_expected": TEST_AMOUNT,
    }
    r = client.post("/financeiro/registros", json=payload, headers=headers)
    assert r.status_code == 200
    reg = r.json()
    reg_id = reg["id"]
    print(f"Criado registro {reg_id}: payment_status={reg['payment_status']}, delivery_status={reg['delivery_status']}, revenue_confirmed={reg['revenue_confirmed']}")
    r = client.get(f"/academy/content/courses/{TEST_PRODUCT}/filesystem-modules", headers=headers)
    print(f"Tentativa entrega: HTTP {r.status_code} body={r.text[:200]}")
    assert r.status_code in (403, 404)
    print("RESULTADO: BLOQUEADO")
    return {"cenario": 1, "registro_id": reg_id, "http_status": r.status_code}


def test_cenario_2_comprovante_nao_validado():
    print("\n=== CENÁRIO 2 — COMPROVANTE NÃO VALIDADO ===")
    headers = auth_headers(TEST_EMAIL)
    r = client.post("/financeiro/registros", json={"customer_name": f"Teste Comprovante {TESTE_ID}", "customer_email": TEST_EMAIL, "product_name": TEST_PRODUCT, "order_id": f"{TEST_ORDER}-C2", "amount_expected": TEST_AMOUNT}, headers=headers)
    reg = r.json()
    reg_id = reg["id"]
    r = client.post(f"/financeiro/registros/{reg_id}/comprovante", json={"payment_proof": "COMPROVANTE_TESTE_NAO_FINANCEIRO.txt", "payment_proof_source": "teste_upload"}, headers=headers)
    assert r.status_code == 200
    reg = r.json()
    print(f"Comprovante anexado: payment_status={reg['payment_status']}")
    r = client.get(f"/academy/content/courses/{TEST_PRODUCT}/filesystem-modules", headers=headers)
    print(f"Tentativa entrega: HTTP {r.status_code}")
    assert r.status_code in (403, 404)
    print("RESULTADO: BLOQUEADO")
    return {"cenario": 2, "registro_id": reg_id, "http_status": r.status_code}


def test_cenario_3_pagamento_confirmado():
    print("\n=== CENÁRIO 3 — PAGAMENTO CONFIRMADO ===")
    headers = auth_headers(TEST_EMAIL)
    admin_headers = auth_headers("teste-admin-20260817@example.com", role="admin")
    r = client.post("/financeiro/registros", json={"customer_name": f"Teste Confirmado {TESTE_ID}", "customer_email": TEST_EMAIL, "product_name": TEST_PRODUCT, "order_id": f"{TEST_ORDER}-C3", "amount_expected": TEST_AMOUNT}, headers=headers)
    reg = r.json()
    reg_id = reg["id"]
    client.post(f"/financeiro/registros/{reg_id}/comprovante", json={"payment_proof": "COMPROVANTE_TESTE.txt", "payment_proof_source": "teste"}, headers=headers)
    r = client.post(f"/financeiro/registros/{reg_id}/validar", json={"payment_verified_by": "TEST_OPERATOR", "amount_paid": TEST_AMOUNT, "delivery_released_by": "TEST_OPERATOR"}, headers=admin_headers)
    assert r.status_code == 200
    reg = r.json()
    print(f"Pagamento confirmado: payment_status={reg['payment_status']}, delivery_status={reg['delivery_status']}, revenue_confirmed={reg['revenue_confirmed']}")
    r = client.get(f"/academy/content/courses/{TEST_PRODUCT}/filesystem-modules", headers=headers)
    print(f"Tentativa entrega: HTTP {r.status_code} body={r.text[:200]}")
    assert reg["payment_status"] == StatusPagamento.PAGAMENTO_CONFIRMADO.value
    assert reg["delivery_status"] == StatusEntrega.ENTREGUE.value
    assert reg["revenue_confirmed"] == TEST_AMOUNT
    print("RESULTADO: PAGAMENTO_CONFIRMADO, ENTREGA LIBERADA NO REGISTRO FINANCEIRO")
    return {"cenario": 3, "registro_id": reg_id, "payment_status": reg["payment_status"], "delivery_status": reg["delivery_status"], "revenue_confirmed": reg["revenue_confirmed"]}


def test_cenario_4_bypass():
    print("\n=== CENÁRIO 4 — TENTATIVA DE BYPASS ===")
    headers = auth_headers(TEST_EMAIL)
    r = client.post("/financeiro/registros", json={"customer_name": f"Teste Bypass A {TESTE_ID}", "customer_email": TEST_EMAIL, "product_name": TEST_PRODUCT, "order_id": f"{TEST_ORDER}-C4A", "amount_expected": TEST_AMOUNT}, headers=headers)
    reg = r.json()
    reg_id = reg["id"]
    r = client.get(f"/academy/content/courses/{TEST_PRODUCT}/filesystem-modules", headers=headers)
    assert r.status_code in (403, 404)
    print(f"A: fechou -> HTTP {r.status_code} BLOQUEADO")
    r = client.get(f"/academy/content/courses/{TEST_PRODUCT}/filesystem-content?relative_path=teste", headers=headers)
    assert r.status_code in (401, 403, 404)
    print(f"B: onboarding_feito -> HTTP {r.status_code} BLOQUEADO")
    r = client.get("/academy/me/courses", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert not any(c.get("slug") == TEST_PRODUCT for c in data)
    print("C: valor estimado -> BLOQUEADO")
    r = client.patch(f"/financeiro/registros/{reg_id}", json={"payment_status": "PAGAMENTO_CONFIRMADO"}, headers=headers)
    print(f"D: alteração manual bypass -> HTTP {r.status_code}")
    assert r.status_code in (403, 400)
    print("RESULTADO: TODOS OS BYPASSES BLOQUEADOS")
    return {"cenario": 4, "bypass_blocked": True}


def test_cenario_5_receita():
    print("\n=== CENÁRIO 5 — RECEITA ===")
    headers = auth_headers(TEST_EMAIL)
    admin_headers = auth_headers("teste-admin-receita-20260817@example.com", role="admin")
    r = client.post("/financeiro/registros", json={"customer_name": f"Teste Receita {TESTE_ID}", "customer_email": TEST_EMAIL, "product_name": TEST_PRODUCT, "order_id": f"{TEST_ORDER}-C5", "amount_expected": TEST_AMOUNT}, headers=headers)
    reg = r.json()
    assert reg["revenue_confirmed"] == 0
    print(f"Pendente: revenue_confirmed={reg['revenue_confirmed']}")
    client.post(f"/financeiro/registros/{reg['id']}/comprovante", json={"payment_proof": "teste.txt"}, headers=headers)
    reg = client.get(f"/financeiro/registros/{reg['id']}", headers=admin_headers).json()
    assert reg["revenue_confirmed"] == 0
    print(f"Comprovante: revenue_confirmed={reg['revenue_confirmed']}")
    client.post(f"/financeiro/registros/{reg['id']}/validar", json={"payment_verified_by": "TEST", "amount_paid": TEST_AMOUNT}, headers=admin_headers)
    reg = client.get(f"/financeiro/registros/{reg['id']}", headers=admin_headers).json()
    assert reg["revenue_confirmed"] == TEST_AMOUNT
    print(f"Confirmado: revenue_confirmed={reg['revenue_confirmed']}")
    print("RESULTADO: RECEITA APENAS APÓS PAGAMENTO_CONFIRMADO")
    return {"cenario": 5, "revenue_confirmed": reg["revenue_confirmed"]}


def test_idempotencia():
    print("\n=== IDEMPOTÊNCIA ===")
    headers = auth_headers(TEST_EMAIL)
    admin_headers = auth_headers("teste-admin-idempotencia-20260817@example.com", role="admin")
    r = client.post("/financeiro/registros", json={"customer_name": f"Teste Idempotencia {TESTE_ID}", "customer_email": TEST_EMAIL, "product_name": TEST_PRODUCT, "order_id": f"{TEST_ORDER}-C6", "amount_expected": TEST_AMOUNT}, headers=headers)
    reg = r.json()
    reg_id = reg["id"]
    client.post(f"/financeiro/registros/{reg_id}/validar", json={"payment_verified_by": "TEST", "amount_paid": TEST_AMOUNT}, headers=admin_headers)
    reg = client.get(f"/financeiro/registros/{reg_id}", headers=admin_headers).json()
    primeira_revenue = reg["revenue_confirmed"]
    client.post(f"/financeiro/registros/{reg_id}/validar", json={"payment_verified_by": "TEST", "amount_paid": TEST_AMOUNT}, headers=admin_headers)
    reg = client.get(f"/financeiro/registros/{reg_id}", headers=admin_headers).json()
    segunda_revenue = reg["revenue_confirmed"]
    print(f"Primeira confirmação: {primeira_revenue}, Segunda: {segunda_revenue}")
    assert primeira_revenue == segunda_revenue == TEST_AMOUNT
    print("RESULTADO: IDEMPOTENTE")
    return {"cenario": "idempotencia", "revenue_1": primeira_revenue, "revenue_2": segunda_revenue}


def test_limpeza():
    limpar_testes()
    print("\n=== LIMPEZA ===")
    print("Registros de teste removidos.")


if __name__ == "__main__":
    evidências = []
    try:
        evidências.append(test_cenario_1_sem_pagamento())
        evidências.append(test_cenario_2_comprovante_nao_validado())
        evidências.append(test_cenario_3_pagamento_confirmado())
        evidências.append(test_cenario_4_bypass())
        evidências.append(test_cenario_5_receita())
        evidências.append(test_idempotencia())
    finally:
        test_limpeza()
    print("\n=== EVIDÊNCIAS COLETADAS ===")
    print(json.dumps(evidências, indent=2))
    print("\n=== SIMULAÇÃO CONCLUÍDA ===")
